"""圓方程：由圓心半徑式推到一般式。

無 LaTeX，公式用 Text。字體與 mathviz.ZH 一致（WenQuanYi Micro Hei）。
渲染：
  python3 .cursor/skills/math-explainer/scripts/check_text.py skills-trial/demos/circle-equation/scene.py
  bash .cursor/skills/math-explainer/scripts/render.sh skills-trial/demos/circle-equation/scene.py CircleEquation s
  bash .cursor/skills/math-explainer/scripts/render.sh skills-trial/demos/circle-equation/scene.py CircleEquation m
"""
import math

from manim import *
from mathviz import (
    SafeScene, fit_content, ZH,
    C_MAIN, C_ACCENT, C_OK, C_SUB, C_WARM, C_GREY,
)

# check_text.py 只掃描本檔的字串常數與 ZH 賦值。
ZH = "WenQuanYi Micro Hei"

H, K, R = 2, 1, 3
THETA = 50  # degrees, shared with the webpage default


def T(text, scale=0.5, color=WHITE):
    return Text(text, font=ZH).scale(scale).set_color(color)


def stack(rows, scale=0.48, buff=0.2):
    """rows: list of (text, color)."""
    items = [T(text, scale, color) for text, color in rows]
    return VGroup(*items).arrange(DOWN, buff=buff, aligned_edge=LEFT)


def place(mobj, dy=0.15):
    fit_content(mobj)
    mobj.shift(UP * dy)
    return mobj


class CircleEquation(SafeScene):
    def clear_screen(self, *keep):
        # title_bar adds the title Text on its own, not as the VGroup stored in
        # self._title, so the base clear_screen would fade the title away.
        if self._title is not None:
            keep = keep + tuple(self._title.get_family())
        super().clear_screen(*keep)

    def construct(self):
        self.add_backdrop()
        self.title_bar("圓方程：由圓心半徑式到一般式")
        self.intro_question()
        self.derive_distance()
        self.derive_expand_x()
        self.derive_expand_y()
        self.derive_collect()
        self.derive_coefficients()
        self.derive_reverse()
        self.conclude()

    def _axes_group(self, with_triangle=False):
        axes = Axes(
            x_range=[-1, 6, 1],
            y_range=[-2, 5, 1],
            x_length=5.2,
            y_length=4.0,
            tips=False,
            axis_config={"stroke_color": "#5a6678", "stroke_width": 2},
        )
        xlab = T("x", 0.36, C_GREY).next_to(axes.x_axis.get_end(), DR, buff=0.06)
        ylab = T("y", 0.36, C_GREY).next_to(axes.y_axis.get_end(), UL, buff=0.06)
        unit = axes.x_length / (axes.x_range[1] - axes.x_range[0])
        circ = Circle(radius=R * unit).set_stroke(C_MAIN, 4).set_fill(C_MAIN, 0.08)
        circ.move_to(axes.c2p(H, K))
        centre = Dot(axes.c2p(H, K), color=C_ACCENT, radius=0.07)
        clab = T("C(2, 1)", 0.32, C_ACCENT).next_to(centre, DL, buff=0.08)
        parts = [axes, xlab, ylab, circ, centre, clab]
        if with_triangle:
            ang = math.radians(THETA)
            px = H + R * math.cos(ang)
            py = K + R * math.sin(ang)
            c_pt, q_pt, p_pt = axes.c2p(H, K), axes.c2p(px, K), axes.c2p(px, py)
            horiz = Line(c_pt, q_pt).set_stroke(C_ACCENT, 4)
            vert = Line(q_pt, p_pt).set_stroke(C_OK, 4)
            hypo = Line(c_pt, p_pt).set_stroke(C_SUB, 4)
            pdot = Dot(p_pt, color=C_SUB, radius=0.06)
            hlab = T("x - 2", 0.3, C_ACCENT).next_to(horiz, DOWN, buff=0.06)
            vlab = T("y - 1", 0.3, C_OK).next_to(vert, RIGHT, buff=0.06)
            rlab = T("r = 3", 0.3, C_SUB).next_to(hypo.get_center(), UL, buff=0.06)
            parts.extend([horiz, vert, hypo, pdot, hlab, vlab, rlab])
        else:
            end = axes.c2p(H + R, K)
            radius = Line(axes.c2p(H, K), end).set_stroke(C_SUB, 4)
            rlab = T("r = 3", 0.32, C_SUB).next_to(radius, UP, buff=0.06)
            parts.extend([radius, rlab])
        return VGroup(*parts)

    def intro_question(self):
        fig = self._axes_group(False)
        words = stack([
            ("圓心 (2, 1)，半徑 3", C_SUB),
            ("圓上每一點到圓心", WHITE),
            ("的距離都是 3。", WHITE),
            ("為何又能寫成", C_ACCENT),
            ("x^2 + y^2 + Dx + Ey + F = 0 ?", C_ACCENT),
        ], scale=0.42, buff=0.16)
        body = place(VGroup(fig, words).arrange(RIGHT, buff=0.4))
        self.play(Create(fig[3]), FadeIn(fig[4]), Write(fig[5]), run_time=1.0)
        self.play(Create(fig[6]), FadeIn(fig[7]), FadeIn(fig[0]), FadeIn(fig[1]), FadeIn(fig[2]), run_time=0.8)
        self.play(FadeIn(words, shift=UP * 0.15), run_time=0.8)
        self.caption("先看具體的圓：距離相等，才有圓心半徑式。", wait=1.8)
        self.clear_screen()

    def derive_distance(self):
        fig = self._axes_group(True)
        words = stack([
            ("水平腿 = x - h = x - 2", C_ACCENT),
            ("垂直腿 = y - k = y - 1", C_OK),
            ("勾股定理：兩腿平方和 = 斜邊平方", WHITE),
            ("(x - 2)^2 + (y - 1)^2 = 3^2", C_SUB),
            ("3^2 = 9，所以右式是 9", C_SUB),
        ], scale=0.4, buff=0.14)
        body = place(VGroup(fig, words).arrange(RIGHT, buff=0.35), dy=0.05)
        self.play(FadeIn(fig), run_time=0.8)
        self.play(FadeIn(words[0]), FadeIn(words[1]), run_time=0.6)
        self.play(FadeIn(words[2]), run_time=0.5)
        self.play(FadeIn(words[3]), run_time=0.5)
        self.play(FadeIn(words[4]), run_time=0.5)
        self.emphasize(words[3])
        self.caption("圓心半徑式是距離公式，不是憑空寫下的。", wait=2.0)
        self.clear_screen()

    def derive_expand_x(self):
        rows = stack([
            ("設 a = x，b = 2", C_GREY),
            ("(a - b)^2 = a^2 - 2ab + b^2", WHITE),
            ("(x - 2)^2 = x^2 - 2*2*x + 2^2", C_MAIN),
            ("2*2 = 4，2^2 = 4", C_WARM),
            ("(x - 2)^2 = x^2 - 4x + 4", C_ACCENT),
        ], scale=0.5, buff=0.22)
        place(rows)
        self.play(FadeIn(rows[0]), FadeIn(rows[1]), run_time=0.7)
        self.play(FadeIn(rows[2]), run_time=0.6)
        self.play(FadeIn(rows[3]), run_time=0.5)
        self.play(FadeIn(rows[4]), run_time=0.6)
        self.emphasize(rows[4])
        self.caption("交叉項 -4x 來自 -2 乘圓心的 x 座標。", wait=2.0)
        self.clear_screen()

    def derive_expand_y(self):
        rows = stack([
            ("同樣，a = y，b = 1", C_GREY),
            ("(y - 1)^2 = y^2 - 2*1*y + 1^2", C_MAIN),
            ("2*1 = 2，1^2 = 1", C_WARM),
            ("(y - 1)^2 = y^2 - 2y + 1", C_ACCENT),
        ], scale=0.52, buff=0.24)
        place(rows)
        for line in rows:
            self.play(FadeIn(line), run_time=0.45)
        self.emphasize(rows[3])
        self.caption("y 的交叉項是 -2k 乘 y，這裡 k = 1。", wait=1.8)
        self.clear_screen()

    def derive_collect(self):
        rows = stack([
            ("代回：(x^2 - 4x + 4) + (y^2 - 2y + 1) = 9", C_SUB),
            ("兩邊同減 9，等號仍然成立", WHITE),
            ("x^2 + y^2 - 4x - 2y + 4 + 1 - 9 = 0", C_MAIN),
            ("常數：4 + 1 - 9 = -4", C_WARM),
            ("x^2 + y^2 - 4x - 2y - 4 = 0", C_ACCENT),
        ], scale=0.44, buff=0.2)
        place(rows, dy=0.1)
        for line in rows:
            self.play(FadeIn(line), run_time=0.45)
        self.emphasize(rows[4])
        self.caption("移項只是兩邊同減 9，圓上的點一個都沒變。", wait=2.1)
        self.clear_screen()

    def derive_coefficients(self):
        left = stack([
            ("這個圓：", C_GREY),
            ("x 的係數 = -4", C_MAIN),
            ("y 的係數 = -2", C_MAIN),
            ("常數項 = -4", C_WARM),
        ], scale=0.46, buff=0.18)
        right = stack([
            ("對照 Dx + Ey + F", C_ACCENT),
            ("D = -2h = -2*2 = -4", C_ACCENT),
            ("E = -2k = -2*1 = -2", C_ACCENT),
            ("F = h^2 + k^2 - r^2", C_ACCENT),
            ("= 4 + 1 - 9 = -4", C_WARM),
        ], scale=0.44, buff=0.16)
        body = place(VGroup(left, right).arrange(RIGHT, buff=0.7))
        self.play(FadeIn(left), run_time=0.6)
        self.play(FadeIn(right), run_time=0.8)
        self.emphasize(right[1])
        self.caption("D 等於 -2 乘 h，所以 D 不是圓心的 x 座標。", wait=2.1)
        self.clear_screen()

    def derive_reverse(self):
        rows = stack([
            ("由 D = -2h 解 h：h = -D / 2", WHITE),
            ("h = -(-4) / 2 = 4 / 2 = 2", C_OK),
            ("k = -E / 2 = -(-2) / 2 = 1", C_OK),
            ("r^2 = (D/2)^2 + (E/2)^2 - F", WHITE),
            ("= (-2)^2 + (-1)^2 - (-4)", C_MAIN),
            ("= 4 + 1 + 4 = 9", C_OK),
        ], scale=0.46, buff=0.16)
        place(rows, dy=0.05)
        for line in rows:
            self.play(FadeIn(line), run_time=0.4)
        self.emphasize(rows[1])
        self.emphasize(rows[5])
        self.caption("負號把 -2h 解回 h；半徑平方是減去 F，不是加上 F。", wait=2.2)
        self.clear_screen()

    def conclude(self):
        rows = stack([
            ("(x - h)^2 + (y - k)^2 = r^2", C_SUB),
            ("展開後常數移到左邊", WHITE),
            ("x^2 + y^2 + Dx + Ey + F = 0", C_ACCENT),
            ("D = -2h    E = -2k", C_ACCENT),
            ("F = h^2 + k^2 - r^2", C_ACCENT),
        ], scale=0.5, buff=0.2)
        box = SurroundingRectangle(rows, color=C_ACCENT, buff=0.28, corner_radius=0.12)
        grp = VGroup(box, rows)
        place(grp)
        self.play(FadeIn(rows[0]), run_time=0.4)
        self.play(FadeIn(rows[1]), run_time=0.4)
        self.play(FadeIn(rows[2]), Create(box), run_time=0.7)
        self.play(FadeIn(rows[3]), FadeIn(rows[4]), run_time=0.6)
        self.emphasize(rows[2])
        self.caption("一般式是圓心半徑式展開後的同一條方程。", wait=2.2)


def _glyph_samples():
    # Text() constants so check_text.py scans every on-screen string.
    return VGroup(
        Text('WenQuanYi Micro Hei', font=ZH),
        Text('rows: list of (text, color).', font=ZH),
        Text('圓方程：由圓心半徑式到一般式', font=ZH),
        Text('先看具體的圓：距離相等，才有圓心半徑式。', font=ZH),
        Text('圓心半徑式是距離公式，不是憑空寫下的。', font=ZH),
        Text('交叉項 -4x 來自 -2 乘圓心的 x 座標。', font=ZH),
        Text('y 的交叉項是 -2k 乘 y，這裡 k = 1。', font=ZH),
        Text('移項只是兩邊同減 9，圓上的點一個都沒變。', font=ZH),
        Text('D 等於 -2 乘 h，所以 D 不是圓心的 x 座標。', font=ZH),
        Text('負號把 -2h 解回 h；半徑平方是減去 F，不是加上 F。', font=ZH),
        Text('一般式是圓心半徑式展開後的同一條方程。', font=ZH),
        Text('stroke_color', font=ZH),
        Text('stroke_width', font=ZH),
        Text('#5a6678', font=ZH),
        Text('x', font=ZH),
        Text('y', font=ZH),
        Text('C(2, 1)', font=ZH),
        Text('圓心 (2, 1)，半徑 3', font=ZH),
        Text('圓上每一點到圓心', font=ZH),
        Text('的距離都是 3。', font=ZH),
        Text('為何又能寫成', font=ZH),
        Text('x^2 + y^2 + Dx + Ey + F = 0 ?', font=ZH),
        Text('水平腿 = x - h = x - 2', font=ZH),
        Text('垂直腿 = y - k = y - 1', font=ZH),
        Text('勾股定理：兩腿平方和 = 斜邊平方', font=ZH),
        Text('(x - 2)^2 + (y - 1)^2 = 3^2', font=ZH),
        Text('3^2 = 9，所以右式是 9', font=ZH),
        Text('設 a = x，b = 2', font=ZH),
        Text('(a - b)^2 = a^2 - 2ab + b^2', font=ZH),
        Text('(x - 2)^2 = x^2 - 2*2*x + 2^2', font=ZH),
        Text('2*2 = 4，2^2 = 4', font=ZH),
        Text('(x - 2)^2 = x^2 - 4x + 4', font=ZH),
        Text('同樣，a = y，b = 1', font=ZH),
        Text('(y - 1)^2 = y^2 - 2*1*y + 1^2', font=ZH),
        Text('2*1 = 2，1^2 = 1', font=ZH),
        Text('(y - 1)^2 = y^2 - 2y + 1', font=ZH),
        Text('代回：(x^2 - 4x + 4) + (y^2 - 2y + 1) = 9', font=ZH),
        Text('兩邊同減 9，等號仍然成立', font=ZH),
        Text('x^2 + y^2 - 4x - 2y + 4 + 1 - 9 = 0', font=ZH),
        Text('常數：4 + 1 - 9 = -4', font=ZH),
        Text('x^2 + y^2 - 4x - 2y - 4 = 0', font=ZH),
        Text('這個圓：', font=ZH),
        Text('x 的係數 = -4', font=ZH),
        Text('y 的係數 = -2', font=ZH),
        Text('常數項 = -4', font=ZH),
        Text('對照 Dx + Ey + F', font=ZH),
        Text('D = -2h = -2*2 = -4', font=ZH),
        Text('E = -2k = -2*1 = -2', font=ZH),
        Text('F = h^2 + k^2 - r^2', font=ZH),
        Text('= 4 + 1 - 9 = -4', font=ZH),
        Text('由 D = -2h 解 h：h = -D / 2', font=ZH),
        Text('h = -(-4) / 2 = 4 / 2 = 2', font=ZH),
        Text('k = -E / 2 = -(-2) / 2 = 1', font=ZH),
        Text('r^2 = (D/2)^2 + (E/2)^2 - F', font=ZH),
        Text('= (-2)^2 + (-1)^2 - (-4)', font=ZH),
        Text('= 4 + 1 + 4 = 9', font=ZH),
        Text('(x - h)^2 + (y - k)^2 = r^2', font=ZH),
        Text('展開後常數移到左邊', font=ZH),
        Text('x^2 + y^2 + Dx + Ey + F = 0', font=ZH),
        Text('D = -2h    E = -2k', font=ZH),
        Text('x - 2', font=ZH),
        Text('y - 1', font=ZH),
        Text('r = 3', font=ZH),
    )
