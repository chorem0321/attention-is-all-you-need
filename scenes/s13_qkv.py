import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *


def card(title, desc, color):
    r = RoundedRectangle(corner_radius=0.15, width=3.6, height=1.3, stroke_color=color,
                         fill_color=color, fill_opacity=0.12, stroke_width=2.5)
    t = T(title, 30, color, bold=True).move_to(r.get_center() + UP * 0.25)
    d = T(desc, 20, GREY_A).move_to(r.get_center() + DOWN * 0.3)
    return VGroup(r, t, d)


class S13QKV(Scene):
    def construct(self):
        head = T("검색 시스템 비유", 26, GREY_A).move_to(UP * 3.4)
        cards = VGroup(card("Query", "검색어: 내가 찾는 것", QC),
                       card("Key", "색인/제목: 매칭 기준", KC),
                       card("Value", "실제 문서: 가져올 내용", VC)).arrange(RIGHT, buff=0.5).move_to(UP * 2.3)
        self.play(FadeIn(head))
        self.play(LaggedStart(*[FadeIn(cd, shift=DOWN * 0.2) for cd in cards], lag_ratio=0.3), run_time=1.6)
        flow = T("Query 로 Key 들과 유사도를 재고 → 그 비율대로 Value 를 섞는다", 22).next_to(cards, DOWN, 0.3)
        self.play(FadeIn(flow))
        self.wait(1)

        # 같은 X 에서 세 투영
        X = mat(2.2, 1.6, XC, "X", "n × d_model")
        X.move_to([-5.0, -1.8, 0])
        self.play(FadeIn(X, shift=RIGHT * 0.3))
        rows = [(QC, "Q", "W<sup>Q</sup>", 0.0), (KC, "K", "W<sup>K</sup>", -1.25), (VC, "V", "W<sup>V</sup>", -2.5)]
        outs = VGroup()
        for col, name, wname, dy in rows:
            y = -0.55 + dy
            W = mat(1.2, 1.0, col, wname, None, size=24, op=0.18).move_to([-1.0, y, 0])
            res = mat(1.0, 1.0, col, name, None, size=30, op=0.45).move_to([2.2, y, 0])
            a1 = Arrow(X.get_right(), W.get_left(), buff=0.15, stroke_width=2.5, color=col, tip_length=0.15)
            a2 = Arrow(W.get_right(), res.get_left(), buff=0.15, stroke_width=2.5, color=col, tip_length=0.15)
            self.play(Create(a1), FadeIn(W), run_time=0.6)
            self.play(Create(a2), TransformFromCopy(X[0], res[0]), FadeIn(res[1]), run_time=0.8)
            outs.add(res)
        eq = M(f"{c('Q', QC)} = X{c('W<sup>Q</sup>', QC)},  {c('K', KC)} = X{c('W<sup>K</sup>', KC)},  "
               f"{c('V', VC)} = X{c('W<sup>V</sup>', VC)}", size=30)
        if eq.width > 3.8:
            eq.scale_to_fit_width(3.8)
        eq.move_to([5.0, -1.2, 0])
        note = T("같은 입력, 서로 다른 역할\n(학습되는 투영 행렬)", 22, GREY_A).next_to(eq, DOWN, 0.4)
        self.play(Write(eq), run_time=1.2)
        self.play(FadeIn(note))
        self.play(*[Indicate(o, color=o[0].get_color()) for o in outs], run_time=1)
        pad_to(self, 16)
