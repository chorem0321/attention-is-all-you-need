import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

COLS = ["animal", "street", "tired"]


class S13OneHead(Scene):
    def construct(self):
        q = T("Query:  it", 34, QC, bold=True).move_to([-4.2, 2.6, 0])
        need = VGroup(T("필요한 정보 1:  '누구'인가? → animal", 24),
                      T("필요한 정보 2:  어떤 상태인가? → tired", 24)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        need.next_to(q, DOWN, 0.5).align_to(q, LEFT)
        self.play(FadeIn(q))
        self.play(LaggedStart(*[FadeIn(n, shift=RIGHT * 0.2) for n in need], lag_ratio=0.4), run_time=1.4)

        org = [2.2, -1.0, 0]
        one = barchart([0.80, 0.10, 0.10], origin=org, w=0.9, gap=0.5, max_h=2.6, labels=COLS)
        split = barchart([0.45, 0.10, 0.45], origin=org, w=0.9, gap=0.5, max_h=2.6, labels=COLS)
        ht = T("하나의 head = 하나의 softmax 분포", 26, AC).next_to(one, UP, 0.5)
        self.play(FadeIn(ht), Create(one[0]), *[GrowFromEdge(b, DOWN) for b in one[1]], FadeIn(one[2]),
                  FadeIn(one[3]), run_time=1.2)
        self.wait(0.6)
        c1 = T("animal 에 집중하면 tired 를 놓친다", 22, GREY_A).move_to([-3.6, -1.0, 0])
        self.play(FadeIn(c1))
        self.wait(0.6)
        self.play(Transform(one, split), run_time=1.4)
        c2 = T("둘 다 보려 하면 → 양쪽 모두 희석 (합 = 1)", 22, RED_C).next_to(c1, DOWN, 0.3).align_to(c1, LEFT)
        self.play(FadeIn(c2))
        ans = T("서로 다른 관점을 동시에?  →  head 를 여러 개!", 30, AC).to_edge(DOWN, buff=0.5)
        self.play(Write(ans), run_time=1.3)
        pad_to(self, 12)
