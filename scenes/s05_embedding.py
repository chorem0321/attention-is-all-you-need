import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

rng = np.random.default_rng(4)


def vec(values, cell=0.3):
    g = VGroup()
    for i, v in enumerate(values):
        sq = Square(cell, stroke_width=1, stroke_color=GREY_B,
                    fill_color=interpolate_color(ManimColor("#2b4b8a"), ManimColor("#e0707a"), (v + 1) / 2),
                    fill_opacity=0.95)
        sq.move_to(DOWN * i * cell)
        g.add(sq)
    return g


class S05Embedding(Scene):
    def construct(self):
        # 1) 문장 → 토큰
        sent = T("Allen walks dog", 40, bold=True).move_to([-3.2, 3.2, 0])
        self.play(Write(sent), run_time=0.9)
        words = ["Allen", "walks", "dog"]
        toks = VGroup(*[box(w, w=1.7, h=0.6, fill="#2a2a2a", size=24) for w in words]).arrange(RIGHT, buff=0.35)
        toks.move_to([-3.2, 2.0, 0])
        tk = T("Tokenize ↓", 20, GREY_A).next_to(sent, RIGHT, 0.4)
        self.play(TransformMatchingShapes(sent.copy(), toks), FadeIn(tk), run_time=1.0)
        bpe = T("실제 논문: BPE 서브워드, 어휘 ≈ 37,000 (EN–DE)", 18, GREY_A).next_to(toks, DOWN, 0.15)
        self.play(FadeIn(bpe), run_time=0.5)

        # 2) 임베딩 테이블 lookup
        table = Rectangle(width=2.6, height=3.4, stroke_color=EC, fill_color=EC, fill_opacity=0.12).move_to([4.3, 0.6, 0])
        rows = VGroup(*[Line(table.get_left() + UP * y, table.get_right() + UP * y, stroke_width=0.6, color=EC,
                             stroke_opacity=0.4) for y in np.linspace(-1.6, 1.6, 17)])
        tl = M("E  (vocab × d<sub>model</sub>)", size=22, color=EC).next_to(table, UP, 0.15)
        self.play(FadeIn(table), Create(rows), FadeIn(tl), run_time=0.8)
        ys = [1.2, -0.2, -1.0]
        hl = VGroup(*[Rectangle(width=2.6, height=0.2, stroke_width=0, fill_color=AC, fill_opacity=0.8)
                      .move_to([4.3, 0.6 + y, 0]) for y in ys])
        links = VGroup(*[CurvedArrow(t.get_bottom() + DOWN * 0.45, h.get_left(), angle=PI / 6, color=GREY_B,
                                     stroke_width=1.8, tip_length=0.12) for t, h in zip(toks, hl)])
        self.play(LaggedStart(*[Create(l) for l in links], lag_ratio=0.2), LaggedStart(*[FadeIn(h) for h in hl], lag_ratio=0.2),
                  run_time=1.0)

        vecs = VGroup(*[vec(rng.uniform(-1, 1, 8)) for _ in words])
        for v, t in zip(vecs, toks):
            v.next_to(t, DOWN, 0.75)
        self.play(FadeOut(links), FadeOut(bpe),
                  *[TransformFromCopy(h, v) for h, v in zip(hl, vecs)], run_time=1.3)
        dim = M("각 토큰 → d<sub>model</sub> = 512 차원 벡터 (그림은 8칸만)", size=22, color=GREY_A
                ).next_to(vecs, DOWN, 0.25)
        self.play(FadeIn(dim))
        sc = M("임베딩 × √d<sub>model</sub> ( = √512 ≈ 22.6 )", size=24, color=EC).move_to([4.3, -1.75, 0])
        sh = T("입력·출력 임베딩 = pre-softmax Linear\n같은 가중치 행렬 공유", 18, GREY_A).next_to(sc, DOWN, 0.18)
        self.play(FadeIn(sc, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(sh), run_time=0.6)
        self.wait(0.6)

        # 3) 임베딩만으로는 부족
        lim = M(f"임베딩엔 {c('순서', AC)}, {c('문맥', QC)} 정보 없음  →  "
                f"{c('② Positional Encoding', AC)} · {c('③ Attention', QC)}", size=26).move_to([0, -3.35, 0])
        self.play(Write(lim), run_time=1.4)
        self.play(Indicate(lim, color=AC, scale_factor=1.03))
        pad_to(self, 15)
