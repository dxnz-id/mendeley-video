from manim import *

BG = "#F6F6F6"
INK = "#2F3334"
MUTED = "#5B6061"
ACCENT = "#46627A"


def pixel_rect(image, box):
    """Map a pixel box on an ImageMobject to a Manim rectangle."""
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


class TestScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        step = Text("LANGKAH 1", font="Roboto", weight=BOLD, color=ACCENT, font_size=18)
        step.move_to([-5.2, 3.45, 0])
        title = Text("Impor referensi", font="Roboto", weight=BOLD, color=INK, font_size=42)
        title.next_to(step, DOWN, aligned_edge=LEFT, buff=0.12)
        self.add(step, title)

        img = ImageMobject("assets/shots/library_card.png")
        img.scale_to_fit_height(5.55)
        img.move_to(DOWN * 0.5)
        self.add(img)

        highlight = pixel_rect(img, (207, 192, 632, 260))
        self.play(Create(highlight), run_time=0.8)

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
        self.play(FadeIn(label_group, shift=LEFT * 0.1), run_time=0.5)
        self.wait(8.5)
