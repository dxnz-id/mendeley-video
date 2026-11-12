from pathlib import Path
import json

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parent.parent
TIMING = json.loads((ROOT / "timing.json").read_text())

BG = "#F6F6F6"
INK = "#2F3334"
MUTED = "#5B6061"
ACCENT = "#46627A"
ACCENT_LIGHT = "#EAF0F4"
WARM_BG = "#F5E6DA"
WARM_INK = "#8A4B2A"
GREEN = "#3E8E5A"
YELLOW = "#F2C94C"
BORDER = "#D9DDDE"
WHITE = "#FFFFFF"

MEMBERS = [
    ("Aminadab Yunus", "202451028"),
    ("Muhammad Rifqi al Khafis", "202551019"),
    ("Arkano Hamada Moslem", "202551034"),
    ("Farrel Aufa Athaya Ardiyono", "202551042"),
    ("Muhammad La’azidannak Rusda", "202551049"),
    ("Aksel Agustiyan", "202551058"),
    ("Muhammad Arief Satria Nugraha", "202551151"),
]


def txt(s, size=16, color=INK, weight=NORMAL, **kwargs):
    return Text(s, font="Roboto", font_size=size, color=color, weight=weight, **kwargs)


def image(path, height):
    img = ImageMobject(str(ROOT / path))
    img.scale_to_fit_height(height)
    return img


def cover_image(path):
    """Scale a screenshot so it covers the 16:9 frame, cropping only at the edges."""
    img = ImageMobject(str(ROOT / path))
    img.scale_to_fit_height(config.frame_height)
    if img.width < config.frame_width:
        img.scale_to_fit_width(config.frame_width)
    return img


def shot_label(text):
    t = txt(text, 11, WHITE, BOLD)
    box = RoundedRectangle(
        corner_radius=0.1,
        width=t.width + 0.5,
        height=t.height + 0.24,
        fill_color="#1F2425",
        fill_opacity=0.9,
        stroke_width=0,
    )
    t.move_to(box.get_center())
    label = VGroup(box, t)
    label.to_corner(DL, buff=0.32)
    return label


def step_bar(labels):
    rows = []
    for i, label in enumerate(labels):
        dot = Circle(
            radius=0.1, fill_color=WHITE, fill_opacity=1,
            stroke_color=BORDER, stroke_width=1,
        )
        num = txt(str(i + 1), 8, MUTED, BOLD).move_to(dot)
        t = txt(label, 10, MUTED)
        row = VGroup(dot, num, t).arrange(RIGHT, buff=0.12)
        rows.append(row)
    rows = VGroup(*rows).arrange(RIGHT, buff=0.45)
    box = RoundedRectangle(
        corner_radius=0.12,
        width=rows.width + 0.6,
        height=0.55,
        fill_color=WHITE,
        fill_opacity=0.92,
        stroke_color=BORDER,
        stroke_width=1,
    )
    box.move_to(rows.get_center())
    bar = VGroup(box, rows)
    bar.to_edge(DOWN, buff=0.18)
    return bar, rows


def card(width, height, fill=WHITE, stroke=BORDER, radius=0.12):
    return RoundedRectangle(
        corner_radius=radius,
        width=width,
        height=height,
        fill_color=fill,
        fill_opacity=1,
        stroke_color=stroke,
        stroke_width=1,
    )


def pixel_rect(image_mob, box, color=ACCENT, stroke_width=4):
    x1, y1, x2, y2 = box
    ih, iw = image_mob.pixel_array.shape[:2]
    left = image_mob.get_left()[0] + (x1 / iw) * image_mob.width
    right = image_mob.get_left()[0] + (x2 / iw) * image_mob.width
    top = image_mob.get_top()[1] - (y1 / ih) * image_mob.height
    bottom = image_mob.get_top()[1] - (y2 / ih) * image_mob.height
    rect = RoundedRectangle(
        corner_radius=0.06,
        width=right - left,
        height=top - bottom,
        color=color,
        stroke_width=stroke_width,
    )
    rect.move_to([(left + right) / 2, (top + bottom) / 2, 0])
    return rect


def pill(text, color=ACCENT, size=16):
    label = txt(text, size, WHITE)
    box = RoundedRectangle(
        corner_radius=0.1,
        width=label.width + 0.3,
        height=label.height + 0.16,
        fill_color=color,
        fill_opacity=1,
        stroke_width=0,
    )
    label.move_to(box.get_center())
    return VGroup(box, label)


def chip(text, color=ACCENT):
    label = txt(text, 12, color)
    box = RoundedRectangle(
        corner_radius=0.12,
        width=label.width + 0.35,
        height=label.height + 0.16,
        fill_color=ACCENT_LIGHT,
        fill_opacity=1,
        stroke_color=color,
        stroke_width=1,
    )
    label.move_to(box.get_center())
    return VGroup(box, label)


def step_header(step, title):
    s = txt(step.upper(), 15, ACCENT, BOLD)
    t = txt(title, 38, INK, BOLD)
    t.next_to(s, DOWN, aligned_edge=LEFT, buff=0.08)
    group = VGroup(s, t)
    group.to_corner(UL, buff=0.7)
    return group


def place_tl(mob, x, y):
    mob.shift([x - mob.get_left()[0], y - mob.get_top()[1], 0])
    return mob


def check_mark(radius=0.14, color=GREEN):
    circle = Circle(radius=radius, fill_color=color, fill_opacity=1, stroke_width=0)
    p1 = Line(LEFT * 0.06 + DOWN * 0.01, DOWN * 0.07, color=WHITE, stroke_width=3)
    p2 = Line(DOWN * 0.07, UP * 0.06 + RIGHT * 0.09, color=WHITE, stroke_width=3)
    return VGroup(circle, p1, p2)


def make_page(width=6.3, height=5.6):
    page = card(width, height, fill=WHITE, stroke=BORDER, radius=0.1)
    bar = RoundedRectangle(
        corner_radius=0.08,
        width=width,
        height=0.42,
        fill_color="#F1F3F4",
        fill_opacity=1,
        stroke_width=0,
    )
    bar.move_to(page.get_top() + DOWN * 0.21)
    dots = VGroup(*[
        Circle(radius=0.045, fill_color="#C7CCCE", fill_opacity=1, stroke_width=0).move_to(
            bar.get_left() + RIGHT * (0.25 + i * 0.16)
        )
        for i in range(3)
    ])
    label = txt("Dokumen1", 7, MUTED).next_to(dots[-1], RIGHT, buff=0.14)
    shell = VGroup(page, bar, dots, label)
    return shell, page


def document_content(page):
    left = page.get_left()[0] + 0.4
    top = page.get_top()[1]
    title = place_tl(txt("Pengaruh Bahasa Madura", 16, INK, BOLD), left, top - 0.72)

    p1 = VGroup(*[
        txt(line, 10.5, INK)
        for line in [
            "Bahasa Indonesia terus berkembang melalui",
            "kontak dengan bahasa daerah. Salah satu",
            "fenomena yang sering muncul adalah",
            "interferensi gramatikal.",
        ]
    ]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    place_tl(p1, left, top - 1.22)

    p2 = VGroup(*[
        txt(line, 10.5, INK)
        for line in [
            "Interferensi ini terlihat pada struktur",
            "kalimat yang belum sesuai kaidah",
            "bahasa Indonesia",
        ]
    ]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    place_tl(p2, left, top - 2.72)

    last = p2[-1]
    cursor = Line(UP * 0.11, DOWN * 0.11, color=ACCENT, stroke_width=2)
    cursor.next_to(last, RIGHT, buff=0.03)
    citation = txt("(Effendy, 2017).", 10.5, ACCENT, BOLD)
    citation.next_to(last, RIGHT, buff=0.04)
    citation.set_opacity(0)

    return VGroup(title, p1, p2, cursor, citation)


def bibliography_content(page):
    left = page.get_left()[0] + 0.4
    top = page.get_top()[1]
    title = place_tl(txt("Daftar Pustaka", 16, INK, BOLD), left, top - 0.72)
    rule = Line(LEFT, RIGHT, color=BORDER, stroke_width=1).set_width(5.3)
    place_tl(rule, left, top - 0.95)

    e1 = VGroup(*[
        txt(line, 8.8, INK)
        for line in [
            "Effendy, M. H. (2017). Interferensi gramatikal bahasa Madura",
            "ke dalam bahasa Indonesia. Dialektika: Jurnal Bahasa,",
            "Sastra, dan Pendidikan Bahasa dan Sastra Indonesia, 4(1), 1–19.",
        ]
    ]).arrange(DOWN, aligned_edge=LEFT, buff=0.03)
    d1 = txt("https://doi.org/10.15408/dialektika.v4i1.6997", 7.8, MUTED)
    d1.next_to(e1, DOWN, aligned_edge=LEFT, buff=0.06)
    entry1 = VGroup(e1, d1)
    place_tl(entry1, left, top - 1.25)

    e2 = VGroup(*[
        txt(line, 8.8, INK)
        for line in [
            "Safi'i, I., Apriyatin, A. N., & Ibrahim, N. (2023). Struktur",
            "dan kaidah kebahasaan teks iklan dalam materi ajar bahasa",
            "Indonesia SMP kelas VIII. Fon: Jurnal Pendidikan Bahasa dan",
            "Sastra Indonesia, 19(1), 139–148.",
        ]
    ]).arrange(DOWN, aligned_edge=LEFT, buff=0.03)
    d2 = txt("https://doi.org/10.25134/fon.v19i1.6855", 7.8, MUTED)
    d2.next_to(e2, DOWN, aligned_edge=LEFT, buff=0.06)
    entry2 = VGroup(e2, d2)
    place_tl(entry2, left, top - 2.45)

    return VGroup(title, rule, entry1, entry2)


def bibliography_card(width=6.4, height=5.2):
    box = card(width, height, fill=WHITE)
    left = box.get_left()[0] + 0.4
    top = box.get_top()[1]
    title = place_tl(txt("Daftar Pustaka", 21, INK, BOLD), left, top - 0.42)
    rule = Line(LEFT, RIGHT, color=BORDER, stroke_width=1).set_width(width - 0.8)
    place_tl(rule, left, top - 0.75)

    def entry(lines, doi, y):
        body = VGroup(*[txt(line, 8.8, INK) for line in lines]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.03
        )
        place_tl(body, left, y)
        url = txt(doi, 7.5, MUTED)
        place_tl(url, left, y - 0.9)
        return VGroup(body, url)

    e1 = entry([
        "Effendy, M. H. (2017). Interferensi gramatikal bahasa Madura",
        "ke dalam bahasa Indonesia. Dialektika: Jurnal Bahasa,",
        "Sastra, dan Pendidikan Bahasa dan Sastra Indonesia, 4(1), 1–19.",
    ], "https://doi.org/10.15408/dialektika.v4i1.6997", top - 1.02)
    e2 = entry([
        "Safi'i, I., Apriyatin, A. N., & Ibrahim, N. (2023). Struktur",
        "dan kaidah kebahasaan teks iklan dalam materi ajar bahasa",
        "Indonesia SMP kelas VIII. Fon: Jurnal Pendidikan Bahasa dan",
        "Sastra Indonesia, 19(1), 139–148.",
    ], "https://doi.org/10.25134/fon.v19i1.6855", top - 2.62)
    return VGroup(box, title, rule), e1, e2


class VideoScene(Scene):
    scene_id = ""

    def setup(self):
        self.camera.background_color = BG
        self.t = TIMING[self.scene_id]
        self.target_duration = self.t["duration"]
        self.cue_map = self.t["cues"]
        self.lead_in = 0.4

    def cue(self, key):
        return self.cue_map[key] + self.lead_in

    def wait_until(self, t):
        delay = t - self.renderer.time
        if delay > 0:
            self.wait(delay)

    def cover(self, path, center_y=0.0):
        self.shot_zoom = 1.0
        img = cover_image(path)
        img.move_to([0, center_y, 0])
        return img

    def focus_shot(self, img, box, zoom=1.6, run_time=0.85):
        iw, ih = img.pixel_array.shape[1], img.pixel_array.shape[0]
        x1, y1, x2, y2 = box
        px = img.get_left()[0] + (((x1 + x2) / 2) / iw) * img.width
        py = img.get_top()[1] - (((y1 + y2) / 2) / ih) * img.height

        img.generate_target()
        img.target.shift(np.array([-px, -py, 0.0]))
        img.target.scale(zoom / self.shot_zoom, about_point=ORIGIN)

        cx, cy, _ = img.target.get_center()
        half_w = config.frame_width / 2
        half_h = config.frame_height / 2
        if img.target.width <= config.frame_width:
            cx = 0.0
        else:
            cx = min(max(cx, half_w - img.target.width / 2), img.target.width / 2 - half_w)
        if img.target.height <= config.frame_height:
            cy = 0.0
        else:
            cy = min(max(cy, half_h - img.target.height / 2), img.target.height / 2 - half_h)
        img.target.move_to([cx, cy, 0])

        self.play(MoveToTarget(img), run_time=run_time)
        self.shot_zoom = zoom

    def finish(self):
        if self.renderer.time > self.target_duration + 0.05:
            raise RuntimeError(
                f"{self.scene_id} overran: {self.renderer.time:.2f}s > {self.target_duration:.2f}s"
            )
        delay = self.target_duration - self.renderer.time
        if delay > 0:
            self.wait(delay)

    def construct(self):
        self.build()
        self.finish()

    def build(self):
        raise NotImplementedError


class Scene01(VideoScene):
    scene_id = "Scene01"

    def build(self):
        kicker = txt("MATA KULIAH BAHASA INDONESIA", 16, ACCENT, BOLD)
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

        heading = txt("Anggota Kelompok", 22, INK, BOLD)
        heading.next_to(rule, DOWN, aligned_edge=LEFT, buff=0.32)

        def row(name, nim):
            n = txt(name, 17, INK, BOLD)
            m = txt(nim, 13, MUTED)
            return VGroup(n, m).arrange(DOWN, aligned_edge=LEFT, buff=0.05)

        left = VGroup(*[row(*m) for m in MEMBERS[:4]]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.24
        )
        right = VGroup(*[row(*m) for m in MEMBERS[4:]]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.24
        )
        left.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.32)
        right.next_to(left, RIGHT, buff=1.3, aligned_edge=UP)

        divider = Line(UP, DOWN, color=BORDER, stroke_width=2).set_height(3.2)
        divider.move_to([
            (left.get_right()[0] + right.get_left()[0]) / 2,
            (left.get_top()[1] + left.get_bottom()[1]) / 2,
            0,
        ])

        footer = txt("Video tutorial Mendeley", 12, MUTED).to_corner(DR, buff=0.8)

        self.play(FadeIn(kicker), FadeIn(title, shift=DOWN * 0.1), Create(rule), run_time=1.0)
        self.play(FadeIn(heading), run_time=0.4)
        self.play(Create(divider), run_time=0.3)
        self.play(
            LaggedStart(*[FadeIn(r, shift=UP * 0.08) for r in left], lag_ratio=0.12),
            LaggedStart(*[FadeIn(r, shift=UP * 0.08) for r in right], lag_ratio=0.12),
            run_time=1.2,
        )
        self.play(FadeIn(footer), run_time=0.4)


class Scene02(VideoScene):
    scene_id = "Scene02"

    def build(self):
        self.add(step_header("Gambaran", "Alur video"))

        banner_box = RoundedRectangle(
            corner_radius=0.12, width=11.8, height=0.8,
            fill_color=WARM_BG, fill_opacity=1, stroke_width=0,
        )
        warn = Circle(radius=0.18, fill_color=WARM_INK, fill_opacity=1, stroke_width=0)
        warn_t = txt("!", 16, WHITE, BOLD).move_to(warn)
        warn_g = VGroup(warn, warn_t)
        warn_g.move_to(banner_box.get_left() + RIGHT * 0.45)
        banner_text = txt("Sitasi manual rawan tidak konsisten.", 17, WARM_INK, BOLD)
        banner_text.next_to(warn_g, RIGHT, buff=0.2)
        banner = VGroup(banner_box, warn_g, banner_text)
        banner.move_to([0, 1.75, 0])

        titles = [
            ("Impor referensi", "PDF dan metadata"),
            ("Sitasi di Word", "Mendeley Cite"),
            ("Daftar pustaka", "Otomatis dan konsisten"),
        ]
        cards = []
        for i, (title, detail) in enumerate(titles):
            box = card(3.6, 2.5, fill="#F0F2F3")
            num = Circle(radius=0.28, fill_color=WHITE, fill_opacity=1, stroke_color=BORDER, stroke_width=2)
            num_t = txt(str(i + 1), 16, MUTED, BOLD).move_to(num)
            t = txt(title, 18, INK, BOLD)
            d = txt(detail, 11, MUTED)
            num.move_to(box.get_corner(UL) + RIGHT * 0.45 + DOWN * 0.45)
            num_t.move_to(num)
            t.next_to(num, RIGHT, buff=0.2).align_to(num, UP)
            d.next_to(t, DOWN, aligned_edge=LEFT, buff=0.1)

            if i == 0:
                ib = RoundedRectangle(
                    corner_radius=0.08, width=0.8, height=1.0,
                    fill_color="#F6E7E3", fill_opacity=1, stroke_color="#D9A79A", stroke_width=1,
                )
                it = txt("PDF", 11, WARM_INK, BOLD).move_to(ib.get_center())
                icon = VGroup(ib, it)
            elif i == 1:
                ib = RoundedRectangle(
                    corner_radius=0.1, width=0.85, height=0.85,
                    fill_color="#E3ECF5", fill_opacity=1, stroke_color="#A9C0D4", stroke_width=1,
                )
                it = txt("W", 28, ACCENT, BOLD).move_to(ib.get_center())
                icon = VGroup(ib, it)
            else:
                ib = RoundedRectangle(
                    corner_radius=0.08, width=0.9, height=1.0,
                    fill_color=WHITE, fill_opacity=1, stroke_color=BORDER, stroke_width=1,
                )
                lines = VGroup()
                for j in range(4):
                    dot = Circle(radius=0.035, fill_color=ACCENT, fill_opacity=1, stroke_width=0)
                    line = Line(LEFT * 0.28, RIGHT * 0.28, color="#AAB6BC", stroke_width=2)
                    row = VGroup(dot, line).arrange(RIGHT, buff=0.08)
                    row.move_to(ib.get_center() + UP * (0.3 - j * 0.2))
                    lines.add(row)
                icon = VGroup(ib, lines)
            icon.move_to(box.get_center() + DOWN * 0.42)

            cards.append(VGroup(box, num, num_t, t, d, icon))

        cards[0].move_to([-4.3, -0.9, 0])
        cards[1].move_to([0, -0.9, 0])
        cards[2].move_to([4.3, -0.9, 0])
        note = txt("Satu library, dipakai berulang.", 15, MUTED).move_to([0, -3.15, 0])

        a1 = Arrow(
            cards[0].get_right() + RIGHT * 0.08,
            cards[1].get_left() + LEFT * 0.08,
            buff=0, color=BORDER, stroke_width=3,
        )
        a2 = Arrow(
            cards[1].get_right() + RIGHT * 0.08,
            cards[2].get_left() + LEFT * 0.08,
            buff=0, color=BORDER, stroke_width=3,
        )

        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards], lag_ratio=0.12),
            Create(a1), Create(a2),
            FadeIn(note, shift=UP * 0.05),
            run_time=0.8,
        )

        self.wait_until(self.cue("problem"))
        self.play(FadeIn(banner, shift=DOWN * 0.1), run_time=0.5)

        for key, card_group in zip(["import", "cite", "bib"], cards):
            self.wait_until(self.cue(key))
            box, num, num_t = card_group[0], card_group[1], card_group[2]
            self.play(
                box.animate.set_fill(ACCENT_LIGHT, 0.55).set_stroke(ACCENT, 3),
                num.animate.set_fill(ACCENT).set_stroke(ACCENT),
                num_t.animate.set_color(WHITE),
                run_time=0.35,
            )


class Scene03(VideoScene):
    scene_id = "Scene03"

    def build(self):
        head = step_header("Sebelum mulai", "Persiapan")
        sub = txt("Empat hal yang perlu disiapkan.", 15, MUTED)
        sub.next_to(head, DOWN, aligned_edge=LEFT, buff=0.15)
        self.add(head, sub)

        specs = [
            ("Akun Mendeley", "Email aktif untuk menyimpan library", None, "@"),
            ("Reference Manager", "Aplikasi desktop untuk PDF dan metadata", "assets/shots/library_card.png", None),
            ("Mendeley Cite", "Add-in untuk Microsoft Word", "assets/shots/cite_panel_card.png", None),
            ("Web Importer", "Ekstensi untuk peramban", "assets/shots/web_importer_card.png", None),
        ]
        positions = [(-3.2, 0.8), (3.2, 0.8), (-3.2, -1.75), (3.2, -1.75)]

        cards = []
        for idx, ((title, sub_text, thumb_path, icon), pos) in enumerate(zip(specs, positions)):
            box = card(5.9, 2.35, fill=WHITE)
            num = Circle(radius=0.24, fill_color=ACCENT, fill_opacity=1, stroke_width=0)
            num_t = txt(str(idx + 1), 14, WHITE, BOLD)
            num_t.move_to(num)
            num.move_to(box.get_corner(UL) + RIGHT * 0.42 + DOWN * 0.42)
            num_t.move_to(num)

            t = txt(title, 15, INK, BOLD)
            t.next_to(num, RIGHT, buff=0.2).align_to(num, UP)
            s = txt(sub_text, 10, MUTED)
            s.next_to(t, DOWN, aligned_edge=LEFT, buff=0.08)

            bits = [box, num, num_t, t, s]
            if thumb_path:
                thumb = image(thumb_path, 1.65)
                thumb.move_to(box.get_right() + LEFT * 1.25 + DOWN * 0.02)
                bits.append(thumb)
            else:
                ic = txt(icon, 46, ACCENT, BOLD)
                ic.move_to(box.get_right() + LEFT * 1.15)
                bits.append(ic)

            group = Group(*bits)
            group.move_to([pos[0], pos[1], 0])

            check = check_mark(0.13)
            check.move_to(group[0].get_corner(UR) + LEFT * 0.3 + DOWN * 0.3)
            check.set_opacity(0)

            self.play(FadeIn(group, shift=UP * 0.12), run_time=0.6)
            self.add(check)
            cards.append((group, check))

        prev_box = None
        for key, (group, check) in zip(["account", "refman", "cite", "web"], cards):
            self.wait_until(self.cue(key))
            box = group[0]
            anims = [
                box.animate.set_fill(ACCENT_LIGHT, 0.55).set_stroke(ACCENT, 2),
                check.animate.set_opacity(1),
            ]
            if prev_box is not None:
                anims.append(prev_box.animate.set_fill(WHITE, 1).set_stroke(BORDER, 1))
            self.play(*anims, run_time=0.35)
            prev_box = box


class Scene04(VideoScene):
    scene_id = "Scene04"

    def build(self):
        bg = FullScreenRectangle(fill_color="#0B0C0C", stroke_width=0)
        img = self.cover("assets/shots/library.png", center_y=-0.6)
        label = shot_label("LANGKAH 1  ·  IMPOR REFERENSI")

        add_box = (75, 35, 480, 130)
        file_box = (205, 135, 670, 225)
        folder_box = (205, 225, 670, 305)
        watched_box = (205, 405, 670, 490)
        list_box = (650, 150, 1160, 500)
        first_row = (655, 185, 1160, 255)

        self.add(bg, img, label)

        self.wait_until(self.cue("add"))
        self.focus_shot(img, add_box, zoom=1.7, run_time=0.7)

        def hbox(box):
            rect = pixel_rect(img, box, YELLOW, 5)
            rect.set_fill(YELLOW, 0.08)
            return rect

        highlight = hbox(add_box)
        self.play(Create(highlight), run_time=0.3)

        self.wait_until(self.cue("import_file"))
        self.play(Transform(highlight, hbox(file_box)), run_time=0.35)

        self.wait_until(self.cue("import_folder"))
        self.play(Transform(highlight, hbox(folder_box)), run_time=0.35)

        self.wait_until(self.cue("library"))
        self.play(FadeOut(highlight), run_time=0.2)
        self.focus_shot(img, list_box, zoom=1.3, run_time=0.75)
        highlight = hbox(first_row)
        status = pill("Masuk ke Library", GREEN, 13)
        status.next_to(highlight, DOWN, buff=0.15)
        self.play(Create(highlight), FadeIn(status, shift=UP * 0.06), run_time=0.4)

        self.wait_until(self.cue("watched"))
        self.play(FadeOut(status), run_time=0.2)
        self.focus_shot(img, watched_box, zoom=1.9, run_time=0.75)
        watched_rect = hbox(watched_box)
        callout = pill("PDF baru otomatis", GREEN, 13)
        callout.move_to([4.4, -2.7, 0])
        self.play(
            Transform(highlight, watched_rect),
            FadeIn(callout, shift=LEFT * 0.06),
            run_time=0.4,
        )


class Scene05(VideoScene):
    scene_id = "Scene05"

    def build(self):
        bg = FullScreenRectangle(fill_color="#0B0C0C", stroke_width=0)
        img = self.cover("assets/raw/guides/your_mendeley_library_0.png", center_y=0.4)
        label = shot_label("LANGKAH 2  ·  CEK METADATA")
        self.add(bg, img, label)

        row_box = (300, 320, 1215, 392)
        title_box = (1225, 250, 1874, 335)
        authors_box = (1225, 335, 1874, 372)
        year_box = (1225, 372, 1874, 410)
        doi_box = (1300, 1020, 1874, 1075)
        folder_box = (30, 620, 320, 675)

        def hbox(box):
            rect = pixel_rect(img, box, YELLOW, 5)
            rect.set_fill(YELLOW, 0.08)
            return rect

        self.wait_until(self.cue("select"))
        self.focus_shot(img, row_box, zoom=1.7, run_time=0.8)
        highlight = hbox(row_box)
        status = pill("Referensi dipilih", ACCENT, 13)
        status.move_to([4.7, -2.7, 0])
        self.play(Create(highlight), FadeIn(status, shift=UP * 0.06), run_time=0.35)

        self.wait_until(self.cue("title"))
        self.play(FadeOut(status), run_time=0.2)
        self.focus_shot(img, (1225, 210, 1874, 500), zoom=1.5, run_time=0.8)
        self.play(Transform(highlight, hbox(title_box)), run_time=0.35)

        self.wait_until(self.cue("authors"))
        self.play(Transform(highlight, hbox(authors_box)), run_time=0.3)

        self.wait_until(self.cue("year"))
        self.play(Transform(highlight, hbox(year_box)), run_time=0.3)

        self.wait_until(self.cue("doi"))
        self.focus_shot(img, (1225, 950, 1874, 1120), zoom=1.7, run_time=0.75)
        self.play(Transform(highlight, hbox(doi_box)), run_time=0.3)

        self.wait_until(self.cue("folder"))
        self.play(FadeOut(highlight), run_time=0.2)
        self.focus_shot(img, (0, 575, 430, 720), zoom=1.7, run_time=0.8)
        highlight = hbox(folder_box)
        folder_note = pill("Collection", ACCENT, 13)
        folder_note.next_to(highlight, RIGHT, buff=0.2)
        self.play(Create(highlight), FadeIn(folder_note, shift=LEFT * 0.06), run_time=0.35)

        self.wait_until(self.cue("tag"))
        tag = chip("Tag: metodologi")
        tag.move_to([4.8, -2.3, 0])
        self.play(FadeIn(tag, shift=UP * 0.08), run_time=0.4)


class Scene06(VideoScene):
    scene_id = "Scene06"

    def build(self):
        bg = FullScreenRectangle(fill_color="#0B0C0C", stroke_width=0)
        img = self.cover("assets/shots/web_importer.png", center_y=1.0)
        label = shot_label("LANGKAH 3  ·  WEB IMPORTER")
        self.add(bg, img, label)

        header_box = (1400, 90, 2450, 200)
        row_box = (1400, 450, 2470, 740)
        add_box = (2280, 240, 2440, 325)

        def hbox(box):
            rect = pixel_rect(img, box, YELLOW, 5)
            rect.set_fill(YELLOW, 0.08)
            return rect

        self.wait_until(self.cue("importer"))
        self.focus_shot(img, header_box, zoom=1.85, run_time=0.8)
        highlight = hbox(header_box)
        self.play(Create(highlight), run_time=0.35)

        self.wait_until(self.cue("importer") + 3.0)
        self.play(FadeOut(highlight), run_time=0.2)
        self.focus_shot(img, row_box, zoom=1.7, run_time=0.75)
        highlight = hbox(row_box)
        self.play(Create(highlight), run_time=0.35)

        self.wait_until(self.cue("select"))
        self.play(highlight.animate.set_stroke(width=6), run_time=0.25)

        self.wait_until(self.cue("add"))
        add_note = pill("Klik Add di kanan atas", ACCENT, 13)
        add_note.move_to([-4.6, 2.7, 0])
        self.play(FadeIn(add_note, shift=RIGHT * 0.06), run_time=0.35)

        self.wait_until(self.cue("library"))
        lib_note = pill("Masuk ke Library", GREEN, 13)
        lib_note.move_to([4.5, -2.7, 0])
        self.play(
            FadeOut(add_note),
            FadeIn(lib_note, shift=UP * 0.06),
            run_time=0.35,
        )


class Scene07(VideoScene):
    scene_id = "Scene07"

    def build(self):
        bg = FullScreenRectangle(fill_color="#0B0C0C", stroke_width=0)
        img = self.cover("assets/shots/cite_card.png", center_y=0.2)
        label = shot_label("LANGKAH 4  ·  SITASI DI WORD")
        self.add(bg, img, label)

        panel_box = (640, 50, 1401, 1074)
        panel_tab = (640, 55, 1050, 118)
        search_box = (660, 310, 1280, 395)
        row_box = (660, 430, 1360, 670)
        insert_box = (750, 620, 940, 665)
        document_box = (100, 240, 640, 520)
        settings_box = (860, 125, 1120, 190)

        def hbox(box):
            rect = pixel_rect(img, box, YELLOW, 5)
            rect.set_fill(YELLOW, 0.08)
            return rect

        self.wait_until(self.cue("panel"))
        self.focus_shot(img, (640, 40, 1401, 600), zoom=1.25, run_time=0.7)
        panel_border = hbox(panel_tab)
        self.play(Create(panel_border), run_time=0.35)
        self.wait(0.3)
        self.play(FadeOut(panel_border), run_time=0.25)

        self.wait_until(self.cue("search"))
        self.focus_shot(img, search_box, zoom=2.0, run_time=0.75)
        highlight = hbox(search_box)
        self.play(Create(highlight), run_time=0.35)

        self.wait_until(self.cue("select"))
        self.focus_shot(img, row_box, zoom=1.6, run_time=0.65)
        self.play(Transform(highlight, hbox(row_box)), run_time=0.35)

        self.wait_until(self.cue("insert"))
        self.focus_shot(img, insert_box, zoom=2.2, run_time=0.65)
        insert_note = pill("Klik Insert citation", ACCENT, 13)
        insert_note.next_to(highlight, DOWN, buff=0.2)
        self.play(
            Transform(highlight, hbox(insert_box)),
            FadeIn(insert_note, shift=DOWN * 0.06),
            run_time=0.35,
        )

        self.wait_until(self.cue("appears"))
        self.play(FadeOut(insert_note), FadeOut(highlight), run_time=0.2)
        self.focus_shot(img, document_box, zoom=1.6, run_time=0.7)
        cite_box = RoundedRectangle(
            corner_radius=0.1, width=4.4, height=1.0,
            fill_color=WHITE, fill_opacity=1, stroke_color=YELLOW, stroke_width=3,
        )
        cite_box.move_to([-4.1, 0.35, 0])
        cite_text = txt("(Effendy, 2017).", 24, ACCENT, BOLD)
        cite_text.move_to(cite_box.get_center())
        citation = VGroup(cite_box, cite_text)
        self.play(FadeIn(citation, shift=UP * 0.08), run_time=0.4)

        self.wait_until(self.cue("settings"))
        self.play(FadeOut(citation), run_time=0.2)
        self.focus_shot(img, settings_box, zoom=2.0, run_time=0.7)
        highlight = hbox(settings_box)
        self.play(Create(highlight), run_time=0.35)

        self.wait_until(self.cue("apa"))
        apa = pill("APA 7", ACCENT, 14)
        apa.next_to(highlight, DOWN, buff=0.22)
        self.play(FadeIn(apa, shift=UP * 0.08), run_time=0.35)

        self.wait_until(self.cue("apa") + 4.5)
        self.play(FadeOut(apa), FadeOut(highlight), run_time=0.2)
        self.focus_shot(img, document_box, zoom=1.5, run_time=0.7)
        citations = VGroup(
            txt("(Effendy, 2017).", 21, ACCENT, BOLD),
            txt("(Safi'i dkk., 2023).", 21, ACCENT, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        cite_card = card(4.6, 1.55, fill=WHITE)
        cite_card.set_stroke(YELLOW, 3)
        citations.move_to(cite_card.get_center())
        same_style = pill("Satu gaya", GREEN, 13)
        same_style.next_to(cite_card, DOWN, buff=0.2)
        final_cites = VGroup(cite_card, citations, same_style)
        final_cites.move_to([-4.0, 0.2, 0])
        self.play(FadeIn(final_cites, shift=UP * 0.08), run_time=0.45)


class Scene08(VideoScene):
    scene_id = "Scene08"

    def build(self):
        bg = FullScreenRectangle(fill_color="#0B0C0C", stroke_width=0)
        img = self.cover("assets/shots/cite_card.png", center_y=0.2)
        label = shot_label("LANGKAH 5  ·  DAFTAR PUSTAKA")
        self.add(bg, img, label)

        more_box = (1215, 120, 1300, 195)

        def hbox(box):
            rect = pixel_rect(img, box, YELLOW, 5)
            rect.set_fill(YELLOW, 0.08)
            return rect

        self.wait_until(self.cue("more"))
        self.focus_shot(img, more_box, zoom=1.55, run_time=0.75)
        highlight = hbox(more_box)
        self.play(Create(highlight), run_time=0.3)

        menu = card(3.3, 2.0, fill=WHITE)
        menu.set_stroke("#9AA0A2", 2)
        menu.move_to([3.9, 2.0, 0])
        insert_bg = RoundedRectangle(
            corner_radius=0.06, width=3.0, height=0.45,
            fill_color=ACCENT_LIGHT, fill_opacity=0, stroke_width=0,
        )
        insert_bg.move_to(menu.get_top() + DOWN * 0.45)
        insert_t = txt("Insert Bibliography", 10, ACCENT, BOLD).move_to(insert_bg)
        export_t = txt("Export", 10, MUTED).move_to(insert_bg.get_center() + DOWN * 0.52)
        refresh_bg = RoundedRectangle(
            corner_radius=0.06, width=3.0, height=0.45,
            fill_color=ACCENT_LIGHT, fill_opacity=0, stroke_width=0,
        )
        refresh_bg.move_to(insert_bg.get_center() + DOWN * 1.04)
        refresh_t = txt("Refresh", 10, MUTED).move_to(refresh_bg)
        menu_group = VGroup(menu, insert_bg, insert_t, export_t, refresh_bg, refresh_t)
        menu_group.set_opacity(0)
        menu_group.set_z_index(40)
        self.add(menu_group)
        self.bring_to_front(menu_group)
        self.play(menu_group.animate.set_opacity(1), run_time=0.4)

        self.wait_until(self.cue("insert_bib"))
        self.play(insert_bg.animate.set_fill(ACCENT_LIGHT, 0.9), run_time=0.3)

        bib, e1, e2 = bibliography_card()
        bib_target = np.array([-3.75, -0.45, 0.0])
        bib_delta = bib_target - bib.get_center()
        bib.move_to(bib_target)
        e1.shift(bib_delta)
        e2.shift(bib_delta)
        bib.set_opacity(0)
        e1.set_opacity(0)
        e2.set_opacity(0)
        bib[0].set_stroke(BORDER, 2)
        bib_shadow = RoundedRectangle(
            corner_radius=0.12, width=6.4, height=5.2,
            fill_color=BLACK, fill_opacity=0.15, stroke_width=0,
        ).move_to(bib_target + np.array([0.08, -0.08, 0.0]))
        bib_shadow.set_z_index(9)
        bib.set_z_index(10)
        e1.set_z_index(10)
        e2.set_z_index(10)
        self.add(bib_shadow, bib, e1, e2)
        self.play(bib.animate.set_opacity(1), run_time=0.6)

        self.wait_until(self.cue("entries"))
        self.play(e1.animate.set_opacity(1), run_time=0.4)
        self.wait(0.25)
        self.play(e2.animate.set_opacity(1), run_time=0.4)

        self.wait_until(self.cue("refresh"))
        updated = VGroup(check_mark(0.12), txt("Daftar diperbarui", 9.5, GREEN, BOLD))
        updated[1].next_to(updated[0], RIGHT, buff=0.1)
        updated.move_to([-3.75, 2.45, 0])
        updated.set_z_index(15)
        self.play(
            insert_bg.animate.set_fill(ACCENT_LIGHT, 0),
            refresh_bg.animate.set_fill(ACCENT_LIGHT, 0.9),
            FadeIn(updated, shift=DOWN * 0.05),
            run_time=0.4,
        )


class Scene09(VideoScene):
    scene_id = "Scene09"

    def build(self):
        head = step_header("Penutup", "Tips")
        sub = txt("Tiga kebiasaan yang membantu.", 15, MUTED)
        sub.next_to(head, DOWN, aligned_edge=LEFT, buff=0.15)
        self.add(head, sub)

        tips = [
            ("Periksa metadata", "Cocokkan judul, penulis, dan tahun setelah impor."),
            ("Satu gaya sitasi", "Pilih APA 7 atau gaya kampus, lalu pakai sampai selesai."),
            ("Cadangkan library", "Penyimpanan gratis 2 GB. Simpan PDF penting di tempat lain."),
        ]
        groups = []
        for i, (title, detail) in enumerate(tips):
            box = card(10.6, 1.25, fill=WHITE)
            num = Circle(radius=0.23, fill_color=ACCENT, fill_opacity=1, stroke_width=0)
            num_t = txt(str(i + 1), 13, WHITE, BOLD).move_to(num)
            t = txt(title, 15, INK, BOLD).next_to(num, RIGHT, buff=0.25).align_to(num, UP)
            d = txt(detail, 10.5, MUTED).next_to(t, DOWN, aligned_edge=LEFT, buff=0.06)
            group = VGroup(box, num, num_t, t, d)
            num.move_to(box.get_corner(UL) + RIGHT * 0.55 + DOWN * 0.62)
            num_t.move_to(num)
            t.next_to(num, RIGHT, buff=0.25).align_to(num, UP)
            d.next_to(t, DOWN, aligned_edge=LEFT, buff=0.06)
            group.move_to([0, 1.2 - i * 1.55, 0])
            groups.append(group)

        for key, group in zip(["metadata", "style", "storage"], groups):
            self.wait_until(self.cue(key))
            self.play(FadeIn(group, shift=UP * 0.1), run_time=0.5)

        close_title = txt("Terima kasih", 40, INK, BOLD)
        close_line = Line(LEFT, RIGHT, color=ACCENT, stroke_width=3).set_width(2.2)
        close_sub = txt("Video tutorial Mendeley", 16, MUTED)
        close_credit = VGroup(
            txt("Tangkapan layar: Mendeley/Elsevier.", 9, MUTED),
            txt("Artikel contoh: Effendy (2017); Safi'i dkk. (2023).", 9, MUTED),
        ).arrange(DOWN, buff=0.05)
        close = VGroup(close_title, close_line, close_sub, close_credit)
        close_title.move_to([0, 0.7, 0])
        close_line.next_to(close_title, DOWN, buff=0.2)
        close_sub.next_to(close_line, DOWN, buff=0.2)
        close_credit.move_to([0, -3.35, 0])

        self.wait_until(self.cue("closing"))
        self.play(
            FadeOut(head),
            FadeOut(sub),
            FadeOut(VGroup(*groups), shift=UP * 0.15),
            FadeIn(close, shift=UP * 0.1),
            run_time=0.8,
        )
