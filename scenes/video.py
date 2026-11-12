from pathlib import Path
import json

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parent.parent
TIMING = json.loads((ROOT / "timing.json").read_text())
BOXES = json.loads((ROOT / "assets" / "ui" / "boxes.json").read_text())

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


def shot_label(text, buff=0.35):
    t = txt(text, 13, WHITE, BOLD)
    box = RoundedRectangle(
        corner_radius=0.1,
        width=t.width + 0.55,
        height=t.height + 0.28,
        fill_color="#1F2425",
        fill_opacity=0.92,
        stroke_width=0,
    )
    t.move_to(box.get_center())
    label = VGroup(box, t)
    label.to_corner(UR, buff=buff)
    label.set_z_index(100)
    return label


def member_rows(name_size=17, nim_size=14, width=9.4, gap=0.42):
    rows = []
    for i, (name, nim) in enumerate(MEMBERS):
        n = txt(name, name_size, INK, BOLD)
        m = txt(nim, nim_size, MUTED)
        n.move_to([-width / 2, -i * gap, 0], aligned_edge=LEFT)
        m.move_to([width / 2, -i * gap, 0], aligned_edge=RIGHT)
        rows.append(VGroup(n, m))
    return VGroup(*rows)


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
    label = txt(text, max(size, 16), WHITE)
    box = RoundedRectangle(
        corner_radius=0.1,
        width=label.width + 0.38,
        height=label.height + 0.2,
        fill_color=color,
        fill_opacity=1,
        stroke_width=0,
    )
    label.move_to(box.get_center())
    return VGroup(box, label)


def chip(text, color=ACCENT):
    label = txt(text, 15, color)
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
        self.lead_in = float(self.t.get("lead_in", 0.4))

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


class Shot:
    """Gambar UI dan kotak highlight bergerak sebagai satu kelompok."""

    def __init__(self, scene, path, screen, center_y=0.0, visible=True):
        self.scene = scene
        self.screen = screen
        self.boxes = BOXES[screen]
        self.img = cover_image(path)
        self.img.move_to([0, center_y, 0])
        self.base_left = self.img.get_left()[0]
        self.base_top = self.img.get_top()[1]
        self.base_center = self.img.get_center()
        self.base_width = self.img.width
        self.base_height = self.img.height
        self.stage = Group(self.img)
        self.zoom = 1.0
        self.highlights = {}
        if visible:
            scene.add(self.stage)

    def highlight(self, key, color=YELLOW, width=5):
        x1, y1, x2, y2 = self.boxes[key]
        rect = pixel_rect(
            self.img, (x1 * 2, y1 * 2, x2 * 2, y2 * 2), color, width
        )
        rect.set_fill(color, opacity=0)
        rect.set_stroke(color, width=width, opacity=0)
        self.stage.add(rect)
        self.highlights[key] = rect
        return rect

    def show(self, key):
        rect = self.highlights[key]
        return rect.animate.set_stroke(opacity=1).set_fill(opacity=0.1)

    def hide(self, key):
        rect = self.highlights[key]
        return rect.animate.set_stroke(opacity=0).set_fill(opacity=0)

    def focus(self, key, zoom=1.35, run_time=0.7):
        x1, y1, x2, y2 = self.boxes[key]
        tx = self.base_left + ((x1 + x2) / 2 / 1920) * self.base_width
        ty = self.base_top - ((y1 + y2) / 2 / 1080) * self.base_height
        current_center = self.stage.get_center()
        width = self.base_width * zoom
        height = self.base_height * zoom
        cx = -zoom * (tx - self.base_center[0])
        cy = -zoom * (ty - self.base_center[1])
        half_w = config.frame_width / 2
        half_h = config.frame_height / 2
        if width <= config.frame_width:
            cx = 0.0
        else:
            cx = min(max(cx, half_w - width / 2), width / 2 - half_w)
        if height <= config.frame_height:
            cy = 0.0
        else:
            cy = min(max(cy, half_h - height / 2), height / 2 - half_h)
        self.stage.generate_target()
        self.stage.target.scale(
            zoom / self.zoom, about_point=current_center
        )
        self.stage.target.shift(
            np.array([cx - current_center[0], cy - current_center[1], 0.0])
        )
        self.scene.play(MoveToTarget(self.stage), run_time=run_time)
        self.zoom = zoom

    def badge(self, text, key, direction=DOWN, buff=0.18, color=GREEN, size=17):
        badge = pill(text, color, size)
        badge.next_to(self.highlights[key], direction, buff=buff)
        margin = 0.3
        if badge.get_right()[0] > config.frame_width / 2 - margin:
            badge.shift(LEFT * (badge.get_right()[0] - (config.frame_width / 2 - margin)))
        if badge.get_left()[0] < -config.frame_width / 2 + margin:
            badge.shift(RIGHT * ((-config.frame_width / 2 + margin) - badge.get_left()[0]))
        if badge.get_top()[1] > config.frame_height / 2 - margin:
            badge.shift(DOWN * (badge.get_top()[1] - (config.frame_height / 2 - margin)))
        if badge.get_bottom()[1] < -config.frame_height / 2 + margin:
            badge.shift(UP * ((-config.frame_height / 2 + margin) - badge.get_bottom()[1]))
        return badge


class Scene01(VideoScene):
    scene_id = "Scene01"

    def build(self):
        kicker = txt("MATA KULIAH BAHASA INDONESIA", 15, ACCENT, BOLD)
        kicker.to_edge(UP, buff=0.55)

        title = Text(
            "Cara Menggunakan Mendeley\nuntuk Karya Ilmiah",
            font="Roboto",
            weight=BOLD,
            color=INK,
            font_size=38,
            line_spacing=0.95,
        )
        title.next_to(kicker, DOWN, buff=0.18)

        rule = Line(LEFT, RIGHT, color=ACCENT, stroke_width=3).set_width(4.2)
        rule.next_to(title, DOWN, buff=0.22)

        heading = txt("Kelompok 7", 21, INK, BOLD)
        heading.next_to(rule, DOWN, buff=0.24)

        rows = member_rows()
        rows.next_to(heading, DOWN, buff=0.22)

        footer = txt("Video tutorial Mendeley", 13, MUTED).to_edge(DOWN, buff=0.55)

        self.play(
            FadeIn(kicker),
            FadeIn(title, shift=DOWN * 0.1),
            Create(rule),
            run_time=0.9,
        )
        self.play(FadeIn(heading), FadeIn(footer), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(r, shift=UP * 0.07) for r in rows], lag_ratio=0.1),
            run_time=1.2,
        )
        self.wait_until(self.lead_in)


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

        self.wait_until(self.cue("import") - 0.25)
        self.play(FadeOut(banner), run_time=0.35)

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
        sub = txt("Empat hal yang perlu disiapkan.", 18, MUTED)
        sub.next_to(head, DOWN, aligned_edge=LEFT, buff=0.15)
        self.add(head, sub)

        specs = [
            ("Akun Mendeley", "Email aktif untuk menyimpan library", None, "@"),
            ("Reference Manager", "Aplikasi desktop untuk kelola PDF", "assets/ui/library_detail.png", None),
            ("Mendeley Cite", "Add-in sitasi di Microsoft Word", "assets/ui/cite_word.png", None),
            ("Web Importer", "Ekstensi impor dari peramban", "assets/ui/web_importer.png", None),
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

            t = txt(title, 17, INK, BOLD)
            t.next_to(num, RIGHT, buff=0.2).align_to(num, UP)
            s = txt(sub_text, 13, MUTED)
            s.next_to(t, DOWN, aligned_edge=LEFT, buff=0.08)

            bits = [box, num, num_t, t, s]
            if thumb_path:
                thumb = image(thumb_path, 1.25)
                thumb.move_to(
                    box.get_right()
                    + LEFT * (thumb.width / 2 + 0.22)
                    + DOWN * 0.5
                )
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
        label = shot_label("LANGKAH 1  ·  IMPOR REFERENSI")
        import_shot = Shot(self, "assets/ui/library_import.png", "library_import")
        detail_shot = Shot(
            self, "assets/ui/library_detail.png", "library_detail", visible=False
        )
        watch_shot = Shot(
            self, "assets/ui/library_import.png", "library_import", visible=False
        )
        for key in ["add", "import_file", "import_folder", "import_library"]:
            import_shot.highlight(key)
        detail_shot.highlight("row")
        watch_shot.highlight("watched")
        self.add(label)

        self.wait_until(self.cue("add"))
        import_shot.focus("add", zoom=1.3, run_time=0.6)
        self.play(import_shot.show("add"), run_time=0.25)

        self.wait_until(self.cue("import_file"))
        self.play(
            import_shot.hide("add"), import_shot.show("import_file"), run_time=0.3
        )

        self.wait_until(self.cue("import_folder"))
        self.play(
            import_shot.hide("import_file"), import_shot.show("import_folder"),
            run_time=0.3,
        )

        self.wait_until(self.cue("import_library"))
        self.play(
            import_shot.hide("import_folder"), import_shot.show("import_library"),
            run_time=0.3,
        )

        self.wait_until(self.cue("library"))
        self.play(
            FadeOut(import_shot.stage),
            FadeIn(detail_shot.stage),
            run_time=0.45,
        )
        detail_shot.focus("row", zoom=1.3, run_time=0.6)
        self.play(detail_shot.show("row"), run_time=0.25)
        status = detail_shot.badge("Masuk ke Library", "row", DOWN, buff=0.8)
        self.play(FadeIn(status, shift=UP * 0.06), run_time=0.3)

        self.wait_until(self.cue("watched") - 0.35)
        self.play(FadeOut(status), run_time=0.25)
        self.wait_until(self.cue("watched"))
        self.play(
            FadeOut(detail_shot.stage),
            FadeIn(watch_shot.stage),
            run_time=0.35,
        )
        watch_shot.focus("watched", zoom=1.3, run_time=0.6)
        self.play(watch_shot.show("watched"), run_time=0.25)
        callout = watch_shot.badge("PDF baru otomatis", "watched", DOWN, buff=0.22)
        self.play(FadeIn(callout, shift=UP * 0.06), run_time=0.3)


class Scene05(VideoScene):
    scene_id = "Scene05"

    def build(self):
        label = shot_label("LANGKAH 2  ·  PERIKSA METADATA", buff=0.15)
        shot = Shot(self, "assets/ui/library_detail.png", "library_detail")
        for key in ["row", "title", "authors", "year", "doi", "folder", "tag"]:
            shot.highlight(key)
        self.add(label)

        self.wait_until(self.cue("select"))
        shot.focus("row", zoom=1.3, run_time=0.6)
        self.play(shot.show("row"), run_time=0.25)

        self.wait_until(self.cue("title"))
        self.play(shot.hide("row"), run_time=0.25)
        shot.focus("title", zoom=1.3, run_time=0.6)
        self.play(shot.show("title"), run_time=0.25)

        self.wait_until(self.cue("authors"))
        self.play(shot.hide("title"), shot.show("authors"), run_time=0.3)

        self.wait_until(self.cue("year"))
        self.play(shot.hide("authors"), shot.show("year"), run_time=0.3)

        self.wait_until(self.cue("doi"))
        self.play(shot.hide("year"), run_time=0.2)
        shot.focus("doi", zoom=1.35, run_time=0.6)
        self.play(shot.show("doi"), run_time=0.25)

        self.wait_until(self.cue("folder"))
        self.play(shot.hide("doi"), run_time=0.2)
        shot.focus("folder", zoom=1.35, run_time=0.6)
        self.play(shot.show("folder"), run_time=0.25)

        self.wait_until(self.cue("tag"))
        self.play(shot.hide("folder"), shot.show("tag"), run_time=0.3)
        tag_note = shot.badge("Tag: metodologi", "tag", DOWN, buff=0.14, color=WARM_INK)
        self.play(FadeIn(tag_note, shift=UP * 0.06), run_time=0.3)


class Scene06(VideoScene):
    scene_id = "Scene06"

    def build(self):
        label = shot_label("LANGKAH 3  ·  WEB IMPORTER")
        shot = Shot(self, "assets/ui/web_importer.png", "web_importer")
        for key in ["header", "row", "add"]:
            shot.highlight(key)
        self.add(label)

        self.wait_until(self.cue("importer"))
        shot.focus("header", zoom=1.25, run_time=0.6)
        self.play(shot.show("header"), run_time=0.25)

        self.wait_until(self.cue("importer") + 3.0)
        self.play(shot.hide("header"), run_time=0.2)
        shot.focus("row", zoom=1.35, run_time=0.6)
        self.play(shot.show("row"), run_time=0.25)

        self.wait_until(self.cue("select"))
        self.play(
            shot.highlights["row"].animate.set_stroke(width=7), run_time=0.3
        )

        self.wait_until(self.cue("add"))
        shot.focus("add", zoom=1.35, run_time=0.6)
        self.play(shot.show("add"), run_time=0.25)

        self.wait_until(self.cue("library"))
        self.play(shot.hide("add"), shot.hide("row"), run_time=0.25)
        shot.focus("row", zoom=1.3, run_time=0.6)
        self.play(shot.show("row"), run_time=0.25)
        lib_note = shot.badge("Masuk ke Library", "row", DOWN, buff=0.3)
        self.play(FadeIn(lib_note, shift=UP * 0.06), run_time=0.3)


class Scene07(VideoScene):
    scene_id = "Scene07"

    def build(self):
        label = shot_label("LANGKAH 4  ·  SITASI DI WORD")
        shot = Shot(self, "assets/ui/cite_word.png", "cite_word")
        settings_shot = Shot(
            self, "assets/ui/cite_settings.png", "cite_settings", visible=False
        )
        for key in ["panel", "settings_tab", "search", "row", "insert", "citation1", "citation2"]:
            shot.highlight(key)
        for key in ["citation_settings", "apa", "document", "citation1", "citation2"]:
            settings_shot.highlight(key)
        self.add(label)

        self.wait_until(self.cue("panel"))
        shot.focus("settings_tab", zoom=1.2, run_time=0.6)
        self.play(shot.show("settings_tab"), run_time=0.25)
        self.wait(0.4)
        self.play(shot.hide("settings_tab"), run_time=0.2)

        self.wait_until(self.cue("search"))
        shot.focus("search", zoom=1.4, run_time=0.6)
        self.play(shot.show("search"), run_time=0.25)

        self.wait_until(self.cue("select"))
        self.play(shot.hide("search"), run_time=0.2)
        shot.focus("row", zoom=1.3, run_time=0.6)
        self.play(shot.show("row"), run_time=0.25)

        self.wait_until(self.cue("insert"))
        self.play(shot.hide("row"), run_time=0.2)
        shot.focus("insert", zoom=1.35, run_time=0.55)
        self.play(shot.show("insert"), run_time=0.25)

        self.wait_until(self.cue("appears"))
        self.play(shot.hide("insert"), run_time=0.2)
        shot.focus("citation1", zoom=1.4, run_time=0.6)
        self.play(shot.show("citation1"), run_time=0.25)

        self.wait_until(self.cue("settings"))
        self.play(
            FadeOut(shot.stage),
            FadeIn(settings_shot.stage),
            run_time=0.45,
        )
        settings_shot.focus("citation_settings", zoom=1.35, run_time=0.6)
        self.play(settings_shot.show("citation_settings"), run_time=0.25)

        self.wait_until(self.cue("apa"))
        self.play(settings_shot.hide("citation_settings"), run_time=0.2)
        settings_shot.focus("apa", zoom=1.3, run_time=0.55)
        self.play(settings_shot.show("apa"), run_time=0.25)

        self.wait_until(self.cue("apa") + 4.5)
        self.play(settings_shot.hide("apa"), run_time=0.2)
        settings_shot.focus("citation1", zoom=1.35, run_time=0.6)
        self.play(
            settings_shot.show("citation1"),
            settings_shot.show("citation2"),
            run_time=0.3,
        )
        same_style = settings_shot.badge(
            "Satu gaya", "citation2", RIGHT, buff=2.2
        )
        self.play(FadeIn(same_style, shift=LEFT * 0.06), run_time=0.3)


class Scene08(VideoScene):
    scene_id = "Scene08"

    def build(self):
        label = shot_label("LANGKAH 5  ·  DAFTAR PUSTAKA")
        shot = Shot(self, "assets/ui/cite_word.png", "cite_word")
        menu_shot = Shot(
            self, "assets/ui/cite_menu.png", "cite_menu", visible=False
        )
        bib_shot = Shot(
            self, "assets/ui/cite_bib.png", "cite_bib", visible=False
        )
        shot.highlight("more")
        menu_shot.highlight("insert_bib")
        menu_shot.highlight("refresh")
        bib_shot.highlight("entries")
        bib_shot.highlight("refresh")
        self.add(label)

        self.wait_until(self.cue("more"))
        shot.focus("more", zoom=1.3, run_time=0.6)
        self.play(shot.show("more"), run_time=0.25)

        self.wait_until(self.cue("insert_bib"))
        self.play(
            shot.hide("more"),
            FadeOut(shot.stage),
            FadeIn(menu_shot.stage),
            run_time=0.45,
        )
        menu_shot.focus("insert_bib", zoom=1.35, run_time=0.6)
        self.play(menu_shot.show("insert_bib"), run_time=0.25)

        self.wait_until(self.cue("entries"))
        self.play(
            menu_shot.hide("insert_bib"),
            FadeOut(menu_shot.stage),
            FadeIn(bib_shot.stage),
            run_time=0.45,
        )
        bib_shot.focus("entries", zoom=1.25, run_time=0.6)
        self.play(bib_shot.show("entries"), run_time=0.25)
        updated = bib_shot.badge(
            "Daftar diperbarui", "entries", DOWN, buff=0.18
        )
        self.play(FadeIn(updated, shift=UP * 0.06), run_time=0.3)

        self.wait_until(self.cue("refresh"))
        self.play(FadeOut(updated), run_time=0.2)
        bib_shot.focus("refresh", zoom=1.35, run_time=0.6)
        self.play(bib_shot.show("refresh"), run_time=0.25)

        self.wait(1.5)
        self.play(bib_shot.hide("refresh"), run_time=0.25)
        bib_shot.focus("entries", zoom=1.2, run_time=1.6)
        self.play(bib_shot.show("entries"), run_time=0.3)
        final_note = bib_shot.badge(
            "Daftar diperbarui", "entries", DOWN, buff=0.18
        )
        self.play(FadeIn(final_note), run_time=0.25)
        self.play(bib_shot.stage.animate.scale(1.015), run_time=3.0)


class Scene09(VideoScene):
    scene_id = "Scene09"

    def build(self):
        head = step_header("Penutup", "Tips")
        sub = txt("Tiga kebiasaan yang membantu.", 18, MUTED)
        sub.next_to(head, DOWN, aligned_edge=LEFT, buff=0.15)
        self.add(head, sub)

        tips = [
            ("Periksa metadata", "Cocokkan judul, penulis, dan tahun setelah impor."),
            ("Satu gaya sitasi", "Pilih APA 7 atau gaya kampus, lalu pakai sampai selesai."),
            ("Cadangkan library", "Penyimpanan gratis 2 GB. Simpan PDF penting di tempat lain."),
        ]
        groups = []
        for i, (title, detail) in enumerate(tips):
            box = card(10.6, 1.45, fill=WHITE)
            num = Circle(radius=0.25, fill_color=ACCENT, fill_opacity=1, stroke_width=0)
            num_t = txt(str(i + 1), 14, WHITE, BOLD).move_to(num)
            t = txt(title, 18, INK, BOLD).next_to(num, RIGHT, buff=0.25).align_to(num, UP)
            d = txt(detail, 14, MUTED).next_to(t, DOWN, aligned_edge=LEFT, buff=0.07)
            group = VGroup(box, num, num_t, t, d)
            num.move_to(box.get_corner(UL) + RIGHT * 0.6 + DOWN * 0.7)
            num_t.move_to(num)
            t.next_to(num, RIGHT, buff=0.25).align_to(num, UP)
            d.next_to(t, DOWN, aligned_edge=LEFT, buff=0.07)
            group.move_to([0, 1.35 - i * 1.65, 0])
            groups.append(group)

        for key, group in zip(["metadata", "style", "storage"], groups):
            self.wait_until(self.cue(key))
            self.play(FadeIn(group, shift=UP * 0.1), run_time=0.5)

        close_title = txt("Terima kasih", 40, INK, BOLD).to_edge(UP, buff=0.55)
        close_line = Line(LEFT, RIGHT, color=ACCENT, stroke_width=3).set_width(2.2)
        close_line.next_to(close_title, DOWN, buff=0.18)
        close_sub = txt("Video tutorial Mendeley", 18, MUTED)
        close_sub.next_to(close_line, DOWN, buff=0.16)
        close_names = member_rows(name_size=15, nim_size=12, width=8.6, gap=0.29)
        close_names.next_to(close_sub, DOWN, buff=0.18)
        close_credit = VGroup(
            txt("Tampilan Mendeley dan Word: rekonstruksi demo.", 12.5, MUTED),
            txt("Artikel contoh: Effendy (2017); Safi'i dkk. (2023).", 12.5, MUTED),
        ).arrange(DOWN, buff=0.06)
        close_credit.move_to([0, -2.95, 0])
        close = VGroup(
            close_title, close_line, close_sub, close_names, close_credit
        )

        self.wait_until(self.cue("closing"))
        self.play(
            FadeOut(head),
            FadeOut(sub),
            FadeOut(VGroup(*groups), shift=UP * 0.15),
            FadeIn(close, shift=UP * 0.1),
            run_time=0.8,
        )
