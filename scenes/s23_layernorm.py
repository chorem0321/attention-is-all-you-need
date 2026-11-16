import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

RAW = np.array([3.1, -0.4, 5.2, 1.0, -2.3, 4.0, 0.6, 2.8, -1.1, 3.6])


class S23LayerNorm(Scene):
    def construct(self):
        f = M("LN(x) = γ ⊙ (x − μ) / √(σ<sup>2</sup> + ε) + β", size=32).move_to([0, 3.35, 0])
        sub = M("μ, σ: 한 토큰 벡터의 d<sub>model</sub> = 512 개 값에 대해 계산", size=22, color=GREY_A).next_to(f, DOWN, 0.15)
        self.play(Write(f), run_time=1.2)
        self.play(FadeIn(sub), run_time=0.5)

        # ① 원래 값 (x + Sublayer(x)): 크기·중심이 들쭉날쭉
        o1 = np.array([-6.6, 0.4, 0])
        b1 = vbar(RAW, o1, scale=0.33, color=XC, neg_color=RED_C)
        t1 = T("x + Sublayer(x)  (한 토큰, 10칸만)", 18, GREY_A).next_to(b1, DOWN, 0.95).align_to(b1, LEFT)
        self.play(FadeIn(b1), FadeIn(t1), run_time=0.8)
        mu = RAW.mean()
        sd = RAW.std()
        mline = DashedLine(o1 + UP * mu * 0.33 + LEFT * 0.1, o1 + UP * mu * 0.33 + RIGHT * 3.5, color=AC, stroke_width=2)
        ml = T(f"μ = {mu:.2f},  σ = {sd:.2f}  (점선 = μ)", 18, AC).next_to(b1, UP, 0.15)
        self.play(Create(mline), FadeIn(ml), run_time=0.7)

        # ② 정규화
        norm = (RAW - mu) / sd
        o2 = np.array([-1.7, 0.4, 0])
        b2 = vbar(norm, o2, scale=0.55, color=NC, neg_color=RED_C)
        ar = Arrow([-2.9, 0.4, 0], [-1.85, 0.4, 0], buff=0, color=GREY_B, stroke_width=3, tip_length=0.14)
        t2 = T("평균 0 · 분산 1", 18, GREY_A).next_to(b2, DOWN, 0.95).align_to(b2, LEFT)
        self.play(Create(ar), TransformFromCopy(b1, b2), FadeIn(t2), run_time=1.2)

        # ③ γ, β
        o3 = np.array([3.2, 0.4, 0])
        b3 = vbar(norm * 1.2 + 0.3, o3, scale=0.55, color=FFC, neg_color=RED_C)
        ar2 = Arrow([2.0, 0.4, 0], [3.05, 0.4, 0], buff=0, color=GREY_B, stroke_width=3, tip_length=0.14)
        t3 = T("γ, β (학습): 필요한 스케일 복원", 18, GREY_A).next_to(b3, DOWN, 0.95).align_to(b3, LEFT)
        self.play(Create(ar2), TransformFromCopy(b2, b3), FadeIn(t3), run_time=1.2)
        self.wait(0.4)

        # LayerNorm vs BatchNorm
        cell = 0.26
        grid = VGroup(*[Square(cell, stroke_width=1, stroke_color=GREY_D, fill_color=GREY_E, fill_opacity=0.5)
                        .move_to([j * cell, -i * cell, 0]) for i in range(5) for j in range(10)])
        grid.move_to([-3.4, -2.75, 0])
        rowh = SurroundingRectangle(VGroup(*grid[10:20]), color=AC, buff=0.02, stroke_width=3)
        colh = SurroundingRectangle(VGroup(*[grid[i * 10 + 3] for i in range(5)]), color=KC, buff=0.02, stroke_width=3)
        gl = T("행 = 토큰,  열 = 차원(feature)", 15, GREY_A).next_to(grid, UP, 0.1)
        self.play(FadeIn(grid), FadeIn(gl), run_time=0.5)
        self.play(Create(rowh), run_time=0.5)
        ln_t = T("LayerNorm: 토큰 하나의 모든 차원 → 배치 크기·문장 길이와 무관", 18, AC).move_to([2.6, -2.45, 0])
        self.play(FadeIn(ln_t), run_time=0.5)
        self.play(Create(colh), run_time=0.5)
        bn_t = T("BatchNorm: 한 차원을 배치 전체로 → 길이 제각각인 문장엔 불편", 18, KC).move_to([2.6, -3.05, 0])
        self.play(FadeIn(bn_t), run_time=0.5)
        why = T("효과: 층을 거듭해도 값의 크기가 폭주·소멸하지 않음 → 학습 안정", 20, WHITE).move_to([0, -3.65, 0])
        self.play(FadeIn(why, shift=UP * 0.1), run_time=0.6)
        pad_to(self, 17)
