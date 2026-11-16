import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

SUBS = ["문장 → 토큰 → 512차원 벡터", "위치마다 고유한 sin/cos 벡터를 더함", "단어끼리 서로 참고해 문맥 반영",
        "x + Attention(x) → LayerNorm", "넓히고 → ReLU로 거르고 → 압축", "x + FFN(x) → LayerNorm",
        "③~⑥ 블록을 6층 쌓기", "다음 토큰 확률 분포"]


class S04Pipeline(Scene):
    def construct(self):
        sent = T("\"Allen walks dog\"", 34, WHITE, bold=True).move_to([0, 3.25, 0])
        self.play(Write(sent), run_time=1.0)

        boxes = VGroup(*[pipe_box(i, SUBS[i]) for i in range(8)])
        arrows = pipe_arrows(boxes)
        first = Arrow(sent.get_bottom(), boxes[0].get_top(), buff=0.12, stroke_width=3, color=GREY_B,
                      tip_length=0.15, path_arc=0.5)
        self.play(GrowArrow(first), FadeIn(boxes[0], shift=DOWN * 0.15), run_time=0.7)
        for i in range(1, 8):
            self.play(GrowArrow(arrows[i - 1]), FadeIn(boxes[i]), run_time=0.45)

        # Encoder block = ③④⑤⑥ (오른쪽 2×2)
        enc = DashedVMobject(SurroundingRectangle(VGroup(boxes[2], boxes[3], boxes[4], boxes[5]), buff=0.18,
                                                  corner_radius=0.2, color=KC, stroke_width=2.5), num_dashes=70)
        enc_l = T("Encoder Block", 22, KC, bold=True).next_to(enc, UP, 0.1).align_to(enc, RIGHT)
        self.play(Create(enc), FadeIn(enc_l), run_time=1.0)
        loop_l = T("↻  이 블록을 × 6 층 반복 (⑦)", 20, KC, bold=True).next_to(enc, DOWN, 0.12).align_to(enc, RIGHT)
        self.play(FadeIn(loop_l, shift=UP * 0.1), run_time=0.8)

        # 토큰 하나가 파이프라인을 따라 흘러간다
        dot = Circle(0.27, color=WHITE, stroke_width=4).move_to(boxes[0][1]).set_z_index(5)
        self.play(FadeIn(dot, scale=2), run_time=0.3)
        for i in range(1, 8):
            self.play(dot.animate.move_to(boxes[i][1].get_center()),
                      Indicate(boxes[i][0], color=PIPE[i][2], scale_factor=1.04), run_time=0.45)
        cap = T("오늘 발표는 이 순서 그대로 따라갑니다", 26, AC).move_to([0, -3.2, 0])
        self.play(FadeIn(cap, shift=UP * 0.2), Flash(dot, color=AC), run_time=0.9)
        pad_to(self, 17)
