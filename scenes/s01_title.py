import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *


class S01Title(Scene):
    def construct(self):
        # 모든 토큰이 서로 연결되는 장식
        n = 7
        dots = VGroup(*[Dot(radius=0.09, color=WHITE) for _ in range(n)])
        dots.arrange(RIGHT, buff=1.1).shift(DOWN * 2.3)
        links = VGroup()
        for i in range(n):
            for j in range(i + 1, n):
                links.add(ArcBetweenPoints(dots[i].get_center(), dots[j].get_center(),
                                           angle=-PI / 2.2, stroke_width=1.6,
                                           color=AC, stroke_opacity=0.55))

        title = T("Attention Is All You Need", 66, bold=True).shift(UP * 1.2)
        sub = T("Vaswani et al.  ·  NeurIPS 2017", 32, GREY_A).next_to(title, DOWN, 0.45)
        rev = T("논문 리뷰  ·  발표: Junsu", 30, AC).next_to(sub, DOWN, 0.35)

        self.play(Write(title), run_time=2)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(rev, shift=UP * 0.2), run_time=0.8)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.1), run_time=1)
        self.play(LaggedStart(*[Create(l) for l in links], lag_ratio=0.03), run_time=2)
        self.play(Indicate(title, color=AC, scale_factor=1.04), run_time=1)
        pad_to(self, 9)
