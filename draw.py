"""Build-time generator for entry.png (run locally, NOT in the judging sandbox).

Deterministically draws a 1024x1024 newspaper-style summary of the world
news of Wednesday 25 November 2026 and saves it as entry.png next to this
file. No randomness, no timestamps, no text metadata in the PNG.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = "#f7f3ea"
INK = "#1a1a1a"
RED = "#8b1a1a"
GREY = "#6b6b6b"
BAR_BG = "#2b2b2b"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return y


def wrap(draw, text, fnt, max_width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines[:3]


ITEMS = [
    ("#8b1a1a", "STRAIT OF HORMUZ", "Two oil tankers hit naval mines and catch fire"),
    ("#1a4a8b", "UKRAINE WAR", "Ukrainian drones set two Russian refineries ablaze"),
    ("#1a6b3c", "MARKETS", "Asia tech stocks plunge: Kospi -6%, Nikkei -2.8%"),
    ("#5b2a86", "NEW YORK", "Jury convicts Huawei of bank fraud, theft"),
    ("#10304f", "SPACE", "Shenzhou-24 docks: Pakistan's first astronaut"),
    ("#0f766e", "PACIFIC", "Australia-Solomon Islands treaty bars foreign bases"),
]


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # --- Header ---
    f_kicker = font(SANS, 32)
    kicker = "T H E   W O R L D   I N   O N E   D A Y"
    centered(draw, 36, kicker, f_kicker, INK)

    f_title = font(SERIF, 44)
    centered(draw, 84, "WEDNESDAY 25 NOVEMBER 2026", f_title, INK)

    draw.rectangle([48, 168, W - 48, 174], fill=RED)

    # --- News grid: 2 columns x 3 rows ---
    margin = 48
    gap_x = 24
    gap_y = 20
    grid_top = 196
    grid_bottom = 836
    cell_w = (W - 2 * margin - gap_x) // 2
    cell_h = (grid_bottom - grid_top - 2 * gap_y) // 3

    f_label = font(SANS, 30)
    f_head = font(SERIF, 40)
    label_h = 44
    pad = 14
    line_h = 50

    for idx, (color, region, headline) in enumerate(ITEMS):
        col = idx % 2
        row = idx // 2
        x0 = margin + col * (cell_w + gap_x)
        y0 = grid_top + row * (cell_h + gap_y)
        x1 = x0 + cell_w
        # label bar
        draw.rectangle([x0, y0, x1, y0 + label_h], fill=color)
        draw.text((x0 + pad, y0 + 6), region, font=f_label, fill="#ffffff")
        # headline, wrapped to cell width
        lines = wrap(draw, headline, f_head, cell_w - 2 * pad)
        ty = y0 + label_h + 12
        for line in lines:
            draw.text((x0 + pad, ty), line, font=f_head, fill=INK)
            ty += line_h

    # --- Bottom bar ---
    bar_top = 852
    bar_bottom = 952
    draw.rectangle([0, bar_top, W, bar_bottom], fill=BAR_BG)
    f_bar = font(SANS, 27)
    centered(draw, bar_top + 14, "ALSO TODAY: Riyadh tower attack injures 11", f_bar, "#ffffff")
    centered(draw, bar_top + 54, "Hostages freed in Cartagena - Pope faults COP31 deadlock", f_bar, "#ffffff")

    # --- Footer ---
    f_foot = font(SANS, 24)
    centered(draw, 968, "25 NOVEMBER 2026 - ONE DAY, ONE PICTURE", f_foot, GREY)

    out_path = __file__.rsplit("/", 1)[0] + "/entry.png"
    img.save(out_path)


if __name__ == "__main__":
    main()
