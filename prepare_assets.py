from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

RAW = Path("assets/raw")
SHOTS = Path("assets/shots")
SHOTS.mkdir(parents=True, exist_ok=True)


def card(src, out, crop, radius=26, pad=52, max_width=None, inner_pad=0, bg=(255, 255, 255, 255)):
    im = Image.open(src).convert("RGBA").crop(crop)
    if max_width and im.width > max_width:
        im = im.resize((max_width, round(im.height * max_width / im.width)), Image.LANCZOS)

    if inner_pad:
        padded = Image.new("RGBA", (im.width + 2 * inner_pad, im.height + 2 * inner_pad), bg)
        padded.alpha_composite(im, (inner_pad, inner_pad))
        im = padded

    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.width, im.height], radius=radius, fill=255)
    im.putalpha(mask)

    canvas = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)
    draw.rounded_rectangle(
        [pad - 8, pad - 2, pad + im.width + 8, pad + im.height + 18],
        radius=radius + 8,
        fill=(0, 0, 0, 70),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    canvas.alpha_composite(shadow)
    canvas.alpha_composite(im, (pad, pad))
    canvas.save(SHOTS / out)
    print(out, canvas.size)


card(RAW / "get-your-library.png", "library_card.png", (162, 150, 1311, 1011))
card(RAW / "get-your-library.png", "library_list_card.png", (810, 235, 1305, 1005), inner_pad=12, bg=(242, 242, 242, 255))
card(RAW / "web_importer.484c7d40.png", "web_importer_card.png", (345, 387, 2801, 2079), max_width=1600)
card(RAW / "cite_desktop.5a079955.png", "cite_panel_card.png", (800, 97, 1489, 1069), max_width=700, inner_pad=18)
card(RAW / "cite_desktop.5a079955.png", "cite_card.png", (192, 99, 1489, 1069), max_width=1400)
