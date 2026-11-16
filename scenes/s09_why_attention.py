import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

WORDS = ["The", "animal", "didn't", "cross", "the", "street", "because", "it", "was", "tired", "."]
# 예시용 가중치 (it → 각 토큰). 합 = 1
W = [0.04, 0.52, 0.03, 0.04, 0.03, 0.12, 0.05, 0.05, 0.04, 0.06, 0.02]
IT = 7


class S09WhyAttention(Scene):
    def construct(self):
        toks = VGroup(*[T(w, 30) for w in WORDS]).arrange(RIGHT, buff=0.32, aligned_edge=DOWN)
        toks.move_to(DOWN * 0.6)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in toks], lag_ratio=0.07), run_time=1.4)
        self.play(toks[IT].animate.set_color(QC).scale(1.15), run_time=0.6)
        q = T("Query: it 은 무엇을 가리키는가?", 26, QC).move_to(DOWN * 2.2)
        self.play(FadeIn(q))

        def arcs(weights, emph=False):
            g = VGroup()
            src = toks[IT].get_top() + UP * 0.08
            for j, w in enumerate(weights):
                if j == IT:
                    g.add(VMobject())
                    continue
                dst = toks[j].get_top() + UP * 0.08
                ang = -PI * 0.55 if j < IT else PI * 0.55
                g.add(ArcBetweenPoints(src, dst, angle=-ang if j < IT else -ang,
                                       color=AC, stroke_width=1 + 24 * w if emph else 2.5,
                                       stroke_opacity=0.25 + 0.75 * min(1, w * 2.2) if emph else 0.5))
            return g

        uni = arcs([1 / 10] * len(WORDS), emph=False)
        self.play(LaggedStart(*[Create(a) for a in uni], lag_ratio=0.05), run_time=1.5)
        self.wait(0.5)
        weighted = arcs(W, emph=True)
        self.play(Transform(uni, weighted), run_time=1.8)
        self.play(toks[1].animate.set_color(AC), Indicate(toks[1], color=AC, scale_factor=1.3), run_time=1.2)

        labels = VGroup(*[T(f"{w:.2f}", 18, AC if w > 0.3 else GREY_B).next_to(toks[j], DOWN, 0.15)
                          for j, w in enumerate(W) if j != IT])
        self.play(FadeIn(labels), run_time=0.8)
        res = T("it 의 새 표현 = 문장 전체의 가중합  →  animal 에 집중", 28).move_to(DOWN * 2.2)
        self.play(ReplacementTransform(q, res))
        note = T("(가중치 값은 설명용 예시)", 18, GREY_B).next_to(res, DOWN, 0.2)
        self.play(FadeIn(note))
        pad_to(self, 13)
