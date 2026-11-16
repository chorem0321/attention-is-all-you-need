import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

WORDS = ["I", "love", "machine", "learning", "."]


def tokens(x_center):
    g = VGroup(*[box(w, w=1.05, h=0.5, fill="#2a2a2a", size=20) for w in WORDS])
    g.arrange(DOWN, buff=0.28).move_to([x_center, -0.3, 0])
    return g


class S02Background(Scene):
    def construct(self):
        div = DashedLine(UP * 3.6, DOWN * 3.6, color=GREY_D)
        lh = T("RNN / seq2seq", 34, bold=True).move_to([-3.6, 3.3, 0])
        rh = T("Transformer", 34, bold=True, color=AC).move_to([3.6, 3.3, 0])
        self.play(Create(div), FadeIn(lh), FadeIn(rh))

        # ── 왼쪽: 순차 처리 ────────────────────────────
        lt = tokens(-5.2)
        hs = VGroup(*[Circle(0.26, color=XC, stroke_width=2) for _ in WORDS])
        for h, t in zip(hs, lt):
            h.next_to(t, RIGHT, 1.0)
        hl = VGroup(*[T(f"h{i+1}", 18, GREY_A).move_to(h) for i, h in enumerate(hs)])
        self.play(FadeIn(lt), run_time=0.6)
        clock = T("step 0", 26, GREY_A).move_to([-2.4, -3.2, 0])
        self.add(clock)
        prev = None
        for i in range(len(WORDS)):
            anims = [Create(Arrow(lt[i].get_right(), hs[i].get_left(), buff=0.05,
                                  stroke_width=2, color=GREY_B, tip_length=0.15)),
                     FadeIn(hs[i]), FadeIn(hl[i]),
                     Transform(clock, T(f"step {i+1}", 26, GREY_A).move_to(clock))]
            if prev is not None:
                anims.append(Create(Arrow(hs[i - 1].get_bottom(), hs[i].get_top(), buff=0.03,
                                          stroke_width=3, color=YELLOW_E, tip_length=0.15)))
            self.play(*anims, run_time=0.55)
            self.play(hs[i].animate.set_fill(XC, 0.5), run_time=0.15)
            prev = hs[i]
        lnote = T("병렬화 불가 · 먼 토큰일수록 경로가 길다", 22, GREY_A).move_to([-3.6, -2.7, 0])
        self.play(FadeIn(lnote))
        far = CurvedArrow(lt[0].get_left() + LEFT * 0.05, lt[4].get_left() + LEFT * 0.05,
                          angle=PI / 2, color=RED_C, stroke_width=3)
        self.play(Create(far), run_time=0.8)

        # ── 오른쪽: 한 번에 모두 연결 ────────────────────
        rt = tokens(2.4)
        rt2 = tokens(5.2)
        self.play(FadeIn(rt), FadeIn(rt2), run_time=0.6)
        lines = VGroup()
        for a in rt:
            for b in rt2:
                lines.add(Line(a.get_right(), b.get_left(), stroke_width=1.8,
                               color=AC, stroke_opacity=0.7))
        clock2 = T("step 1", 26, AC).move_to([3.8, -3.2, 0])
        self.play(*[Create(l) for l in lines], FadeIn(clock2), run_time=1.2)
        rnote = T("모든 토큰 쌍을 한 번에 연결 (경로 길이 1)", 22, GREY_A).move_to([3.8, -2.7, 0])
        self.play(FadeIn(rnote))
        self.play(Indicate(rh, color=AC))
        pad_to(self, 15)
