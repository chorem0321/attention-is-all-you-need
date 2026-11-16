import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

ALPHA = [0.10, 0.60, 0.20, 0.10]


def vcol(color, n=5, cell=0.34, op=0.8):
    return VGroup(*[Square(cell, stroke_width=1, stroke_color=color, fill_color=color, fill_opacity=op)
                    .shift(DOWN * i * cell) for i in range(n)])


class S10WeightedSum(Scene):
    def construct(self):
        a = lambda i: c(f"α<sub>{i}</sub>", AC)
        v = lambda i: c(f"V<sub>{i}</sub>", VC)
        eq = M(f"Output = {a(1)}{v(1)} + {a(2)}{v(2)} + … + {a('m')}{v('m')}",
               size=40).to_edge(UP, buff=0.5)
        cons = M(f"Σ {c('α<sub>i</sub>', AC)} = 1,   {c('α<sub>i</sub>', AC)} ≥ 0", None, size=28,
                 color=GREY_A).next_to(eq, DOWN, 0.25)
        self.play(Write(eq), run_time=1.6)
        self.play(FadeIn(cons))

        # Value 벡터들
        vs = VGroup(*[vcol(VC) for _ in ALPHA]).arrange(RIGHT, buff=1.0).move_to(LEFT * 2.3 + DOWN * 1.0)
        vl = VGroup(*[M(v(i + 1), size=28).next_to(vs[i], DOWN, 0.2) for i in range(4)])
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.2) for x in vs], lag_ratio=0.15), FadeIn(vl), run_time=1.2)

        # α 막대: 각 V 열 바로 위에 정렬 (간격 = V 열 간격)
        step = vs[1].get_x() - vs[0].get_x()
        bw = 0.6
        bars = barchart(ALPHA, origin=[vs[0].get_x() - bw / 2, vs.get_top()[1] + 0.3, 0],
                        w=bw, gap=step - bw, max_h=1.4, size=20)
        al = VGroup(*[M(a(i + 1), size=24).next_to(bars[1][i], LEFT, 0.08).align_to(bars[1][i], DOWN)
                      for i in range(4)])
        self.play(Create(bars[0]), *[GrowFromEdge(b, DOWN) for b in bars[1]], FadeIn(bars[2]), FadeIn(al),
                  run_time=1.2)

        # 각 V 를 α 만큼 "남긴다" (투명도)
        self.play(*[x.animate.set_fill(opacity=0.12 + 0.85 * w / max(ALPHA)) for x, w in zip(vs, ALPHA)],
                  run_time=1.2)
        self.wait(0.4)

        out = vcol(VC, op=0.9).move_to(RIGHT * 4.6 + DOWN * 1.0)
        out_l = T("Output", 26).next_to(out, DOWN, 0.2)
        plus = VGroup(*[T("+", 30, GREY_B).move_to((vs[i].get_center() + vs[i + 1].get_center()) / 2)
                        for i in range(3)])
        arr = Arrow(vs.get_right() + RIGHT * 0.2, out.get_left() + LEFT * 0.2, color=GREY_B, stroke_width=3)
        self.play(FadeIn(plus), Create(arr))
        self.play(*[TransformFromCopy(x, out.copy()) for x in vs], FadeIn(out_l), run_time=1.6)
        self.add(out)
        self.play(Indicate(vs[1], color=AC), Indicate(bars[1][1], color=AC), run_time=1)
        msg = T("큰 α 를 받은 Value 가 출력에 더 많이 반영된다", 26, GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(msg, shift=UP * 0.2))
        pad_to(self, 14)
