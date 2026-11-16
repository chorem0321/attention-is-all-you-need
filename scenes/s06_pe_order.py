import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

rng = np.random.default_rng(11)
COL = {"Allen": EC, "walks": QC, "dog": VC}


def tokvec(word, cell=0.28, n=6):
    vals = {"Allen": [0.8, -0.3, 0.5, -0.9, 0.2, 0.6], "walks": [-0.5, 0.9, -0.1, 0.4, -0.8, 0.1],
            "dog": [0.3, 0.2, -0.7, 0.9, 0.5, -0.4]}[word]
    g = VGroup()
    for i, v in enumerate(vals[:n]):
        sq = Square(cell, stroke_width=1, stroke_color=COL[word],
                    fill_color=interpolate_color(ManimColor("#2b4b8a"), ManimColor("#e0707a"), (v + 1) / 2),
                    fill_opacity=0.95).move_to(DOWN * i * cell)
        g.add(sq)
    lab = T(word, 20, COL[word]).next_to(g, UP, 0.12)
    return VGroup(g, lab)


class S06PeOrder(Scene):
    def construct(self):
        s1 = ["Allen", "walks", "dog"]
        s2 = ["dog", "walks", "Allen"]
        t1 = T("Allen walks dog", 30, bold=True).move_to([-3.6, 3.3, 0])
        t2 = T("dog walks Allen", 30, bold=True).move_to([3.6, 3.3, 0])
        m1 = T("앨런이 개를 산책시킨다", 18, GREY_A).next_to(t1, DOWN, 0.1)
        m2 = T("개가 앨런을 산책시킨다 (?)", 18, GREY_A).next_to(t2, DOWN, 0.1)
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.7)
        self.play(FadeIn(m1), FadeIn(m2), run_time=0.6)

        v1 = VGroup(*[tokvec(w) for w in s1]).arrange(RIGHT, buff=0.55).move_to([-3.6, 1.0, 0])
        v2 = VGroup(*[tokvec(w) for w in s2]).arrange(RIGHT, buff=0.55).move_to([3.6, 1.0, 0])
        self.play(LaggedStart(*[FadeIn(v, shift=DOWN * 0.2) for v in [*v1, *v2]], lag_ratio=0.1), run_time=1.2)
        # 같은 단어 = 같은 벡터
        links = VGroup()
        for i, w in enumerate(s1):
            j = s2.index(w)
            links.add(ArcBetweenPoints(v1[i][0].get_bottom() + DOWN * 0.08, v2[j][0].get_bottom() + DOWN * 0.08,
                                       angle=PI / 4, color=COL[w], stroke_width=2.2))
        self.play(LaggedStart(*[Create(l) for l in links], lag_ratio=0.25), run_time=1.3)
        same = T("두 문장의 벡터 = 같은 집합 { Allen, walks, dog }", 24, GREY_A).move_to([0, -1.7, 0])
        self.play(FadeIn(same, shift=UP * 0.15), run_time=0.6)

        eq = M("Attention(P·X) = P·Attention(X)   (P: 순서 바꾸기)", size=26, color=WHITE).move_to([0, -2.4, 0])
        why = T("순서를 섞으면 출력도 똑같이 섞일 뿐  →  Allen 의 표현은 두 문장에서 동일", 22, AC).move_to([0, -3.0, 0])
        self.play(Write(eq), run_time=1.2)
        self.play(FadeIn(why), run_time=0.6)
        self.wait(1.0)

        # 해결: 위치 벡터를 더한다
        self.play(FadeOut(VGroup(links, same, eq, why, m1, m2)), run_time=0.5)
        fix = M(f"x<sub>pos</sub> = {c('Embedding(token)', EC)} + {c('PE(pos)', AC)}", size=32).move_to([0, -1.9, 0])
        pes = VGroup()
        for grp in (v1, v2):
            for k, tv in enumerate(grp):
                pe = VGroup(*[Square(0.28, stroke_width=1, stroke_color=AC, fill_color=AC,
                                     fill_opacity=0.25 + 0.6 * abs(np.sin((k + 1) / (1 + 2 * d))))
                              .move_to(DOWN * d * 0.28) for d in range(6)])
                pe.next_to(tv[0], RIGHT, 0.06)
                pes.add(pe)
        self.play(Write(fix), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(p, shift=LEFT * 0.15) for p in pes], lag_ratio=0.06), run_time=1.0)
        res = T("같은 dog 라도 0번째 / 2번째 자리면 다른 입력 벡터  →  순서가 구분된다", 22, AC).move_to([0, -2.8, 0])
        self.play(FadeIn(res, shift=UP * 0.15))
        note = T("더하기(+): PE 차원 = d_model 이라 바로 합산 가능 (concat 하면 차원 증가)", 18, GREY_A).move_to([0, -3.4, 0])
        self.play(FadeIn(note))
        pad_to(self, 17)
