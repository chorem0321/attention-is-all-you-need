import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

TOK = ["I", "love", "machine", "learning"]
# 예시 score = QKᵀ/√d_k (설명용 값)
S = np.array([[2.1, 0.3, -0.5, 0.8],
              [0.4, 1.8, 0.9, -0.2],
              [-0.3, 1.1, 2.0, 1.2],
              [0.6, -0.1, 1.5, 2.2]])
A = softmax(S, axis=1)
MASK = np.triu(np.ones_like(S, dtype=bool), k=1)
SM = np.where(MASK, -np.inf, S)
AM = softmax(SM, axis=1)

# 수식 조각별 글자 수 (공백 제외) — 조각 단위로 등장시키기 위함
PIECES = [17, 8, 3, 4, 1, 1]


class S16ScaledDotProduct(Scene):
    def construct(self):
        eq = M(f"Attention({c('Q', QC)}, {c('K', KC)}, {c('V', VC)}) = "
               f"{c('softmax(', AC)} {c('Q', QC)}{c('K<sup>T</sup>', KC)} / √d<sub>k</sub> {c(')', AC)} {c('V', VC)}",
               size=40).move_to(UP * 3.2)
        if len(eq.submobjects) == sum(PIECES):
            idx = np.cumsum([0] + PIECES)
            parts = [VGroup(*eq.submobjects[idx[i]:idx[i + 1]]) for i in range(len(PIECES))]
            self.play(Write(parts[0]), run_time=1.0)
            for p in parts[1:]:
                self.play(FadeIn(p, shift=UP * 0.15), run_time=0.45)
            self.play(Indicate(parts[2], color=QC), run_time=0.6)
            self.play(Indicate(parts[3], color=GREY_A), run_time=0.6)
        else:  # 글리프 수가 예상과 다르면 통째로
            self.play(Write(eq), run_time=2.5)

        # ── Q × Kᵀ → score 히트맵 ─────────────────────────
        cell = 0.55
        hs = heatmap(S, cell=cell, color=XC, vmax=2.2, fmt="{:.1f}", size=17).move_to([-3.4, 0.0, 0])
        qb = mat(0.55, 4 * cell, QC, "Q", None, size=26, op=0.4).next_to(hs, LEFT, 0.35)
        kb = mat(4 * cell, 0.55, KC, "K<sup>T</sup>", None, size=24, op=0.4).next_to(hs, UP, 0.3)
        sl = M(f"{c('Q', QC)}{c('K<sup>T</sup>', KC)} / √d<sub>k</sub>", size=24).next_to(hs, DOWN, 0.3)
        self.play(FadeIn(qb, shift=RIGHT * 0.2), FadeIn(kb, shift=DOWN * 0.2), run_time=0.7)
        self.play(TransformFromCopy(VGroup(qb[0], kb[0]), hs[0]), run_time=1.0)
        self.play(FadeIn(hs[1]), FadeIn(sl), run_time=0.6)

        # softmax (행 단위)
        ha = heatmap(A, cell=cell, color=AC, fmt="{:.2f}", size=15).move_to(hs)
        sl2 = T("softmax: 각 행의 합 = 1", 22, AC).move_to(sl)
        self.play(Transform(hs, ha), Transform(sl, sl2), run_time=1.2)
        row = SurroundingRectangle(VGroup(*hs[0][0:4]), color=QC, buff=0.03, stroke_width=3)
        self.play(Create(row), run_time=0.5)
        self.play(FadeOut(row), run_time=0.3)

        # × V = Output
        times = T("×", 32, GREY_B).next_to(hs, RIGHT, 0.25)
        vb = mat(0.8, 4 * cell, VC, "V", None, size=26, op=0.4).next_to(times, RIGHT, 0.25)
        eqs = T("=", 32, GREY_B).next_to(vb, RIGHT, 0.25)
        ob = mat(0.8, 4 * cell, AC, "Z", None, size=26, op=0.35).next_to(eqs, RIGHT, 0.25)
        ol = T("각 토큰의 새 표현", 18, GREY_A).next_to(ob, DOWN, 0.15)
        self.play(FadeIn(times), FadeIn(vb, shift=LEFT * 0.2), run_time=0.6)
        self.play(FadeIn(eqs), TransformFromCopy(VGroup(hs[0], vb[0]), ob[0]), FadeIn(ob[1]), FadeIn(ol),
                  run_time=1.2)

        # ── Decoder masking ──────────────────────────────
        mt = T("Decoder: Masking", 26, bold=True).move_to([4.9, 2.1, 0])
        hm = heatmap(S, rows=TOK, cols=None, cell=0.5, color=XC, vmax=2.2, fmt="{:.1f}", size=15,
                     lab_size=16).move_to([5.0, 0.0, 0])
        self.play(FadeIn(mt), FadeIn(hm), run_time=0.8)
        hmm = heatmap(SM, rows=TOK, cell=0.5, color=XC, vmax=2.2, fmt="{:.1f}", size=15,
                      lab_size=16).move_to(hm)
        mtxt = T("미래 위치 = −∞", 20, RED_C).next_to(hm, DOWN, 0.3)
        self.play(Transform(hm, hmm), FadeIn(mtxt), run_time=1.0)
        hma = heatmap(AM, rows=TOK, cell=0.5, color=AC, fmt="{:.2f}", size=13, lab_size=16).move_to(hm)
        mtxt2 = T("softmax 후 0 → 이전 토큰만 참조", 18, AC).move_to(mtxt)
        self.play(Transform(hm, hma), Transform(mtxt, mtxt2), run_time=1.2)
        note = T("자기회귀(auto-regressive) 성질 유지: 생성 시 미래 단어를 볼 수 없음", 22, GREY_A).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(note, shift=UP * 0.2))
        pad_to(self, 20)
