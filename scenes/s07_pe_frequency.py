import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

W_FAST = 1.0  # i = 0 : ω = 1/10000^0
W_SLOW = 0.1  # i = 64: ω = 1/10000^(128/512) = 0.1
P2 = 44       # 44 / 2π ≈ 7.003 → 빠른 파동에서는 pos 0 과 거의 같은 위상


class S07PeFrequency(Scene):
    def construct(self):
        q = T("주기 함수인데 어떻게 위치마다 '고유'할까?", 30, bold=True).move_to([0, 3.4, 0])
        f1 = M("PE<sub>(pos, 2i)</sub> = sin(pos · ω<sub>i</sub>),   PE<sub>(pos, 2i+1)</sub> = cos(pos · ω<sub>i</sub>),   "
               "ω<sub>i</sub> = 1 / 10000<sup>2i / d<sub>model</sub></sup>", size=22, color=GREY_A).next_to(q, DOWN, 0.2)
        self.play(Write(q), run_time=0.9)
        self.play(FadeIn(f1), run_time=0.7)

        def ax_at(y):
            return Axes(x_range=[0, 48, 4], y_range=[-1.2, 1.2, 1], x_length=6.6, y_length=1.55, tips=False,
                        axis_config={"stroke_width": 1.5, "color": GREY_D}).move_to([-3.3, y, 0])

        a1, a2 = ax_at(1.05), ax_at(-1.15)
        c1 = a1.plot(lambda p: np.sin(W_FAST * p), x_range=[0, 48, 0.05], color=QC, stroke_width=2.5)
        c2 = a2.plot(lambda p: np.sin(W_SLOW * p), x_range=[0, 48, 0.05], color=KC, stroke_width=2.5)
        l1 = M("i = 0 : ω = 1  (빠름, 파장 2π ≈ 6.3)", size=18, color=QC).next_to(a1, UP, 0.02).align_to(a1, LEFT)
        l2 = M("i = 64 : ω = 0.1  (느림, 파장 ≈ 63)", size=18, color=KC).next_to(a2, UP, 0.02).align_to(a2, LEFT)
        self.play(Create(a1), Create(c1), FadeIn(l1), run_time=1.2)

        def marks(ax, w):
            g = VGroup()
            for p, col in ((0, AC), (P2, RED_C)):
                d = Dot(ax.c2p(p, np.sin(w * p)), radius=0.08, color=col)
                v = DashedLine(ax.c2p(p, -1.2), ax.c2p(p, 1.2), stroke_width=1.5, color=col, dash_length=0.06)
                g.add(VGroup(v, d))
            return g

        m1 = marks(a1, W_FAST)
        t0 = T("pos 0", 16, AC).next_to(m1[0], DOWN, 0.02)
        t44 = T("pos 44", 16, RED_C).next_to(m1[1], DOWN, 0.02)
        self.play(FadeIn(m1), FadeIn(t0), FadeIn(t44), run_time=0.7)
        warn = T("한 주파수만 보면 pos 0 ≈ pos 44 (44 ≈ 7바퀴) → 구분 불가", 20, RED_C).next_to(a1, DOWN, 0.05)
        self.play(FadeIn(warn), run_time=0.6)
        self.wait(0.6)

        self.play(FadeOut(warn), Create(a2), Create(c2), FadeIn(l2), run_time=1.2)
        m2 = marks(a2, W_SLOW)
        self.play(FadeIn(m2), run_time=0.5)

        # 오른쪽: 실제 값 (sin, cos 쌍)
        def row(lbl, vals, col):
            s = "  ".join(f"{v:+.2f}" for v in vals)
            return VGroup(T(lbl, 20, col), T(s, 20, WHITE, font="Consolas")).arrange(RIGHT, buff=0.3)

        r0 = row("pos 0 ", [0, 1, 0, 1], AC)
        r44 = row("pos 44", [np.sin(44), np.cos(44), np.sin(4.4), np.cos(4.4)], RED_C)
        VGroup(r0, r44).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([3.75, 1.05, 0])
        r44[1].align_to(r0[1], LEFT)
        nums = r0[1]
        hdr = VGroup(T("빠른 (sin, cos)", 16, QC).move_to([nums.get_left()[0] + nums.width * 0.25, 0, 0]),
                     T("느린 (sin, cos)", 16, KC).move_to([nums.get_left()[0] + nums.width * 0.75, 0, 0])
                     ).set_y(r0.get_top()[1] + 0.25)
        tbl = VGroup(hdr, r0, r44)
        self.play(FadeIn(tbl[0]), FadeIn(r0), run_time=0.5)
        self.play(FadeIn(r44), run_time=0.5)
        hi = SurroundingRectangle(r44[1], color=KC, buff=0.06)
        ok = T("느린 파동이 둘을 확실히 갈라놓음", 18, KC).next_to(tbl, DOWN, 0.15)
        self.play(Create(hi), FadeIn(ok), run_time=0.6)

        # 이진수 비유
        bits = VGroup()
        for p in range(8):
            b = format(p, "03b")
            line = VGroup(T(f"{p}", 18, GREY_A),
                          *[Square(0.3, stroke_width=1, stroke_color=GREY_B,
                                   fill_color=[KC, FFC, QC][k], fill_opacity=0.85 if b[k] == "1" else 0.05)
                            for k in range(3)]).arrange(RIGHT, buff=0.08)
            bits.add(line)
        bits.arrange(DOWN, buff=0.04).move_to([1.3, -1.75, 0])
        bl = T("이진수 비유", 18, GREY_A).next_to(bits, UP, 0.1)
        bt = T("오른쪽 비트: 매 칸 뒤집힘 (고주파)\n왼쪽 비트: 4칸마다 바뀜 (저주파)\n→ 비트 조합이 위치를 유일하게 결정\nsin/cos = 그 연속값 버전", 17, GREY_A,
               align=LEFT).next_to(bits, RIGHT, 0.35)
        self.play(FadeIn(bl), LaggedStart(*[FadeIn(b) for b in bits], lag_ratio=0.08), run_time=1.0)
        self.play(FadeIn(bt), run_time=0.6)

        fin = T("256개 주파수 × (sin, cos) = 512차원: 모든 파동이 동시에 같은 위상으로 돌아올 일은 사실상 없음 → 결정론적 · 고유",
                19, AC).move_to([0, -3.6, 0])
        if fin.width > 13.6:
            fin.scale_to_fit_width(13.6)
        self.play(Write(fin), run_time=1.4)
        pad_to(self, 20)
