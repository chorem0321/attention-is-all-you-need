import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

DK = 64
RAW = np.array([24.0, 16.0, 8.0, 0.0])  # d_k 가 클 때의 큰 score 예시
SCALED = RAW / np.sqrt(DK)  # [3, 2, 1, 0]


class S11Scaling(Scene):
    def construct(self):
        # 근거 (논문 각주 4)
        l1 = M(f"{c('q', QC)}, {c('k', KC)} 성분 ~ 평균 0, 분산 1 (독립)", size=28).move_to([-3.3, 3.2, 0])
        l2 = M(f"⇒  Var({c('q', QC)}·{c('k', KC)}) = d<sub>k</sub>", size=30).next_to(l1, DOWN, 0.25).align_to(l1, LEFT)
        l3 = M("d<sub>k</sub> ↑  ⇒  score 크기 ↑  ⇒  softmax 포화  ⇒  기울기 ≈ 0", size=28,
               color=GREY_A).next_to(l2, DOWN, 0.25).align_to(l1, LEFT)
        self.play(Write(l1), run_time=1.2)
        self.play(Write(l2), run_time=1)
        self.play(FadeIn(l3, shift=UP * 0.2), run_time=0.8)

        labs = ["k1", "k2", "k3", "k4"]
        # 왼쪽: 원래 score → softmax
        sraw = barchart(RAW, origin=[-6.3, -2.6, 0], w=0.5, gap=0.25, max_h=2.2, vmax=24,
                        color=GREY_B, fmt="{:.0f}", labels=labs, size=18)
        p_raw = softmax(RAW)
        braw = barchart(p_raw, origin=[-2.9, -2.6, 0], w=0.5, gap=0.25, max_h=2.2, color=AC,
                        fmt="{:.2f}", labels=labs, size=18)
        t_s = T("score", 22, GREY_A).next_to(sraw, UP, 0.25)
        t_p = T("softmax", 22, AC).next_to(braw, UP, 0.25).align_to(t_s, DOWN)
        arr = Arrow(sraw.get_right(), braw.get_left(), buff=0.15, color=GREY_B, stroke_width=3)
        self.play(FadeIn(sraw), FadeIn(t_s), run_time=0.8)
        self.play(Create(arr), FadeIn(braw), FadeIn(t_p), run_time=1)
        sat = T("거의 one-hot  →  포화", 22, RED_C).next_to(braw, DOWN, 0.15)
        self.play(FadeIn(sat), Indicate(braw[1][0], color=RED_C))
        self.wait(0.6)

        # 오른쪽: √d_k 로 나눈 뒤
        div = M(f"÷ √d<sub>k</sub> = ÷ {int(np.sqrt(DK))}", size=30, color=QC).move_to([3.6, 1.0, 0])
        sscl = barchart(SCALED, origin=[0.6, -2.6, 0], w=0.5, gap=0.25, max_h=2.2, vmax=3,
                        color=GREY_B, fmt="{:.0f}", labels=labs, size=18)
        p_scl = softmax(SCALED)
        bscl = barchart(p_scl, origin=[3.9, -2.6, 0], w=0.5, gap=0.25, max_h=2.2, color=AC,
                        fmt="{:.2f}", labels=labs, size=18)
        t_s2 = T("score / √d_k", 22, GREY_A).next_to(sscl, UP, 0.25)
        t_p2 = T("softmax", 22, AC).next_to(bscl, UP, 0.25).align_to(t_s2, DOWN)
        arr2 = Arrow(sscl.get_right(), bscl.get_left(), buff=0.15, color=GREY_B, stroke_width=3)
        self.play(FadeIn(div, shift=DOWN * 0.2))
        self.play(TransformFromCopy(sraw, sscl), FadeIn(t_s2), run_time=1.2)
        self.play(Create(arr2), TransformFromCopy(braw, bscl), FadeIn(t_p2), run_time=1.2)
        ok = T("부드러운 분포 → 기울기 유지", 20, VC).next_to(bscl, DOWN, 0.15).align_to(bscl, RIGHT)
        self.play(FadeIn(ok))
        self.play(Indicate(bscl[1], color=AC))
        pad_to(self, 15)
