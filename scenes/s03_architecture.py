import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

BW, BH, GAP = 3.0, 0.42, 0.14


def stack(labels_fills, x, y_bottom):
    """아래에서 위로 박스를 쌓고 연결 화살표를 만든다."""
    boxes = VGroup()
    y = y_bottom
    for lab, fill in labels_fills:
        b = box(lab, w=BW, h=BH, fill=fill, size=18)
        b.move_to([x, y + BH / 2, 0])
        boxes.add(b)
        y += BH + GAP
    arrows = VGroup(*[Arrow(boxes[i].get_top(), boxes[i + 1].get_bottom(), buff=0,
                            stroke_width=2, tip_length=0.1, max_tip_length_to_length_ratio=0.5,
                            color=GREY_B)
                      for i in range(len(boxes) - 1)])
    return boxes, arrows


def pe_node(pt):
    circ = Circle(0.17, color=WHITE, stroke_width=2).move_to(pt)
    plus = VGroup(Line(UP * 0.1, DOWN * 0.1), Line(LEFT * 0.1, RIGHT * 0.1)).move_to(pt)
    wave = FunctionGraph(lambda t: 0.12 * np.sin(6 * t), x_range=[-0.5, 0.5],
                         color=AC, stroke_width=2).next_to(circ, LEFT, 0.25)
    lab = T("Positional\nEncoding", 14, GREY_A).next_to(wave, LEFT, 0.12)
    return VGroup(circ, plus, wave, lab)


class S03Architecture(Scene):
    def construct(self):
        ex, dx = -3.2, 3.2
        y0 = -3.55

        # ── Encoder ─────────────────────────────────
        inp = T("Inputs", 18, GREY_A).move_to([ex, y0 + 0.1, 0])
        emb = box("Input Embedding", w=BW, h=BH, fill=EC, size=18).move_to([ex, y0 + 0.7, 0])
        pe = pe_node([ex, y0 + 1.35, 0])
        enc_boxes, enc_arrows = stack([("Multi-Head Attention", AC),
                                       ("Add & Norm", NC),
                                       ("Feed Forward", FFC),
                                       ("Add & Norm", NC)], ex, y0 + 1.85)
        enc_frame = SurroundingRectangle(enc_boxes, buff=0.16, corner_radius=0.12,
                                         color=GREY_B, stroke_width=2)
        nx = T("N = 6 ×", 22, bold=True).next_to(enc_frame, LEFT, 0.2)
        a1 = Arrow(inp.get_top(), emb.get_bottom(), buff=0.05, stroke_width=2, tip_length=0.1, color=GREY_B)
        a2 = Line(emb.get_top(), pe[0].get_bottom(), stroke_width=2, color=GREY_B)
        a3 = Arrow(pe[0].get_top(), enc_boxes[0].get_bottom(), buff=0, stroke_width=2, tip_length=0.1, color=GREY_B)
        enc_title = T("Encoder", 26, bold=True).next_to(enc_frame, UP, 0.2).align_to(enc_frame, LEFT)

        self.play(FadeIn(inp), Create(a1), FadeIn(emb, shift=UP * 0.2), run_time=0.8)
        self.play(Create(a2), FadeIn(pe), run_time=0.8)
        self.play(Create(a3), run_time=0.3)
        for b, a in zip(enc_boxes, [None] + list(enc_arrows)):
            anims = [FadeIn(b, shift=UP * 0.2)]
            if a is not None:
                anims.append(Create(a))
            self.play(*anims, run_time=0.45)
        self.play(Create(enc_frame), Write(nx), FadeIn(enc_title), run_time=0.8)

        # ── Decoder ─────────────────────────────────
        outp = T("Outputs (shifted right)", 18, GREY_A).move_to([dx, y0 + 0.1, 0])
        demb = box("Output Embedding", w=BW, h=BH, fill=EC, size=18).move_to([dx, y0 + 0.7, 0])
        dpe = pe_node([dx, y0 + 1.35, 0])
        dec_boxes, dec_arrows = stack([("Masked Multi-Head Attention", AC),
                                       ("Add & Norm", NC),
                                       ("Multi-Head Attention", AC),
                                       ("Add & Norm", NC),
                                       ("Feed Forward", FFC),
                                       ("Add & Norm", NC)], dx, y0 + 1.85)
        dec_frame = SurroundingRectangle(dec_boxes, buff=0.16, corner_radius=0.12,
                                         color=GREY_B, stroke_width=2)
        nx2 = T("× N = 6", 22, bold=True).next_to(dec_frame, RIGHT, 0.2)
        lin = box("Linear", w=1.5, h=0.36, fill="#3b5068", size=16).next_to(dec_frame, UP, 0.18)
        sm = box("Softmax", w=1.5, h=0.36, fill="#3b6850", size=16).next_to(lin, UP, 0.1)
        prob = T("Output Probabilities", 16, GREY_A).next_to(sm, UP, 0.08)
        b1 = Arrow(outp.get_top(), demb.get_bottom(), buff=0.05, stroke_width=2, tip_length=0.1, color=GREY_B)
        b2 = Line(demb.get_top(), dpe[0].get_bottom(), stroke_width=2, color=GREY_B)
        b3 = Arrow(dpe[0].get_top(), dec_boxes[0].get_bottom(), buff=0, stroke_width=2, tip_length=0.1, color=GREY_B)
        dec_title = T("Decoder", 26, bold=True).next_to(nx2, UP, 0.3).shift(LEFT * 0.1)

        self.play(FadeIn(outp), Create(b1), FadeIn(demb, shift=UP * 0.2), run_time=0.8)
        self.play(Create(b2), FadeIn(dpe), Create(b3), run_time=0.8)
        for b, a in zip(dec_boxes, [None] + list(dec_arrows)):
            anims = [FadeIn(b, shift=UP * 0.2)]
            if a is not None:
                anims.append(Create(a))
            self.play(*anims, run_time=0.35)
        self.play(Create(dec_frame), Write(nx2), FadeIn(dec_title), run_time=0.8)
        self.play(FadeIn(lin, shift=UP * 0.1), FadeIn(sm, shift=UP * 0.1), FadeIn(prob), run_time=0.8)

        # ── Encoder 출력 → Decoder cross-attention (K, V) ─────
        start = enc_frame.get_corner(UR) + LEFT * 0.35
        mid = np.array([0, enc_frame.get_top()[1] + 0.25, 0])
        end = dec_boxes[2].get_left()
        cross = VMobject(stroke_color=KC, stroke_width=3)
        cross.set_points_as_corners([start, [start[0], mid[1], 0], [0, mid[1], 0],
                                     [0, end[1], 0], end])
        tip = Arrow(end + LEFT * 0.4, end, buff=0, color=KC, stroke_width=3, tip_length=0.15)
        kv = MarkupText(c("K", KC) + ", " + c("V", VC), font=MFONT, font_size=24).next_to([0, mid[1], 0], UP, 0.1)
        self.play(Create(cross), Create(tip), FadeIn(kv), run_time=1.2)
        self.play(Indicate(dec_boxes[2], color=AC), Indicate(enc_boxes[0], color=AC), run_time=1)
        pad_to(self, 18)
