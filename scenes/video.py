from pathlib import Path
import json

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
        self.add(step_header("Langkah 1", "Impor referensi"))

        img = image("assets/shots/library_card.png", 5.4)
        img.move_to([-3.05, -0.7, 0])
        self.add(img)

        panel = card(4.35, 5.4, fill=WHITE)
        panel.move_to([4.35, -0.7, 0])
        self.add(panel)

        p_title = txt("Langkah impor", 16, INK, BOLD)
        p_title.move_to(panel.get_corner(UL) + RIGHT * 1.6 + DOWN * 0.4)
        self.add(p_title)

        labels = [
            "Add reference",
            "Import file(s)",
            "Import folder",
            "Set up watched folder",
        ]
        rows = []
        for i, label in enumerate(labels):
            bg = RoundedRectangle(
                corner_radius=0.1, width=3.85, height=0.5,
                fill_color=ACCENT_LIGHT, fill_opacity=0, stroke_width=0,
            )
            num = Circle(radius=0.17, fill_color=WHITE, fill_opacity=1, stroke_color=BORDER, stroke_width=2)
            num.move_to(bg.get_left() + RIGHT * 0.35)
            num_t = txt(str(i + 1), 11, MUTED, BOLD).move_to(num)
            t = txt(label, 12, INK)
            t.next_to(num, RIGHT, buff=0.18)
            row = VGroup(bg, num, num_t, t)
            row.move_to([4.35, 1.0 - i * 0.74, 0])
            rows.append(row)
            self.add(row)

        status_check = check_mark(0.13)
        status_text = txt("Referensi masuk ke Library", 11, GREEN, BOLD)
        status = VGroup(status_check, status_text)
        status_check.move_to(LEFT * 1.55)
        status_text.next_to(status_check, RIGHT, buff=0.12)
        status.move_to([4.35, -1.95, 0])
        status.set_opacity(0)
        self.add(status)

        targets = {
            "add": (195, 78, 475, 150),
            "import_file": (218, 170, 650, 248),
            "import_folder": (218, 275, 650, 355),
            "watched": (218, 465, 650, 545),
            "library": (680, 200, 1200, 850),
        }
        highlight = pixel_rect(img, targets["add"])
        self.wait_until(self.cue("add"))
        self.play(Create(highlight), run_time=0.4)

        for i, key in enumerate(["add", "import_file", "import_folder", "watched"]):
            if i > 0:
                self.wait_until(self.cue(key))
                new_rect = pixel_rect(img, targets[key])
                self.play(Transform(highlight, new_rect), run_time=0.45)
            if i > 0:
                prev = rows[i - 1]
                prev[0].set_fill(ACCENT_LIGHT, 0)
                prev[1].set_fill(GREEN).set_stroke(GREEN)
                prev[2].set_opacity(0)
                check = check_mark(0.13)
                check.move_to(prev[1].get_center())
                self.add(check)
            active = rows[i]
            self.play(
                active[0].animate.set_fill(ACCENT_LIGHT, 0.8),
                active[1].animate.set_fill(ACCENT).set_stroke(ACCENT),
                active[2].animate.set_color(WHITE),
                run_time=0.25,
            )

        self.wait_until(self.cue("library"))
        new_rect = pixel_rect(img, targets["library"])
        self.play(
            Transform(highlight, new_rect),
            status.animate.set_opacity(1),
            run_time=0.5,
        )


class Scene05(VideoScene):
    scene_id = "Scene05"

    def build(self):
        self.add(step_header("Langkah 2", "Cek metadata"))

        list_panel = card(3.7, 5.2, fill=WHITE)
        list_panel.move_to([-4.55, -0.7, 0])
        self.add(list_panel)

        lx = list_panel.get_left()[0]
        ly = list_panel.get_top()[1]
        for label, x in [("AUTHORS", lx + 0.16), ("YEAR", lx + 1.82), ("TITLE", lx + 2.42)]:
            h = txt(label, 7.5, MUTED, BOLD)
            h.move_to([x, ly - 0.26, 0], aligned_edge=LEFT)
            self.add(h)
        header_rule = Line(LEFT, RIGHT, color=BORDER, stroke_width=1).set_width(3.4)
        header_rule.move_to([list_panel.get_center()[0], ly - 0.42, 0])
        self.add(header_rule)

        refs = [
            ("Effendy, M. H.", "2017", "Interferensi..."),
            ("Safi'i, I., dkk.", "2023", "Struktur teks..."),
            ("Agrawal, S.", "2022", "Visual perception"),
            ("Bennett, K.", "2015", "A young..."),
            ("Banati, P.", "2021", "Addiction..."),
            ("Biddle, S. J. H.", "2019", "Physiology..."),
            ("Bjørn, L.", "2017", "Gene..."),
            ("Boelens, M.", "2022", "Impact..."),
        ]
        for i, (author, year, title) in enumerate(refs):
            y = ly - 0.72 - i * 0.53
            if i == 0:
                bg = RoundedRectangle(
                    corner_radius=0.05, width=3.35, height=0.45,
                    fill_color=ACCENT_LIGHT, fill_opacity=1, stroke_width=0,
                )
                bg.move_to([list_panel.get_center()[0], y, 0])
                self.add(bg)
            color = ACCENT if i == 0 else INK
            weight = BOLD if i == 0 else NORMAL
            a = txt(author, 7.5, color, weight)
            a.move_to([lx + 0.16, y, 0], aligned_edge=LEFT)
            yr = txt(year, 7.5, ACCENT if i == 0 else MUTED)
            yr.move_to([lx + 1.82, y, 0], aligned_edge=LEFT)
            ti = txt(title, 7.0, ACCENT if i == 0 else MUTED, weight)
            ti.move_to([lx + 2.42, y, 0], aligned_edge=LEFT)
            self.add(a, yr, ti)

        panel = card(7.0, 5.2, fill=WHITE)
        panel.move_to([2.35, -0.7, 0])
        self.add(panel)

        title = txt("Detail referensi", 17, INK, BOLD)
        title.move_to(panel.get_corner(UL) + RIGHT * 1.55 + DOWN * 0.25)
        self.add(title)
        badge = check_mark(0.16)
        badge.move_to(panel.get_corner(UR) + LEFT * 0.35 + DOWN * 0.35)
        badge.set_opacity(0)
        self.add(badge)

        left = panel.get_left()[0] + 0.45

        fields = []
        def add_field(label, value, y, height=0.58, value_size=12.5):
            lb = txt(label, 9, MUTED, BOLD)
            vl = txt(value, value_size, INK)
            place_tl(lb, left, y)
            place_tl(vl, left, y - 0.22)
            bg = RoundedRectangle(
                corner_radius=0.08, width=6.1, height=height,
                fill_color=ACCENT_LIGHT, fill_opacity=0, stroke_width=0,
            )
            bg.move_to([panel.get_center()[0], (y + y - 0.22 - vl.height / 2) / 2, 0])
            bg.shift(UP * 0.06)
            group = VGroup(bg, lb, vl)
            self.add(group)
            fields.append((group, bg))
            return group

        add_field("JUDUL", "Interferensi gramatikal bahasa Madura\nke dalam bahasa Indonesia", 1.1, 0.9, 11.5)
        add_field("PENULIS", "Moh. Hafid Effendy", 0.05)
        add_field("TAHUN", "2017", -0.6)
        add_field("DOI", "10.15408/dialektika.v4i1.6997", -1.25)
        add_field("JENIS", "Jurnal", -1.9)

        note_box = RoundedRectangle(
            corner_radius=0.1, width=6.1, height=0.65,
            fill_color=WARM_BG, fill_opacity=1, stroke_width=0,
        )
        note_text = txt("Metadata PDF lama sering tidak lengkap.", 10.5, WARM_INK, BOLD)
        note = VGroup(note_box, note_text)
        note_text.move_to(note_box.get_center())
        note.move_to([panel.get_center()[0], -2.8, 0])
        note.set_opacity(0)
        self.add(note)

        chip1 = chip("Folder: Bab 2")
        chip2 = chip("Tag: metodologi")
        chips = VGroup(chip1, chip2).arrange(RIGHT, buff=0.2)
        chips.move_to([panel.get_center()[0], -2.8, 0])
        chips.set_opacity(0)
        self.add(chips)

        for key, (group, bg) in zip(["title", "authors", "year", "doi"], fields):
            self.wait_until(self.cue(key))
            self.play(bg.animate.set_fill(ACCENT_LIGHT, 0.85), run_time=0.3)

        self.play(badge.animate.set_opacity(1), run_time=0.3)

        self.wait_until(12.0)
        self.play(note.animate.set_opacity(1), run_time=0.4)

        self.wait_until(self.cue("folder"))
        self.play(
            note.animate.set_opacity(0),
            chip1.animate.set_opacity(1),
            run_time=0.4,
        )
        self.wait_until(self.cue("tag"))
        self.play(chip2.animate.set_opacity(1), run_time=0.4)


class Scene06(VideoScene):
    scene_id = "Scene06"

    def build(self):
        head = step_header("Langkah 3", "Web Importer")
        sub = txt("Simpan referensi langsung dari halaman web.", 15, MUTED)
        sub.next_to(head, DOWN, aligned_edge=LEFT, buff=0.15)
        self.add(head, sub)

        img = image("assets/shots/web_importer_card.png", 5.3)
        img.move_to([0, -0.75, 0])
        self.add(img)

        add_rect = pixel_rect(img, (1490, 100, 1600, 165))
        row_rect = pixel_rect(img, (965, 270, 1615, 450))

        highlight = pixel_rect(img, (950, 50, 1625, 200), stroke_width=3)
        self.wait_until(self.cue("importer"))
        self.play(Create(highlight), run_time=0.45)

        self.wait_until(self.cue("add"))
        label_add = pill("Klik Add", size=15)
        label_add.next_to(add_rect, DOWN, buff=0.15)
        self.play(
            Transform(highlight, add_rect),
            FadeIn(label_add, shift=DOWN * 0.08),
            run_time=0.45,
        )

        self.wait_until(self.cue("library"))
        label_lib = pill("Masuk ke Library", size=15)
        label_lib.next_to(row_rect, LEFT, buff=0.15)
        self.play(
            Transform(highlight, row_rect),
            FadeOut(label_add),
            FadeIn(label_lib, shift=RIGHT * 0.08),
            run_time=0.45,
        )


class Scene07(VideoScene):
    scene_id = "Scene07"

    def build(self):
        head = step_header("Langkah 4", "Sitasi di Word")
        sub = txt("Gunakan add-in Mendeley Cite di Microsoft Word.", 15, MUTED)
        sub.next_to(head, DOWN, aligned_edge=LEFT, buff=0.15)
        self.add(head, sub)

        page_shell, page = make_page(6.3, 5.6)
        page_shell.move_to([-2.75, -0.95, 0])
        panel_img = image("assets/shots/cite_panel_card.png", 5.6)
        panel_img.move_to([4.2, -0.95, 0])
        self.add(page_shell, panel_img)

        content = document_content(page)
        self.add(content)
        cursor = content[-2]
        citation = content[-1]

        panel_border = SurroundingRectangle(panel_img, color=ACCENT, buff=0.04, stroke_width=3)
        self.wait_until(self.cue("panel"))
        self.play(Create(panel_border), run_time=0.35)
        self.play(FadeOut(panel_border), run_time=0.35)

        search_rect = pixel_rect(panel_img, (105, 340, 700, 415))
        row_rect = pixel_rect(panel_img, (105, 470, 700, 700))
        insert_rect = pixel_rect(panel_img, (160, 650, 335, 695))
        settings_rect = pixel_rect(panel_img, (280, 150, 515, 205))

        highlight = search_rect
        self.wait_until(self.cue("search"))
        self.play(Create(highlight), run_time=0.4)

        self.wait_until(self.cue("select"))
        self.play(Transform(highlight, row_rect), run_time=0.4)

        self.wait_until(self.cue("insert"))
        self.play(Transform(highlight, insert_rect), run_time=0.4)

        self.wait_until(self.cue("appears"))
        glow = SurroundingRectangle(citation, color=YELLOW, buff=0.04, fill_opacity=0.25, stroke_width=0)
        citation.set_z_index(1)
        glow.set_z_index(0.5)
        self.play(
            citation.animate.set_opacity(1),
            FadeOut(cursor),
            FadeIn(glow),
            run_time=0.5,
        )

        self.wait_until(self.cue("settings"))
        self.play(Transform(highlight, settings_rect), run_time=0.4)

        self.wait_until(self.cue("apa"))
        apa = pill("APA 7", size=15)
        apa.next_to(settings_rect, DOWN, buff=0.28)
        self.play(FadeIn(apa, shift=UP * 0.08), run_time=0.4)

        second = VGroup(
            txt("Interferensi juga muncul pada teks iklan", 10.5, INK),
            txt("(Safi'i dkk., 2023).", 10.5, ACCENT, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        second.move_to([page.get_left()[0] + 0.4 + second.width / 2, page.get_bottom()[1] + 0.85, 0])
        second.set_opacity(0)
        self.add(second)
        self.wait_until(self.cue("apa") + 7.0)
        self.play(second.animate.set_opacity(1), run_time=0.5)


class Scene08(VideoScene):
    scene_id = "Scene08"

    def build(self):
        head = step_header("Langkah 5", "Daftar pustaka")
        sub = txt("Mendeley menyusun entri dari kutipan yang sudah masuk.", 15, MUTED)
        sub.next_to(head, DOWN, aligned_edge=LEFT, buff=0.15)
        self.add(head, sub)

        page_shell, page = make_page(6.3, 5.6)
        page_shell.move_to([-2.75, -0.95, 0])
        panel_img = image("assets/shots/cite_panel_card.png", 5.6)
        panel_img.move_to([4.2, -0.95, 0])
        self.add(page_shell, panel_img)

        doc = document_content(page)
        doc[-1].set_opacity(1)
        doc[-2].set_opacity(0)
        self.add(doc)

        more_btn = RoundedRectangle(
            corner_radius=0.08, width=3.8, height=0.38,
            fill_color="#F4F5F5", fill_opacity=1, stroke_color=BORDER, stroke_width=1,
        )
        more_btn.move_to([panel_img.get_center()[0], panel_img.get_bottom()[1] + 0.38, 0])
        more_label = txt("More", 10, ACCENT, BOLD).move_to(more_btn.get_center())
        self.add(more_btn, more_label)

        menu = card(3.0, 1.7, fill=WHITE)
        menu.move_to([panel_img.get_center()[0], panel_img.get_bottom()[1] + 1.5, 0])
        insert_bg = RoundedRectangle(
            corner_radius=0.06, width=2.8, height=0.42,
            fill_color=ACCENT_LIGHT, fill_opacity=0, stroke_width=0,
        )
        insert_bg.move_to(menu.get_top() + DOWN * 0.42)
        insert_t = txt("Insert Bibliography", 9.5, ACCENT, BOLD).move_to(insert_bg.get_center())
        export_t = txt("Export", 9.5, MUTED).move_to(insert_bg.get_center() + DOWN * 0.5)
        refresh_t = txt("Refresh", 9.5, MUTED).move_to(insert_bg.get_center() + DOWN * 1.0)
        menu_group = VGroup(menu, insert_bg, insert_t, export_t, refresh_t)
        menu_group.set_opacity(0)
        self.add(menu_group)

        self.wait_until(self.cue("more"))
        self.play(menu_group.animate.set_opacity(1), run_time=0.4)

        self.wait_until(self.cue("insert_bib"))
        self.play(insert_bg.animate.set_fill(ACCENT_LIGHT, 0.9), run_time=0.3)

        bib = bibliography_content(page)
        bib.set_opacity(0)
        self.add(bib)
        self.play(
            FadeOut(doc, shift=UP * 0.05),
            bib[0:2].animate.set_opacity(1),
            run_time=0.8,
        )

        self.wait_until(self.cue("entries"))
        self.play(bib[2].animate.set_opacity(1), run_time=0.4)
        self.wait(0.3)
        self.play(bib[3].animate.set_opacity(1), run_time=0.4)

        self.wait_until(self.cue("refresh"))
        refresh_bg = RoundedRectangle(
            corner_radius=0.06, width=2.8, height=0.42,
            fill_color=ACCENT_LIGHT, fill_opacity=0, stroke_width=0,
        )
        refresh_bg.move_to(refresh_t.get_center())
        self.add(refresh_bg)
        self.bring_to_front(refresh_t)
        updated = VGroup(check_mark(0.12), txt("Daftar diperbarui", 9.5, GREEN, BOLD))
        updated[1].next_to(updated[0], RIGHT, buff=0.1)
        updated.move_to([page.get_right()[0] - 1.0, page.get_top()[1] - 0.72, 0])
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
