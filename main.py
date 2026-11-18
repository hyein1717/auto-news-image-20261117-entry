"""news-image-20261117: one image summing up the world news of
Tuesday 17 November 2026.

Deterministic, stdlib-only except Pillow for the image work. The program
composes a newspaper front page (1024x1024) from the shipped hero photo
plus crisp typeset text (fonts are shipped in assets/fonts, so the render
is identical in any container), then applies the playbook post-processing:
resize 1024x1024 LANCZOS, Sharpness 1.18, Contrast 1.08, save PNG.

If Pillow is absent, it falls back to copying the pre-rendered page
(assets/page.png), which is the same composition rendered in advance.
Either path writes byte-identical output on every run.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SIZE = 1024

# Colours: deep navy front page, red masthead accent, warm gold subline.
NAVY = (11, 21, 38)
PANEL = (16, 30, 52)
RED = (200, 16, 46)
GOLD = (232, 184, 75)
WHITE = (245, 247, 250)
GREY = (201, 212, 227)
FAINT = (148, 163, 184)
LINE = (30, 46, 69)

DATE = "17 NOVEMBER 2026"
SUBLINE = "TUESDAY  ·  THE WORLD IN ONE DAY"
CAPTION = "KERCH BRIDGE, CRIMEA — A ROAD SPAN COLLAPSED AFTER A SECOND DAY OF STRIKES"

# Five stories, chosen for consequence and breadth across regions/fields.
# Every line is factual as reported on 17 November 2026; no speculation.
STORIES = [
    ("KERCH BRIDGE HIT",
     "Ukraine strikes Crimea bridge a second day; a road span collapses."),
    ("GULF ON EDGE",
     "Tanker hits a mine near Hormuz; Iranian drones fired at a US radar site in Bahrain."),
    ("ASEAN IN MANILA",
     "Trump lands for summit; Xi-Trump-Putin to meet Thursday in Shenzhen."),
    ("VULCAN ROCKET LOST",
     "ULA launch fails; 40 Amazon internet satellites destroyed."),
    ("NVIDIA REPORTS",
     "First earnings since Jensen Huang stepped down."),
]

FOOTER = ("ALSO: JPMORGAN BLAMES A SOFTWARE BUG FOR BANK GLITCH  ·  "
          "UK SANCTIONS 8 FIRMS OVER WEST BANK SETTLEMENTS")


def _font(name, size):
    """Load a shipped font; fall back to Pillow's default bitmap font."""
    from PIL import ImageFont
    path = os.path.join(HERE, "assets", "fonts", name)
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def _fit(draw, text, font_path, start, minimum, max_width):
    """Largest font size from start down to minimum that fits max_width."""
    from PIL import ImageFont
    size = start
    while size > minimum:
        font = ImageFont.truetype(
            os.path.join(HERE, "assets", "fonts", font_path), size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 1
    return ImageFont.truetype(
        os.path.join(HERE, "assets", "fonts", font_path), minimum)


def _text_center(draw, y, text, font, fill):
    draw.text((SIZE / 2, y), text, font=font, fill=fill, anchor="ma")


def compose():
    from PIL import Image, ImageDraw, ImageEnhance, ImageOps

    page = Image.new("RGB", (SIZE, SIZE), NAVY)
    draw = ImageDraw.Draw(page)

    # --- Masthead -------------------------------------------------------
    draw.rectangle([0, 0, SIZE, 10], fill=RED)
    date_font = _fit(draw, DATE, "DejaVuSans-Bold.ttf", 92, 60, SIZE - 60)
    _text_center(draw, 26, DATE, date_font, WHITE)
    sub_font = _font("DejaVuSans.ttf", 30)
    _text_center(draw, 128, SUBLINE, sub_font, GOLD)
    draw.line([40, 172, SIZE - 40, 172], fill=LINE, width=2)
    draw.line([SIZE / 2 - 90, 166, SIZE / 2 + 90, 166], fill=GOLD, width=3)

    # --- Hero photo -----------------------------------------------------
    hero = Image.open(os.path.join(HERE, "assets", "hero.jpg")).convert("RGB")
    hero = ImageOps.fit(hero, (SIZE, 380), Image.LANCZOS)
    page.paste(hero, (0, 174))
    # Caption strip over the hero's bottom edge.
    strip = Image.new("RGBA", (SIZE, 44), (5, 10, 20, 205))
    page.paste(strip, (0, 510), strip)
    cap_draw = ImageDraw.Draw(page)
    cap_font = _fit(cap_draw, CAPTION, "DejaVuSans-Bold.ttf", 24, 16, SIZE - 48)
    cap_draw.text((24, 521), CAPTION, font=cap_font, fill=WHITE)

    # --- Story rows -----------------------------------------------------
    y = 566
    row_h = 82
    for i, (head, sub) in enumerate(STORIES):
        # Red number chip.
        cx, cy = 66, y + 36
        draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=RED)
        num_font = _font("DejaVuSans-Bold.ttf", 28)
        draw.text((cx, cy), str(i + 1), font=num_font, fill=WHITE,
                  anchor="mm")
        head_font = _fit(draw, head, "DejaVuSans-Bold.ttf", 36, 24, SIZE - 150)
        draw.text((112, y + 2), head, font=head_font, fill=WHITE)
        sub_font = _fit(draw, sub, "DejaVuSans.ttf", 24, 17, SIZE - 150)
        draw.text((112, y + 44), sub, font=sub_font, fill=GREY)
        if i < len(STORIES) - 1:
            draw.line([112, y + row_h - 6, SIZE - 40, y + row_h - 6],
                      fill=LINE, width=1)
        y += row_h

    # --- Footer ---------------------------------------------------------
    foot_font = _fit(draw, FOOTER, "DejaVuSans.ttf", 19, 14, SIZE - 60)
    _text_center(draw, 984, FOOTER, foot_font, FAINT)

    # --- Playbook post-processing ---------------------------------------
    page = page.resize((SIZE, SIZE), Image.LANCZOS)
    page = ImageEnhance.Sharpness(page).enhance(1.18)
    page = ImageEnhance.Contrast(page).enhance(1.08)
    return page


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    try:
        import PIL  # noqa: F401  (presence check only)
        page = compose()
        page.save(out_path, format="PNG", optimize=False)
    except ImportError:
        # No Pillow in this container: copy the pre-rendered page.
        shutil.copyfile(os.path.join(HERE, "assets", "page.png"), out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
