import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *


class S10DotProduct(Scene):
    def construct(self):
        f1 = M(f"score({c('q', QC)}, {c('k', KC)}) = {c('q', QC)} · {c('k', KC)} = "
               f"Σ<sub>i</sub> {c('q<sub>i</sub>', QC)}{c('k<sub>i</sub>', KC)}", size=34).move_to([-3.4, 2.9, 0])
        f2 = M(f"= |{c('q', QC)}| |{c('k', KC)}| cos θ", size=34).next_to(f1, DOWN, 0.3).align_to(f1, LEFT)
        self.play(Write(f1), run_time=1.5)
        self.play(Write(f2), run_time=1)

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=5.2, y_length=5.2,
                            background_line_style={"stroke_color": GREY_D, "stroke_width": 1,
                                                   "stroke_opacity": 0.6}).move_to([3.4, -0.4, 0])
        o = plane.c2p(0, 0)
        R = 2.4
        qang = 20 * DEGREES
        q = Arrow(o, plane.c2p(R * np.cos(qang), R * np.sin(qang)), buff=0, color=QC, stroke_width=6)
        ql = T("q", 30, QC, bold=True).next_to(q.get_end(), RIGHT, 0.1)
        theta = ValueTracker(150 * DEGREES)

        def kvec():
            a = qang + theta.get_value()
            return Arrow(o, plane.c2p(R * np.cos(a), R * np.sin(a)), buff=0, color=KC, stroke_width=6)

        k = always_redraw(kvec)
        kl = always_redraw(lambda: T("k", 30, KC, bold=True).next_to(k.get_end(), UP, 0.1))
        arc = always_redraw(lambda: Arc(radius=0.6, start_angle=qang, angle=theta.get_value(),
                                        arc_center=o, color=WHITE, stroke_width=2))
        tl = always_redraw(lambda: T("θ", 24).move_to(o + 0.9 * np.array(
            [np.cos(qang + theta.get_value() / 2), np.sin(qang + theta.get_value() / 2), 0])))

        self.play(Create(plane), run_time=1)
        self.play(GrowArrow(q), FadeIn(ql))
        self.add(k, kl, arc, tl)
        self.wait(0.3)

        # 점수 게이지 (왼쪽)
        gauge_bg = Rectangle(width=0.6, height=3.6, stroke_color=GREY_B, stroke_width=2).move_to([-4.6, -1.3, 0])
        zero = Line(gauge_bg.get_left() + LEFT * 0.1, gauge_bg.get_right() + RIGHT * 0.1, color=GREY_B
                    ).move_to(gauge_bg.get_center())
        mid = gauge_bg.get_center()

        def score():
            return np.cos(theta.get_value()) * 1.0  # |q||k| = 1 로 정규화

        fill = always_redraw(lambda: Rectangle(width=0.6, height=max(abs(score()) * 1.8, 0.01), stroke_width=0,
                                               fill_color=AC if score() >= 0 else MUTE, fill_opacity=0.9)
                             .move_to(mid + UP * score() * 0.9))
        val = always_redraw(lambda: T(f"q·k = {score():+.2f}", 28, AC).next_to(gauge_bg, RIGHT, 0.4))
        cap = T("(|q| = |k| = 1 로 정규화)", 18, GREY_B).next_to(gauge_bg, RIGHT, 0.4).shift(DOWN * 0.7)
        self.play(Create(gauge_bg), Create(zero), FadeIn(fill), FadeIn(val), FadeIn(cap))

        self.play(theta.animate.set_value(95 * DEGREES), run_time=2)
        self.play(theta.animate.set_value(15 * DEGREES), run_time=2.5)
        msg = T("각도가 좁을수록(방향이 비슷할수록) score ↑", 26).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(msg, shift=UP * 0.2))
        self.play(Indicate(val, color=AC))
        pad_to(self, 14)
