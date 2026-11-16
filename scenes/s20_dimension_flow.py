import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

# 512 → 2.4 단위, 64 → 0.3, 4 토큰 → 높이 1.2 (4×4 는 보기 위해 정사각형)
U = 2.4 / 512
RH = 1.2


def blk(cols, color, label, dims, op=0.35, w=None):
    return mat(w if w else cols * U, RH, color, label, dims, size=22, op=op)


class S20DimensionFlow(Scene):
    def construct(self):
        y1, y2 = 1.6, -1.4
        X = blk(512, XC, "X", "4 × 512").move_to([-5.4, y1, 0])
        self.play(FadeIn(X, shift=RIGHT * 0.3))

        # 한 head 의 Q, K, V
        q = blk(64, QC, "Q", "4 × 64").move_to([-3.0, y1 + 0.0, 0])
        k = blk(64, KC, "K", "4 × 64").next_to(q, RIGHT, 0.35)
        v = blk(64, VC, "V", "4 × 64").next_to(k, RIGHT, 0.35)
        a1 = Arrow(X.get_right(), q.get_left(), buff=0.1, stroke_width=2.5, color=GREY_B, tip_length=0.15)
        hl = T("head i (×W_i)", 18, GREY_A).next_to(VGroup(q, k, v), UP, 0.25)
        self.play(Create(a1), TransformFromCopy(X[0], q[0]), TransformFromCopy(X[0], k[0]),
                  TransformFromCopy(X[0], v[0]), FadeIn(VGroup(q[1], k[1], v[1], q[2], k[2], v[2])), FadeIn(hl),
                  run_time=1.4)

        # QKᵀ: 4×4
        s = mat(RH, RH, AC, "QK<sup>T</sup>", "4 × 4", size=20, op=0.45).move_to([1.6, y1, 0])
        a2 = Arrow(v.get_right(), s.get_left(), buff=0.12, stroke_width=2.5, color=GREY_B, tip_length=0.15)
        self.play(Create(a2), TransformFromCopy(VGroup(q[0], k[0]), s[0]), FadeIn(s[1]), FadeIn(s[2]), run_time=1.0)
        # head 출력 4×64
        ho = blk(64, AC, "head", "4 × 64", op=0.5).move_to([3.6, y1, 0])
        ho[1].scale(0.8)
        a3 = Arrow(s.get_right(), ho.get_left(), buff=0.12, stroke_width=2.5, color=GREY_B, tip_length=0.15)
        sv = T("softmax · V", 16, GREY_A).next_to(a3, UP, 0.08)
        self.play(Create(a3), FadeIn(sv), TransformFromCopy(VGroup(s[0], v[0]), ho[0]), FadeIn(ho[1]), FadeIn(ho[2]),
                  run_time=1.0)
        self.wait(0.4)

        # 8 개 head concat → 4×512
        heads = VGroup(*[Rectangle(width=64 * U, height=RH, stroke_color=WHITE, stroke_width=1,
                                   fill_color=AC, fill_opacity=0.25 + 0.06 * i) for i in range(8)]).arrange(RIGHT, buff=0)
        heads.move_to([-3.6, y2, 0])
        hlab = T("Concat(head1..8)\n4 × (8·64) = 4 × 512", 18, GREY_A).next_to(heads, DOWN, 0.15)
        # 두 줄 사이 빈 통로(y = -0.15)로만 지나가는 꺾은 화살표 → 도형을 가리지 않음
        ych = -0.15
        p0 = np.array([ho.get_x(), ho[2].get_bottom()[1] - 0.12, 0])
        p1 = np.array([ho.get_x(), ych, 0])
        p2 = np.array([heads.get_x(), ych, 0])
        p3 = heads.get_top() + UP * 0.08
        path = VMobject(stroke_color=GREY_B, stroke_width=2.5).set_points_as_corners([p0, p1, p2])
        tip = Arrow(p2, p3, buff=0, stroke_width=2.5, color=GREY_B, tip_length=0.15,
                    max_tip_length_to_length_ratio=0.5)
        h8 = T("× 8 heads (병렬)", 18, AC).next_to((p1 + p2) / 2, UP, 0.1)
        a4 = VGroup(path, tip)
        self.play(Create(path), FadeIn(h8), run_time=0.6)
        self.play(GrowArrow(tip), run_time=0.3)
        self.play(LaggedStart(*[TransformFromCopy(ho[0], h) for h in heads], lag_ratio=0.12), FadeIn(hlab),
                  run_time=1.6)

        # × W^O (512×512) → 4×512
        times = T("×", 30, GREY_B).next_to(heads, RIGHT, 0.25)
        wo = mat(512 * U * 0.5, 512 * U * 0.5, FFC, "W<sup>O</sup>", "512 × 512", size=22, op=0.3).next_to(times, RIGHT, 0.25)
        eq = T("=", 30, GREY_B).next_to(wo, RIGHT, 0.25)
        out = blk(512, AC, "Output", "4 × 512", op=0.45).next_to(eq, RIGHT, 0.25)
        self.play(FadeIn(times), FadeIn(wo), run_time=0.7)
        self.play(FadeIn(eq), TransformFromCopy(heads, out[0]), FadeIn(out[1]), FadeIn(out[2]), run_time=1.2)

        msg = M("d<sub>k</sub> = d<sub>v</sub> = d<sub>model</sub> / h = 512 / 8 = 64  →  "
                "총 연산량 ≈ single-head (full dim)", size=26, color=AC).to_edge(DOWN, buff=0.35)
        self.play(Write(msg), run_time=1.5)
        self.play(Indicate(VGroup(X, out), color=AC), run_time=1)
        pad_to(self, 17)
