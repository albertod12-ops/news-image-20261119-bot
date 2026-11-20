#!/usr/bin/env python3
"""news-image-20261119 v17: 36 stories, newspaper front page after the top 1.
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


def draw_tracked(d, x, y, text, fnt, fill, target_w):
    """Draw text letter-spaced so it spans exactly target_w."""
    nat = sum(d.textlength(ch, font=fnt) for ch in text)
    gaps = max(len(text) - 1, 1)
    track = (target_w - nat) / gaps
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=fnt, fill=fill)
        cx += d.textlength(ch, font=fnt) + track


F_TITLE = font("LiberationSerif-Bold.ttf", 60, FLIB)
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
        # three leaders seated at one round table (below the focal text)
        d.rectangle([w * 0.08, h - 24, w * 0.92, h - 12], fill=(90, 60, 30))
        for i in range(3):
            cx = int(w * (0.22 + i * 0.28))
            d.ellipse([cx - 9, h - 42, cx + 9, h - 24], fill=(230, 200, 160))
            d.polygon([(cx - 13, h - 24), (cx + 13, h - 24), (cx + 8, h - 40),
                       (cx - 8, h - 40)], fill=(20, 20, 20) if i != 1 else (180, 30, 30))
        # nameplates on the table front, like the top-1 entry
        for i, name in enumerate(("TRUMP", "XI", "PUTIN")):
            cx = int(w * (0.22 + i * 0.28))
            d.rectangle([cx - 17, h - 23, cx + 17, h - 13], fill="white")
            d.text((cx, h - 22), name, font=F_LABEL, fill=INK, anchor="ma")
    elif key == "gta":
        for i in range(h):
            t = i / h
            d.line([0, i, w, i], fill=(int(88 + 120 * t), int(40 + 60 * t),
                                       int(140 - 60 * t)))
        d.ellipse([w // 2 - 26, h // 2 - 34, w // 2 + 26, h // 2 + 18],
                  fill=(255, 190, 60))
        _skyline(d, w, h, h, (20, 8, 40), 11)
        for px in (14, w - 22):
            d.line([px, h - 30, px + 4, h - 62], fill=(10, 30, 10), width=3)
            for a in (-50, -20, 10, 40):
                d.line([px + 2, h - 60, px + 2 + int(22 * math.sin(math.radians(a))),
                        h - 60 - int(14 * abs(math.cos(math.radians(a))))],
                       fill=(10, 30, 10), width=2)
        # NZ midnight: clock striking 12 top right, queue outside a shop, PS5 box
        d.ellipse([w - 40, 6, w - 14, 32], fill="white")
        d.line([w - 27, 19, w - 27, 10], fill=NAVY, width=2)
        d.line([w - 27, 19, w - 22, 15], fill=NAVY, width=2)
        d.rectangle([w - 52, h - 26, w - 12, h - 8], fill=(10, 10, 30),
                    outline="white", width=1)
        d.text((w - 32, h - 17), "PS5", font=F_SRC, fill="white", anchor="mm")
        for i in range(4):
            cx = 30 + i * 18
            d.ellipse([cx - 5, h - 16, cx + 5, h - 6], fill=(230, 200, 160))
            d.rectangle([cx - 7, h - 6, cx + 7, h], fill=(20, 20, 40))
    elif key == "anthropic":
        d.rectangle([0, 0, w, h], fill=(8, 70, 52))
        for gy in range(0, h, 16):
            d.line([0, gy, w, gy], fill=(24, 100, 74), width=1)
        pts = [(8, h - 18), (w * 0.25, h - 34), (w * 0.45, h - 26),
               (w * 0.65, h - 48), (w * 0.85, h - 58), (w - 8, h - 66)]
        for i in range(len(pts) - 1):
            d.line([pts[i], pts[i + 1]], fill=(255, 210, 31), width=3)
        for i, (cx, cy) in enumerate(pts[1:-1]):
            col = (60, 220, 120) if i % 2 == 0 else (230, 70, 60)
            d.rectangle([cx - 3, cy - 8, cx + 3, cy + 8], fill=col)
        # Nasdaq tower with ANT screen + opening bell
        d.rectangle([w - 40, 6, w - 8, h - 40], fill=(10, 20, 40),
                    outline=(255, 210, 31), width=1)
        d.text((w - 24, 16), "ANT", font=F_SRC, fill=(255, 210, 31), anchor="ma")
        d.text((w - 24, 30), "$83", font=F_SRC, fill="white", anchor="ma")
        d.arc([12, 6, 40, 30], 180, 360, fill=GOLD, width=3)
        d.ellipse([24, 30, 28, 36], fill=GOLD)
    elif key == "icj":
        d.rectangle([0, 0, w, h], fill=(226, 218, 196))
        d.polygon([(w * 0.2, 26), (w * 0.8, 26), (w * 0.5, 8)], fill=(120, 110, 95))
        for i in range(4):
            cx = int(w * (0.22 + i * 0.19))
            d.rectangle([cx, 28, cx + 10, h - 12], fill=(240, 234, 220),
                        outline=(120, 110, 95))
        d.rectangle([0, h - 12, w, h], fill=(120, 110, 95))
        # nameplates Gambia v Myanmar (footprints dropped: scrim covers the bottom)
        d.rectangle([8, 34, 52, 46], fill=NAVY)
        d.text((30, 40), "GAMBIA", font=F_SRC, fill="white", anchor="mm")
        d.rectangle([w - 60, 34, w - 8, 46], fill=NAVY)
        d.text((w - 34, 40), "MYANMAR", font=F_SRC, fill="white", anchor="mm")
    elif key == "cop31":
        d.rectangle([0, 0, w, h], fill=(16, 100, 180))
        d.ellipse([w // 2 - 26, 8, w // 2 + 26, 60], fill=(30, 170, 110))
        d.ellipse([w // 2 - 18, 16, w // 2 - 2, 30], fill=(30, 110, 200))
        d.ellipse([w // 2 + 4, 34, w // 2 + 20, 52], fill=(30, 110, 200))
        d.rectangle([w - 26, 14, w - 18, h - 14], fill="white")
        d.rectangle([w - 26, h - 30, w - 18, h - 14], fill=(220, 40, 40))
        d.ellipse([w - 30, h - 22, w - 14, h - 6], fill=(220, 40, 40))
        # 48-hour hourglass top left + draft page stamped 2035 top right
        d.polygon([(14, 8), (34, 8), (24, 22), (14, 36), (34, 36), (24, 22)],
                  fill=(255, 210, 31))
        d.rectangle([w - 78, 8, w - 34, 22], fill="white")
        d.text((w - 56, 15), "2035", font=F_SRC, fill=NAVY, anchor="mm")
    elif key == "akvan":
        d.rectangle([0, 0, w, h], fill=(12, 70, 160))
        cx, cy = w // 2, h // 2 + 4
        for r in range(34, 4, -6):
            d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300,
                  fill=(255, 255, 255), width=3)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 210, 31))
        # arrows inland, top left (scrim covers the bottom) + 145 km/h gauge
        for i in range(3):
            ax = 14 + i * 22
            d.line([ax, 14, ax + 12, 14], fill=YELLOW, width=2)
            d.polygon([(ax + 12, 10), (ax + 12, 18), (ax + 18, 14)],
                      fill=YELLOW)
        d.text((w - 8, 8), "145 km/h", font=F_SRC, fill="white", anchor="ra")
    elif key == "kerch":
        d.rectangle([0, 0, w, h], fill=(14, 30, 80))
        # bridge arc + deck across the strait, explosion star mid-span
        d.arc([8, 30, w - 8, h + 30], 200, 340, fill=(150, 150, 150), width=3)
        d.rectangle([8, h - 40, w - 8, h - 36], fill=(150, 150, 150))
        for px in (30, w // 2, w - 34):
            d.line([px, h - 40, px, h - 52], fill=(150, 150, 150), width=2)
        cx, cy = w // 2, h - 52
        for a in range(0, 360, 45):
            d.line([cx, cy, cx + int(16 * math.cos(math.radians(a))),
                    cy + int(16 * math.sin(math.radians(a)))],
                   fill=YELLOW, width=3)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 120, 0))
        # halted train, smoke rising
        d.rectangle([w - 66, h - 34, w - 14, h - 22], fill=(200, 40, 40))
        d.ellipse([cx - 14, 8, cx - 4, 18], fill=(180, 180, 180))
        d.ellipse([cx - 2, 2, cx + 10, 14], fill=(200, 200, 200))
    elif key == "han":
        d.rectangle([0, 0, w, h], fill=(26, 70, 96))
        d.polygon([(w * 0.2, 30), (w * 0.8, 30), (w * 0.5, 12)], fill=(140, 130, 110))
        for i in range(4):
            cx = int(w * (0.22 + i * 0.19))
            d.rectangle([cx, 32, cx + 10, h - 12], fill=(235, 230, 218),
                        outline=(140, 130, 110))
        # gavel top right + struck-through 15 top left
        d.line([w - 44, 12, w - 16, 26], fill=(150, 100, 50), width=5)
        d.rectangle([w - 50, 8, w - 38, 20], fill=(120, 80, 40))
        d.text((14, 10), "15", font=F_ART2, fill="white")
        d.line([10, 26, 34, 8], fill=RED, width=3)
    elif key == "greenland":
        d.rectangle([0, 0, w, h], fill=(24, 130, 200))
        d.rectangle([0, h - 26, w, h], fill=(16, 100, 180))
        # icebergs + Danish flag left, US flag right
        d.polygon([(w * 0.1, h - 26), (w * 0.3, h - 62), (w * 0.5, h - 26)],
                  fill="white")
        d.polygon([(w * 0.55, h - 26), (w * 0.72, h - 52), (w * 0.9, h - 26)],
                  fill=(230, 240, 245))
        d.rectangle([10, 8, 34, 22], fill=(200, 20, 40))
        d.rectangle([10, 13, 34, 17], fill="white")
        d.rectangle([20, 8, 24, 22], fill="white")
        _flag(d, w - 36, 8, 26, 14, "us")
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
        d.rectangle([w - 16, 8, w - 8, h - 30], fill="white", outline=INK)
        for i in range(0, h - 38, 10):
            d.rectangle([w - 16, 8 + i, w - 8, 8 + i + 5], fill=INK)
    elif key == "riyadh":
        d.rectangle([0, 0, w, h], fill=(10, 20, 50))
        _skyline(d, w, h, h - 30, (6, 12, 34), 11)
        # missile trail from top right + explosion star
        d.line([w - 12, 6, w - 60, 34], fill=(255, 220, 120), width=3)
        cx, cy = w - 62, 36
        for a in range(0, 360, 45):
            d.line([cx, cy, cx + int(14 * math.cos(math.radians(a))),
                    cy + int(14 * math.sin(math.radians(a)))],
                   fill=YELLOW, width=3)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 120, 0))
        d.ellipse([w - 14, 4, w - 6, 12], fill=(255, 210, 31))
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
    elif key == "australia":
        d.rectangle([0, 0, w, h], fill=(245, 240, 228))
        vals = [0.72, 0.6, 0.62, 0.45, 0.3]
        bw = w // 6
        for i, v in enumerate(vals):
            x = 12 + i * bw
            d.rectangle([x, h - 14 - int(v * (h - 30)), x + bw - 6, h - 14],
                        fill=(200, 40, 40) if i == len(vals) - 1 else (90, 90, 90))
        d.line([(12, 22), (w - 12, h - 22)], fill=RED, width=3)
        # gauge needle at 4.9% + -44,000 ledger line (both above the scrim)
        d.arc([w - 56, 4, w - 8, 52], 180, 360, fill=NAVY, width=2)
        d.line([w - 32, 28, w - 16, 14], fill=RED, width=2)
        d.text((w - 32, 32), "4.9%", font=F_SRC, fill=NAVY, anchor="ma")
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

    # ---- masthead 0-108: date in the top-1 face (Liberation Serif Bold = Times) ----
    d.rectangle([12, 8, 86, 80], fill=RED)
    d.text((49, 12), "NOV", font=F_DATE2, fill="white", anchor="ma")
    d.text((49, 26), "19", font=F_DATE, fill="white", anchor="ma")
    d.text((49, 60), "THU \u00b7 2026", font=F_DATE2, fill="white", anchor="ma")
    d.text((98, 1), "THE WORLD IN ONE DAY", font=F_EYE, fill=RED)
    d.line([98, 20, 1012, 20], fill=INK, width=1)
    draw_tracked(d, 98, 13, "Thursday 19 November 2026", F_TITLE, INK, 839)
    d.text((98, 83), "Trump, Xi and Putin share one table \u00b7 World Court finds "
           "Myanmar guilty of genocide \u00b7 COP31's draft drops fossil fuels",
           font=F_DECKLINE, fill=RED)
    d.text((1012, 1), "36 STORIES \u00b7 7 REGIONS \u00b7 ONE PAGE",
           font=F_EYE, fill=INK, anchor="ra")
    d.rectangle([0, 108, W, 111], fill=GOLD)

    # ---- big-numbers strip 110-148 ----
    sw6 = (W - 24) / 6.0
    for si, (val, cap) in enumerate(STATS):
        sx = 12 + si * sw6
        if si > 0:
            d.line([sx - 6, 116, sx - 6, 148], fill=RULE, width=1)
        d.text((sx + 4, 114), val, font=F_STATB, fill=NAVY)
        d.text((sx + 4, 136), cap, font=F_STATC, fill=GREY)

    # ---- THE DAY BY HOURS timeline 154-186 ----
    d.rectangle([12, 154, 100, 186], fill=RED)
    d.text((56, 155), "THE DAY", font=F_TTIME, fill="white", anchor="ma")
    d.text((56, 169), "BY HOURS", font=F_TTIME, fill="white", anchor="ma")
    bx = 104
    bw = (W - 12 - bx) / 8.0
    for i, (t, txt) in enumerate(TIMELINE):
        cx = bx + i * bw
        if i > 0:
            d.line([cx, 156, cx, 184], fill=RULE, width=1)
        d.text((cx + 5, 157), t, font=F_TTIME, fill=NAVY)
        d.text((cx + 5, 169), txt, font=F_TTEXT, fill=INK)
    d.line([12, 188, W - 12, 188], fill=RULE, width=1)

    # ---- heroes 191-373: lead 396 wide, rails 294 (hierarchy, not equal thirds) ----
    hy = 191
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
        d.text((cx + 10 + pw, hy + 97), "%d  %s \u00b7 %s" % (num, reg, topic),
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

    # ---- smalls 379-705 (2 rows x 5, image 196x84) ----
    sw_ = 196
    for r in range(2):
        for c in range(5):
            k = 3 + r * 5 + c
            num, reg, topic, src, status, head, deck, big, small, key = FRONT[k]
            cx = 12 + c * (sw_ + 8)
            cy = 379 + r * 166
            im = art_image(key, sw_, 84)
            idd = ImageDraw.Draw(im)
            art_text(im, idd, 0, 0, sw_, 84, big, small, F_LBL2, F_LBL2_S)
            img.paste(im, (cx, cy))
            d.rectangle([cx, cy + 84, cx + sw_, cy + 99], fill=NAVY)
            d.text((cx + 4, cy + 85), "%d  %s \u00b7 %s" % (num, reg, topic),
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

    # ---- map + also 711-951 (map taller, also-list roomier) ----
    my = 711
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
        d.text((x, y), "%d" % num, font=F_ALSO_N, fill=RED)
        full = "%s: %s" % (city, txt)
        lines = wrap(d, full, F_ALSO, colw - 22, max_lines=1)
        d.text((x + 20, y), lines[0] if lines else "", font=F_ALSO, fill=INK)

    # ---- date check 963-991: thin 2-line band (was a 40px box) ----
    dy = 963
    d.rectangle([12, dy, 1012, dy + 28], outline=RED, width=2)
    chk = ("DATE CHECK \u2014 Left out, first reported Wednesday 18 November: Iranian drone "
           "interceptions \u00b7 EU's \u20ac45bn loan \u00b7 House 251\u201311 Jeffries vote \u00b7 "
           "Voyager 1, one light-day out \u00b7 Peltola's Alaska win \u00b7 "
           "Qeshm strikes (17 Nov) \u00b7 Van Gogh's $190.4m sale. Not yet news: Akvan's landfall "
           "(Fri 20 Nov) \u00b7 COP31's final deal (Fri 20 Nov).")
    clines = wrap(d, chk, F_DATECHK, 976, max_lines=2)
    for j, ln in enumerate(clines):
        d.text((20, dy + j * 12), ln, font=F_DATECHK, fill=INK)

    # ---- footer 997-1020 ----
    fy = 997
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
