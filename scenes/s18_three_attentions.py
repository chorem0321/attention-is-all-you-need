import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

N = 4


def col(x, y_top, color, labels, gap=0.75):
    dots = VGroup()
    for i in range(N):
        d = Dot([x, y_top - i * gap, 0], radius=0.11, color=color)
        dots.add(d)
    ls = VGroup(*[T(s, 16, GREY_A).next_to(dots[i], LEFT if x < 0 else RIGHT, 0.12) for i, s in enumerate(labels)])
    return dots, ls


class S18ThreeAttentions(Scene):
    def construct(self):
        xs = [-4.7, 0.0, 4.7]
        titles = ["Encoder self-attention", "Decoder masked self-attention", "Encoder–Decoder attention"]
        subs = ["Q, K, V 모두 인코더 (입력 문장)", "Q, K, V 모두 디코더, 미래 차단", "Q = 디코더,  K, V = 인코더 출력"]
        src = ["I", "love", "ML", "."]
        tgt = ["<s>", "나는", "ML을", "좋아해"]
        panels = VGroup(*[RoundedRectangle(corner_radius=0.15, width=4.4, height=5.6, stroke_color=GREY_D,
                                           stroke_width=2).move_to([x, -0.35, 0]) for x in xs])
        ttl = VGroup(*[T(t, 20, bold=True).next_to(p, UP, 0.0).shift(DOWN * 0.45) for t, p in zip(titles, panels)])
        sub = VGroup(*[T(s, 17, GREY_A).next_to(t, DOWN, 0.15) for s, t in zip(subs, ttl)])

        # 1. Encoder self-attention: all-to-all
        self.play(Create(panels[0]), FadeIn(ttl[0]), FadeIn(sub[0]), run_time=0.7)
        l1, l1l = col(xs[0] - 1.0, 1.2, KC, src)
        r1, _ = col(xs[0] + 1.0, 1.2, QC, src)
        r1l = VGroup(*[T(s, 16, GREY_A).next_to(r1[i], RIGHT, 0.12) for i, s in enumerate(src)])
        e1 = VGroup(*[Line(r1[i].get_center(), l1[j].get_center(), stroke_width=2, color=AC, stroke_opacity=0.6)
                      for i in range(N) for j in range(N)])
        self.play(FadeIn(l1), FadeIn(l1l), FadeIn(r1), FadeIn(r1l), run_time=0.5)
        self.play(Create(e1), run_time=1.0)
        n1 = T("양방향: 모든 위치 참조", 18, AC).move_to([xs[0], -2.6, 0])
        self.play(FadeIn(n1))

        # 2. Decoder masked self-attention: j ≤ i
        self.play(Create(panels[1]), FadeIn(ttl[1]), FadeIn(sub[1]), run_time=0.7)
        l2, l2l = col(xs[1] - 1.0, 1.2, KC, tgt)
        r2, _ = col(xs[1] + 1.0, 1.2, QC, tgt)
        r2l = VGroup(*[T(s, 16, GREY_A).next_to(r2[i], RIGHT, 0.12) for i, s in enumerate(tgt)])
        e2 = VGroup(*[Line(r2[i].get_center(), l2[j].get_center(), stroke_width=2, color=AC, stroke_opacity=0.7)
                      for i in range(N) for j in range(N) if j <= i])
        blocked = VGroup(*[DashedLine(r2[i].get_center(), l2[j].get_center(), stroke_width=1.5, color=RED_E,
                                      stroke_opacity=0.6, dash_length=0.06)
                           for i in range(N) for j in range(N) if j > i])
        self.play(FadeIn(l2), FadeIn(l2l), FadeIn(r2), FadeIn(r2l), run_time=0.5)
        self.play(Create(blocked), run_time=0.6)
        self.play(Create(e2), FadeOut(blocked), run_time=1.0)
        n2 = T("왼쪽(이전) 토큰만 참조", 18, AC).move_to([xs[1], -2.6, 0])
        self.play(FadeIn(n2))

        # 3. Cross attention
        self.play(Create(panels[2]), FadeIn(ttl[2]), FadeIn(sub[2]), run_time=0.7)
        l3, l3l = col(xs[2] - 1.0, 1.2, KC, src)
        l3l = VGroup(*[T(s, 16, GREY_A).next_to(l3[i], LEFT, 0.12) for i, s in enumerate(src)])
        r3, _ = col(xs[2] + 1.0, 1.2, QC, tgt)
        r3l = VGroup(*[T(s, 16, GREY_A).next_to(r3[i], RIGHT, 0.12) for i, s in enumerate(tgt)])
        kvl = M(c("K", KC) + ", " + c("V", VC) + "  인코더", size=18).next_to(l3, DOWN, 0.3)
        ql = M(c("Q", QC) + "  디코더", size=18).next_to(r3, DOWN, 0.3)
        e3 = VGroup(*[Line(r3[i].get_center(), l3[j].get_center(), stroke_width=2, color=AC, stroke_opacity=0.6)
                      for i in range(N) for j in range(N)])
        self.play(FadeIn(l3), FadeIn(l3l), FadeIn(r3), FadeIn(r3l), FadeIn(kvl), FadeIn(ql), run_time=0.6)
        self.play(Create(e3), run_time=1.0)
        n3 = T("번역할 때 원문의 어디를 볼지 결정", 18, AC).move_to([xs[2], -2.6, 0])
        self.play(FadeIn(n3))
        self.play(*[Indicate(p, color=AC, scale_factor=1.02) for p in panels], run_time=1.0)
        pad_to(self, 15)
