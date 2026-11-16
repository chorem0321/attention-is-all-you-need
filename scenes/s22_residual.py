import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *


class S22Residual(Scene):
    def construct(self):
        # ── 왼쪽: Add & Norm 블록 ───────────────────
        X = -3.6
        xin = T("x  (Attention 입력)", 22).move_to([X, -3.2, 0])
        sub = box("Multi-Head Attention", w=3.2, h=0.75, fill="#3a3220", size=20, stroke=QC).move_to([X, -1.6, 0])
        drop = T("Dropout 0.1", 15, GREY_A).next_to(sub, RIGHT, 0.15)
        plus = plus_node([X, -0.1, 0])
        ln = box("LayerNorm", w=2.6, h=0.6, fill=NC, size=20).move_to([X, 1.1, 0])
        out = T("다음 sublayer (FFN) 로", 20, GREY_A).move_to([X, 2.4, 0])
        a1 = Arrow(xin.get_top(), sub.get_bottom(), buff=0.1, stroke_width=3, color=GREY_B, tip_length=0.14)
        a2 = Arrow(sub.get_top(), plus.get_bottom(), buff=0.03, stroke_width=3, color=GREY_B, tip_length=0.14)
        a3 = Arrow(plus.get_top(), ln.get_bottom(), buff=0.03, stroke_width=3, color=GREY_B, tip_length=0.14)
        a4 = Arrow(ln.get_top(), out.get_bottom(), buff=0.08, stroke_width=3, color=GREY_B, tip_length=0.14)
        p0 = xin.get_top() + UP * 0.35
        skip = VMobject(stroke_color=AC, stroke_width=4).set_points_as_corners(
            [p0, p0 + LEFT * 2.2, [X - 2.2, -0.1, 0], plus.get_left()])
        sl = T("residual (지름길)", 18, AC).next_to([X - 2.2, -1.6, 0], RIGHT, 0.08).rotate(PI / 2).move_to([X - 2.45, -1.6, 0])
        self.play(FadeIn(xin), Create(a1), FadeIn(sub), run_time=0.8)
        self.play(Create(a2), FadeIn(plus), FadeIn(drop), run_time=0.6)
        self.play(Create(skip), FadeIn(sl), run_time=1.0)
        self.play(Create(a3), FadeIn(ln), Create(a4), FadeIn(out), run_time=0.8)
        f = M(f"LayerNorm( {c('x', AC)} + Dropout(Sublayer(x)) )", size=28).move_to([X, 3.3, 0])
        self.play(Write(f), run_time=1.1)

        # ── 오른쪽: 왜 필요한가 ───────────────────
        R = 3.5
        h1 = T("① 정보 보존: '수정분'만 학습", 22, AC, bold=True).move_to([R, 3.3, 0])
        self.play(FadeIn(h1), run_time=0.5)
        vx = Arrow([R - 2.3, 1.5, 0], [R + 0.6, 2.4, 0], buff=0, color=WHITE, stroke_width=4, tip_length=0.16)
        vd = Arrow(vx.get_end(), vx.get_end() + np.array([0.9, -0.5, 0]), buff=0, color=QC, stroke_width=4, tip_length=0.16)
        vs = Arrow(vx.get_start(), vd.get_end(), buff=0, color=AC, stroke_width=4, tip_length=0.16)
        lx = T("x", 20).next_to(vx.get_center(), UP, 0.1)
        ld = T("Δ = Attention(x)", 18, QC).next_to(vd.get_end(), RIGHT, 0.1)
        ls = T("x + Δ", 18, AC).next_to(vs.get_center(), DOWN, 0.1)
        self.play(GrowArrow(vx), FadeIn(lx), run_time=0.5)
        self.play(GrowArrow(vd), FadeIn(ld), run_time=0.5)
        self.play(GrowArrow(vs), FadeIn(ls), run_time=0.6)
        n1 = T("원래 단어 정보(x)는 그대로, 문맥 정보만 덧칠", 17, GREY_A).move_to([R, 0.95, 0])
        self.play(FadeIn(n1), run_time=0.5)

        h2 = T("② 기울기 고속도로", 22, AC, bold=True).move_to([R, 0.15, 0])
        g = M(f"∂(x + F(x)) / ∂x = {c('I', AC)} + ∂F/∂x", size=28).next_to(h2, DOWN, 0.25)
        self.play(FadeIn(h2), Write(g), run_time=1.0)
        # 6층을 거슬러 내려가는 기울기
        layers = VGroup(*[Rectangle(width=0.55, height=0.35, stroke_color=GREY_B, stroke_width=1.2,
                                    fill_color=NC, fill_opacity=0.25) for _ in range(6)]).arrange(RIGHT, buff=0.18)
        layers.move_to([R + 0.3, -2.0, 0])
        lt = T("층 6 → 1", 15, GREY_A).next_to(layers, LEFT, 0.2)
        self.play(FadeIn(layers), FadeIn(lt), run_time=0.4)
        fade = VGroup(*[Line(layers[i].get_bottom() + DOWN * 0.15, layers[i].get_bottom() + DOWN * 0.15 + RIGHT * 0.73,
                             color=RED_C, stroke_width=5 * 0.6 ** (5 - i), stroke_opacity=0.9) for i in range(5, 0, -1)])
        hw = Line(layers.get_corner(UR) + UP * 0.15, layers.get_corner(UL) + UP * 0.15, color=AC, stroke_width=5).add_tip(tip_length=0.15)
        f1 = T("residual 없으면: 곱해질수록 소멸", 15, RED_C).next_to(layers, DOWN, 0.35)
        f2 = T("I 경로: 그대로 전달", 15, AC).next_to(layers, UP, 0.3)
        self.play(LaggedStart(*[Create(l) for l in fade], lag_ratio=0.2), FadeIn(f1), run_time=1.0)
        self.play(Create(hw), FadeIn(f2), run_time=0.8)
        self.play(Indicate(skip, color=AC), run_time=0.8)
        pad_to(self, 18)
