import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

COLS = ["animal", "street", "tired"]
H1 = np.array([[0.80, 0.10, 0.10]])
H2 = np.array([[0.10, 0.10, 0.80]])


class S18MultiHeadIntuition(Scene):
    def construct(self):
        q = T("Query:  it", 30, QC, bold=True).move_to(UP * 3.1)
        self.play(FadeIn(q))

        def panel(vals, name, desc, x):
            hm = heatmap(vals, rows=["it"], cols=COLS, cell=1.15, color=AC, size=26, lab_size=22)
            hm.move_to([x, 0.6, 0])
            t = T(name, 30, bold=True).next_to(hm, UP, 0.7)
            d = T(desc, 22, GREY_A).next_to(hm, DOWN, 0.4)
            return hm, t, d

        h1, t1, d1 = panel(H1, "Head 1", "지시 대상 (it → animal)", -3.4)
        h2, t2, d2 = panel(H2, "Head 2", "상태/속성 (it → tired)", 3.4)
        for hm, t, d, vals in [(h1, t1, d1, H1), (h2, t2, d2, H2)]:
            self.play(FadeIn(t), FadeIn(hm[2]), FadeIn(hm[3]), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(cl) for cl in hm[0]], lag_ratio=0.2), FadeIn(hm[1]), run_time=1.0)
            k = int(np.argmax(vals[0]))
            self.play(Indicate(hm[0][k], color=AC, scale_factor=1.15), FadeIn(d), run_time=0.9)
        self.wait(0.4)
        msg = T("head 마다 독립적인 softmax  →  서로 다른 관계를 동시에 포착", 26).to_edge(DOWN, buff=0.9)
        note = T("(값은 설명용 예시)", 18, GREY_B).next_to(msg, DOWN, 0.2)
        self.play(FadeIn(msg, shift=UP * 0.2), FadeIn(note))
        self.play(Circumscribe(VGroup(h1, h2), color=AC), run_time=1.4)
        pad_to(self, 11)
