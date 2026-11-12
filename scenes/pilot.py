from manim import *

BG = "#F6F6F6"
INK = "#2F3334"
MUTED = "#5B6061"
ACCENT = "#46627A"

MEMBERS = [
    ("Aminadab Yunus", "202451028"),
    ("Muhammad Rifqi al Khafis", "202551019"),
    ("Arkano Hamada Moslem", "202551034"),
    ("Farrel Aufa Athaya Ardiyono", "202551042"),
    ("Muhammad La'azidannak Rusda", "202551049"),
    ("Aksel Agustiyan", "202551058"),
    ("Muhammad Arief Satria Nugraha", "202551151"),
]


def pixel_rect(image, box):
    x1, y1, x2, y2 = box
    ih, iw = image.pixel_array.shape[:2]
    left = image.get_left()[0] + (x1 / iw) * image.width
    right = image.get_left()[0] + (x2 / iw) * image.width
    top = image.get_top()[1] - (y1 / ih) * image.height
    bottom = image.get_top()[1] - (y2 / ih) * image.height
    rect = RoundedRectangle(
        corner_radius=0.06,
        width=right - left,
        height=top - bottom,
        color=ACCENT,
        stroke_width=4,
    )
    rect.move_to([(left + right) / 2, (top + bottom) / 2, 0])
    return rect


class MemberScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        kicker = Text(
            "MATA KULIAH BAHASA INDONESIA",
            font="Roboto",
            weight=BOLD,
            color=ACCENT,
            font_size=16,
        )
        kicker.to_corner(UL, buff=0.8)

        title = Text(
            "Cara Menggunakan Mendeley\nuntuk Karya Ilmiah",
            font="Roboto",
            weight=BOLD,
            color=INK,
            font_size=38,
            line_spacing=0.95,
        )
        title.next_to(kicker, DOWN, aligned_edge=LEFT, buff=0.2)

        rule = Line(LEFT, RIGHT, color=ACCENT, stroke_width=3).set_width(3.8)
        rule.next_to(title, DOWN, aligned_edge=LEFT, buff=0.28)

        heading = Text("Anggota Kelompok", font="Roboto", weight=BOLD, color=INK, font_size=22)
        heading.next_to(rule, DOWN, aligned_edge=LEFT, buff=0.32)

        def row(name, nim):
            n = Text(name, font="Roboto", weight=BOLD, color=INK, font_size=17)
            m = Text(nim, font="Roboto", color=MUTED, font_size=13)
            return VGroup(n, m).arrange(DOWN, aligned_edge=LEFT, buff=0.05)

        left = VGroup(*[row(*m) for m in MEMBERS[:4]]).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        right = VGroup(*[row(*m) for m in MEMBERS[4:]]).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        left.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.32)
        right.align_to(left, UP).next_to(left, RIGHT, buff=1.3)

        divider = Line(UP, DOWN, color="#D7DBDC", stroke_width=2).set_height(3.2)
        divider.move_to([(left.get_right()[0] + right.get_left()[0]) / 2, (left.get_top()[1] + left.get_bottom()[1]) / 2, 0])

        self.play(FadeIn(kicker), FadeIn(title, shift=DOWN * 0.1), Create(rule), run_time=1.0)
        self.play(FadeIn(heading), run_time=0.4)
        self.play(Create(divider), run_time=0.3)
        self.play(
            LaggedStart(*[FadeIn(r, shift=UP * 0.08) for r in left], lag_ratio=0.12),
            LaggedStart(*[FadeIn(r, shift=UP * 0.08) for r in right], lag_ratio=0.12),
            run_time=1.2,
        )
        self.wait(9.0)


class ImportScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        step = Text("LANGKAH 1", font="Roboto", weight=BOLD, color=ACCENT, font_size=17)
        step.move_to([-5.3, 3.45, 0])
        title = Text("Impor referensi", font="Roboto", weight=BOLD, color=INK, font_size=40)
        title.next_to(step, DOWN, aligned_edge=LEFT, buff=0.1)
        self.add(step, title)

        img = ImageMobject("assets/shots/library_card.png")
        img.scale_to_fit_height(5.55)
        img.move_to(DOWN * 0.5)
        self.add(img)

        highlight = pixel_rect(img, (207, 192, 632, 260))
        label = Text("Klik", font="Roboto", color=WHITE, font_size=17)
        label_box = RoundedRectangle(
            corner_radius=0.1,
            width=label.width + 0.3,
            height=label.height + 0.16,
            fill_color=ACCENT,
            fill_opacity=1,
            stroke_width=0,
        )
        label_group = VGroup(label_box, label)
        label.move_to(label_box.get_center())
        label_group.next_to(highlight, RIGHT, buff=0.15)

        self.wait(3.5)
        self.play(Create(highlight), run_time=0.7)
        self.play(FadeIn(label_group, shift=LEFT * 0.1), run_time=0.4)
        self.wait(13.0)
