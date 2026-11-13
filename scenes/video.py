from pathlib import Path
import json

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parent.parent
TIMING = json.loads((ROOT / "timing.json").read_text())
BOXES = json.loads((ROOT / "assets" / "ui" / "boxes.json").read_text())

# Material 3 Expressive, mengikuti deck ppt-implementasi-mendeley.
BG = "#F6F6F6"
INK = "#2F3334"
MUTED = "#5B6061"
P = "#46627A"
ON_P = "#F6F9FF"
PC = "#B0C8E0"
ON_PC = "#355169"
SC = "#C1E0E0"
ON_SC = "#3D6060"
TC = "#DCE7D6"
ON_TC = "#536350"
RAIL = "#ECEEEE"
CARD = "#E6E9E9"
ACCENT = P
ACCENT_LIGHT = PC
PRIMARY = P
ON_PRIMARY = ON_P
PRIMARY_CONTAINER = PC
ON_PRIMARY_CONTAINER = ON_PC
SECONDARY = ON_SC
SECONDARY_CONTAINER = SC
ON_SECONDARY_CONTAINER = ON_SC
TERTIARY = ON_TC
TERTIARY_CONTAINER = TC
ON_TERTIARY_CONTAINER = ON_TC
SURFACE = BG
ON_SURFACE = INK
SURFACE_LOW = CARD
SURFACE_CONTAINER = RAIL
SURFACE_HIGH = "#E0E4E4"
SURFACE_HIGHEST = "#D5DADA"
OUTLINE = "#8A9494"
WARM_BG = PC
WARM_INK = ON_PC
GREEN = P
YELLOW = P
BORDER = "#C9D0D0"
WHITE = "#FFFFFF"
CONTENT_LEFT = -5.26
CONTENT_CENTER = 0.7
M3 = ROOT / "assets" / "m3"

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


def shape_icon(name, height=1.0, opacity=1.0):
    img = ImageMobject(str(M3 / f"{name}.png"))
    img.scale_to_fit_height(height)
    if opacity != 1:
        img.set_opacity(opacity)
    return img


def cover_image(path):
    """Scale a screenshot so it covers the 16:9 frame, cropping only at the edges."""
    img = ImageMobject(str(ROOT / path))
    img.scale_to_fit_height(config.frame_height)
    if img.width < config.frame_width:
        img.scale_to_fit_width(config.frame_width)
    return img


def shot_label(step, text, buff=0.55):
    number = txt(str(step), 15, PRIMARY, BOLD)
    separator = txt("|", 13, MUTED, BOLD)
    description = txt(text, 11.5, ON_SURFACE, BOLD)
    content = VGroup(number, separator, description).arrange(RIGHT, buff=0.16)
    box = RoundedRectangle(
        corner_radius=0.23,
        width=content.width + 0.5,
        height=0.46,
        fill_color=WHITE,
        fill_opacity=0.96,
        stroke_color=BORDER,
        stroke_width=1,
    )
    content.move_to(box.get_center())
    label = VGroup(box, content)
    label.to_corner(UL, buff=buff)
    label.set_z_index(100)
    return label


def member_grid(name_size=17, nim_size=13, width=5.5, gap=0.46, column_gap=1.0):
    rows = []
    for name, nim in MEMBERS:
        n = txt(name, name_size, INK, BOLD)
        m = txt(nim, nim_size, MUTED)
        n.move_to([-width / 2, 0, 0], aligned_edge=LEFT)
        m.move_to([width / 2, 0, 0], aligned_edge=RIGHT)
        rows.append(VGroup(n, m))
    left = VGroup(*rows[:4]).arrange(DOWN, aligned_edge=LEFT, buff=gap)
    right = VGroup(*rows[4:]).arrange(DOWN, aligned_edge=LEFT, buff=gap)
    right.next_to(left, RIGHT, buff=column_gap, aligned_edge=UP)
    return VGroup(left, right)


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


def card(width, height, fill=SURFACE_LOW, stroke=None, radius=0.24):
    return RoundedRectangle(
        corner_radius=radius,
        width=width,
        height=height,
        fill_color=fill,
        fill_opacity=1,
        stroke_color=stroke or OUTLINE,
        stroke_width=1 if stroke else 0,
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


def pill(text, color=PRIMARY, size=17, text_color=None):
    label = txt(text, max(size, 16), text_color or ON_PRIMARY, BOLD)
    box = RoundedRectangle(
        corner_radius=0.3,
        width=label.width + 0.5,
        height=label.height + 0.22,
        fill_color=color,
        fill_opacity=1,
        stroke_width=0,
    )
    label.move_to(box.get_center())
    return VGroup(box, label)


def chip(text, color=PRIMARY):
    label = txt(text, 14, ON_PRIMARY_CONTAINER, BOLD)
    box = RoundedRectangle(
        corner_radius=0.2,
        width=label.width + 0.42,
        height=label.height + 0.18,
        fill_color=PRIMARY_CONTAINER,
        fill_opacity=1,
        stroke_width=0,
    )
    label.move_to(box.get_center())
    return VGroup(box, label)


def page_header(title):
    t = txt(title, 44, INK, BOLD)
    t.to_corner(UL, buff=0.7)
    t.shift(RIGHT * (CONTENT_LEFT - t.get_left()[0]))
    return t


RAIL_SECTIONS = [
    ("rail_latar", "Latar"),
    ("rail_mengenal", "Mengenal"),
    ("rail_praktik", "Praktik"),
    ("rail_evaluasi", "Evaluasi"),
    ("rail_penutup", "Penutup"),
]


def left_rail(active=0):
    rail = RoundedRectangle(
        corner_radius=0.3, width=1.18, height=7.16,
        fill_color=RAIL, fill_opacity=1, stroke_width=0,
    ).move_to([-6.1, 0, 0])
    logo = shape_icon("logo_rail", 0.7).move_to([-6.1, 2.95, 0])
    items = Group()
    for k, (icon_name, label) in enumerate(RAIL_SECTIONS):
        y = 1.9 - k * 1.2
        if k == active:
            items.add(
                RoundedRectangle(
                    corner_radius=0.3, width=1.0, height=1.02,
                    fill_color=PC, fill_opacity=1, stroke_width=0,
                ).move_to([-6.1, y, 0])
            )
        items.add(shape_icon(icon_name, 0.36, 1 if k == active else 0.5).move_to([-6.1, y + 0.18, 0]))
        items.add(
            txt(label, 9, ON_PC if k == active else MUTED, BOLD if k == active else NORMAL)
            .move_to([-6.1, y - 0.25, 0])
        )
    return Group(rail, logo, items)


def slide_num(n):
    return txt(f"{n:02d} / 09", 9, MUTED).to_corner(DR, buff=0.4)


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
        title = Text(
            "Cara Menggunakan Mendeley\nuntuk Karya Ilmiah",
            font="Roboto",
            weight=BOLD,
            color=INK,
            font_size=46,
            line_spacing=0.92,
        )
        title.to_corner(UL, buff=0.7)

        subtitle = txt("Tutorial pengelolaan referensi", 17, PRIMARY, BOLD)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.28)

        cover_icon = shape_icon("cover_library", 2.35).move_to([4.65, 2.0, 0])
        quote_icon = shape_icon("quote_clover", 0.9).move_to([5.8, 0.55, 0])

        panel = card(12.4, 3.0, fill=SURFACE_LOW, radius=0.32)
        panel.move_to([0, -1.55, 0])

        group_label = chip("Kelompok 7")
        group_label.move_to(panel.get_corner(UL) + RIGHT * 0.9 + DOWN * 0.38)

        grid = member_grid(name_size=17, nim_size=13, width=5.5, gap=0.38, column_gap=0.9)
        grid.move_to(panel.get_center() + DOWN * 0.16)

        footer = txt("Video tutorial Mendeley  ·  01 / 09", 12, MUTED)
        footer.to_corner(DR, buff=0.55)

        self.play(
            FadeIn(title, shift=DOWN * 0.1),
            FadeIn(cover_icon, shift=UP * 0.1),
            run_time=0.9,
        )
        self.play(
            FadeIn(subtitle), FadeIn(quote_icon),
            FadeIn(panel), FadeIn(footer),
            run_time=0.5,
        )
        self.play(
            FadeIn(group_label, shift=UP * 0.05),
            LaggedStart(
                *[FadeIn(r, shift=UP * 0.07) for r in [*grid[0], *grid[1]]],
                lag_ratio=0.1,
            ),
            run_time=1.2,
        )
        self.wait_until(self.lead_in)


class Scene02(VideoScene):
    scene_id = "Scene02"

    def build(self):
        self.add(left_rail(0))
        self.add(page_header("Alur video"))
        self.add(slide_num(2))

        banner_box = RoundedRectangle(
            corner_radius=0.3, width=11.4, height=0.86,
            fill_color=PC, fill_opacity=1, stroke_width=0,
        )
        banner_icon = shape_icon("timer_burst", 0.72)
        banner_icon.move_to(banner_box.get_left() + RIGHT * 0.52)
        banner_text = txt("Sitasi manual rawan tidak konsisten.", 18, ON_PC, BOLD)
        banner_text.next_to(banner_icon, RIGHT, buff=0.2)
        banner = Group(banner_box, banner_icon, banner_text).move_to([CONTENT_CENTER, 1.7, 0])

        specs = [
            ("Impor referensi", "PDF dan metadata", "upload_flower", CARD, INK),
            ("Sitasi di Word", "Mendeley Cite", "quote_navy_flower", SC, ON_SC),
            ("Daftar pustaka", "Otomatis dan konsisten", "mendeley_flower", TC, ON_TC),
        ]
        cards = []
        for i, (title, detail, icon_name, fill, text_color) in enumerate(specs):
            box = card(3.3, 2.55, fill=fill, radius=0.3)
            icon = shape_icon(icon_name, 0.82)
            icon.move_to(box.get_corner(UL) + RIGHT * 0.52 + DOWN * 0.5)
            t = txt(title, 17, text_color, BOLD)
            t.next_to(icon, RIGHT, buff=0.12).align_to(icon, UP)
            d = txt(detail, 11, text_color).next_to(t, DOWN, aligned_edge=LEFT, buff=0.08)
            big = txt(f"0{i + 1}", 54, text_color, BOLD).set_opacity(0.16)
            big.move_to(box.get_corner(DR) + LEFT * 0.5 + UP * 0.42, aligned_edge=DR)
            cards.append(Group(box, big, icon, t, d))

        cards[0].move_to([-3.65, -0.9, 0])
        cards[1].move_to([CONTENT_CENTER, -0.9, 0])
        cards[2].move_to([5.05, -0.9, 0])
        note = txt("Satu library, dipakai berulang.", 14, MUTED)
        note.move_to([CONTENT_CENTER, -3.12, 0])

        a1 = shape_icon("arrow_navy", 0.42)
        a1.move_to([(cards[0].get_right()[0] + cards[1].get_left()[0]) / 2, -0.9, 0])
        a2 = shape_icon("arrow_navy", 0.42)
        a2.move_to([(cards[1].get_right()[0] + cards[2].get_left()[0]) / 2, -0.9, 0])

        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards], lag_ratio=0.12),
            FadeIn(a1), FadeIn(a2),
            FadeIn(note, shift=UP * 0.05),
            run_time=0.8,
        )

        self.wait_until(self.cue("problem"))
        self.play(FadeIn(banner, shift=DOWN * 0.1), run_time=0.5)

        self.wait_until(self.cue("import") - 0.25)
        self.play(FadeOut(banner), run_time=0.35)

        prev_box = None
        for key, card_group in zip(["import", "cite", "bib"], cards):
            self.wait_until(self.cue(key))
            box = card_group[0]
            anims = [box.animate.set_stroke(P, 5)]
            if prev_box is not None:
                anims.append(prev_box.animate.set_stroke(width=0))
            self.play(*anims, run_time=0.35)
            prev_box = box


class Scene03(VideoScene):
    scene_id = "Scene03"

    def build(self):
        self.add(left_rail(2))
        head = page_header("Persiapan")
        sub = txt("Empat hal yang perlu disiapkan.", 18, MUTED)
        sub.next_to(head, DOWN, aligned_edge=LEFT, buff=0.15)
        self.add(head, sub, slide_num(3))

        specs = [
            ("Buat akun", "Daftar dengan email aktif.", "personadd_burst", CARD, INK),
            ("Reference Manager", "Simpan, kelompokkan, dan anotasi PDF.", "mendeley_flower", SC, ON_SC),
            ("Mendeley Cite", "Sisipkan kutipan dari Word.", "cite_flower", TC, ON_TC),
            ("Web Importer", "Simpan referensi dari halaman web.", "webimporter_squircle", CARD, INK),
        ]
        positions = [(-2.35, 0.55), (3.75, 0.55), (-2.35, -1.95), (3.75, -1.95)]

        cards = []
        for idx, ((title, sub_text, icon_name, fill, text_color), pos) in enumerate(
            zip(specs, positions)
        ):
            box = card(5.65, 2.35, fill=fill, radius=0.3)
            icon = shape_icon(icon_name, 1.0)
            icon.move_to(box.get_right() + LEFT * 0.95 + DOWN * 0.05)
            num = txt(f"0{idx + 1}", 46, text_color, BOLD).set_opacity(0.12)
            num.move_to(box.get_corner(DL) + RIGHT * 0.72 + UP * 0.42)
            t = txt(title, 18, text_color, BOLD)
            t.move_to(box.get_left() + RIGHT * 0.35 + UP * 0.42, aligned_edge=LEFT)
            s = txt(sub_text, 12.5, text_color)
            s.next_to(t, DOWN, aligned_edge=LEFT, buff=0.08)

            group = Group(box, num, icon, t, s)
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
                box.animate.set_stroke(P, 4),
                check.animate.set_opacity(1),
            ]
            if prev_box is not None:
                anims.append(prev_box.animate.set_stroke(width=0))
            self.play(*anims, run_time=0.35)
            prev_box = box


class Scene04(VideoScene):
    scene_id = "Scene04"

    def build(self):
        label = shot_label(1, "Impor referensi")
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
        label = shot_label(2, "Periksa metadata")
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
        tag_note = shot.badge("Tag: metodologi", "tag", DOWN, buff=0.14, color=SECONDARY)
        self.play(FadeIn(tag_note, shift=UP * 0.06), run_time=0.3)


class Scene06(VideoScene):
    scene_id = "Scene06"

    def build(self):
        label = shot_label(3, "Web importer")
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
        label = shot_label(4, "Sitasi di Word")
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
        label = shot_label(5, "Daftar pustaka")
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
        rail = left_rail(3)
        head = page_header("Tips")
        sub = txt("Tiga kebiasaan yang membantu.", 18, MUTED)
        sub.next_to(head, DOWN, aligned_edge=LEFT, buff=0.15)
        page = slide_num(9)
        self.add(rail, head, sub, page)

        tips = [
            ("Periksa metadata", "Cocokkan judul, penulis, dan tahun setelah impor.", "factcheck_sunny", CARD, INK),
            ("Satu gaya sitasi", "Pilih APA 7 atau gaya kampus, lalu pakai sampai selesai.", "quote_navy_flower", SC, ON_SC),
            ("Cadangkan library", "Penyimpanan gratis 2 GB. Simpan PDF penting di tempat lain.", "download_squircle", TC, ON_TC),
        ]
        groups = []
        for i, (title, detail, icon_name, fill, text_color) in enumerate(tips):
            box = card(11.4, 1.55, fill=fill, radius=0.3)
            icon = shape_icon(icon_name, 0.95)
            icon.move_to(box.get_left() + RIGHT * 0.8)
            t = txt(title, 20, text_color, BOLD)
            t.next_to(icon, RIGHT, buff=0.24).align_to(icon, UP)
            d = txt(detail, 14, text_color).next_to(t, DOWN, aligned_edge=LEFT, buff=0.07)
            big = txt(f"0{i + 1}", 46, text_color, BOLD).set_opacity(0.18)
            big.move_to(box.get_corner(DR) + LEFT * 0.55 + UP * 0.4, aligned_edge=DR)
            group = Group(box, big, icon, t, d)
            group.move_to([CONTENT_CENTER, 1.0 - i * 1.7, 0])
            groups.append(group)

        for key, group in zip(["metadata", "style", "storage"], groups):
            self.wait_until(self.cue(key))
            self.play(FadeIn(group, shift=UP * 0.1), run_time=0.5)

        close_title = txt("Terima kasih", 52, INK, BOLD)
        close_title.move_to([-6.0, 2.55, 0], aligned_edge=LEFT)
        close_sub = txt("Kelompok 7  ·  Video tutorial Mendeley", 16, MUTED)
        close_sub.next_to(close_title, DOWN, aligned_edge=LEFT, buff=0.24)
        close_icon = shape_icon("quote_clover", 2.45).move_to([4.75, 1.75, 0])
        close_credit = VGroup(
            txt("Tampilan Mendeley: rekonstruksi demo. Ribbon Word: Microsoft.", 12.5, MUTED),
            txt("Artikel contoh: Effendy (2017); Safi'i dkk. (2023).", 12.5, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        close_credit.move_to([-6.0, -2.05, 0], aligned_edge=LEFT)
        close_footer = txt("09 / 09", 11, MUTED).to_corner(DR, buff=0.55)
        close = Group(
            close_title, close_sub, close_icon,
            close_credit, close_footer,
        )

        self.wait_until(self.cue("closing"))
        self.play(
            FadeOut(rail),
            FadeOut(head),
            FadeOut(sub),
            FadeOut(page),
            FadeOut(Group(*groups), shift=UP * 0.15),
            FadeIn(close, shift=UP * 0.1),
            run_time=0.8,
        )
