#!/usr/bin/env python3
"""news-image-20261119 v20: 36 stories, newspaper front page after the top 1.
Draws entry.png (1024x1024, deterministic) from world.geo.json only.
v17 vs v16: user order 2026-11-20 15:58 WIB ("Buat sama seperti sebelumnya,
tapi jarak antara garis dan text sama, kemudian untuk text di dalam kotak yang
biru dari angka 1-14 itu harus berada di tengah-tengah kotak, jangan terlalu
bawah begitu. Dan setiap garis atau kotak yang kamu buat, harus ada jarak,
biar teks terlihat jelas"):
  - Masthead rule gaps equalised (pixel-measured: v16 line touched the right
    kicker — its glyphs ended at y 19, the line was at 19; left gap 2px,
    below 7px). Both kickers now y=1 (glyphs 5..15), line y=20, title drawn
    at y=13 (glyphs 25..80): 5px above the line, 5px below it.
  - Blue kicker strips (heroes 1-3 + smalls 4-13): text was 2.5px below
    centre (pixel-measured hero strip: glyphs 284..291 in strip 277..293).
    All strip text now centred on the glyph centre: heroes kicker/source
    hy+97, pill text hy+98 (pill rect already centred); smalls kicker cy+84,
    pill rect cy+86..96, pill text cy+85.
  - Every line/box now has clear distance: deck glyphs end y 105, so the
    gold rule moves 103 -> 108 (3px gap); timeline red box enlarged 28 ->
    32px tall because "BY HOURS" glyphs overflowed its bottom by ~3px
    (white pixels at rows 178/180); stats dividers extended to 148 so the
    captions do not pass them; DATE CHECK text moved to dy+1 (gaps 5 top /
    3 bottom). All bands below shift +5 (gold rule) and the timeline
    enlargement pushes heroes onward +5 more: stats 110, timeline 154,
    heroes 191, smalls 379, map 711, date check 963, footer 997, ending
    ~1020.
v18 vs v17: user order 2026-11-20 16:04 WIB ("Okey bagus, untuk kotak garis
merah bawah masih blm berjarak bagus tuh") — the bottom spacing of the two
red boxes was still unbalanced (pixel-measured v17): timeline box "THE DAY"
glyphs 160..168 / "BY HOURS" 174..182 in box 154..186 = 6px top / 4px
bottom; DATE CHECK glyphs 968..976 / 980..988 in box 963..991 = 5px top /
3px bottom. Both texts moved up 1px: timeline "THE DAY" 156 -> 155,
"BY HOURS" 170 -> 169 (gaps 5/5); DATE CHECK lines dy+1 -> dy+0 and
dy+13 -> dy+12 (gaps 4/4). No band shifts.
v19 vs v18: user order 2026-11-20 16:06 WIB ("Bagus, untuk Thursday masih
terlihat berjarak per huruf, coba buat seperti top 1") — the v16 letter-
spacing is gone: title back to natural untracked LiberationSerif-Bold
(Times, same face as top 1) at 68px, which measures 839.3px wide — the same
width as the tracked 60px, so the width is unchanged but the letters now sit
naturally. draw_tracked helper removed. 68px glyphs are 61px tall (vs 55),
so the deck moves 83 -> 84 (glyphs 89..106, 3px below the title) and the
gold rule 108 -> 109; every band below shifts +1 (stats 111, timeline 155,
heroes 192, smalls 380, map 712, date check 964, footer 998, ending ~1021).
v20 vs v19: user order 2026-11-20 16:10 WIB — (a) numbering 1-36 gets a
period ("1. SHENZHEN", "14. Gaza"): heroes/smalls kicker format "%d. %s" and
also-list "%d." (measured: "36." is 15.7px in F_ALSO_N, text at x+20 still
clears it by 4px; longest kicker "9. COPENHAGEN · SECURITY" is 136px, 8px
clear of the source). Map pins 1-13 stay bare numbers inside their circles.
(b) art upgrade via 100milionseek (DeepSeek deepseek-v4.1-flash-free,
~/workspace/makefun/news-image-20261119-scratch/v20/ask_ds.py): 4 calls —
heroes (2500 tok, truncated after ICJ), COP31+smalls (truncated after COP31),
smalls 4-8 and 9-13 (both complete). Lessons: first call timed out at 120s
(long prompt) — shorten the prompt + raise timeout to 180s; jev-1.13-free
returns HTTP 400 (do not use); the reasoning model returns empty content when
the cap is spent on reasoning — ask_ds.py recovers reasoning_content, and
short prompts + max_tokens 1500-2500 answer directly. Implemented, scene
only (in-art big/small text still via art_text/focal_text overlays):
summit +3 flags + gold nameplates + gold table edge; ICJ 15 columns 9 paper
+ 6 ink = the 9-6 vote + Myanmar flag + star; COP31 hourglass left + globe
right + thermometer; GTA sun right + gold clock top-left + PS5 box + queue
right; ANTHROPIC paper + navy grid + gold stair-step + red arrowhead + navy
ticker strip; AKVAN spiral left + ink eye + red warning triangle; KERCH gold
deck with gap + red sagging span + 3 smoke ellipses; HAN navy + gold gavel +
yellow scales (courthouse removed, same motif as ICJ); GREENLAND navy sea +
paper berg + 2 flags on one gold pole; RIYADH red interceptor trail + gold
burst + city dots; COLOMBIA 3 paper placards; AUSTRALIA 4 navy bars + red
arrow (gauge removed); MARATHON gold medal + red circle-slash (finish post
removed).
NOTE: the first draw.py run right after an edit can render the pre-edit file
(sizes matched the previous version in v15/v16/v18) — always verify with 2-3
runs and take the later sha.
Run: python3 draw.py  -> writes entry.png in this directory."""
import json
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (250, 246, 235)
INK = (17, 17, 17)
NAVY = (16, 62, 150)
RED = (220, 28, 60)
GOLD = (232, 178, 36)
YELLOW = (255, 210, 31)
GREY = (90, 90, 90)
RULE = (180, 170, 150)
OCEAN = (198, 226, 240)
SAND = (238, 220, 165)

FD = "/usr/share/fonts/truetype/dejavu"
FNOTO = "/usr/share/fonts/truetype/noto"
FLIB = "/usr/share/fonts/truetype/liberation"


def font(name, size, base=FD):
    return ImageFont.truetype(os.path.join(base, name), size)


F_TITLE = font("LiberationSerif-Bold.ttf", 68, FLIB)
F_EYE = font("NotoSans-Black.ttf", 13, FNOTO)
F_DECKLINE = font("NotoSerif-Italic.ttf", 16, FNOTO)
F_DATE = font("NotoSans-Black.ttf", 30, FNOTO)
F_DATE2 = font("NotoSans-Bold.ttf", 11, FNOTO)
F_TTIME = font("NotoSans-Bold.ttf", 12, FNOTO)
F_TTEXT = font("NotoSans-Bold.ttf", 10, FNOTO)
F_KICK = font("NotoSans-Bold.ttf", 10, FNOTO)
F_PILL = font("NotoSans-Bold.ttf", 8, FNOTO)
F_SRC = font("NotoSans-Bold.ttf", 9, FNOTO)
F_HEAD = font("NotoSerif-Black.ttf", 20, FNOTO)
F_HEAD_S = font("NotoSerif-Black.ttf", 16, FNOTO)
F_DECK = font("NotoSans-Bold.ttf", 11, FNOTO)
F_DECK_S = font("NotoSans-Bold.ttf", 10, FNOTO)
F_LABEL = font("NotoSans-Bold.ttf", 8, FNOTO)
F_PIN = font("NotoSans-Bold.ttf", 11, FNOTO)
F_ART = font("NotoSans-Black.ttf", 24, FNOTO)
F_ART_S = font("NotoSans-Bold.ttf", 12, FNOTO)
F_ART2 = font("NotoSans-Black.ttf", 17, FNOTO)
F_ART2_S = font("NotoSans-Bold.ttf", 11, FNOTO)
F_FOC = font("NotoSans-Black.ttf", 30, FNOTO)
F_FOC_S = font("NotoSans-Bold.ttf", 12, FNOTO)
F_FOC23 = font("NotoSans-Black.ttf", 20, FNOTO)   # 2/3 of F_FOC (hero 1 only)
F_FOC23_S = font("NotoSans-Bold.ttf", 9, FNOTO)  # 2/3 of F_FOC_S
F_LBL = font("NotoSans-Black.ttf", 16, FNOTO)     # 2/3 of F_ART (hero 3 label)
F_LBL_S = font("NotoSans-Bold.ttf", 9, FNOTO)    # 2/3 of F_ART_S
F_LBL2 = font("NotoSans-Black.ttf", 12, FNOTO)    # 2/3 of F_ART2 (small-card labels)
F_LBL2_S = font("NotoSans-Bold.ttf", 8, FNOTO)   # 2/3 of F_ART2_S
F_ALSO = font("NotoSans-Bold.ttf", 11, FNOTO)
F_ALSO_N = font("NotoSans-Bold.ttf", 11, FNOTO)
F_SEC = font("NotoSans-Black.ttf", 13, FNOTO)
F_STATB = font("NotoSerif-Black.ttf", 21, FNOTO)
F_STATC = font("NotoSans-Bold.ttf", 10, FNOTO)
F_LEGEND = font("NotoSans-Bold.ttf", 10, FNOTO)
F_DATECHK = font("NotoSans-Bold.ttf", 11, FNOTO)
F_FOOT = font("NotoSans-Bold.ttf", 10, FNOTO)

PILL_COL = {"REPORTED": (16, 165, 90), "FORECAST": (20, 110, 230),
            "CLAIM": (230, 150, 0)}

TIMELINE = [
    ("00:00 NZ", "GTA VI unlocks"),
    ("04:42 RIYADH", "Air-raid sirens"),
    ("08:40 SEOUL", "Suneung begins"),
    ("09:30 NY", "ANT starts trading"),
    ("10:00 HAGUE", "ICJ ruling read"),
    ("12:45 SHENZHEN", "Trump meets Xi"),
    ("P.M.", "Three-way talks"),
    ("NIGHT", "COP31 final 48h"),
]

# num, region, topic, source, status, headline, deck, art big, art small, art key
FRONT = [
    (1, "SHENZHEN", "SUMMIT", "AP \u00b7 REUTERS", "REPORTED",
     "Trump, Xi and Putin hold first three-way summit",
     "90 minutes, then a 'Declaration on Peace': nuclear risk, energy, UN reform. Kyiv not in the room.",
     "SHENZHEN 12:45", "TRUMP\u2013XI\u2013PUTIN FIRST", "summit"),
    (2, "THE HAGUE", "LAW", "ICJ", "REPORTED",
     "World Court: Myanmar committed genocide",
     "First state held liable; 9\u20136, 10,000 killed, reparations ordered.",
     "MYANMAR GUILTY", "9\u20136 \u00b7 FIRST STATE HELD LIABLE", "icj"),
    (3, "ANTALYA", "CLIMATE", "UNFCCC", "REPORTED",
     "COP31 draft drops fossil fuels",
     "Ministers take over the text; $120bn aid fund still open.",
     "COP31", "DRAFT DROPS FOSSIL FUELS", "cop31"),
    (4, "NEW YORK", "GAMES", "SENSOR TOWER", "REPORTED",
     "GTA VI out today, New Zealand first",
     "Midnight unlocks; 15.9m pre-orders.",
     "GTA VI", "METACRITIC 99 \u00b7 $79.99", "gta"),
    (5, "NASDAQ", "MARKETS", "SEC \u00b7 REUTERS", "REPORTED",
     "Anthropic IPO debuts, biggest on record",
     "Priced at $83; raised $81.3bn, valued near $1.5tn.",
     "ANT $83", "$81.3BN RAISED", "anthropic"),
    (6, "ODISHA", "STORM", "IMD", "FORECAST",
     "Akvan bears down on Odisha",
     "204,070 listed to move; landfall due Friday, gusts 145 km/h.",
     "AKVAN", "204,070 TOLD TO MOVE", "akvan"),
    (7, "KERCH", "WAR", "REUTERS", "REPORTED",
     "Ukraine hits Crimea bridge again",
     "Third strike in a week; rail span hit, trains halted.",
     "KERCH BRIDGE", "3RD STRIKE IN A WEEK", "kerch"),
    (8, "SEOUL", "LAW", "REUTERS", "REPORTED",
     "Top court overturns Han's 15-year term",
     "Supreme Court sends the case back for retrial.",
     "15-YEAR TERM", "OVERTURNED \u00b7 RETRIAL", "han"),
    (9, "COPENHAGEN", "SECURITY", "AP", "REPORTED",
     "Denmark backs Arctic pact with US",
     "Parliament votes 109\u20130; more US bases in Greenland.",
     "109\u20130", "ARCTIC PACT APPROVED", "greenland"),
    (10, "RIYADH", "WAR", "REUTERS", "REPORTED",
     "Saudis shoot down Houthi missiles",
     "Sirens at 04:42; missile intercepted, debris damage.",
     "OVER RIYADH", "SIRENS 04:42", "riyadh"),
    (11, "BOGOTA", "LABOUR", "CUT", "REPORTED",
     "Colombia's unions strike nationwide",
     "Workers and teachers march against the tax bill.",
     "NATIONAL STRIKE", "CUT + FECODE", "colombia"),
    (12, "CANBERRA", "ECONOMY", "ABS", "REPORTED",
     "Australia's jobless rate rises to 4.9%",
     "Highest since 2021; 44,000 fewer employed in October.",
     "JOBLESS 4.9%", "HIGHEST SINCE 2021", "australia"),
    (13, "NAIROBI", "SPORT", "AIU", "REPORTED",
     "Marathon champion banned for doping",
     "Kenya's Jepchirchir gets 3 years for EPO.",
     "3-YEAR BAN", "EPO \u00b7 SYDNEY WIN LOST", "marathon"),
]

# num, city, text
ALSO = [
    (14, "Gaza", "Israel ends tank raid past truce line"),
    (15, "Florida", "a foot of rain; 300 rescue calls"),
    (16, "Mexico City", "Banxico cuts rates to 6.25%"),
    (17, "London", "National Grid debunks AI blackout post"),
    (18, "New Delhi", "schools reopen as smog curbs lift"),
    (19, "Canberra", "sanctions three Israelis, four groups"),
    (20, "Mogadishu", "Somalia accuses UAE of secret bases"),
    (21, "Frankfurt", "Deutsche Bank in $582m Epstein deals"),
    (22, "Washington", "senators warn of AI cyber threats"),
    (23, "Ottawa", "Carney seeks right China deal"),
    (24, "Tokyo", "India and Japan review defence ties"),
    (25, "Bengaluru", "Amazon $7bn renewables pledge"),
    (26, "Hormuz", "Iran says mines set 3 tankers ablaze"),
    (27, "Jakarta", "asset-seizure law ends 18-year wait"),
    (28, "Baghdad", "six French ISIL members jailed"),
    (29, "Caracas", "Hegseth signs US-Venezuela deal"),
    (30, "Washington", "Vance: no 'forever war' in Gulf"),
    (31, "Seoul", "half a million sit college entrance exam"),
    (32, "Washington", "Liu Yuming takes House Dem chair"),
    (33, "Brussels", "EU delays methane rules two years"),
    (34, "Benghazi", "cocaine and millions of pills seized"),
    (35, "Manama", "Bapco refinery back after attacks"),
    (36, "La Paz", "Bolivia El Nino emergency; 78,000 hit"),
]

STATS = [
    ("3", "presidents, one table"),
    ("$81.3bn", "Anthropic IPO, a record"),
    ("9\u20136", "World Court genocide vote"),
    ("109\u20130", "Danish vote on Arctic pact"),
    ("204,070", "listed to evacuate"),
    ("551,864", "Suneung sitters"),
]

LEGEND = [
    ("REPORTED", "confirmed by named sources"),
    ("FORECAST", "landfall, schedule or draft"),
    ("CLAIM", "one side says so, unverified"),
]

PINS = {
    1: (114.1, 22.5), 2: (174.8, -36.8), 3: (-74.0, 40.7), 4: (4.5, 52.1),
    5: (30.7, 36.9), 6: (85.8, 20.2), 7: (35.4, 45.3), 8: (127.0, 37.5),
    9: (12.6, 55.7), 10: (46.7, 24.7), 11: (-74.1, 4.7),
    12: (149.1, -35.3), 13: (36.8, -1.3),
}
DOTS = {
    14: (34.4, 31.5), 15: (-80.1, 26.1), 16: (-99.1, 19.4), 17: (-0.1, 51.5),
    18: (77.2, 28.6), 19: (149.1, -35.3), 20: (45.3, 2.0), 21: (8.7, 50.1),
    22: (-77.0, 38.9), 23: (-75.7, 45.4), 24: (139.7, 35.7), 25: (77.6, 13.0),
    26: (56.3, 26.6), 27: (106.8, -6.2), 28: (44.4, 33.3), 29: (-66.9, 10.5),
    30: (-77.0, 38.9), 31: (127.0, 37.5), 32: (-77.0, 38.9), 33: (4.4, 50.8),
    34: (20.1, 32.1), 35: (50.6, 26.2), 36: (-68.1, -16.5),
}

PROBLEMS = []


def wrap(d, text, fnt, width, max_lines=None):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines is not None and len(lines) > max_lines:
        PROBLEMS.append("TRUNCATED (%d lines): %s" % (len(lines), text))
        lines = lines[:max_lines]
    return lines


def art_text(img, d, x, y, w, h, big, small, f_big, f_small):
    """Big short text inside the art: white bold on a dark scrim, bottom-left."""
    bw = int(d.textlength(big, font=f_big))
    sw = int(d.textlength(small, font=f_small)) if small else 0
    if max(bw, sw) + 22 > w:
        PROBLEMS.append("ART TEXT TOO WIDE: %s / %s" % (big, small))
    tw = max(bw, sw)
    bh = f_big.size + f_small.size + 10
    ox = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ox)
    od.rounded_rectangle([x + 4, y + h - bh - 4, x + 4 + tw + 12, y + h - 4],
                         radius=3, fill=(0, 0, 0, 115))
    img.paste(ox, (0, 0), ox)
    d.text((x + 10, y + h - bh), big, font=f_big, fill="white",
           stroke_width=1, stroke_fill=(0, 0, 0))
    if small:
        d.text((x + 10, y + h - bh + f_big.size + 2), small, font=f_small,
               fill="white", stroke_width=1, stroke_fill=(0, 0, 0))


def focal_text(d, x, y, w, h, big, small, f_big, f_small, color, center):
    col = {"YELLOW": YELLOW, "NAVY": NAVY, "WHITE": "white"}[color]
    small_col = "white" if color != "NAVY" else NAVY
    stroke = 0 if color == "NAVY" else 1
    if center:
        bx = x + (w - d.textlength(big, font=f_big)) / 2
        sx = x + (w - d.textlength(small, font=f_small)) / 2 if small else 0
        d.text((bx, y + 8), big, font=f_big, fill=col,
               stroke_width=stroke, stroke_fill=(0, 0, 0))
        if small:
            d.text((sx, y + 8 + f_big.size + 4), small, font=f_small,
                   fill=small_col, stroke_width=stroke, stroke_fill=(0, 0, 0))
    else:
        d.text((x + 8, y + 8), big, font=f_big, fill=col,
               stroke_width=stroke, stroke_fill=(0, 0, 0))
        if small:
            d.text((x + 8, y + 8 + f_big.size + 4), small, font=f_small,
                   fill=small_col, stroke_width=stroke, stroke_fill=(0, 0, 0))


def _star(d, cx, cy, r_out, r_in, fill="white"):
    """Small 5-point star centred at (cx, cy)."""
    pts = []
    for k in range(10):
        r = r_out if k % 2 == 0 else r_in
        a = math.radians(-90 + k * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def _skyline(d, w, h, base, col, seed):
    import random
    rnd = random.Random(seed)
    x = 0
    while x < w:
        bw = rnd.randint(14, 30)
        bh = rnd.randint(int(h * 0.3), int(h * 0.75))
        d.rectangle([x, base - bh, x + bw, base], fill=col)
        for wy in range(base - bh + 6, base - 4, 10):
            for wx in range(x + 3, x + bw - 3, 7):
                if rnd.random() < 0.5:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 210, 31))
        x += bw + 3


def _flag(d, x, y, w, h, kind):
    if kind == "us":
        for i in range(7):
            d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                        fill=(178, 34, 52) if i % 2 == 0 else "white")
        d.rectangle([x, y, x + w * 0.4, y + h * 0.55], fill=(30, 50, 120))
        for sy in range(3):
            for sx in range(4):
                d.ellipse([x + 3 + sx * 7, y + 3 + sy * 6,
                           x + 6 + sx * 7, y + 6 + sy * 6], fill="white")
    elif kind == "cn":
        d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        d.ellipse([x + 3, y + 3, x + 11, y + 11], fill=(255, 222, 0))
        for sx, sy in [(16, 4), (20, 9), (16, 14)]:
            d.ellipse([x + sx, y + sy, x + sx + 4, y + sy + 4], fill=(255, 222, 0))
    elif kind == "ru":
        d.rectangle([x, y, x + w, y + h / 3], fill="white")
        d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 60, 180))
        d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(200, 20, 30))


def art_image(key, w, h):
    """Flat-vector picture for one front story, drawn in code."""
    img = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(img)
    if key == "summit":
        d.rectangle([0, 0, w, h], fill=(22, 52, 110))
        _skyline(d, w, h, h - 34, (12, 30, 70), 7)
        # wall clock 12:45, top right (no label: the focal text says 12:45)
        d.ellipse([w - 46, 6, w - 24, 28], fill="white")
        d.line([w - 35, 17, w - 35, 9], fill=NAVY, width=2)
        d.line([w - 35, 17, w - 30, 13], fill=NAVY, width=2)
        # three flags above the leaders (DeepSeek v20: one flag per leader)
        _flag(d, 72, 34, 30, 20, "us")
        _flag(d, 183, 34, 30, 20, "cn")
        _flag(d, 294, 34, 30, 20, "ru")
        # three leaders seated at one round table (below the focal text)
        d.rectangle([w * 0.08, h - 24, w * 0.92, h - 12], fill=(90, 60, 30))
        d.line([w * 0.08, h - 24, w * 0.92, h - 24], fill=GOLD, width=2)
        for i in range(3):
            cx = int(w * (0.22 + i * 0.28))
            d.ellipse([cx - 9, h - 42, cx + 9, h - 24], fill=(230, 200, 160))
            d.polygon([(cx - 13, h - 24), (cx + 13, h - 24), (cx + 8, h - 40),
                       (cx - 8, h - 40)], fill=(20, 20, 20) if i != 1 else (180, 30, 30))
        # nameplates on the table front, gold like the top-1 entry (DeepSeek v20)
        for i, name in enumerate(("TRUMP", "XI", "PUTIN")):
            cx = int(w * (0.22 + i * 0.28))
            d.rectangle([cx - 17, h - 23, cx + 17, h - 13], fill=GOLD)
            d.text((cx, h - 22), name, font=F_LABEL, fill=INK, anchor="ma")
    elif key == "gta":
        for i in range(h):
            t = i / h
            d.line([0, i, w, i], fill=(int(88 + 120 * t), int(40 + 60 * t),
                                       int(140 - 60 * t)))
        # sun, right (DeepSeek v20)
        d.ellipse([136, 28, 164, 56], fill=(255, 190, 60))
        _skyline(d, w, h, h, (20, 8, 40), 11)
        for px in (14, w - 22):
            d.line([px, h - 30, px + 4, h - 62], fill=(10, 30, 10), width=3)
            for a in (-50, -20, 10, 40):
                d.line([px + 2, h - 60, px + 2 + int(22 * math.sin(math.radians(a))),
                        h - 60 - int(14 * abs(math.cos(math.radians(a))))],
                       fill=(10, 30, 10), width=2)
        # NZ midnight: gold clock top left, PS5 box, queue of 4
        d.ellipse([8, 8, 28, 28], fill=GOLD)
        d.line([18, 18, 18, 10], fill=NAVY, width=2)
        d.line([18, 18, 23, 14], fill=NAVY, width=2)
        d.rectangle([60, 58, 82, 72], fill=(10, 10, 30), outline="white", width=1)
        d.text((71, 65), "PS5", font=F_SRC, fill="white", anchor="mm")
        for i in range(4):
            cx = 110 + i * 18
            d.ellipse([cx - 5, h - 16, cx + 5, h - 6], fill=(230, 200, 160))
            d.rectangle([cx - 7, h - 6, cx + 7, h], fill=(20, 20, 40))
    elif key == "anthropic":
        d.rectangle([0, 0, w, h], fill=PAPER)
        for gy in range(0, h, 14):
            d.line([0, gy, w, gy], fill=NAVY, width=1)
        # gold stair-step chart climbing to a red arrowhead (DeepSeek v20)
        steps = [(8, 66), (48, 66), (48, 52), (88, 52), (88, 38),
                 (128, 38), (128, 24), (168, 24)]
        for i in range(len(steps) - 1):
            d.line([steps[i], steps[i + 1]], fill=GOLD, width=3)
        d.polygon([(168, 24), (180, 18), (168, 12)], fill=RED)
        # navy ticker strip along the bottom right (clear of the text scrim)
        d.rectangle([100, h - 8, w, h], fill=NAVY)
        for tx in (108, 124, 140, 156, 172):
            d.line([tx, h - 6, tx + 8, h - 6], fill=GOLD, width=2)
    elif key == "icj":
        d.rectangle([0, 0, w, h], fill=(226, 218, 196))
        # pediment + 15 columns: first 9 paper, last 6 ink = the 9-6 vote (DeepSeek v20)
        d.polygon([(104, 36), (198, 12), (292, 36)], fill=(120, 110, 95))
        for i in range(15):
            cx = 116 + i * 11
            if i < 9:
                d.rectangle([cx, 40, cx + 7, 74], fill=(244, 239, 226),
                            outline=(120, 110, 95))
            else:
                d.rectangle([cx, 40, cx + 7, 74], fill=NAVY, outline="white")
        # steps
        d.rectangle([110, 76, 282, 80], fill=(240, 234, 220))
        d.rectangle([104, 80, 288, 84], fill=(240, 234, 220))
        d.rectangle([98, 84, 292, 90], fill=(240, 234, 220))
        # Myanmar flag top left (yellow/green/red + white star)
        d.rectangle([12, 8, 38, 13], fill=(254, 203, 0))
        d.rectangle([12, 13, 38, 18], fill=(0, 140, 60))
        d.rectangle([12, 18, 38, 24], fill=(220, 40, 40))
        _star(d, 25, 16, 5, 2)
    elif key == "cop31":
        d.rectangle([0, 0, w, h], fill=(11, 110, 110))
        # yellow hourglass, left: two gold-framed triangles + sand stream + pile
        d.polygon([(22, 8), (74, 8), (48, 44)], fill=(255, 210, 31))
        d.polygon([(48, 44), (74, 80), (22, 80)], fill=(255, 210, 31))
        d.line([22, 8, 74, 8], fill=GOLD, width=3)
        d.line([22, 80, 74, 80], fill=GOLD, width=3)
        d.line([48, 44, 48, 66], fill=(255, 210, 31), width=3)
        d.ellipse([38, 72, 58, 78], fill=(255, 210, 31))
        # green globe, right: gold outline + meridian/latitude lines
        d.ellipse([198, 16, 268, 86], fill=(30, 170, 110), outline=GOLD, width=2)
        d.line([233, 18, 233, 84], fill=GOLD, width=1)
        d.line([202, 38, 264, 38], fill=GOLD, width=1)
        d.line([202, 62, 264, 62], fill=GOLD, width=1)
        # red thermometer spearing the globe's left edge
        d.rectangle([176, 10, 182, 62], fill=(220, 40, 40))
        d.ellipse([170, 58, 184, 72], fill=(220, 40, 40))
        for ty in (18, 32, 46):
            d.line([168, ty, 174, ty], fill=GOLD, width=2)
    elif key == "akvan":
        d.rectangle([0, 0, w, h], fill=(12, 70, 160))
        # spiral centred left (DeepSeek v20): three paper arcs + ink eye
        cx, cy = 58, 42
        for r in (6, 14, 22):
            d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300,
                  fill="white", width=3)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=INK)
        # arrows inland, top left + red warning triangle top right
        for i in range(3):
            ax = 14 + i * 22
            d.line([ax, 14, ax + 12, 14], fill=YELLOW, width=2)
            d.polygon([(ax + 12, 10), (ax + 12, 18), (ax + 18, 14)],
                      fill=YELLOW)
        d.polygon([(175, 12), (185, 32), (165, 32)], fill=RED)
        d.text((175, 22), "!", font=F_ART2_S, fill=YELLOW, anchor="mm")
    elif key == "kerch":
        d.rectangle([0, 0, w, h], fill=(14, 30, 80))
        # bridge arc + gold deck with a gap mid-span, red span sagging (DeepSeek v20)
        d.arc([8, 30, w - 8, h + 30], 200, 340, fill=(150, 150, 150), width=3)
        d.rectangle([8, h - 40, 100, h - 36], fill=GOLD)
        d.rectangle([130, h - 40, w - 8, h - 36], fill=GOLD)
        for px in (30, w - 34):
            d.line([px, h - 40, px, h - 52], fill=(150, 150, 150), width=2)
        d.polygon([(100, h - 40), (130, h - 40), (122, h - 28), (108, h - 28)],
                  fill=(200, 40, 40))
        # halted train, three smoke ellipses rising from the gap
        d.rectangle([w - 66, h - 34, w - 14, h - 22], fill=(200, 40, 40))
        d.ellipse([102, 8, 114, 18], fill=(200, 200, 200))
        d.ellipse([112, 2, 126, 14], fill=(220, 220, 220))
        d.ellipse([122, 8, 134, 18], fill=(200, 200, 200))
    elif key == "han":
        d.rectangle([0, 0, w, h], fill=NAVY)
        # struck-through 15 top left (the overturned sentence)
        d.text((14, 10), "15", font=F_ART2, fill="white")
        d.line([10, 26, 34, 8], fill=RED, width=3)
        # gold gavel angled top right (DeepSeek v20)
        d.line([w - 44, 12, w - 16, 26], fill=GOLD, width=5)
        d.rectangle([w - 50, 8, w - 38, 20], fill=(200, 160, 40))
        # yellow scales on a paper beam, centre right
        d.line([140, 24, 140, 42], fill="white", width=2)
        d.line([110, 42, 170, 42], fill="white", width=2)
        d.polygon([(118, 42), (138, 42), (128, 58)], fill=YELLOW)
        d.polygon([(142, 42), (162, 42), (152, 58)], fill=YELLOW)
    elif key == "greenland":
        d.rectangle([0, 0, w, h], fill=(24, 130, 200))
        # navy sea band (DeepSeek v20)
        d.rectangle([0, 64, w, h], fill=NAVY)
        # paper iceberg + second smaller berg, bases on the sea
        d.polygon([(8, 64), (40, 64), (24, 26)], fill="white")
        d.polygon([(w * 0.55, 64), (w * 0.72, 52), (w * 0.9, 64)],
                  fill=(230, 240, 245))
        # two flags on one gold pole, right
        d.line([150, 26, 150, 52], fill=GOLD, width=2)
        d.rectangle([142, 26, 150, 38], fill=(200, 20, 40))
        d.rectangle([142, 30, 150, 34], fill="white")
        d.rectangle([145, 26, 147, 38], fill="white")
        _flag(d, 152, 26, 8, 12, "us")
    elif key == "marathon":
        d.rectangle([0, 0, w, h], fill=(246, 241, 226))
        # track lanes + runner + finish line
        for i in range(3):
            d.line([0, h - 46 + i * 12, w, h - 46 + i * 12], fill=(222, 62, 48),
                   width=2)
        cx, cy = w // 2 - 10, h - 52
        d.ellipse([cx - 5, cy - 12, cx + 5, cy - 2], fill=(20, 20, 20))
        d.line([cx, cy - 2, cx + 4, cy + 12], fill=(20, 20, 20), width=3)
        d.line([cx, cy + 2, cx - 12, cy - 6], fill=(20, 20, 20), width=3)
        d.line([cx, cy + 2, cx + 12, cy + 8], fill=(20, 20, 20), width=3)
        d.line([cx + 4, cy + 12, cx - 6, cy + 22], fill=(20, 20, 20), width=3)
        d.line([cx + 4, cy + 12, cx + 14, cy + 20], fill=(20, 20, 20), width=3)
        # gold medal with a red circle-slash (the ban) (DeepSeek v20)
        d.ellipse([128, 18, 152, 42], fill=GOLD)
        d.ellipse([124, 14, 156, 46], outline=RED, width=3)
        d.line([126, 16, 154, 44], fill=RED, width=3)
    elif key == "riyadh":
        d.rectangle([0, 0, w, h], fill=(10, 20, 50))
        _skyline(d, w, h, h - 30, (6, 12, 34), 11)
        # red interceptor trail rising to a gold burst (DeepSeek v20)
        d.polygon([(20, 80), (60, 44), (120, 20), (124, 24), (64, 48), (24, 84)],
                  fill=RED)
        d.ellipse([114, 12, 126, 24], fill=GOLD)
        for a in range(0, 360, 45):
            d.line([120, 18, 120 + int(12 * math.cos(math.radians(a))),
                    18 + int(12 * math.sin(math.radians(a)))],
                   fill=YELLOW, width=2)
        # yellow city dots along the base
        for dx in (30, 70, 110, 150, 180):
            d.ellipse([dx, 74, dx + 4, 78], fill=YELLOW)
    elif key == "ukraine":
        d.rectangle([0, 0, w, h // 2], fill=(0, 90, 180))
        d.rectangle([0, h // 2, w, h], fill=(255, 210, 31))
        d.ellipse([w // 2 - 8, h // 2 - 14, w // 2 + 8, h // 2 + 14],
                  fill=RED, outline="white", width=2)
        # empty chair top right + folded flag in a closed briefcase top left
        d.rectangle([w - 44, 12, w - 12, 16], fill=(90, 60, 30))
        d.rectangle([w - 42, 16, w - 38, 30], fill=(90, 60, 30))
        d.rectangle([w - 18, 16, w - 14, 30], fill=(90, 60, 30))
        d.rectangle([12, 10, 52, 22], fill=(60, 40, 20))
        d.rectangle([14, 12, 32, 20], fill=(0, 90, 180))
        d.rectangle([34, 12, 50, 20], fill=(255, 210, 31))
    elif key == "apec":
        d.rectangle([0, 0, w, h], fill=(14, 90, 90))
        _skyline(d, w, h, h, (8, 50, 55), 21)
        d.ellipse([w // 2 - 16, 10, w // 2 + 16, 42], fill=GOLD)
        d.text((w // 2, 26), "21", font=F_ART2, fill=NAVY, anchor="mm")
        # ring of mini flags along the bottom edge (signed page dropped: scrim covers it)
        for i in range(7):
            fx = 10 + i * (w - 20) // 7
            d.rectangle([fx, h - 8, fx + 8, h - 3],
                        fill=[(178, 34, 52), (222, 41, 16), (0, 60, 180),
                              (255, 210, 31), (30, 140, 80), (20, 150, 160),
                              (200, 40, 40)][i])
    elif key == "florida":
        d.rectangle([0, 0, w, h], fill=(90, 120, 150))
        for i in range(14):
            x = (i * 23) % w
            d.line([x, 8 + (i % 3) * 12, x - 8, 30 + (i % 3) * 12],
                   fill=(220, 230, 240), width=2)
        d.rectangle([w * 0.15, h - 34, w * 0.55, h - 12], fill=(60, 50, 40))
        d.polygon([(w * 0.12, h - 34), (w * 0.35, h - 52), (w * 0.58, h - 34)],
                  fill=(140, 40, 40))
        d.rectangle([0, h - 10, w, h], fill=(30, 80, 140))
        # 1-ft ruler top left + rescue boat top right (scrim covers the bottom)
        d.rectangle([10, 8, 18, 40], fill="white")
        for i in range(4):
            d.line([10, 12 + i * 9, 16, 12 + i * 9], fill=NAVY, width=1)
        d.text((24, 12), "1 FT", font=F_SRC, fill="white")
        d.polygon([(w - 72, 10), (w - 28, 10), (w - 34, 24),
                   (w - 66, 24)], fill=(255, 210, 31))
        d.ellipse([w - 54, 2, w - 44, 12], fill=(230, 200, 160))
    elif key == "suneung":
        d.rectangle([0, 0, w, h], fill=(232, 226, 210))
        d.rectangle([8, 8, w - 8, 26], fill=(40, 60, 90))
        d.ellipse([w - 30, 12, w - 14, 28], fill="white")
        for r in range(2):
            for c in range(3):
                x = 16 + c * (w // 3)
                y = 36 + r * 26
                d.rectangle([x, y, x + w // 4, y + 16], fill=(150, 120, 80))
                d.ellipse([x + w // 8 - 6, y - 10, x + w // 8 + 6, y + 2],
                          fill=(230, 200, 160))
        # plane held overhead, flights paused
        d.polygon([(w - 70, 14), (w - 30, 18), (w - 70, 22)], fill=(90, 90, 90))
        d.polygon([(w - 58, 10), (w - 48, 18), (w - 58, 20)], fill=(90, 90, 90))
        d.line([w - 74, 18, w - 26, 18], fill=RED, width=2)
    elif key == "colombia":
        d.rectangle([0, 0, w, h], fill=(240, 220, 160))
        for i in range(7):
            x = 10 + i * (w // 7)
            d.ellipse([x, h - 44, x + 16, h - 28], fill=(200, 140, 90))
            d.rectangle([x + 2, h - 28, x + 14, h - 8], fill=(40, 90, 160))
        d.rectangle([w // 2 - 34, 8, w // 2 + 34, 30], fill="white",
                    outline=RED, width=2)
        d.text((w // 2, 19), "PARO", font=F_ART2_S, fill=RED, anchor="mm")
        # second union banner top left + torn tax-bill page top right
        d.rectangle([8, 8, 62, 26], fill=NAVY)
        d.text((35, 17), "FECODE", font=F_SRC, fill="white", anchor="mm")
        d.polygon([(w - 40, 8), (w - 12, 8), (w - 16, 24),
                   (w - 26, 16), (w - 34, 24)], fill="white",
                  outline=(120, 120, 120))
        # paper placards held up by the crowd (DeepSeek v20)
        for px in (24, 84, 144):
            d.rectangle([px, 32, px + 14, 42], fill="white", outline=INK)
    elif key == "australia":
        d.rectangle([0, 0, w, h], fill=(245, 240, 228))
        # four navy bars rising left to right (DeepSeek v20)
        for i, top in enumerate((52, 42, 32, 22)):
            x = 24 + i * 40
            d.rectangle([x, top, x + 16, 70], fill=NAVY)
        # red arrow climbing above the bars
        d.line([(20, 56), (164, 20)], fill=RED, width=3)
        d.polygon([(164, 20), (148, 18), (160, 32)], fill=RED)
        # -44,000 ledger line (kept: the other key number)
        d.text((12, 8), "-44,000", font=F_SRC, fill=RED)
    elif key == "libya":
        d.rectangle([0, 0, w, h], fill=(30, 30, 40))
        for i in range(5):
            x = 14 + i * 34
            d.rounded_rectangle([x, h // 2 - 8, x + 26, h // 2 + 8], radius=8,
                                fill="white" if i % 2 == 0 else (255, 210, 31))
        d.rectangle([w // 2 - 30, 10, w // 2 + 30, 26], fill=(120, 90, 60))
        # balance scale with a "?" — quantity unverified, no number shown
        d.line([w - 30, 8, w - 30, 34], fill=GOLD, width=2)
        d.line([w - 46, 12, w - 14, 12], fill=GOLD, width=2)
        d.arc([w - 46, 12, w - 36, 26], 0, 180, fill=GOLD, width=2)
        d.arc([w - 24, 12, w - 14, 26], 0, 180, fill=GOLD, width=2)
        d.text((w - 30, 30), "?", font=F_ART2, fill=GOLD, anchor="ma")
    return img


# pixel nudges so clustered pins stay readable (map is small): the pin circle
# moves by (dx, dy) and a thin leader line points back to the true spot.
# 5 Antalya crowds 7 Kerch; 8 Seoul (Han) collides with the Suneung dot;
# 9 Copenhagen crowds 4 The Hague; 10 Riyadh crowds 7 Kerch.
PIN_OFF = {2: (-12, -14), 5: (-24, 20), 8: (-16, -14), 9: (16, -12), 10: (14, 10)}


def draw_map(d, x0, y0, mw, mh):
    with open(os.path.join(HERE, "world.geo.json")) as f:
        gj = json.load(f)
    polys = []
    for feat in gj["features"]:
        geom = feat["geometry"]
        if geom["type"] == "Polygon":
            polys.append(geom["coordinates"])
        elif geom["type"] == "MultiPolygon":
            polys.extend(geom["coordinates"])
    for poly in polys:
        for ring in poly:
            pts = []
            for lon, lat in ring:
                px = (lon + 180.0) / 360.0 * mw
                py = (90.0 - lat) / 180.0 * mh
                pts.append((px, py))
            # filled continents (v5: like the top entries), not dots
            d.polygon([(x0 + px, y0 + py) for px, py in pts],
                      fill=SAND)

    def proj(lon, lat):
        return (x0 + (lon + 180.0) / 360.0 * mw,
                y0 + (90.0 - lat) / 180.0 * mh)

    for n, (lon, lat) in DOTS.items():
        px, py = proj(lon, lat)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=NAVY)
    for n, (lon, lat) in PINS.items():
        px, py = proj(lon, lat)
        dx, dy = PIN_OFF.get(n, (0, 0))
        if (dx, dy) != (0, 0):
            # leader line from the true spot to the moved pin circle
            d.line([px, py, px + dx, py + dy], fill=RED, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
            px, py = px + dx, py + dy
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline="white")
        t = str(n)
        tw = d.textlength(t, font=F_PIN)
        d.text((px - tw / 2, py - 5), t, font=F_PIN, fill="white")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead 0-109: date in the top-1 face (Liberation Serif Bold = Times) ----
    d.rectangle([12, 8, 86, 80], fill=RED)
    d.text((49, 12), "NOV", font=F_DATE2, fill="white", anchor="ma")
    d.text((49, 26), "19", font=F_DATE, fill="white", anchor="ma")
    d.text((49, 60), "THU \u00b7 2026", font=F_DATE2, fill="white", anchor="ma")
    d.text((98, 1), "THE WORLD IN ONE DAY", font=F_EYE, fill=RED)
    d.line([98, 20, 1012, 20], fill=INK, width=1)
    d.text((98, 11), "Thursday 19 November 2026", font=F_TITLE, fill=INK)
    d.text((98, 84), "Trump, Xi and Putin share one table \u00b7 World Court finds "
           "Myanmar guilty of genocide \u00b7 COP31's draft drops fossil fuels",
           font=F_DECKLINE, fill=RED)
    d.text((1012, 1), "36 STORIES \u00b7 7 REGIONS \u00b7 ONE PAGE",
           font=F_EYE, fill=INK, anchor="ra")
    d.rectangle([0, 109, W, 112], fill=GOLD)

    # ---- big-numbers strip 111-149 ----
    sw6 = (W - 24) / 6.0
    for si, (val, cap) in enumerate(STATS):
        sx = 12 + si * sw6
        if si > 0:
            d.line([sx - 6, 117, sx - 6, 149], fill=RULE, width=1)
        d.text((sx + 4, 115), val, font=F_STATB, fill=NAVY)
        d.text((sx + 4, 137), cap, font=F_STATC, fill=GREY)

    # ---- THE DAY BY HOURS timeline 155-187 ----
    d.rectangle([12, 155, 100, 187], fill=RED)
    d.text((56, 156), "THE DAY", font=F_TTIME, fill="white", anchor="ma")
    d.text((56, 170), "BY HOURS", font=F_TTIME, fill="white", anchor="ma")
    bx = 104
    bw = (W - 12 - bx) / 8.0
    for i, (t, txt) in enumerate(TIMELINE):
        cx = bx + i * bw
        if i > 0:
            d.line([cx, 157, cx, 185], fill=RULE, width=1)
        d.text((cx + 5, 158), t, font=F_TTIME, fill=NAVY)
        d.text((cx + 5, 170), txt, font=F_TTEXT, fill=INK)
    d.line([12, 189, W - 12, 189], fill=RULE, width=1)

    # ---- heroes 192-374: lead 396 wide, rails 294 (hierarchy, not equal thirds) ----
    hy = 192
    hws = [396, 294, 294]
    for i, (num, reg, topic, src, status, head, deck, big, small, key) in enumerate(FRONT[:3]):
        hw = hws[i]
        cx = 12 + sum(hws[:i]) + 8 * i
        im = art_image(key, hw, 96)
        idd = ImageDraw.Draw(im)
        if key == "summit":
            focal_text(idd, 0, 0, hw, 96, big, small, F_FOC23, F_FOC23_S, "YELLOW", True)
        elif key == "gta":
            focal_text(idd, 0, 0, hw, 96, big, small, F_FOC, F_FOC_S, "WHITE", True)
        else:
            art_text(im, idd, 0, 0, hw, 96, big, small, F_LBL, F_LBL_S)
        img.paste(im, (cx, hy))
        d.rectangle([cx, hy + 96, cx + hw, hy + 112], fill=NAVY)
        pw = d.textlength(status, font=F_PILL) + 10
        d.rounded_rectangle([cx + 4, hy + 99, cx + 4 + pw, hy + 109],
                            radius=2, fill=PILL_COL[status])
        d.text((cx + 9, hy + 98), status, font=F_PILL, fill="white")
        d.text((cx + 10 + pw, hy + 97), "%d. %s \u00b7 %s" % (num, reg, topic),
               font=F_KICK, fill="white")
        sw = d.textlength(src, font=F_SRC)
        d.text((cx + hw - 5 - sw, hy + 97), src, font=F_SRC, fill=GOLD)
        lines = wrap(d, head, F_HEAD, hw - 6, max_lines=2)
        for j, ln in enumerate(lines):
            d.text((cx + 3, hy + 116 + j * 22), ln, font=F_HEAD, fill=INK)
        dlines = wrap(d, deck, F_DECK, hw - 6, max_lines=2)
        for j, ln in enumerate(dlines):
            d.text((cx + 3, hy + 116 + len(lines) * 22 + 2 + j * 13),
                   ln, font=F_DECK, fill=(60, 60, 60))

    # ---- smalls 380-706 (2 rows x 5, image 196x84) ----
    sw_ = 196
    for r in range(2):
        for c in range(5):
            k = 3 + r * 5 + c
            num, reg, topic, src, status, head, deck, big, small, key = FRONT[k]
            cx = 12 + c * (sw_ + 8)
            cy = 380 + r * 166
            im = art_image(key, sw_, 84)
            idd = ImageDraw.Draw(im)
            art_text(im, idd, 0, 0, sw_, 84, big, small, F_LBL2, F_LBL2_S)
            img.paste(im, (cx, cy))
            d.rectangle([cx, cy + 84, cx + sw_, cy + 99], fill=NAVY)
            d.text((cx + 4, cy + 85), "%d. %s \u00b7 %s" % (num, reg, topic),
                   font=F_KICK, fill="white")
            pw = d.textlength(status, font=F_PILL) + 10
            d.rounded_rectangle([cx + sw_ - 4 - pw, cy + 86, cx + sw_ - 4, cy + 96],
                                radius=2, fill=PILL_COL[status])
            d.text((cx + sw_ + 1 - pw, cy + 85), status, font=F_PILL, fill="white")
            lines = wrap(d, head, F_HEAD_S, sw_ - 4, max_lines=2)
            for j, ln in enumerate(lines):
                d.text((cx + 2, cy + 102 + j * 18), ln, font=F_HEAD_S, fill=INK)
            dlines = wrap(d, deck + " \u2014 " + src, F_DECK_S, sw_ - 4, max_lines=2)
            for j, ln in enumerate(dlines):
                d.text((cx + 2, cy + 102 + len(lines) * 18 + 1 + j * 13),
                       ln, font=F_DECK_S, fill=(60, 60, 60))

    # ---- map + also 712-952 (map taller, also-list roomier) ----
    my = 712
    d.text((12, my), "WHERE IT HAPPENED", font=F_SEC, fill=INK)
    d.line([12, my + 16, 348, my + 16], fill=INK, width=1)
    d.rectangle([12, my + 22, 348, my + 172], fill=OCEAN, outline=RULE, width=1)
    draw_map(d, 12, my + 22, 336, 150)
    d.text((12, my + 176), "Red numbers 1\u201313, dark dots 14\u201336.",
           font=F_TTEXT, fill=GREY)
    # how-sure-are-we legend under the map (was the stats row)
    d.text((12, my + 192), "HOW SURE ARE WE?", font=F_SEC, fill=INK)
    for li, (st, expl) in enumerate(LEGEND):
        ly = my + 210 + li * 12
        d.rectangle([12, ly, 20, ly + 8], fill=PILL_COL[st])
        d.text((24, ly - 1), st, font=F_LEGEND, fill=INK)
        d.text((86, ly - 1), expl, font=F_LEGEND, fill=GREY)

    ax = 364
    d.text((ax, my), "ALSO ON THURSDAY 19 NOVEMBER", font=F_SEC, fill=INK)
    d.text((1012, my), "23 MORE STORIES", font=F_SEC, fill=INK, anchor="ra")
    d.line([ax, my + 16, 1012, my + 16], fill=INK, width=1)
    colw = 320
    rows = 12
    for i, (num, city, txt) in enumerate(ALSO):
        col = 0 if i < rows else 1
        row = i if i < rows else i - rows
        x = ax + col * (colw + 8)
        y = my + 22 + row * 13
        d.text((x, y), "%d." % num, font=F_ALSO_N, fill=RED)
        full = "%s: %s" % (city, txt)
        lines = wrap(d, full, F_ALSO, colw - 22, max_lines=1)
        d.text((x + 20, y), lines[0] if lines else "", font=F_ALSO, fill=INK)

    # ---- date check 964-992: thin 2-line band (was a 40px box) ----
    dy = 964
    d.rectangle([12, dy, 1012, dy + 28], outline=RED, width=2)
    chk = ("DATE CHECK \u2014 Left out, first reported Wednesday 18 November: Iranian drone "
           "interceptions \u00b7 EU's \u20ac45bn loan \u00b7 House 251\u201311 Jeffries vote \u00b7 "
           "Voyager 1, one light-day out \u00b7 Peltola's Alaska win \u00b7 "
           "Qeshm strikes (17 Nov) \u00b7 Van Gogh's $190.4m sale. Not yet news: Akvan's landfall "
           "(Fri 20 Nov) \u00b7 COP31's final deal (Fri 20 Nov).")
    clines = wrap(d, chk, F_DATECHK, 976, max_lines=2)
    for j, ln in enumerate(clines):
        d.text((20, dy + j * 12), ln, font=F_DATECHK, fill=INK)

    # ---- footer 998-1021 ----
    fy = 998
    d.text((512, fy), "Reads at three sizes: the date and 3 leads at thumbnail size \u00b7 "
           "13 pictures at half size \u00b7 all 36 stories at full size.",
           font=F_FOOT, fill=GREY, anchor="ma")
    d.text((512, fy + 13), "Pins 1\u201313, dots 14\u201336. Sources: AP \u00b7 Reuters \u00b7 AFP \u00b7 Yonhap \u00b7 "
           "IMD \u00b7 ICJ \u00b7 SEC \u00b7 ABS \u00b7 AIU. Original illustrations.",
           font=F_FOOT, fill=GREY, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    img.save(out)
    print("saved", out, os.path.getsize(out), "bytes")
    if PROBLEMS:
        print("PROBLEMS:")
        for p in PROBLEMS:
            print(" -", p)
    else:
        print("no truncation")


if __name__ == "__main__":
    main()
