import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

H = 8
HEAD_COLORS = color_gradient([ManimColor(AC), ManimColor("#C86BFF")], H)


class S15MultiHeadFormula(Scene):
    def construct(self):
        f1 = M(f"head<sub>i</sub> = Attention({c('QW<sub>i</sub><sup>Q</sup>', QC)}, "
               f"{c('KW<sub>i</sub><sup>K</sup>', KC)}, {c('VW<sub>i</sub><sup>V</sup>', VC)})", size=36).move_to(UP * 3.2)
        f2 = M("MultiHead(Q, K, V) = Concat(head<sub>1</sub>, …, head<sub>h</sub>) W<sup>O</sup>",
               size=36).next_to(f1, DOWN, 0.3)
        self.play(Write(f1), run_time=1.6)
        self.play(Write(f2), run_time=1.6)

        # Concat 블록 [H1 | ... | H8]
        bw, bh = 0.42, 1.4
        hs = VGroup(*[Rectangle(width=bw, height=bh, stroke_color=WHITE, stroke_width=1.2,
                                fill_color=HEAD_COLORS[i], fill_opacity=0.6) for i in range(H)]).arrange(RIGHT, buff=0)
        hs.move_to([-4.2, -0.6, 0])
        hl = VGroup(*[T(f"H{i+1}", 16).move_to(hs[i]) for i in range(H)])
        cap1 = T("Concat  (n × h·d_v)", 20, GREY_A).next_to(hs, DOWN, 0.2)
        self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.3) for r in hs], lag_ratio=0.08), FadeIn(hl), FadeIn(cap1),
                  run_time=1.2)

        # W^O 를 head 단위 행 블록으로
        times = T("×", 34, GREY_B).next_to(hs, RIGHT, 0.3)
        wh = 0.3
        wo = VGroup(*[Rectangle(width=1.6, height=wh, stroke_color=WHITE, stroke_width=1.2,
                                fill_color=HEAD_COLORS[i], fill_opacity=0.25) for i in range(H)]).arrange(DOWN, buff=0)
        wo.next_to(times, RIGHT, 0.3)
        wl = VGroup(*[M(f"W<sub>{i+1}</sub><sup>O</sup>", size=15).move_to(wo[i]) for i in range(H)])
        cap2 = M("W<sup>O</sup>  (h·d<sub>v</sub> × d<sub>model</sub>)", size=20, color=GREY_A).next_to(wo, DOWN, 0.2)
        self.play(FadeIn(times), FadeIn(wo), FadeIn(wl), FadeIn(cap2), run_time=1.0)

        # 블록 분해: Concat 은 열 블록, W^O 는 행 블록으로 쪼개진다
        hblocks = VGroup(*[VGroup(hs[i], hl[i]) for i in range(H)])
        wblocks = VGroup(*[VGroup(wo[i], wl[i]) for i in range(H)])
        wc = wblocks.get_center()
        right = hblocks.get_right()[0]
        hblocks.generate_target()
        hblocks.target.arrange(RIGHT, buff=0.1).move_to(hblocks.get_center())
        hblocks.target.shift(RIGHT * (right - hblocks.target.get_right()[0]))  # 오른쪽 끝 고정
        self.play(MoveToTarget(hblocks),
                  wblocks.animate.arrange(DOWN, buff=0.07).move_to(wc),
                  FadeOut(cap1), FadeOut(cap2), run_time=1.0)

        # 쌍 강조: H_i ↔ W_i^O
        for i in [0, 1, H - 1]:
            self.play(Indicate(VGroup(hs[i], hl[i]), color=AC), Indicate(VGroup(wo[i], wl[i]), color=AC),
                      run_time=0.6)

        eq = M("= " + " + ".join([f"H<sub>{i}</sub>W<sub>{i}</sub><sup>O</sup>" for i in (1, 2)])
               + " + … + H<sub>8</sub>W<sub>8</sub><sup>O</sup>  =  Σ<sub>i</sub> H<sub>i</sub>W<sub>i</sub><sup>O</sup>",
               size=32).move_to(DOWN * 2.6)
        self.play(Write(eq), run_time=1.6)
        msg = T("W^O = 각 head 의 출력을\n하나로 '섞는' 선형 결합", 26, AC).move_to([3.9, -0.6, 0])
        self.play(FadeIn(msg, shift=LEFT * 0.2))
        self.play(Circumscribe(eq, color=AC), run_time=1.2)
        pad_to(self, 17)
