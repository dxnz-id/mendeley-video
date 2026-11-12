"""Render the demo app screens at 2x and extract element boxes for Manim."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
UI = ROOT / "assets" / "ui"
HTML = UI / "ui.html"
CHROME = "chromium-browser"
SCREENS = [
    "library_import",
    "library_detail",
    "web_importer",
    "cite_word",
    "cite_settings",
    "cite_menu",
    "cite_bib",
]


def run(args: list[str]) -> str:
    return subprocess.run(args, check=True, text=True, capture_output=True).stdout


def main() -> None:
    boxes = {}
    for screen in SCREENS:
        url = f"file://{HTML}?screen={screen}"
        png = UI / f"{screen}.png"
        run([
            CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
            "--hide-scrollbars", "--disable-dev-shm-usage",
            "--force-device-scale-factor=2", "--window-size=1920,1080",
            f"--screenshot={png}", url,
        ])
        dom = run([
            CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
            "--disable-dev-shm-usage", "--dump-dom", url,
        ])
        m = re.search(
            r'<script type="application/json" id="boxes">(.*?)</script>',
            dom,
            re.S,
        )
        if not m:
            raise RuntimeError(f"boxes not found for {screen}")
        boxes[screen] = json.loads(m.group(1))
        print(screen, png.stat().st_size // 1024, "KB", len(boxes[screen]), "boxes")
    (UI / "boxes.json").write_text(json.dumps(boxes, indent=2) + "\n")
    print("Wrote", UI / "boxes.json")


if __name__ == "__main__":
    main()
