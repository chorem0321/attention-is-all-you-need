import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

D = 512


class S08PeRelative(Scene):
    def construct(self):
        # ── 왼쪽: 파장 = 등비수열 2π → 10000·2π (log 스케일) ─────────
        hl = T("상수 10000의 존재 이유", 24, bold=True).move_to([-3.6, 3.35, 0])
        self.play(FadeIn(hl), run_time=0.5)
        idx = [0, 32, 64, 96, 128, 160, 192, 224, 255]
        lam = [2 * np.pi * 10000 ** (2 * i / D) for i in idx]
        logv = np.log10(lam)
        base = np.array([-6.6, -1.6, 0])
        bars = VGroup()
        for k, (i, lv) in enumerate(zip(idx, logv)):
            h = (lv - 0.0) / 5.0 * 3.6
            r = Rectangle(width=0.42, height=h, stroke_width=0, fill_color=interpolate_color(ManimColor(QC), ManimColor(KC), k / 8),
                          fill_opacity=0.9).move_to(base + RIGHT * (k * 0.6 + 0.21) + UP * h / 2)
            bars.add(r)
        bl = Line(base + LEFT * 0.1, base + RIGHT * 5.5, color=GREY_B, stroke_width=1.5)
        xl = VGroup(*[T(str(i), 14, GREY_A).next_to(bars[k], DOWN, 0.08) for k, i in enumerate(idx)])
        xlab = T("차원 쌍 i", 16, GREY_A).next_to(xl, DOWN, 0.08)
        self.play(Create(bl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), FadeIn(xl), FadeIn(xlab),
                  run_time=1.4)
        lo = T("2π ≈ 6.3 토큰", 16, QC).align_to(bars[0], LEFT).set_y(bars[3].get_top()[1] + 0.25)
        hi = T("≈ 10000·2π ≈ 6만 토큰", 16, KC).next_to(bars[-1], UP, 0.08).shift(LEFT * 0.6)
        ll = T("파장 (log 스케일, 등비수열)", 16, GREY_A).move_to([-3.85, 2.75, 0])
        self.play(FadeIn(lo), FadeIn(hi), FadeIn(ll), run_time=0.7)
        why = T("짧은 파장: 바로 옆 토큰 구분\n긴 파장: 아주 긴 문장에서도 한 바퀴 안 돎\n"
                "작으면 → 느린 파동도 금방 반복 / 크면 → 고차원이 거의 상수\n"
                "10000 은 그 사이의 경험적 선택 (논문은 값 비교 실험 없음)", 16, GREY_A, align=LEFT
                ).move_to([-3.65, -2.95, 0])
        self.play(FadeIn(why), run_time=0.8)

        # ── 오른쪽: 상대 위치 = 회전 (선형 변환) ─────────────────
        hr = T("상대 위치: PE(pos+k) = R(k) · PE(pos)", 24, bold=True).move_to([3.6, 3.35, 0])
        self.play(FadeIn(hr), run_time=0.5)
        ctr = np.array([3.0, 0.9, 0])
        R = 1.5
        circ = Circle(R, color=GREY_D, stroke_width=2).move_to(ctr)
        axl = VGroup(Line(ctr + LEFT * 1.8, ctr + RIGHT * 1.8, color=GREY_D, stroke_width=1),
                     Line(ctr + DOWN * 1.8, ctr + UP * 1.8, color=GREY_D, stroke_width=1))
        sx = T("sin", 14, GREY_A).next_to(ctr + RIGHT * 1.8, DOWN, 0.05)
        cy = T("cos", 14, GREY_A).next_to(ctr + UP * 1.8, RIGHT, 0.05)
        self.play(Create(circ), FadeIn(axl), FadeIn(sx), FadeIn(cy), run_time=0.6)
        w, k = 0.35, 3

        def pt(p):  # (x, y) = (sin ωp, cos ωp)
            return ctr + R * np.array([np.sin(w * p), np.cos(w * p), 0])

        for p0, col in ((1, AC), (6, VC)):
            d0 = Dot(pt(p0), color=col, radius=0.09)
            d1 = Dot(pt(p0 + k), color=col, radius=0.09)
            l0 = T(f"pos {p0}", 15, col).next_to(d0, normalize(pt(p0) - ctr), 0.1)
            l1 = T(f"pos {p0 + k}", 15, col).next_to(d1, normalize(pt(p0 + k) - ctr), 0.1)
            arc = Arc(radius=R + 0.22, start_angle=PI / 2 - w * p0, angle=-w * k, arc_center=ctr, color=col,
                      stroke_width=3).add_tip(tip_length=0.14)
            self.play(FadeIn(d0), FadeIn(l0), run_time=0.4)
            self.play(Create(arc), TransformFromCopy(d0, d1), FadeIn(l1), run_time=0.9)
        same = T("어느 pos 에서 출발해도 k칸 이동 = 같은 각도 ωk 회전", 18, AC).move_to([3.6, -1.15, 0])
        self.play(FadeIn(same), run_time=0.6)
        mat_ = M("[sin ω(p+k), cos ω(p+k)] = [sin ωp, cos ωp] · [[cos ωk, −sin ωk], [sin ωk, cos ωk]]", size=17
                 ).move_to([3.6, -1.75, 0])
        if mat_.width > 6.4:
            mat_.scale_to_fit_width(6.4)
        self.play(Write(mat_), run_time=1.0)
        rel = T("pos 와 무관한 고정 행렬 → '몇 칸 떨어졌나'를 선형으로 학습하기 쉬움\n"
                "학습형 위치 임베딩도 거의 동일 (Table 3 E: 25.7 vs 25.8)\n"
                "sinusoid 선택 이유: 학습보다 긴 문장으로 외삽 가능성", 16, GREY_A, align=LEFT)
        rel.scale_to_fit_width(min(rel.width, 6.4)).move_to([3.7, -2.95, 0])
        self.play(FadeIn(rel), run_time=0.8)
        pad_to(self, 20)
