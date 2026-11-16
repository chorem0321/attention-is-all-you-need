import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

rng = np.random.default_rng(4)


def vec(values, cell=0.32):
    g = VGroup()
    for i, v in enumerate(values):
        sq = Square(cell, stroke_width=1, stroke_color=GREY_B,
                    fill_color=interpolate_color(ManimColor("#2b4b8a"), ManimColor("#e0707a"), (v + 1) / 2),
                    fill_opacity=0.95)
        sq.move_to(DOWN * i * cell)
        g.add(sq)
    return g


class S04Embedding(Scene):
    def construct(self):
        words = ["I", "love", "machine", "learning"]
        toks = VGroup(*[box(w, w=1.9, h=0.6, fill="#2a2a2a", size=26) for w in words])
        toks.arrange(RIGHT, buff=0.6).move_to(UP * 2.6 + LEFT * 2.2)
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in toks], lag_ratio=0.15), run_time=1.2)

        vecs = VGroup(*[vec(rng.uniform(-1, 1, 6)) for _ in words])
        for v, t in zip(vecs, toks):
            v.next_to(t, DOWN, 0.9)
        arrows = VGroup(*[Arrow(t.get_bottom(), v.get_top(), buff=0.08, stroke_width=2,
                                tip_length=0.12, color=GREY_B) for t, v in zip(toks, vecs)])
        lab = T("Embedding lookup", 24, EC).next_to(arrows, RIGHT, 0.4)
        dim = M(f"d<sub>model</sub> = 512", r"d_{\text{model}} = 512", size=28,
                color=GREY_A).next_to(lab, DOWN, 0.15)
        self.play(*[Create(a) for a in arrows], FadeIn(lab), run_time=0.8)
        self.play(*[TransformFromCopy(t[0], v) for t, v in zip(toks, vecs)], run_time=1.4)
        self.play(FadeIn(dim))
        self.wait(1)

        # 같은 단어, 다른 문맥
        self.play(FadeOut(VGroup(toks, vecs, arrows, lab, dim)), run_time=0.6)
        s1 = T("I sat on the river  bank .", 30).move_to(UP * 2.4 + LEFT * 3)
        s2 = T("I opened a  bank  account .", 30).move_to(UP * 2.4 + RIGHT * 3)
        self.play(FadeIn(s1), FadeIn(s2))
        # Text 의 submobject 는 공백을 제외한 글자 순서
        k1 = s1.text.replace(" ", "").find("bank")
        k2 = s2.text.replace(" ", "").find("bank")
        bank1, bank2 = s1[k1:k1 + 4], s2[k2:k2 + 4]
        self.play(bank1.animate.set_color(AC), bank2.animate.set_color(AC))
        same = rng.uniform(-1, 1, 6)
        v1, v2 = vec(same).next_to(bank1, DOWN, 0.8), vec(same).next_to(bank2, DOWN, 0.8)
        self.play(TransformFromCopy(bank1, v1), TransformFromCopy(bank2, v2), run_time=1.2)
        eq = T("=", 60).move_to((v1.get_center() + v2.get_center()) / 2)
        self.play(Write(eq))
        q = T("강가(river)  vs  은행(account)  —  같은 벡터?", 28, GREY_A).move_to(DOWN * 1.6)
        self.play(FadeIn(q, shift=UP * 0.2))
        ans = T("문맥을 반영하려면 다른 토큰을 '참고'해야 한다  →  Attention", 30, AC).move_to(DOWN * 2.6)
        self.play(Write(ans), run_time=1.5)
        self.play(Indicate(ans, color=AC))
        pad_to(self, 15)
