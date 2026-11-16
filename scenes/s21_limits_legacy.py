import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *


def grid(n, size=2.6):
    cell = size / n
    g = VGroup(*[Square(cell, stroke_width=0.8 if n < 16 else 0.4, stroke_color=GREY_B,
                        fill_color=AC, fill_opacity=0.55)
                 .move_to([j * cell, -i * cell, 0]) for i in range(n) for j in range(n)])
    return g


class S21LimitsLegacy(Scene):
    def construct(self):
        lt = T("한계", 32, bold=True, color=RED_C).move_to([-3.6, 3.2, 0])
        rt = T("의의", 32, bold=True, color=AC).move_to([3.6, 3.2, 0])
        div = DashedLine(UP * 3.6, DOWN * 3.6, color=GREY_D)
        self.play(FadeIn(lt), Create(div))

        # O(n^2) attention matrix
        center = np.array([-3.6, 0.6, 0])
        g = grid(4).move_to(center)
        lab = T("n = 4  →  16 칸", 22).next_to(g, DOWN, 0.3)
        self.play(FadeIn(g), FadeIn(lab))
        for n in (8, 16):
            g2 = grid(n).move_to(center)
            lab2 = T(f"n = {n}  →  {n*n} 칸", 22).move_to(lab)
            self.play(Transform(g, g2), Transform(lab, lab2), run_time=1.0)
        mem = T("attention 행렬 메모리·연산 O(n²)\n→ 긴 문서/고해상도 입력에 부담", 22, GREY_A).next_to(lab, DOWN, 0.35)
        pe = T("순서 정보가 구조에 없음\n→ Positional Encoding 으로 외부 주입", 22, GREY_A).next_to(mem, DOWN, 0.35)
        self.play(FadeIn(mem, shift=UP * 0.2))
        self.play(FadeIn(pe, shift=UP * 0.2))

        # Legacy tree
        self.play(FadeIn(rt))
        root = box("Transformer (2017)", w=3.2, h=0.7, fill="#4a3216", size=22, stroke=AC).move_to([3.6, 1.6, 0])
        kids = VGroup(box("BERT\n(Encoder)", w=1.9, h=0.95, fill="#1b2f4a", size=18, stroke=KC),
                      box("GPT\n(Decoder)", w=1.9, h=0.95, fill="#4a4216", size=18, stroke=QC),
                      box("ViT\n(이미지 패치)", w=1.9, h=0.95, fill="#1b4a2a", size=18, stroke=VC)
                      ).arrange(RIGHT, buff=0.3).move_to([3.6, -0.6, 0])
        arrows = VGroup(*[Arrow(root.get_bottom(), k.get_top(), buff=0.08, stroke_width=2.5, color=GREY_B,
                                tip_length=0.15) for k in kids])
        self.play(FadeIn(root, shift=DOWN * 0.2))
        self.play(LaggedStart(*[AnimationGroup(Create(a), FadeIn(k, shift=DOWN * 0.2)) for a, k in zip(arrows, kids)],
                              lag_ratio=0.35), run_time=1.6)
        leg = T("recurrence 없이 attention 만으로\n→ 대규모 병렬 학습 · 현대 LLM 의 기반", 22, AC).move_to([3.6, -2.4, 0])
        self.play(Write(leg), run_time=1.4)
        self.play(Indicate(root, color=AC))
        pad_to(self, 13)
