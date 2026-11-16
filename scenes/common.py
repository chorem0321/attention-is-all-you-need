"""공통 스타일/헬퍼. 모든 씬은 `from common import *` 로 사용한다.

색 규칙 (모든 씬 통일)
    Query = 노랑(QC), Key = 파랑(KC), Value = 초록(VC), Attention weight = 주황(AC)

LaTeX 가 설치되어 있으면 M(...) 이 MathTex 를 쓰고, 없으면 Pango MarkupText
(<sub>/<sup>) 로 대체한다. DecimalNumber / Matrix / Axes 숫자 라벨은 LaTeX 가
필요하므로 이 프로젝트에서는 쓰지 않는다.
"""
import re
import shutil

import numpy as np
from manim import *  # noqa: F401,F403

HAS_LATEX = shutil.which("latex") is not None

config.background_color = "#000000"

# ── 색 ───────────────────────────────────────────────────────────────
QC = "#FFD84D"  # Query  (노랑)
KC = "#4DA3FF"  # Key    (파랑)
VC = "#5BD17A"  # Value  (초록)
AC = "#FF9A3C"  # Attention weight (주황)
XC = "#B8B8B8"  # 입력 X / 중립
FFC = "#A98BE0"  # FFN
NC = "#8C8C8C"  # Add & Norm
EC = "#E0707A"  # Embedding
MUTE = "#7A7A7A"

FONT = "Malgun Gothic"  # 한글 + 라틴
MFONT = "Cambria"  # 수식 대체용


def T(s, size=30, color=WHITE, bold=False, font=FONT, align=None):
    """일반 텍스트 (한글 가능). 줄바꿈이 있으면 줄마다 Text 를 만들어 간격을 확보한다
    (manim Text 의 기본 줄간격은 한글에서 줄이 겹친다)."""
    w = BOLD if bold else NORMAL
    if "\n" in s:
        lines = [Text(l if l else " ", font=font, font_size=size, color=color, weight=w) for l in s.split("\n")]
        g = VGroup(*lines).arrange(DOWN, buff=size * 0.011, aligned_edge=align if align is not None else ORIGIN)
        return g
    return Text(s, font=font, font_size=size, color=color, weight=w)


_HANGUL = re.compile(r"([ㄱ-ㆎ가-힣]+)")


def M(markup, tex=None, size=40, color=WHITE):
    """수식. LaTeX 가 있고 tex 가 주어지면 MathTex, 아니면 MarkupText.
    수식 폰트(Cambria)에는 한글 글리프가 없으므로 한글 구간은 FONT 로 감싼다."""
    if HAS_LATEX and tex is not None:
        return MathTex(tex, font_size=size * 1.15, color=color)
    markup = _HANGUL.sub(lambda m: f'<span font_family="{FONT}">{m.group(1)}</span>', markup)
    return MarkupText(markup, font=MFONT, font_size=size, color=color)


def c(s, col):
    """MarkupText 안에서 부분 색칠."""
    return f'<span foreground="{col}">{s}</span>'


def box(label, w=2.6, h=0.5, fill="#333333", size=20, color=WHITE, op=0.85,
        stroke=WHITE):
    r = RoundedRectangle(corner_radius=0.08, width=w, height=h,
                         fill_color=fill, fill_opacity=op,
                         stroke_color=stroke, stroke_width=1.5)
    t = T(label, size, color).move_to(r)
    if t.width > w - 0.15:
        t.scale_to_fit_width(w - 0.15)
    return VGroup(r, t)


def mat(w, h, color, label=None, dims=None, size=26, op=0.3):
    """행렬 블록: 색 사각형 + 가운데 라벨(markup) + 아래 차원 표기."""
    r = Rectangle(width=w, height=h, fill_color=color, fill_opacity=op,
                  stroke_color=color, stroke_width=2)
    g = VGroup(r)
    if label:
        lab = M(label, size=size, color=color).move_to(r)
        if lab.width > w * 0.9:
            lab.scale_to_fit_width(w * 0.9)
        g.add(lab)
    if dims:
        g.add(T(dims, 18, GREY_A).next_to(r, DOWN, 0.1))
    return g


def barchart(vals, origin=ORIGIN, w=0.7, gap=0.35, max_h=3.0, color=AC,
             labels=None, show_val=True, fmt="{:.2f}", vmax=1.0, size=22):
    """아래쪽 기준선이 origin 에 오는 막대 그래프.
    반환: VGroup(base, bars, value_texts, label_texts)"""
    origin = np.array(origin, dtype=float)
    bars, vt, lt = VGroup(), VGroup(), VGroup()
    for i, v in enumerate(vals):
        h = max(v / vmax * max_h, 0.02)
        x = origin + RIGHT * (i * (w + gap) + w / 2)
        r = Rectangle(width=w, height=h, stroke_width=0,
                      fill_color=color, fill_opacity=0.9)
        r.move_to(x + UP * h / 2)
        bars.add(r)
        if show_val:
            vt.add(T(fmt.format(v), size).next_to(r, UP, 0.1))
        if labels:
            lt.add(T(labels[i], size, GREY_A).next_to(x, DOWN, 0.18))
    total = len(vals) * (w + gap) - gap
    base = Line(origin + LEFT * 0.15, origin + RIGHT * (total + 0.15),
                color=GREY_B, stroke_width=2)
    return VGroup(base, bars, vt, lt)


def heatmap(vals, rows=None, cols=None, cell=0.6, color=AC, show=True,
            size=18, fmt="{:.2f}", vmax=1.0, lab_size=20):
    """반환: VGroup(cells, nums, row_labels, col_labels), 왼쪽 위가 원점."""
    vals = np.asarray(vals, dtype=float)
    n, m = vals.shape
    cells, nums = VGroup(), VGroup()
    for i in range(n):
        for j in range(m):
            v = vals[i, j]
            if np.isneginf(v):
                sq = Square(cell, stroke_color=GREY_B, stroke_width=1,
                            fill_color="#222222", fill_opacity=1)
                txt = "−∞"
                tc = GREY_B
            else:
                a = float(np.clip(v / vmax, 0, 1))
                sq = Square(cell, stroke_color=GREY_B, stroke_width=1,
                            fill_color=color, fill_opacity=0.06 + 0.9 * a)
                txt = fmt.format(v)
                tc = BLACK if a > 0.55 else WHITE
            sq.move_to(np.array([j * cell, -i * cell, 0]))
            cells.add(sq)
            if show:
                t = T(txt, size, tc)
                if t.width > cell * 0.9:
                    t.scale_to_fit_width(cell * 0.9)
                nums.add(t.move_to(sq))
    rl, cl = VGroup(), VGroup()
    if rows:
        for i, s in enumerate(rows):
            rl.add(T(s, lab_size, GREY_A).next_to(cells[i * m], LEFT, 0.15))
    if cols:
        for j, s in enumerate(cols):
            cl.add(T(s, lab_size, GREY_A).next_to(cells[j], UP, 0.15))
    return VGroup(cells, nums, rl, cl)


def softmax(x, axis=-1):
    x = np.asarray(x, dtype=float)
    x = x - np.max(x, axis=axis, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=axis, keepdims=True)


def pad_to(scene, seconds):
    """씬 총 길이를 최소 seconds 로 맞춘다."""
    remain = seconds - scene.renderer.time
    if remain > 0.05:
        scene.wait(remain)
