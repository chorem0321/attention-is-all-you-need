"""scenes/sNN_*.py 의 manim 씬을 모두 렌더링하고 media/slides/sNN.mp4 로 모은다.

사용법
    python transformer_ppt.py            # -ql (480p15) 전체, 빠른 확인용
    python transformer_ppt.py -q h       # -qh (1080p60) 전체
    python transformer_ppt.py -q h 5 12  # 5번, 12번 슬라이드만
    python transformer_ppt.py -j 2       # 병렬 프로세스 수 (기본 3)

결과: media/slides/sNN.mp4, media/slides/render_report.json
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCENES = ROOT / "scenes"
MEDIA = ROOT / "media"
OUT = MEDIA / "slides"
QDIR = {"l": "480p15", "m": "720p30", "h": "1080p60", "k": "2160p60"}


def find_scenes():
    items = []
    for f in sorted(SCENES.glob("s[0-9][0-9]_*.py")):
        m = re.search(r"^class\s+(\w+)\s*\(\s*Scene\s*\)", f.read_text(encoding="utf-8"), re.M)
        if m:
            items.append((int(f.name[1:3]), f, m.group(1)))
    return items


def render(item, quality):
    num, path, cls = item
    t0 = time.time()
    cmd = [sys.executable, "-m", "manim", "render", f"-q{quality}", "--media_dir", str(MEDIA),
           "--disable_caching", str(path), cls]
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    src = MEDIA / "videos" / path.stem / QDIR[quality] / f"{cls}.mp4"
    ok = p.returncode == 0 and src.exists()
    dst = OUT / f"s{num:02d}.mp4"
    if ok:
        shutil.copyfile(src, dst)
    tail = "\n".join((p.stdout + p.stderr).strip().splitlines()[-25:])
    return {"slide": num, "scene": cls, "file": path.name, "ok": ok, "seconds": round(time.time() - t0, 1),
            "output": str(dst.relative_to(ROOT)) if ok else None, "log_tail": None if ok else tail}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-q", "--quality", default="l", choices=list(QDIR))
    ap.add_argument("-j", "--jobs", type=int, default=3)
    ap.add_argument("only", nargs="*", type=int, help="렌더링할 슬라이드 번호")
    a = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    items = [i for i in find_scenes() if not a.only or i[0] in a.only]
    print(f"{len(items)}개 씬 렌더링 (-q{a.quality}, jobs={a.jobs})")
    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        results = []
        for r in ex.map(lambda it: render(it, a.quality), items):
            print(f"  s{r['slide']:02d} {r['scene']:<26} {'OK ' if r['ok'] else 'FAIL'} {r['seconds']}s")
            results.append(r)

    # 병렬 렌더링 시 manim 의 공유 텍스트 캐시(media/texts)에서 드물게 경쟁 상태가 생긴다
    # → 실패한 씬만 직렬로 한 번 더 시도
    retry = [it for it in items if any(r["slide"] == it[0] and not r["ok"] for r in results)]
    for it in retry:
        r = render(it, a.quality)
        print(f"  s{r['slide']:02d} {r['scene']:<26} {'OK ' if r['ok'] else 'FAIL'} {r['seconds']}s (재시도)")
        results = [r if x["slide"] == r["slide"] else x for x in results]

    rp = OUT / "render_report.json"
    old = json.loads(rp.read_text(encoding="utf-8")) if rp.exists() else {}
    old.setdefault("slides", {})
    for r in results:
        old["slides"][f"s{r['slide']:02d}"] = dict(r, quality=a.quality)
    rp.write_text(json.dumps(old, ensure_ascii=False, indent=2), encoding="utf-8")

    fails = [r for r in results if not r["ok"]]
    if fails:
        print("\n실패한 씬:")
        for r in fails:
            print(f"--- s{r['slide']:02d} {r['scene']} ---\n{r['log_tail']}\n")
        sys.exit(1)
    print("모두 성공")


if __name__ == "__main__":
    main()
