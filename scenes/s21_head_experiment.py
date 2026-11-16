import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

# 논문 Table 3 (A) + base 행. EN-DE dev set (newstest2013) BLEU
HS = [1, 4, 8, 16, 32]
DK = [512, 128, 64, 32, 16]
BLEU = [24.9, 25.5, 25.8, 25.8, 25.4]
YMIN, YMAX = 24.5, 26.0


class S21HeadExperiment(Scene):
    def construct(self):
        x0, y0 = -6.0, -2.3
        W, Hh = 6.6, 4.4
        bw, gap = 0.85, 0.45

        def ypos(b):
            return y0 + (b - YMIN) / (YMAX - YMIN) * Hh

        yaxis = Line([x0, y0, 0], [x0, y0 + Hh, 0], color=GREY_B)
        xaxis = Line([x0, y0, 0], [x0 + W, y0, 0], color=GREY_B)
        ticks = VGroup()
        for b in [24.5, 25.0, 25.5, 26.0]:
            ticks.add(Line([x0 - 0.08, ypos(b), 0], [x0, ypos(b), 0], color=GREY_B))
            ticks.add(T(f"{b:.1f}", 16, GREY_A).next_to([x0 - 0.08, ypos(b), 0], LEFT, 0.08))
            ticks.add(DashedLine([x0, ypos(b), 0], [x0 + W, ypos(b), 0], color=GREY_D, stroke_width=1))
        yl = T("BLEU (dev)", 18, GREY_A).next_to(yaxis, UP, 0.15)
        cut = T("※ 세로축 24.5 부터 시작", 16, RED_C).next_to(xaxis, DOWN, 0.75).align_to(xaxis, LEFT)
        self.play(Create(yaxis), Create(xaxis), FadeIn(ticks), FadeIn(yl), FadeIn(cut), run_time=1.0)

        bars, vals, labs = VGroup(), VGroup(), VGroup()
        for i, (h, d, b) in enumerate(zip(HS, DK, BLEU)):
            cx = x0 + 0.5 + i * (bw + gap) + bw / 2
            hgt = ypos(b) - y0
            r = Rectangle(width=bw, height=hgt, stroke_width=0, fill_color=AC,
                          fill_opacity=0.95 if b == max(BLEU) else 0.45).move_to([cx, y0 + hgt / 2, 0])
            bars.add(r)
            vals.add(T(f"{b}", 20, AC if b == max(BLEU) else WHITE).next_to(r, UP, 0.08))
            labs.add(VGroup(T(f"h={h}", 18), T(f"d_k={d}", 14, GREY_B)).arrange(DOWN, buff=0.05)
                     .next_to([cx, y0, 0], DOWN, 0.12))
        self.play(FadeIn(labs), run_time=0.5)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), run_time=1.8)
        self.play(FadeIn(vals), run_time=0.6)
        self.play(Indicate(VGroup(bars[2], bars[3]), color=AC), run_time=1)
        self.play(Indicate(VGroup(bars[0], vals[0]), color=RED_C),
                  Indicate(VGroup(bars[4], vals[4]), color=RED_C), run_time=1)

        src = T("Vaswani et al. 2017, Table 3 (A) — 연산량 고정 (d_k = d_v = 512/h)", 16, GREY_B
                ).move_to([x0 + W / 2, y0 + Hh + 0.75, 0])
        self.play(FadeIn(src))

        pts = VGroup(
            T("single-head: 최고 대비 −0.9 BLEU", 24),
            T("head 가 너무 많아도 하락 (h=32: 25.4)", 24),
            T("→ 많다고 무조건 좋지 않다", 26, AC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.9, 1.6, 0])
        for p in pts:
            self.play(FadeIn(p, shift=LEFT * 0.2), run_time=0.6)
        fol = VGroup(T("후속 연구", 22, bold=True),
                     T("Voita et al. 2019 — 소수의 '전문화된' head 가\n핵심, 나머지는 pruning 가능", 18, GREY_A),
                     T("Michel et al. 2019 — 'Are Sixteen Heads\nReally Better than One?' 다수 head 제거 가능", 18, GREY_A)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.9, -1.5, 0])
        box_ = SurroundingRectangle(fol, color=GREY_D, buff=0.2, corner_radius=0.1)
        self.play(FadeIn(fol), Create(box_), run_time=1.0)
        pad_to(self, 15)
