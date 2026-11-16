import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *


class S19PeFfnResidual(Scene):
    def construct(self):
        xs = [-4.75, 0.0, 4.75]
        heads = ["Positional Encoding", "Position-wise FFN", "Residual + LayerNorm"]
        ht = VGroup(*[T(h, 26, bold=True).move_to([x, 3.3, 0]) for h, x in zip(heads, xs)])
        divs = VGroup(*[DashedLine([x, 3.6, 0], [x, -3.6, 0], color=GREY_D) for x in (-2.375, 2.375)])
        self.add(divs)

        # ── 1. Positional Encoding ─────────────────
        self.play(FadeIn(ht[0]))
        f1 = M("PE<sub>(pos, 2i)</sub> = sin(pos / 10000<sup>2i/d<sub>model</sub></sup>)", size=20).move_to([xs[0], 2.6, 0])
        f2 = M("PE<sub>(pos, 2i+1)</sub> = cos(pos / 10000<sup>2i/d<sub>model</sub></sup>)", size=20).next_to(f1, DOWN, 0.15)
        for f in (f1, f2):
            if f.width > 4.3:
                f.scale_to_fit_width(4.3)
        f1.set_x(xs[0])
        f2.next_to(f1, DOWN, 0.15)
        self.play(Write(f1), Write(f2), run_time=1.4)
        ax = Axes(x_range=[0, 20, 5], y_range=[-1.2, 1.2, 1], x_length=4.2, y_length=2.6, tips=False,
                  axis_config={"stroke_width": 2, "color": GREY_B}).move_to([xs[0], -0.2, 0])
        cols = [AC, QC, VC, KC]
        curves = VGroup(
            ax.plot(lambda p: np.sin(p / 10000 ** (0 / 16)), x_range=[0, 20], color=cols[0], stroke_width=3),
            ax.plot(lambda p: np.cos(p / 10000 ** (0 / 16)), x_range=[0, 20], color=cols[1], stroke_width=3),
            ax.plot(lambda p: np.sin(p / 10000 ** (4 / 16)), x_range=[0, 20], color=cols[2], stroke_width=3),
            ax.plot(lambda p: np.sin(p / 10000 ** (8 / 16)), x_range=[0, 20], color=cols[3], stroke_width=3),
        )
        xl = T("pos", 16, GREY_A).next_to(ax, DOWN, 0.1)
        self.play(Create(ax), FadeIn(xl), run_time=0.6)
        self.play(LaggedStart(*[Create(cv) for cv in curves], lag_ratio=0.35), run_time=2.2)
        d1 = T("차원마다 다른 주파수\n(파장 2π ~ 10000·2π)\n임베딩에 더해 위치 정보 주입", 16, GREY_A
               ).next_to(xl, DOWN, 0.25)
        self.play(FadeIn(d1))

        # ── 2. FFN ─────────────────────────────────
        self.play(FadeIn(ht[1]))
        f3 = M("FFN(x) = max(0, xW<sub>1</sub> + b<sub>1</sub>) W<sub>2</sub> + b<sub>2</sub>", size=24
               )
        if f3.width > 4.3:
            f3.scale_to_fit_width(4.3)
        f3.move_to([xs[1], 2.6, 0])
        self.play(Write(f3), run_time=1.2)
        l_in = Rectangle(width=0.5, height=1.4, color=XC, fill_opacity=0.3).move_to([xs[1] - 1.5, -0.2, 0])
        l_hid = Rectangle(width=0.5, height=3.2, color=FFC, fill_opacity=0.35).move_to([xs[1], -0.2, 0])
        l_out = Rectangle(width=0.5, height=1.4, color=XC, fill_opacity=0.3).move_to([xs[1] + 1.5, -0.2, 0])
        t_in = T("512", 18).next_to(l_in, DOWN, 0.12)
        t_hid = T("d_ff = 2048", 18, FFC).next_to(l_hid, DOWN, 0.12)
        t_out = T("512", 18).next_to(l_out, DOWN, 0.12)
        relu = T("ReLU", 16, FFC).next_to(l_hid, UP, 0.1)
        fan1 = VGroup(*[Line(l_in.get_right(), l_hid.get_left() + UP * dy, stroke_width=1, color=GREY_B, stroke_opacity=0.5)
                        for dy in np.linspace(-1.5, 1.5, 7)])
        fan2 = VGroup(*[Line(l_hid.get_right() + UP * dy, l_out.get_left(), stroke_width=1, color=GREY_B, stroke_opacity=0.5)
                        for dy in np.linspace(-1.5, 1.5, 7)])
        self.play(FadeIn(l_in), FadeIn(t_in), run_time=0.4)
        self.play(Create(fan1), GrowFromCenter(l_hid), FadeIn(t_hid), FadeIn(relu), run_time=0.9)
        self.play(Create(fan2), FadeIn(l_out), FadeIn(t_out), run_time=0.7)
        d2 = T("각 위치에 독립 · 동일하게 적용\n(층마다 파라미터는 다름)", 16, GREY_A).move_to([xs[1], -2.75, 0])
        self.play(FadeIn(d2))

        # ── 3. Residual + LayerNorm ───────────────
        self.play(FadeIn(ht[2]))
        f4 = M("LayerNorm(x + Sublayer(x))", size=24).move_to([xs[2], 2.6, 0])
        self.play(Write(f4), run_time=1.0)
        xin = T("x", 26).move_to([xs[2], -2.6, 0])
        sub = box("Sublayer\n(Attention / FFN)", w=2.2, h=0.9, fill="#333333", size=16).move_to([xs[2], -1.0, 0])
        plus = VGroup(Circle(0.2, color=WHITE, stroke_width=2),
                      Line(UP * 0.12, DOWN * 0.12), Line(LEFT * 0.12, RIGHT * 0.12)).move_to([xs[2], 0.4, 0])
        ln = box("LayerNorm", w=2.0, h=0.5, fill=NC, size=18).move_to([xs[2], 1.4, 0])
        a1 = Arrow(xin.get_top(), sub.get_bottom(), buff=0.1, stroke_width=2.5, color=GREY_B, tip_length=0.12)
        a2 = Arrow(sub.get_top(), plus.get_bottom(), buff=0.03, stroke_width=2.5, color=GREY_B, tip_length=0.12)
        a3 = Arrow(plus.get_top(), ln.get_bottom(), buff=0.03, stroke_width=2.5, color=GREY_B, tip_length=0.12)
        skip = VMobject(stroke_color=AC, stroke_width=3.5)
        p0 = xin.get_top() + UP * 0.25
        skip.set_points_as_corners([p0, p0 + RIGHT * 1.6, [xs[2] + 1.6, 0.4, 0], plus.get_right()])
        sl = T("residual", 16, AC).next_to(p0 + RIGHT * 0.9, DOWN, 0.08)
        self.play(FadeIn(xin), Create(a1), FadeIn(sub), run_time=0.7)
        self.play(Create(a2), FadeIn(plus), Create(a3), FadeIn(ln), run_time=0.8)
        self.play(Create(skip), FadeIn(sl), run_time=1.0)
        d3 = T("깊게 쌓아도 기울기 흐름 유지\n모든 sublayer 출력 = d_model 512", 16, GREY_A).move_to([xs[2], -3.3, 0])
        self.play(FadeIn(d3))
        self.play(Indicate(skip, color=AC), run_time=0.8)
        pad_to(self, 20)
