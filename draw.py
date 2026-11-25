#!/usr/bin/env python3
"""Draw entry.png: a newspaper-style front page of 2026-11-25 world news.

Pure PIL, deterministic: no network, no randomness, no clock reads.
Only the three system font files below are read.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

SERIF_BOLD = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
SERIF_REG = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"
SANS_REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_INDEX = 2  # Simplified Chinese face inside the TTC collections

W, H = 1024, 1024
PAPER = (247, 242, 231)   # #f7f2e7
INK = (26, 26, 26)        # #1a1a1a
RED = (176, 58, 46)       # #b03a2e
GREY = (110, 104, 92)
WHITE = (245, 242, 235)
LIGHT_RED = (232, 120, 100)

MARGIN = 36


def font(path, size):
    return ImageFont.truetype(path, size, index=FONT_INDEX)


def wrap(draw, text, fnt, max_width):
    """Wrap text by measured pixel width, character by character."""
    lines, cur = [], ""
    for ch in text:
        trial = cur + ch
        if ch in "。，、；：％%）":
            # closing punctuation never starts a new line
            cur = trial
        elif cur and draw.textlength(trial, font=fnt) > max_width:
            lines.append(cur)
            cur = ch
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def center(draw, text, fnt, y, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return w


# ---------------------------------------------------------------- pictograms
def pic_ship(d, x, y):
    # tanker hull + mast + waves + flame
    d.polygon([(x, y + 26), (x + 78, y + 26), (x + 66, y + 42), (x + 10, y + 42)],
              outline=INK, width=3)
    d.line([(x + 30, y + 26), (x + 30, y + 8), (x + 52, y + 8)], fill=INK, width=3)
    d.rectangle([x + 8, y + 18, x + 26, y + 26], outline=INK, width=3)
    for i in range(3):
        wx = x + i * 30
        d.arc([wx, y + 46, wx + 26, y + 60], 0, 180, fill=INK, width=3)
    d.polygon([(x + 62, y - 6), (x + 70, y + 8), (x + 78, y - 2),
               (x + 74, y + 14), (x + 66, y + 14), (x + 58, y + 6)], fill=RED)


def pic_drone_factory(d, x, y):
    # quadcopter drone above a factory, small flame
    cx, cy = x + 24, y + 12
    for dx, dy in ((-14, -8), (14, -8), (-14, 8), (14, 8)):
        d.ellipse([cx + dx - 6, cy + dy - 3, cx + dx + 6, cy + dy + 3],
                  outline=INK, width=2)
    d.rectangle([cx - 6, cy - 4, cx + 6, cy + 4], outline=INK, width=2)
    d.line([(cx, cy + 4), (cx, cy + 12)], fill=INK, width=2)
    fx = x + 52
    d.rectangle([fx, y + 34, fx + 52, y + 56], outline=INK, width=3)
    d.polygon([(fx + 4, y + 34), (fx + 14, y + 18), (fx + 14, y + 34)],
              outline=INK, width=3)
    d.rectangle([fx + 30, y + 12, fx + 38, y + 34], outline=INK, width=3)
    d.polygon([(fx + 40, y - 4), (fx + 45, y + 6), (fx + 50, y - 2),
               (fx + 47, y + 10), (fx + 41, y + 10)], fill=RED)


def pic_chart(d, x, y):
    # falling polyline with arrow head, axis
    d.line([(x, y + 4), (x, y + 52), (x + 92, y + 52)], fill=INK, width=3)
    pts = [(x + 6, y + 10), (x + 30, y + 22), (x + 48, y + 16), (x + 84, y + 44)]
    d.line(pts, fill=RED, width=4)
    d.polygon([(x + 84, y + 44), (x + 70, y + 42), (x + 82, y + 32)], fill=RED)


def pic_scales(d, x, y):
    # balance scales
    cx = x + 44
    d.line([(cx, y + 2), (cx, y + 50)], fill=INK, width=3)
    d.line([(x + 8, y + 10), (x + 80, y + 10)], fill=INK, width=3)
    d.ellipse([cx - 4, y - 2, cx + 4, y + 6], fill=INK)
    for px in (x + 8, x + 80):
        d.line([(px, y + 10), (px - 10, y + 32)], fill=INK, width=2)
        d.line([(px, y + 10), (px + 10, y + 32)], fill=INK, width=2)
        d.arc([px - 13, y + 22, px + 13, y + 40], 0, 180, fill=INK, width=3)
    d.line([(x + 28, y + 54), (x + 60, y + 54)], fill=INK, width=3)


def pic_rocket(d, x, y):
    # rocket with window and flame
    cx = x + 40
    d.polygon([(cx, y - 4), (cx + 13, y + 16), (cx + 13, y + 40),
               (cx - 13, y + 40), (cx - 13, y + 16)], outline=INK, width=3)
    d.ellipse([cx - 6, y + 14, cx + 6, y + 26], outline=INK, width=2)
    d.polygon([(cx - 13, y + 34), (cx - 24, y + 50), (cx - 13, y + 48)],
              outline=INK, width=3)
    d.polygon([(cx + 13, y + 34), (cx + 24, y + 50), (cx + 13, y + 48)],
              outline=INK, width=3)
    d.polygon([(cx - 5, y + 44), (cx, y + 60), (cx + 5, y + 44)], fill=RED)
    d.line([(x + 4, y + 52), (x + 16, y + 52)], fill=INK, width=2)
    d.line([(x + 66, y + 52), (x + 78, y + 52)], fill=INK, width=2)


def pic_tower(d, x, y):
    # tower block with windows and an impact star
    tx = x + 26
    d.rectangle([tx, y - 2, tx + 34, y + 56], outline=INK, width=3)
    for r in range(4):
        for c in range(2):
            d.rectangle([tx + 6 + c * 14, y + 6 + r * 12,
                         tx + 14 + c * 14, y + 13 + r * 12], fill=GREY)
    cx, cy = tx + 40, y + 10
    for a in range(0, 360, 45):
        x2 = cx + 13 * math.cos(math.radians(a))
        y2 = cy + 13 * math.sin(math.radians(a))
        d.line([(cx, cy), (x2, y2)], fill=RED, width=3)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)


PICTOGRAMS = [pic_ship, pic_drone_factory, pic_chart,
              pic_scales, pic_rocket, pic_tower]


NEWS = [
    ("海湾", "霍尔木兹两油轮触雷起火",
     "霍尔木兹海峡两艘油轮触雷起火，关键航道安全再引关注。"),
    ("战事", "乌无人机焚俄两座炼油厂",
     "乌克兰无人机夜袭俄罗斯境内两座炼油厂，引发大火。"),
    ("财经", "亚洲科技股大跌",
     "科技股领跌亚洲市场：韩国Kospi指数重挫6%，日经指数跌2.8%。"),
    ("司法", "美陪审团判华为罪名成立",
     "美国陪审团裁定华为银行欺诈、窃取商业机密罪名成立。"),
    ("航天", "神舟二十四对接天宫",
     "神舟二十四号飞船成功对接天宫空间站，巴基斯坦首位航天员随行。"),
    ("中东", "利雅得塔楼遇袭11伤",
     "沙特首都利雅得一座塔楼遭袭击，至少11人受伤。"),
]

BRIEFS = [
    "澳大利亚与所罗门群岛签署新条约",
    "哥伦比亚卡塔赫纳人质获释",
    "教皇批评COP31气候谈判陷僵局",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ------------------------------------------------------------- masthead
    f_mast = font(SERIF_BOLD, 56)
    center(d, "寰宇日报", f_mast, 22, INK)
    f_eng = font(SANS_REG, 15)
    eng = "T H E   G L O B A L   D A I L Y"
    ew = d.textlength(eng, font=f_eng)
    d.text(((W - ew) / 2, 88), eng, font=f_eng, fill=GREY)

    f_date = font(SERIF_BOLD, 30)
    date_main = "2026年11月25日 星期三"
    dw = d.textlength(date_main, font=f_date)
    f_date_small = font(SANS_REG, 16)
    date_small = "2026-11-25"
    sw = d.textlength(date_small, font=f_date_small)
    total = dw + 14 + sw
    x0 = (W - total) / 2
    d.text((x0, 112), date_main, font=f_date, fill=RED)
    d.text((x0 + dw + 14, 124), date_small, font=f_date_small, fill=INK)

    # double rule under the masthead
    d.line([(MARGIN, 156), (W - MARGIN, 156)], fill=INK, width=3)
    d.line([(MARGIN, 161), (W - MARGIN, 161)], fill=INK, width=1)

    # ------------------------------------------------------------- news grid
    grid_top = 176
    bar_top = H - 90
    grid_bottom = bar_top - 14
    col_w = (W - 2 * MARGIN - 16) / 2
    row_h = (grid_bottom - grid_top) / 3

    f_cat = font(SANS_REG, 18)
    f_title = font(SERIF_BOLD, 27)
    f_body = font(SANS_REG, 20)

    for i, (cat, title, body) in enumerate(NEWS):
        col, row = i % 2, i // 2
        cx = MARGIN + col * (col_w + 16)
        cy = grid_top + row * row_h
        inner_w = col_w - 28
        tx = cx + 14
        ty = cy + 12
        # category tag
        d.text((tx, ty), "【" + cat + "】", font=f_cat, fill=RED)
        # big index number, top right of the cell
        f_num = font(SERIF_BOLD, 30)
        num = str(i + 1)
        nw = d.textlength(num, font=f_num)
        d.text((cx + col_w - 14 - nw, ty - 4), num, font=f_num, fill=GREY)
        # title
        d.text((tx, ty + 30), title, font=f_title, fill=INK)
        # body, at most 3 lines
        lines = wrap(d, body, f_body, inner_w)[:3]
        for j, ln in enumerate(lines):
            d.text((tx, ty + 74 + j * 27), ln, font=f_body, fill=INK)
        # pictogram
        PICTOGRAMS[i](d, tx + 4, cy + row_h - 78)
        # separators
        if col == 0:
            d.line([(MARGIN + col_w + 8, cy + 8),
                    (MARGIN + col_w + 8, cy + row_h - 8)], fill=GREY, width=1)
        if row < 2:
            d.line([(cx + 6, cy + row_h - 4), (cx + col_w - 6, cy + row_h - 4)],
                   fill=GREY, width=1)

    # ------------------------------------------------------------- briefs bar
    d.rectangle([0, bar_top, W, H], fill=INK)
    f_tag = font(SERIF_BOLD, 22)
    d.text((MARGIN, bar_top + 31), "简讯", font=f_tag, fill=LIGHT_RED)
    f_brief = font(SANS_REG, 19)
    brief_text = "  •  ".join(BRIEFS)
    blines = wrap(d, brief_text, f_brief, W - 2 * MARGIN - 76)[:2]
    brief_y = bar_top + (90 - len(blines) * 28) // 2 + 2
    for j, ln in enumerate(blines):
        d.text((MARGIN + 76, brief_y + j * 28), ln, font=f_brief, fill=WHITE)
    # thin red rule on top of the bar
    d.line([(0, bar_top), (W, bar_top)], fill=RED, width=3)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG")
    print(out)


if __name__ == "__main__":
    main()
