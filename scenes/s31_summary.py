import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

KEYS = ["learned E × √d_model", "sin/cos 다중 주파수", "softmax(QKᵀ/√d_k)V × 8 heads",
        "LN(x + Attn(x))", "max(0, xW₁+b₁)W₂+b₂", "LN(z + FFN(z))", "같은 구조 6층", "→ 다음 토큰 확률"]


class S31Summary(Scene):
    def construct(self):
        title = T("Allen walks dog  →  8단계 정리", 32, bold=True).move_to([0, 3.25, 0])
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.6)
        boxes = VGroup(*[pipe_box(i, KEYS[i]) for i in range(8)])
        arrows = pipe_arrows(boxes)
        self.play(FadeIn(boxes[0], shift=RIGHT * 0.2), run_time=0.5)
        for i in range(1, 8):
            self.play(GrowArrow(arrows[i - 1]), FadeIn(boxes[i]), run_time=0.45)
        self.wait(0.4)
        self.play(LaggedStart(*[Indicate(b, scale_factor=1.05, color=PIPE[k][2]) for k, b in enumerate(boxes)],
                              lag_ratio=0.12), run_time=2.2)
        core = T("펼치고(W₁) → 거르고(ReLU) → 압축(W₂),  섞고(Attention) → 보존(Residual) → 안정(LayerNorm)", 20, GREY_A
                 ).move_to([0, -2.55, 0])
        if core.width > 13.6:
            core.scale_to_fit_width(13.6)
        self.play(FadeIn(core), run_time=0.8)
        final = T("Transformer 1팀", 34, AC, bold=True).move_to([0, -3.4, 0])
        self.play(Write(final), run_time=1.2)
        self.play(Circumscribe(final, color=AC), run_time=1.2)
        pad_to(self, 15)
