import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

CANDS = ["산책시킨다", "데리고", "본다", "먹인다", "</s>"]
PROBS = [0.72, 0.12, 0.07, 0.05, 0.04]  # 설명용 예시


class S28Output(Scene):
    def construct(self):
        # 디코더가 지금까지 만든 출력
        prev = VGroup(*[box(w, w=1.5, h=0.5, fill="#1d2a1f", size=18, stroke=VC) for w in ["<s>", "앨런이", "개를"]]
                      ).arrange(RIGHT, buff=0.15).move_to([-3.3, 3.2, 0])
        pl = T("출력:", 16, GREY_A).next_to(prev, LEFT, 0.2)
        self.play(FadeIn(prev), FadeIn(pl), run_time=0.6)
        dec = box("Decoder × 6", w=3.0, h=0.65, fill="#1b2433", size=20, stroke=KC).move_to([-3.3, 2.0, 0])
        enc = T("인코더 출력\n(Allen walks dog)", 16, GREY_A).next_to(dec, LEFT, 0.3)
        a0 = Arrow(prev.get_bottom(), dec.get_top(), buff=0.06, stroke_width=2.5, color=GREY_B, tip_length=0.12)
        a_e = Arrow(enc.get_right(), dec.get_left(), buff=0.06, stroke_width=2.5, color=VC, tip_length=0.12)
        self.play(Create(a0), FadeIn(dec), FadeIn(enc), Create(a_e), run_time=0.8)

        # 마지막 위치의 벡터 (512)
        hv = VGroup(*[Square(0.22, stroke_width=1, stroke_color=GREY_B, fill_color=KC,
                             fill_opacity=0.2 + 0.7 * abs(np.sin(i * 1.7))) for i in range(8)]).arrange(RIGHT, buff=0)
        hv.next_to(dec, DOWN, 0.55)
        hl = T("마지막 위치 벡터 (512)", 16, GREY_A).next_to(hv, DOWN, 0.1)
        a1 = Arrow(dec.get_bottom(), hv.get_top(), buff=0.05, stroke_width=2.5, color=GREY_B, tip_length=0.12)
        self.play(Create(a1), FadeIn(hv), FadeIn(hl), run_time=0.6)

        lin = box("Linear  512 → 어휘 수 (≈37,000)", w=4.4, h=0.6, fill="#2a2a2a", size=18).move_to([-3.3, -0.65, 0])
        share = T("가중치 = 임베딩 행렬과 공유", 15, EC).next_to(lin, DOWN, 0.08)
        a2 = Arrow(hl.get_bottom(), lin.get_top(), buff=0.06, stroke_width=2.5, color=GREY_B, tip_length=0.12)
        self.play(Create(a2), FadeIn(lin), FadeIn(share), run_time=0.7)
        sm = box("Softmax", w=2.4, h=0.55, fill="#3a2a1a", size=20, stroke=AC).move_to([-3.3, -2.0, 0])
        a3 = Arrow(share.get_bottom(), sm.get_top(), buff=0.06, stroke_width=2.5, color=GREY_B, tip_length=0.12)
        self.play(Create(a3), FadeIn(sm), run_time=0.5)

        # 확률 분포
        bc = barchart(PROBS, origin=[0.0, -2.3, 0], w=0.95, gap=0.45, max_h=3.6, color=AC, labels=CANDS,
                      fmt="{:.2f}", size=18)
        bt = T("다음 토큰 확률 (값은 예시)", 20, AC).next_to(bc, UP, 0.2)
        a4 = Arrow(sm.get_right(), bc[0].get_left(), buff=0.15, stroke_width=2.5, color=GREY_B, tip_length=0.12)
        self.play(Create(a4), FadeIn(bc[0]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bc[1]], lag_ratio=0.1),
                  FadeIn(bc[2]), FadeIn(bc[3]), FadeIn(bt), run_time=1.3)
        self.play(Indicate(bc[1][0], color=YELLOW), run_time=0.7)

        # 자기회귀: 선택된 토큰을 붙이고 다시 디코더로
        new = box("산책시킨다", w=1.7, h=0.5, fill="#3a2a1a", size=18, stroke=AC).next_to(prev, RIGHT, 0.15)
        self.play(TransformFromCopy(bc[3][0], new), run_time=1.0)
        loop = T("→ 출력에 붙여 다시 디코더로 (자기회귀), </s> 나올 때까지 반복", 18, GREY_A).move_to([2.6, 2.3, 0])
        beam = T("논문: beam search (beam 4, length penalty α = 0.6)", 17, GREY_A).next_to(loop, DOWN, 0.15)
        self.play(FadeIn(loop), FadeIn(beam), run_time=0.7)
        cls = T("참고: 분류 모델(BERT 등, 후속)은 [CLS] 벡터 → Linear → 클래스", 16, GREY_B).move_to([0, -3.65, 0])
        self.play(FadeIn(cls), run_time=0.5)
        pad_to(self, 16)
