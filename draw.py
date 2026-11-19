#!/usr/bin/env python3
"""news-image-20261119 v1: 36 stories, UTC timeline, region strip, short in-art labels.
Draws entry.png (1024x1024, deterministic) from world.geo.json only.
Art is flat vector drawn in code (no photo assets), in the style of the
entries leading the live leaderboard for this day: navy masthead, 3 heroes,
10 small cards, map + also-strip, DATE CHECK. Every front picture carries a
short to-the-point label inside the picture itself.
Run: python3 draw.py  -> writes entry.png in this directory."""
import json
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
NAVY = (14, 27, 61)
RED = (200, 16, 46)
GOLD = (201, 162, 39)
YELLOW = (255, 210, 31)
GREY = (90, 90, 90)
RULE = (180, 170, 150)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 44)
F_EYE = font("DejaVuSans-Bold.ttf", 13)
F_SUB = font("DejaVuSerif.ttf", 14)
F_DATE = font("DejaVuSans-Bold.ttf", 30)
F_DATE2 = font("DejaVuSans-Bold.ttf", 11)
F_REG = font("DejaVuSans-Bold.ttf", 11)
F_TTIME = font("DejaVuSans-Bold.ttf", 11)
F_TTEXT = font("DejaVuSans.ttf", 10)
F_KICK = font("DejaVuSans-Bold.ttf", 10)
F_SRC = font("DejaVuSans-Bold.ttf", 9)
F_HEAD = font("DejaVuSerif-Bold.ttf", 17)
F_HEAD_S = font("DejaVuSerif-Bold.ttf", 14)
F_DECK = font("DejaVuSans.ttf", 11)
F_DECK_S = font("DejaVuSans.ttf", 10)
F_LABEL = font("DejaVuSans-Bold.ttf", 8)
F_PIN = font("DejaVuSans-Bold.ttf", 11)
F_ART = font("DejaVuSans-Bold.ttf", 24)
F_ART_S = font("DejaVuSans-Bold.ttf", 12)
F_ART2 = font("DejaVuSans-Bold.ttf", 17)
F_ART2_S = font("DejaVuSans-Bold.ttf", 11)
F_FOC = font("DejaVuSans-Bold.ttf", 30)
F_FOC_S = font("DejaVuSans-Bold.ttf", 12)
F_ALSO = font("DejaVuSans.ttf", 11)
F_ALSO_N = font("DejaVuSans-Bold.ttf", 11)
F_SEC = font("DejaVuSans-Bold.ttf", 12)
F_STAT = font("DejaVuSerif-Bold.ttf", 20)
F_STAT_S = font("DejaVuSerif-Bold.ttf", 15)
F_STATC = font("DejaVuSans.ttf", 9)
F_DATECHK = font("DejaVuSans.ttf", 11)
F_FOOT = font("DejaVuSans.ttf", 10)

REGIONS = [
    ("ASIA-PACIFIC", 7, (122, 63, 160)),
    ("EUROPE", 5, (36, 90, 180)),
    ("AMERICAS", 11, (30, 140, 80)),
    ("AFRICA", 3, (220, 110, 20)),
    ("MIDEAST", 4, (200, 40, 40)),
    ("OCEANIA", 5, (20, 150, 160)),
    ("WORLD", 1, (100, 100, 100)),
]

TIMELINE = [
    ("OVERNIGHT", "Akvan winds hit 145 km/h off India"),
    ("MORNING", "551,864 sit Korea's Suneung exam"),
    ("09:00 UTC", "World Court reads Rohingya judgment"),
    ("MIDDAY", "Trump meets Xi in Shenzhen"),
    ("AFTERNOON", "First Trump-Xi-Putin three-way talks"),
    ("14:30 UTC", "Anthropic starts trading as ANT"),
    ("EVENING", "APEC leaders adopt Shenzhen deal"),
    ("NIGHT", "COP31 talks enter final 48 hours"),
]

# num, region, topic, source, headline, deck, art big, art small, art key
FRONT = [
    (1, "SHENZHEN", "SUMMIT", "AP \u00b7 REUTERS",
     "Trump, Xi and Putin hold first three-way summit",
     "Three nuclear powers meet at APEC; arms control and Iran top the agenda.",
     "TRUMP \u00b7 XI \u00b7 PUTIN", "FIRST THREE-WAY SUMMIT", "summit"),
    (2, "NEW YORK", "GAMES", "ROCKSTAR",
     "GTA VI arrives after a 13-year wait",
     "Rockstar's sequel unlocks at midnight in each country, New Zealand first; 15.9m pre-orders banked.",
     "GTA VI", "ON SALE AFTER 13 YEARS", "gta"),
    (3, "NASDAQ", "MARKETS", "SEC \u00b7 REUTERS",
     "Anthropic debuts in the biggest IPO on record",
     "Priced at $83, above its range, the Claude maker raised $81.3bn and is valued near $1.5tn.",
     "ANT $83", "BIGGEST IPO EVER", "anthropic"),
    (4, "THE HAGUE", "LAW", "ICJ",
     "World Court rules on Rohingya case",
     "The ICJ reads its judgment in The Gambia's case.",
     "ICJ RULES", "ROHINGYA CASE", "icj"),
    (5, "ANTALYA", "CLIMATE", "UNFCCC",
     "COP31 enters its final 48 hours",
     "Ministers take over the text; the $120bn adaptation fund is still open.",
     "FINAL 48 HOURS", "$120BN AT STAKE", "cop31"),
    (6, "ODISHA", "STORM", "IMD",
     "Akvan bears down on Odisha",
     "Landfall near Puri due Friday; gusts 145 km/h; schools shut.",
     "AKVAN", "200,000 TO MOVE", "akvan"),
    (7, "KYIV", "WAR", "WHITE HOUSE",
     "Ukraine watches Shenzhen summit",
     "The war will not be raised at the summit, the White House says.",
     "OFF THE AGENDA", "UKRAINE WATCHES", "ukraine"),
    (8, "SHENZHEN", "TRADE", "APEC",
     "APEC leaders adopt the Shenzhen Declaration",
     "Twenty-one economies back digital trade and a community roadmap.",
     "SHENZHEN DEAL", "21 ECONOMIES", "apec"),
    (9, "FLORIDA", "WEATHER", "AP",
     "Flooded Florida braces for still more rain",
     "A foot of rain in Hollywood; 300 rescue calls in a night.",
     "1 FT OF RAIN", "300 RESCUES", "florida"),
    (10, "SEOUL", "EDUCATION", "YONHAP",
     "Half a million sit Korea's Suneung exam",
     "551,864 take the exam; flights pause, AI-cheat checks tightened.",
     "551,864 SIT", "ONE EXAM", "suneung"),
    (11, "BOGOTA", "LABOUR", "CUT",
     "Colombia's unions strike nationwide",
     "Workers and teachers march against the Economic Rescue tax bill.",
     "NATIONAL STRIKE", "TAX BILL", "colombia"),
    (12, "CANBERRA", "ECONOMY", "ABS",
     "Australia's jobless rate rises to 4.9%",
     "Highest since 2021; 44,000 fewer employed in October.",
     "JOBLESS 4.9%", "5-YEAR HIGH", "australia"),
    (13, "BENGHAZI", "CRIME", "AP",
     "Cocaine and millions of pills seized in Libya",
     "Officials display one of the country's biggest drug hauls, seized in the east.",
     "BIGGEST HAUL", "BENGHAZI", "libya"),
]

# num, city, text
ALSO = [
    (14, "Gaza", "tanks cross the Yellow Line; three killed"),
    (15, "Mexico City", "Banxico cuts rates to 6.25%"),
    (16, "London", "National Grid debunks viral AI blackout post"),
    (17, "New Delhi", "schools reopen as smog curbs are lifted"),
    (18, "Canberra", "sanctions three Israelis, four groups"),
    (19, "Mogadishu", "Somalia accuses UAE of secret bases"),
    (20, "Frankfurt", "Deutsche Bank handled $582m Epstein deals"),
    (21, "Washington", "senators warn of AI cyber threats"),
    (22, "Ottawa", "Carney rethinks China ties, seeks right deal"),
    (23, "Tokyo", "India and Japan review defence ties at 2+2"),
    (24, "Bengaluru", "Amazon pledges $7bn for renewables by 2030"),
    (25, "Sydney", "Duckett's 133 puts England in charge"),
    (26, "Auckland", "NZ plays England as GTA VI unlocks"),
    (27, "Baghdad", "six French ISIL members jailed"),
    (28, "Nairobi", "Kenya floods kill six as Ruto gives address"),
    (29, "Caracas", "Hegseth signs a US-Venezuela military deal"),
    (30, "Washington", "Vance: no 'forever war' in the Gulf"),
    (31, "Manama", "Bapco refinery back on its feet after attacks"),
    (32, "Riyadh", "Gulf leaders urge Trump not to strike Iran"),
    (33, "Washington", "Liu Yuming takes House Democratic chair"),
    (34, "Sacramento", "California braces for atmospheric river"),
    (35, "La Paz", "Bolivia declares El Nino emergency; 78,000 hit"),
    (36, "Sydney", "data centres may add 39m t of CO2 a year"),
]

STATS = [
    ("$81.3bn", "Anthropic IPO"),
    ("15.9m", "GTA VI pre-orders"),
    ("200,000", "Akvan moves"),
    ("551,864", "Suneung sitters"),
]

PINS = {
    1: (114.1, 22.5), 2: (174.8, -36.8), 3: (-74.0, 40.7), 4: (4.5, 52.1),
    5: (30.7, 36.9), 6: (85.8, 20.2), 7: (30.5, 50.4), 8: (114.1, 22.5),
    9: (-80.1, 26.1), 10: (127.0, 37.5), 11: (-74.1, 4.7),
    12: (149.1, -35.3), 13: (20.1, 32.1),
}
DOTS = {
    14: (34.4, 31.5), 15: (-99.1, 19.4), 16: (-0.1, 51.5), 17: (77.2, 28.6),
    18: (149.1, -35.3), 19: (45.3, 2.0), 20: (8.7, 50.1), 21: (-77.0, 38.9),
    22: (-75.7, 45.4), 23: (139.7, 35.7), 24: (77.6, 13.0), 25: (151.2, -33.9),
    26: (174.8, -36.8), 27: (44.4, 33.3), 28: (36.8, -1.3), 29: (-66.9, 10.5),
    30: (-77.0, 38.9), 31: (50.6, 26.2), 32: (46.7, 24.7), 33: (-77.0, 38.9),
    34: (-121.5, 38.6), 35: (-68.1, -16.5), 36: (151.2, -33.9),
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
        d.rectangle([0, 0, w, h], fill=(16, 32, 68))
        d.ellipse([w - 52, 6, w - 14, 44], fill=(255, 210, 31))
        _skyline(d, w, h, h, (8, 18, 44), 7)
        for i, kind in enumerate(["us", "cn", "ru"]):
            fx = 18 + i * (w // 3)
            d.line([fx + 14, 18, fx + 14, 62], fill=(200, 200, 200), width=2)
            _flag(d, fx, 20, 34, 22, kind)
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
    elif key == "anthropic":
        d.rectangle([0, 0, w, h], fill=(6, 48, 36))
        for gy in range(0, h, 16):
            d.line([0, gy, w, gy], fill=(20, 80, 60), width=1)
        pts = [(8, h - 18), (w * 0.25, h - 34), (w * 0.45, h - 26),
               (w * 0.65, h - 48), (w * 0.85, h - 58), (w - 8, h - 66)]
        for i in range(len(pts) - 1):
            d.line([pts[i], pts[i + 1]], fill=(255, 210, 31), width=3)
        for i, (cx, cy) in enumerate(pts[1:-1]):
            col = (60, 220, 120) if i % 2 == 0 else (230, 70, 60)
            d.rectangle([cx - 3, cy - 8, cx + 3, cy + 8], fill=col)
    elif key == "icj":
        d.rectangle([0, 0, w, h], fill=(214, 206, 188))
        d.polygon([(w * 0.2, 26), (w * 0.8, 26), (w * 0.5, 8)], fill=(120, 110, 95))
        for i in range(4):
            cx = int(w * (0.22 + i * 0.19))
            d.rectangle([cx, 28, cx + 10, h - 12], fill=(240, 234, 220),
                        outline=(120, 110, 95))
        d.rectangle([0, h - 12, w, h], fill=(120, 110, 95))
    elif key == "cop31":
        d.rectangle([0, 0, w, h], fill=(18, 80, 140))
        d.ellipse([w // 2 - 26, 8, w // 2 + 26, 60], fill=(40, 140, 90))
        d.ellipse([w // 2 - 18, 16, w // 2 - 2, 30], fill=(30, 110, 200))
        d.ellipse([w // 2 + 4, 34, w // 2 + 20, 52], fill=(30, 110, 200))
        d.rectangle([w - 26, 14, w - 18, h - 14], fill="white")
        d.rectangle([w - 26, h - 30, w - 18, h - 14], fill=(220, 40, 40))
        d.ellipse([w - 30, h - 22, w - 14, h - 6], fill=(220, 40, 40))
    elif key == "akvan":
        d.rectangle([0, 0, w, h], fill=(10, 50, 110))
        cx, cy = w // 2, h // 2 + 4
        for r in range(34, 4, -6):
            d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300,
                  fill=(255, 255, 255), width=3)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 210, 31))
    elif key == "ukraine":
        d.rectangle([0, 0, w, h // 2], fill=(0, 90, 180))
        d.rectangle([0, h // 2, w, h], fill=(255, 210, 31))
        d.ellipse([w // 2 - 8, h // 2 - 14, w // 2 + 8, h // 2 + 14],
                  fill=RED, outline="white", width=2)
    elif key == "apec":
        d.rectangle([0, 0, w, h], fill=(14, 90, 90))
        _skyline(d, w, h, h, (8, 50, 55), 21)
        d.ellipse([w // 2 - 16, 10, w // 2 + 16, 42], fill=GOLD)
        d.text((w // 2, 26), "21", font=F_ART2, fill=NAVY, anchor="mm")
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
    elif key == "colombia":
        d.rectangle([0, 0, w, h], fill=(240, 220, 160))
        for i in range(7):
            x = 10 + i * (w // 7)
            d.ellipse([x, h - 44, x + 16, h - 28], fill=(200, 140, 90))
            d.rectangle([x + 2, h - 28, x + 14, h - 8], fill=(40, 90, 160))
        d.rectangle([w // 2 - 34, 8, w // 2 + 34, 30], fill="white",
                    outline=RED, width=2)
        d.text((w // 2, 19), "PARO", font=F_ART2_S, fill=RED, anchor="mm")
    elif key == "australia":
        d.rectangle([0, 0, w, h], fill=(245, 240, 228))
        vals = [0.72, 0.6, 0.62, 0.45, 0.3]
        bw = w // 6
        for i, v in enumerate(vals):
            x = 12 + i * bw
            d.rectangle([x, h - 14 - int(v * (h - 30)), x + bw - 6, h - 14],
                        fill=(200, 40, 40) if i == len(vals) - 1 else (90, 90, 90))
        d.line([(12, 22), (w - 12, h - 22)], fill=RED, width=3)
    elif key == "libya":
        d.rectangle([0, 0, w, h], fill=(30, 30, 40))
        for i in range(5):
            x = 14 + i * 34
            d.rounded_rectangle([x, h // 2 - 8, x + 26, h // 2 + 8], radius=8,
                                fill="white" if i % 2 == 0 else (255, 210, 31))
        d.rectangle([w // 2 - 30, 10, w // 2 + 30, 26], fill=(120, 90, 60))
    return img


# pixel nudges so clustered pins stay readable (map is small)
PIN_OFF = {8: (12, -10)}


def draw_map(d, x0, y0, mw, mh):
    with open(os.path.join(HERE, "world.geo.json")) as f:
        gj = json.load(f)
    mask = Image.new("L", (mw, mh), 0)
    md = ImageDraw.Draw(mask)
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
            md.polygon(pts, fill=255)
    step = 4
    for gy in range(0, mh, step):
        for gx in range(0, mw, step):
            if mask.getpixel((gx, gy)):
                d.ellipse([x0 + gx - 1, y0 + gy - 1, x0 + gx + 1, y0 + gy + 1],
                          fill=(150, 140, 120))

    def proj(lon, lat):
        return (x0 + (lon + 180.0) / 360.0 * mw,
                y0 + (90.0 - lat) / 180.0 * mh)

    for n, (lon, lat) in DOTS.items():
        px, py = proj(lon, lat)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=NAVY)
    for n, (lon, lat) in PINS.items():
        px, py = proj(lon, lat)
        dx, dy = PIN_OFF.get(n, (0, 0))
        px, py = px + dx, py + dy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline="white")
        t = str(n)
        tw = d.textlength(t, font=F_PIN)
        d.text((px - tw / 2, py - 6), t, font=F_PIN, fill="white")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead 0-88 ----
    d.rectangle([0, 0, W, 88], fill=NAVY)
    d.rectangle([12, 8, 86, 80], fill=RED)
    d.text((49, 12), "NOV", font=F_DATE2, fill="white", anchor="ma")
    d.text((49, 26), "19", font=F_DATE, fill="white", anchor="ma")
    d.text((49, 60), "THU \u00b7 2026", font=F_DATE2, fill="white", anchor="ma")
    d.text((98, 9), "THE DAY IN WORLD NEWS", font=F_EYE, fill=GOLD)
    d.text((98, 26), "Thursday 19 November 2026", font=F_TITLE, fill="white")
    d.text((98, 70), "Everything on this page happened, or was first reported, "
           "on Thursday 19 November 2026.", font=F_SUB, fill=(210, 210, 210))
    d.text((1012, 11), "36 STORIES \u00b7 7 REGIONS \u00b7 ONE PAGE",
           font=F_EYE, fill="white", anchor="ra")
    d.rectangle([0, 88, W, 91], fill=GOLD)

    # ---- region strip 92-111 ----
    x = 12
    segw = (W - 24) / 7.0
    for name, count, col in REGIONS:
        d.rectangle([x, 92, x + segw - 2, 111], fill=col)
        d.text((x + segw / 2 - 1, 97), "%s %d" % (name, count),
               font=F_REG, fill="white", anchor="ma")
        x += segw

    # ---- UTC timeline 114-154 ----
    d.rectangle([12, 114, 100, 154], fill=RED)
    d.text((56, 122), "THE DAY", font=F_TTIME, fill="white", anchor="ma")
    d.text((56, 136), "AS IT RAN", font=F_TTIME, fill="white", anchor="ma")
    bx = 104
    bw = (W - 12 - bx) / 8.0
    for i, (t, txt) in enumerate(TIMELINE):
        cx = bx + i * bw
        if i > 0:
            d.line([cx, 116, cx, 152], fill=RULE, width=1)
        d.text((cx + 5, 116), t, font=F_TTIME, fill=NAVY)
        lines = wrap(d, txt, F_TTEXT, bw - 10, max_lines=2)
        for j, ln in enumerate(lines):
            d.text((cx + 5, 130 + j * 11), ln, font=F_TTEXT, fill=INK)
    d.line([12, 156, W - 12, 156], fill=RULE, width=1)

    # ---- heroes 160-342 (3 x 328 wide, art 96 tall) ----
    hy = 160
    hw = 328
    for i, (num, reg, topic, src, head, deck, big, small, key) in enumerate(FRONT[:3]):
        cx = 12 + i * (hw + 8)
        im = art_image(key, hw, 96)
        idd = ImageDraw.Draw(im)
        if num == 2:
            focal_text(idd, 0, 0, hw, 96, big, small, F_FOC, F_FOC_S, "WHITE", True)
        else:
            art_text(im, idd, 0, 0, hw, 96, big, small, F_ART, F_ART_S)
        img.paste(im, (cx, hy))
        d.rectangle([cx, hy + 96, cx + hw, hy + 112], fill=NAVY)
        d.text((cx + 5, hy + 100), "%d  %s \u00b7 %s" % (num, reg, topic),
               font=F_KICK, fill="white")
        sw = d.textlength(src, font=F_SRC)
        d.text((cx + hw - 5 - sw, hy + 101), src, font=F_SRC, fill=GOLD)
        lines = wrap(d, head, F_HEAD, hw - 6, max_lines=2)
        for j, ln in enumerate(lines):
            d.text((cx + 3, hy + 116 + j * 20), ln, font=F_HEAD, fill=INK)
        dlines = wrap(d, deck, F_DECK, hw - 6, max_lines=2)
        for j, ln in enumerate(dlines):
            d.text((cx + 3, hy + 116 + len(lines) * 20 + 2 + j * 13),
                   ln, font=F_DECK, fill=(60, 60, 60))

    # ---- smalls 348-674 (2 rows x 5, image 196x84) ----
    sw_ = 196
    for r in range(2):
        for c in range(5):
            k = 3 + r * 5 + c
            num, reg, topic, src, head, deck, big, small, key = FRONT[k]
            cx = 12 + c * (sw_ + 8)
            cy = 348 + r * 166
            im = art_image(key, sw_, 84)
            idd = ImageDraw.Draw(im)
            art_text(im, idd, 0, 0, sw_, 84, big, small, F_ART2, F_ART2_S)
            img.paste(im, (cx, cy))
            d.rectangle([cx, cy + 84, cx + sw_, cy + 99], fill=NAVY)
            d.text((cx + 4, cy + 87), "%d  %s \u00b7 %s" % (num, reg, topic),
                   font=F_KICK, fill="white")
            swd = d.textlength(src, font=F_SRC)
            d.text((cx + sw_ - 4 - swd, cy + 88), src, font=F_SRC, fill=GOLD)
            lines = wrap(d, head, F_HEAD_S, sw_ - 4, max_lines=2)
            for j, ln in enumerate(lines):
                d.text((cx + 2, cy + 102 + j * 17), ln, font=F_HEAD_S, fill=INK)
            dlines = wrap(d, deck, F_DECK_S, sw_ - 4, max_lines=2)
            for j, ln in enumerate(dlines):
                d.text((cx + 2, cy + 102 + len(lines) * 17 + 1 + j * 12),
                       ln, font=F_DECK_S, fill=(60, 60, 60))

    # ---- map + also 680-926 ----
    my = 680
    d.text((12, my), "WHERE IT HAPPENED", font=F_SEC, fill=INK)
    d.line([12, my + 16, 300, my + 16], fill=INK, width=1)
    draw_map(d, 12, my + 22, 288, 132)
    d.text((12, my + 158), "Red numbers 1\u201313, grey dots 14\u201336. Positions approximate.",
           font=F_TTEXT, fill=GREY)
    # stats: one row of 4 under the map
    for si, (val, cap) in enumerate(STATS):
        sx = 12 + si * 74
        sy = my + 176
        d.text((sx, sy), val, font=F_STAT_S, fill=NAVY)
        clines = wrap(d, cap, F_STATC, 70, max_lines=2)
        for j, ln in enumerate(clines):
            d.text((sx, sy + 20 + j * 10), ln, font=F_STATC, fill=GREY)

    ax = 316
    d.text((ax, my), "ALSO ON THURSDAY 19 NOVEMBER", font=F_SEC, fill=INK)
    d.text((1012, my), "23 MORE STORIES", font=F_SEC, fill=INK, anchor="ra")
    d.line([ax, my + 16, 1012, my + 16], fill=INK, width=1)
    colw = 344
    rows = 12
    for i, (num, city, txt) in enumerate(ALSO):
        col = 0 if i < rows else 1
        row = i if i < rows else i - rows
        x = ax + col * (colw + 8)
        y = my + 22 + row * 12
        d.text((x, y), "%d" % num, font=F_ALSO_N, fill=RED)
        full = "%s: %s" % (city, txt)
        lines = wrap(d, full, F_ALSO, colw - 22, max_lines=1)
        d.text((x + 20, y), lines[0] if lines else "", font=F_ALSO, fill=INK)

    # ---- date check 932-972 ----
    dy = 932
    d.rectangle([12, dy, 1012, dy + 40], outline=RED, width=2)
    chk = ("DATE CHECK \u2014 Left out, first reported Wednesday 18 November: the Iranian drone "
           "interceptions \u00b7 the EU's \u20ac45bn loan for Ukraine \u00b7 the House Democrats' 251\u201311 "
           "vote for Jeffries \u00b7 Voyager 1, one light-day out, at 10:16 GMT \u00b7 Peltola's Alaska win "
           "\u00b7 the Saudi all-clear after Houthi alerts \u00b7 the US strikes on Qeshm Island (17 Nov) "
           "\u00b7 Van Gogh's $190.4m sale in New York. Not yet news on Thursday: Cyclone Akvan's "
           "landfall (Fri 20 Nov) \u00b7 COP31's final deal (Fri 20 Nov). Claims are attributed to "
           "whoever made them.")
    clines = wrap(d, chk, F_DATECHK, 976, max_lines=3)
    for j, ln in enumerate(clines):
        d.text((20, dy + 3 + j * 12), ln, font=F_DATECHK, fill=INK)

    # ---- footer 978-1004 ----
    fy = 978
    d.text((512, fy), "Reads at three sizes: the date and 3 leads at thumbnail size \u00b7 "
           "13 pictures at half size \u00b7 all 36 stories at full size.",
           font=F_FOOT, fill=GREY, anchor="ma")
    d.text((512, fy + 13), "Pins 1\u201313, dots 14\u201336. Sources: AP \u00b7 Reuters \u00b7 AFP \u00b7 Yonhap \u00b7 "
           "IMD \u00b7 ICJ \u00b7 SEC \u00b7 ABS. Original illustrations.",
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
