import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

rng = np.random.default_rng(7)
NH = 14  # 2048 개 은닉 노드를 14개로 표현


class S24FfnStructure(Scene):
    def construct(self):
        f = M("FFN(x) = max(0, xW<sub>1</sub> + b<sub>1</sub>) W<sub>2</sub> + b<sub>2</sub>", size=32).move_to([0, 3.35, 0])
        self.play(Write(f), run_time=1.1)

        xi, xh, xo = -4.6, -0.4, 3.8
        ins = VGroup(*[Dot(radius=0.11, color=XC) for _ in range(5)]).arrange(DOWN, buff=0.38).move_to([xi, 0.2, 0])
        hid = VGroup(*[Circle(0.13, color=FFC, stroke_width=2, fill_color=FFC, fill_opacity=0.15) for _ in range(NH)]
                     ).arrange(DOWN, buff=0.05).move_to([xh, 0.45, 0])
        outs = VGroup(*[Dot(radius=0.11, color=XC) for _ in range(5)]).arrange(DOWN, buff=0.38).move_to([xo, 0.2, 0])
        li = T("d_model = 512", 20, GREY_A).next_to(ins, DOWN, 0.3)
        lh = T("d_ff = 2048 (4배)", 20, FFC).next_to(hid, RIGHT, 0.25).shift(DOWN * 1.6)
        lh.add_background_rectangle(color=BLACK, opacity=0.9, buff=0.06)
        lo = T("512", 20, GREY_A).next_to(outs, DOWN, 0.3)
        self.play(FadeIn(ins), FadeIn(li), run_time=0.5)

        e1 = VGroup(*[Line(a.get_center(), b.get_center(), stroke_width=0.6, color=GREY_B, stroke_opacity=0.35)
                      for a in ins for b in hid])
        w1 = T("W₁ : 512 × 2048\n① 넓게 펼치기", 20, WHITE).move_to([(xi + xh) / 2, 2.35, 0])
        self.play(Create(e1), FadeIn(hid), FadeIn(lh), FadeIn(w1), run_time=1.4)

        # ReLU: 음수 노드는 꺼짐
        z = rng.normal(0, 1, NH)
        on = z > 0
        relu = T("② ReLU = max(0, ·)", 22, AC).next_to(hid, RIGHT, 0.25).shift(UP * 1.4)
        self.play(FadeIn(relu), run_time=0.4)
        self.play(*[h.animate.set_fill(AC if o else BLACK, opacity=0.9 if o else 1).set_stroke(AC if o else GREY_D)
                    for h, o in zip(hid, on)], run_time=1.0)
        cnt = T(f"이번 입력: {on.sum()}/{NH} 노드만 켜짐", 18, AC).next_to(relu, DOWN, 0.15)
        self.play(FadeIn(cnt), run_time=0.4)

        e2 = VGroup(*[Line(a.get_center(), b.get_center(), stroke_width=0.8 if o else 0.3, color=AC if o else GREY_D,
                           stroke_opacity=0.6 if o else 0.2) for a, o in zip(hid, on) for b in outs])
        w2 = T("W₂ : 2048 × 512\n③ 다시 압축", 20, WHITE).move_to([(xh + xo) / 2 + 0.3, -2.35, 0])
        self.play(Create(e2), FadeIn(outs), FadeIn(lo), FadeIn(w2), run_time=1.2)
        self.wait(0.4)

        # position-wise: 토큰마다 독립 · 동일
        toks = VGroup(*[box(w, w=1.4, h=0.45, fill="#2a2a2a", size=18) for w in ["Allen", "walks", "dog"]]
                      ).arrange(DOWN, buff=0.15).move_to([-6.3, -2.6, 0])
        same = T("Position-wise: 각 토큰에 같은 W₁·W₂ 를 따로 적용\n(토큰끼리 섞는 건 Attention, FFN 은 토큰 내부 가공)\n"
                 "층마다 파라미터는 다름 · 커널 크기 1 conv 와 동일", 17, GREY_A, align=LEFT).next_to(toks, RIGHT, 0.3)
        self.play(FadeIn(toks), FadeIn(same), run_time=0.8)
        self.play(LaggedStart(*[Indicate(t, color=FFC) for t in toks], lag_ratio=0.25), run_time=1.0)
        pad_to(self, 16)
