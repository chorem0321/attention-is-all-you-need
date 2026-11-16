import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *


def stat(big, unit, sub, color):
    b = T(big, 64, color, bold=True)
    u = T(unit, 24, color).next_to(b, RIGHT, 0.15).align_to(b, DOWN)
    s = T(sub, 18, GREY_A).next_to(VGroup(b, u), DOWN, 0.12)
    return VGroup(b, u, s)


class S29Results(Scene):
    def construct(self):
        # ── BLEU (논문 Table 2, newstest2014) ─────────
        de_t = T("WMT14 EN→DE", 24, bold=True)
        fr_t = T("WMT14 EN→FR", 24, bold=True)
        de = stat("28.4", "BLEU", "기존 최고(앙상블 포함) 대비 +2 BLEU 이상", AC)
        fr = stat("41.0", "BLEU", "단일 모델 SOTA", AC)
        g1 = VGroup(de_t, de).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([-4.3, 2.3, 0])
        g2 = VGroup(fr_t, fr).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([0.3, 2.3, 0])
        self.play(FadeIn(de_t), run_time=0.4)
        self.play(FadeIn(de, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(fr_t), run_time=0.4)
        self.play(FadeIn(fr, shift=UP * 0.3), run_time=0.8)

        cost = VGroup(T("학습 비용", 24, bold=True),
                      T("NVIDIA P100 × 8 (1대)", 20, GREY_A),
                      T("base: 100K step ≈ 12시간", 20),
                      T("big: 300K step = 3.5일", 20),
                      T("기존 대비 학습 FLOPs 대폭 감소", 18, VC)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        cost.move_to([4.7, 2.2, 0])
        self.play(LaggedStart(*[FadeIn(x, shift=LEFT * 0.2) for x in cost], lag_ratio=0.2), run_time=1.4)

        # ── Table 1 ──────────────────────────────────
        rows = [["Layer Type", "Complexity / Layer", "Sequential Ops", "Max Path Length"],
                ["Self-Attention", "O(n²·d)", "O(1)", "O(1)"],
                ["Recurrent", "O(n·d²)", "O(n)", "O(n)"],
                ["Convolutional", "O(k·n·d²)", "O(1)", "O(log_k(n))"]]
        colx = [-4.6, -1.3, 1.6, 4.5]
        y_top = -0.35
        rh = 0.62
        cells = VGroup()
        for r, row in enumerate(rows):
            for j, s in enumerate(row):
                t = T(s, 22 if r else 20, WHITE if r else GREY_A, bold=(r == 0))
                t.move_to([colx[j], y_top - r * rh, 0])
                cells.add(t)
        hline = Line([-6.4, y_top - rh / 2, 0], [6.4, y_top - rh / 2, 0], color=GREY_B)
        cap = T("Table 1 (n: 길이, d: 차원, k: 커널 크기)", 16, GREY_B).move_to([0, y_top - 4 * rh + 0.05, 0])
        self.play(FadeIn(cells[0:4]), Create(hline), run_time=0.6)
        for r in range(1, 4):
            self.play(FadeIn(cells[4 * r:4 * r + 4], shift=UP * 0.1), run_time=0.45)
        self.play(FadeIn(cap))
        hl = SurroundingRectangle(cells[4:8], color=AC, buff=0.12, corner_radius=0.08)
        self.play(Create(hl), run_time=0.7)
        self.play(Indicate(cells[6], color=AC), Indicate(cells[7], color=AC), run_time=1)
        note = T("n < d (일반적인 문장 길이) 이면 self-attention 이 recurrent 보다 빠름", 20, AC).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note, shift=UP * 0.2))
        pad_to(self, 16)
