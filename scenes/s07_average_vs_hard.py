import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *


class S07AverageVsHard(Scene):
    def construct(self):
        # 왼쪽: Average
        lt = T("Average", 32, bold=True).move_to([-3.5, 3.1, 0])
        lf = M(f"{c('α<sub>i</sub>', AC)} = 1/m", size=30).next_to(lt, DOWN, 0.2)
        avg = barchart([0.25] * 4, origin=[-5.3, -0.6, 0], w=0.6, gap=0.35, max_h=2.4,
                       labels=["V1", "V2", "V3", "V4"])
        ln = T("모든 위치를 똑같이 → 구분 없음", 22, GREY_A).next_to(avg, DOWN, 0.3)

        # 오른쪽: Hard selection
        rt = T("Hard Selection", 32, bold=True).move_to([3.5, 3.1, 0])
        rf = M(f"{c('α', AC)} = (0, 1, 0)   one-hot", size=30).next_to(rt, DOWN, 0.2)
        hard = barchart([0, 1, 0], origin=[2.4, -0.6, 0], w=0.6, gap=0.35, max_h=2.4,
                        labels=["V1", "V2", "V3"])
        rn = T("하나만 고름 → 나머지 정보는 버림", 22, GREY_A).next_to(hard, DOWN, 0.3)

        self.play(FadeIn(lt), Write(lf))
        self.play(Create(avg[0]), *[GrowFromEdge(b, DOWN) for b in avg[1]], FadeIn(avg[2]), FadeIn(avg[3]),
                  run_time=1.2)
        self.play(FadeIn(ln))
        self.wait(0.6)
        self.play(FadeIn(rt), Write(rf))
        self.play(Create(hard[0]), *[GrowFromEdge(b, DOWN) for b in hard[1]], FadeIn(hard[2]), FadeIn(hard[3]),
                  run_time=1.2)
        self.play(FadeIn(rn))
        self.play(Indicate(hard[1][1], color=AC))
        self.wait(0.6)

        # 스펙트럼
        line = Line([-5, -2.9, 0], [5, -2.9, 0], color=GREY_B, stroke_width=4)
        e1 = Dot(line.get_start(), color=WHITE)
        e2 = Dot(line.get_end(), color=WHITE)
        l1 = T("Average", 22).next_to(e1, DOWN, 0.15)
        l2 = T("Hard", 22).next_to(e2, DOWN, 0.15)
        self.play(Create(line), FadeIn(e1), FadeIn(e2), FadeIn(l1), FadeIn(l2))
        qm = T("?", 56, AC, bold=True).move_to([0, -2.6, 0])
        self.play(FadeIn(qm, scale=0.5))
        self.play(Indicate(qm, scale_factor=1.4, color=AC), run_time=1)
        self.play(Wiggle(qm), run_time=1)
        between = T("그 사이 어딘가?", 22, AC).next_to(qm, RIGHT, 0.3)
        self.play(FadeIn(between))
        pad_to(self, 13)
