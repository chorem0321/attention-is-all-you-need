import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *


class S26Stack(Scene):
    def construct(self):
        # ── 왼쪽: 인코더 블록 하나 (Add & Norm ② 강조) ──
        X = -4.0
        names = [("Multi-Head Attention", "#3a3220", QC), ("Add & Norm ①", NC, WHITE),
                 ("Feed Forward", "#2c2440", FFC), ("Add & Norm ②", NC, WHITE)]
        blks = VGroup(*[box(n, w=3.0, h=0.6, fill=f, size=19, stroke=s) for n, f, s in names])
        ys = [-1.5, -0.5, 0.6, 1.6]
        for b, y in zip(blks, ys):
            b.move_to([X, y, 0])
        inp = T("x (③ 입력)", 18, GREY_A).move_to([X, -2.75, 0])
        arr = VGroup(Arrow(inp.get_top(), blks[0].get_bottom(), buff=0.08, stroke_width=2.5, color=GREY_B, tip_length=0.12),
                     *[Arrow(blks[i].get_top(), blks[i + 1].get_bottom(), buff=0.04, stroke_width=2.5, color=GREY_B,
                             tip_length=0.12) for i in range(3)])
        outa = Arrow(blks[3].get_top(), blks[3].get_top() + UP * 0.7, buff=0.04, stroke_width=2.5, color=GREY_B, tip_length=0.12)

        def skip(y0, y1, col):
            return VMobject(stroke_color=col, stroke_width=3).set_points_as_corners(
                [[X, y0, 0], [X - 1.9, y0, 0], [X - 1.9, y1, 0], [X - 1.5, y1, 0]])

        s1 = skip(-2.2, -0.5, AC)
        s2 = skip(0.05, 1.6, AC)
        frame = SurroundingRectangle(blks, buff=0.25, color=KC, corner_radius=0.15)
        fl = T("Encoder Layer", 20, KC, bold=True).next_to(frame, UP, 0.08).shift(UP * 0.7)
        self.play(FadeIn(inp), Create(arr[0]), FadeIn(blks[0]), run_time=0.6)
        self.play(Create(arr[1]), FadeIn(blks[1]), Create(s1), run_time=0.6)
        self.play(Create(arr[2]), FadeIn(blks[2]), run_time=0.5)
        self.play(Create(arr[3]), FadeIn(blks[3]), Create(s2), run_time=0.7)
        f2 = M("⑥ LayerNorm( z + FFN(z) )", size=24, color=AC).next_to(blks[3], RIGHT, 0.35)
        self.play(Write(f2), Indicate(blks[3], color=AC), Create(outa), run_time=1.0)
        self.play(Create(frame), FadeIn(fl), run_time=0.6)
        self.wait(0.4)

        # ── 오른쪽: × 6 쌓기 ──────────────────────
        self.play(FadeOut(f2), run_time=0.3)
        mini = VGroup(*[box(f"Layer {i + 1}", w=2.6, h=0.5, fill="#1b2433", size=18, stroke=KC) for i in range(6)]
                      ).arrange(UP, buff=0.18).move_to([2.2, -0.15, 0])
        self.play(TransformFromCopy(frame, mini[0]), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in mini[1:]], lag_ratio=0.15), run_time=1.2)
        br = Brace(mini, RIGHT, color=KC)
        bl = T("N = 6\n(구조 같고\n가중치는 층마다 다름)", 17, KC).next_to(br, RIGHT, 0.15)
        self.play(GrowFromCenter(br), FadeIn(bl), run_time=0.6)
        tok = T("Allen walks dog", 18, WHITE).next_to(mini, DOWN, 0.35)
        dot = Dot(mini[0].get_bottom() + DOWN * 0.1, color=AC, radius=0.1)
        self.play(FadeIn(tok), FadeIn(dot), run_time=0.4)
        self.play(dot.animate.move_to(mini[-1].get_top() + UP * 0.15), run_time=1.6, rate_func=linear)
        mem = T("인코더 출력 (3 × 512)\n→ 디코더의 K, V", 18, VC).next_to(mini, UP, 0.3)
        self.play(FadeIn(mem, shift=UP * 0.1), run_time=0.6)
        lo = T("하위 층: 가까운 단어·구문 관계", 16, GREY_A).next_to(mini[1], LEFT, 0.25)
        hi = T("상위 층: 더 넓은 문맥·의미", 16, GREY_A).next_to(mini[4], LEFT, 0.25)
        cav = T("※ 층별 역할은 후속 분석 연구들의 경향 (논문 주장 아님)", 15, GREY_B).move_to([2.3, -3.65, 0])
        self.play(FadeIn(lo), FadeIn(hi), FadeIn(cav), run_time=0.7)
        pad_to(self, 17)
