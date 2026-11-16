import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

NH = 10
ON_WALKS = [1, 0, 1, 1, 0, 0, 1, 0, 1, 0]
ON_DOG = [0, 1, 0, 1, 1, 0, 0, 1, 0, 1]


class S25FfnNonlinear(Scene):
    def construct(self):
        # ── ① ReLU 가 없다면 ─────────────────────
        h1 = T("① 활성화 함수가 없다면", 24, bold=True).move_to([-3.6, 3.35, 0])
        e1 = M("W<sub>2</sub>(W<sub>1</sub>x) = (W<sub>2</sub>W<sub>1</sub>) x = W x", size=30).next_to(h1, DOWN, 0.35)
        n1 = T("2048로 넓혀도 결국 512×512 선형변환 하나\n→ 직선(평면)만 표현, 넓힌 의미가 없음", 18, RED_C).next_to(e1, DOWN, 0.25)
        self.play(FadeIn(h1), run_time=0.4)
        self.play(Write(e1), run_time=1.0)
        self.play(FadeIn(n1), run_time=0.6)

        # ── ② 입력마다 다른 노드 조합 ──────────────
        h2 = T("② ReLU: 입력이 '스위치'를 정한다", 24, bold=True).move_to([3.6, 3.35, 0])
        self.play(FadeIn(h2), run_time=0.4)

        def layer(on, y, word, col):
            nodes = VGroup(*[Circle(0.17, stroke_width=2, stroke_color=AC if o else GREY_D,
                                    fill_color=AC if o else BLACK, fill_opacity=0.9 if o else 1) for o in on]
                           ).arrange(RIGHT, buff=0.1).move_to([4.1, y, 0])
            lab = T(f"\"{word}\"", 20, col).next_to(nodes, LEFT, 0.25)
            return VGroup(lab, nodes)

        lw = layer(ON_WALKS, 2.35, "walks", QC)
        ld = layer(ON_DOG, 1.65, "dog", VC)
        self.play(FadeIn(lw), run_time=0.6)
        self.play(FadeIn(ld), run_time=0.6)
        e2 = M("FFN(x) = W<sub>2</sub> · D(x) · (W<sub>1</sub>x + b<sub>1</sub>),   D(x) = diag( 1[W<sub>1</sub>x + b<sub>1</sub> > 0] )",
               size=19).move_to([3.6, 0.95, 0])
        if e2.width > 6.9:
            e2.scale_to_fit_width(6.9)
        n2 = T("켜지는 노드 조합 D(x) 가 입력마다 달라짐\n→ 입력 영역마다 다른 선형함수 = 조각별 선형 → 비선형", 18, AC).next_to(e2, DOWN, 0.2)
        self.play(Write(e2), run_time=1.0)
        self.play(FadeIn(n2), run_time=0.6)

        # ── ③ ReLU 조합으로 곡선 만들기 ───────────
        ax = Axes(x_range=[-3, 3, 1], y_range=[-1.5, 1.5, 1], x_length=6.0, y_length=2.6, tips=False,
                  axis_config={"stroke_width": 1.5, "color": GREY_D}).move_to([-3.4, -1.75, 0])
        h3 = T("③ 꺾인 직선(ReLU)을 여러 개 더하면 → 곡선", 20, bold=True).next_to(ax, UP, 0.2)
        target = ax.plot(lambda x: np.sin(1.2 * x), x_range=[-3, 3, 0.02], color=GREY_B, stroke_width=2)
        target = DashedVMobject(target, num_dashes=60)
        knots = np.linspace(-3, 3, 9)
        ys = np.sin(1.2 * knots)
        slopes = np.diff(ys) / np.diff(knots)

        def pw(x, upto):
            v = ys[0] + slopes[0] * (x - knots[0])
            for j in range(1, upto):
                v += (slopes[j] - slopes[j - 1]) * max(0.0, x - knots[j])
            return v

        self.play(FadeIn(h3), Create(ax), Create(target), run_time=0.9)
        cur = ax.plot(lambda x: pw(x, 1), x_range=[-3, 3, 0.02], color=AC, stroke_width=3)
        cnt = T("ReLU 1개", 18, AC).next_to(ax, RIGHT, 0.2).shift(UP * 0.6)
        self.play(Create(cur), FadeIn(cnt), run_time=0.6)
        for n in (2, 4, 8):
            nxt = ax.plot(lambda x, n=n: pw(x, n), x_range=[-3, 3, 0.02], color=AC, stroke_width=3)
            nc = T(f"ReLU {n}개", 18, AC).move_to(cnt)
            self.play(Transform(cur, nxt), Transform(cnt, nc), run_time=0.7)
        n3 = T("2048개 노드 = 2048개의 '꺾임'\n→ 복잡한 비선형 패턴을 정교하게 근사", 18, GREY_A, align=LEFT).next_to(cnt, DOWN, 0.3).align_to(cnt, LEFT)
        self.play(FadeIn(n3), run_time=0.6)
        gelu = T("논문은 ReLU · BERT/GPT 는 매끄러운 버전 GELU", 17, GREY_A).move_to([3.7, -3.55, 0])
        self.play(FadeIn(gelu), run_time=0.5)
        pad_to(self, 19)
