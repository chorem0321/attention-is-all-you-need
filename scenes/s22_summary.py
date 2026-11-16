import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

STEPS = [("Weighted Sum", VC), ("Soft Selection", AC), ("Q / K / V", QC), ("Dot Product", KC),
         ("Scaling √d_k", GREY_A), ("Softmax", AC), ("Scaled Dot-Product", AC),
         ("Multi-Head", "#C86BFF"), ("Concat", "#C86BFF"), ("W^O", FFC)]


class S22Summary(Scene):
    def construct(self):
        boxes = VGroup()
        for name, col in STEPS:
            boxes.add(box(name, w=2.3, h=0.8, fill="#1a1a1a", size=20, color=col, stroke=col))
        row1 = VGroup(*boxes[:5]).arrange(RIGHT, buff=0.45).move_to(UP * 1.4)
        row2 = VGroup(*boxes[5:]).arrange(LEFT, buff=0.45).move_to(DOWN * 1.0)  # 뱀 모양
        arrows = VGroup()
        for i in range(len(boxes) - 1):
            a, b = boxes[i], boxes[i + 1]
            if i == 4:
                arrows.add(Arrow(a.get_bottom(), b.get_top(), buff=0.08, stroke_width=3, color=GREY_B, tip_length=0.15))
            elif i < 4:
                arrows.add(Arrow(a.get_right(), b.get_left(), buff=0.05, stroke_width=3, color=GREY_B, tip_length=0.15))
            else:
                arrows.add(Arrow(a.get_left(), b.get_right(), buff=0.05, stroke_width=3, color=GREY_B, tip_length=0.15))

        self.play(FadeIn(boxes[0], shift=RIGHT * 0.2), run_time=0.6)
        for i in range(1, len(boxes)):
            self.play(GrowArrow(arrows[i - 1]), FadeIn(boxes[i], shift=0.15 * (RIGHT if i < 5 else LEFT)),
                      run_time=0.55)
        self.wait(0.5)
        self.play(LaggedStart(*[Indicate(b, scale_factor=1.08) for b in boxes], lag_ratio=0.12), run_time=2.5)

        eq = M(f"MultiHead = Concat(head<sub>1</sub>…head<sub>h</sub>) W<sup>O</sup>,   "
               f"head = softmax({c('Q', QC)}{c('K<sup>T</sup>', KC)}/√d<sub>k</sub>){c('V', VC)}", size=28
               ).move_to(DOWN * 2.6)
        self.play(Write(eq), run_time=1.6)
        final = T("Attention Is All You Need", 40, AC, bold=True).move_to(UP * 3.1)
        self.play(FadeIn(final, shift=DOWN * 0.2))
        self.play(Circumscribe(final, color=AC), run_time=1.2)
        pad_to(self, 16)
