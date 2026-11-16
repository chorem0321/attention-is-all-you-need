import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *


class S08SoftSelection(Scene):
    def construct(self):
        org = [-5.6, -0.2, 0]
        hard = barchart([0, 1, 0], origin=org, w=0.7, gap=0.4, max_h=2.6, labels=["V1", "V2", "V3"])
        soft = barchart([0.15, 0.70, 0.15], origin=org, w=0.7, gap=0.4, max_h=2.6, labels=["V1", "V2", "V3"])
        head = T("Hard  (0, 1, 0)", 30, bold=True).move_to([-4.0, 3.2, 0])
        head2 = T("Soft  (0.15, 0.70, 0.15)", 30, bold=True, color=AC).move_to([-4.0, 3.2, 0])
        self.play(FadeIn(head), Create(hard[0]), *[GrowFromEdge(b, DOWN) for b in hard[1]],
                  FadeIn(hard[2]), FadeIn(hard[3]), run_time=1.2)
        self.wait(0.6)
        self.play(Transform(hard, soft), Transform(head, head2), run_time=1.6)
        n1 = T("가장 관련 있는 곳에 집중하면서도\n다른 위치 정보도 조금씩 섞는다", 24, GREY_A,
               ).next_to(hard, DOWN, 0.45)
        self.play(FadeIn(n1, shift=UP * 0.2))

        # 스펙트럼 위 위치
        line = Line([-5.4, -3.0, 0], [-0.8, -3.0, 0], color=GREY_B, stroke_width=4)
        l1 = T("Average", 18).next_to(line.get_start(), DOWN, 0.15)
        l2 = T("Hard", 18).next_to(line.get_end(), DOWN, 0.15)
        mark = Triangle(color=AC, fill_opacity=1).scale(0.12).rotate(PI).move_to(line.point_from_proportion(0.7) + UP * 0.2)
        ml = T("Soft", 20, AC).next_to(mark, UP, 0.08)
        self.play(Create(line), FadeIn(l1), FadeIn(l2), FadeIn(mark, shift=DOWN * 0.2), FadeIn(ml))

        # 오른쪽: 미분 가능성 비교
        ax1 = Axes(x_range=[-3, 3, 1], y_range=[0, 1.1, 0.5], x_length=2.6, y_length=1.6,
                   tips=False, axis_config={"stroke_width": 2, "color": GREY_B}).move_to([2.0, 1.4, 0])
        ax2 = ax1.copy().move_to([5.3, 1.4, 0])
        step = VGroup(ax1.plot(lambda x: 0, x_range=[-3, -0.001], color=RED_C, stroke_width=4),
                      ax1.plot(lambda x: 1, x_range=[0.001, 3], color=RED_C, stroke_width=4))
        smooth = ax2.plot(lambda x: 1 / (1 + np.exp(-2.2 * x)), x_range=[-3, 3], color=AC, stroke_width=4)
        t1 = T("Hard: argmax", 22, RED_C).next_to(ax1, UP, 0.25)
        t2 = T("Soft: softmax", 22, AC).next_to(ax2, UP, 0.25)
        d1 = T("기울기 = 0\n(거의 모든 곳)\n→ 학습이 까다로움", 18, GREY_A).next_to(ax1, DOWN, 0.3)
        d2 = T("어디서나\n미분 가능\n→ 경사하강 학습", 18, GREY_A).next_to(ax2, DOWN, 0.3)
        self.play(Create(ax1), Create(ax2), FadeIn(t1), FadeIn(t2), run_time=1)
        self.play(Create(step), Create(smooth), run_time=1.5)
        self.play(FadeIn(d1), FadeIn(d2))
        foot = T("※ Hard attention 도 불가능은 아님\n(REINFORCE 등 샘플링 기반 학습)", 18, GREY_B
                 ).move_to([3.65, -2.6, 0])
        self.play(FadeIn(foot))
        self.play(Indicate(smooth, color=AC))
        pad_to(self, 15)
