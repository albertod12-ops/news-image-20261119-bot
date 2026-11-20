#!/usr/bin/env python3
"""news-image-20261119 v21: 36 stories, newspaper front page after the top 1.
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
v21 vs v20: user order 2026-11-20 16:26 WIB ("tiap gambar dan penjelasan
dikasih garis kotak-kotak seperti di top 1, jadi semua nya sudah jelas per
kotak dan ada jarak, dan font mereka lebih bagus juga, lebih presisi"):
- Every card boxed like top 1 (lb1.png): 1px INK outline around the whole
  card (art + kicker strip + headline + deck), fixed bottom per row so the
  boxes align; 8px paper gutters between cards (existing 8px card spacing)
  + 5-6px gaps between rows. To buy the vertical space: heroes art 96 -> 90
  and smalls art 84 -> 80, smalls start 380 -> 384, map 712 -> 716 (date
  check/footer unchanged). Heroes box bottom hy+186 = 378 (6px gap to
  smalls); smalls box bottom cy+161 (5px gap between rows, 5px to the map).
  Art/strip/pill shifted with the new heights (v17 centring preserved);
  summit flags moved up 6px (y28) so the leaders (now 6px higher) keep
  their 2px gap; RIYADH trail bottom points y80/84 -> y79 (art now 80 tall).
- Fonts, Times like top 1 + the masthead: headlines NotoSerif-Black ->
  LiberationSerif-Bold 20/16 (measured ~18% narrower, so 2-line wraps hold
  with the new 8px text insets); decks NotoSans-Bold -> LiberationSerif
  regular 12/11. Headline/deck text inset 8px inside the box (wrap width
  hw-16 / sw_-16); heroes strip contents also 8px in, smalls strip keeps
  v20's 4px in (measured: "12. CANBERRA · ECONOMY" 130.2px + REPORTED pill
  51.5px would overlap by ~2px at 8px in). Leading: heroes 22/14, smalls
  17/13.
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
F_KICK_S = font("NotoSans-Bold.ttf", 9, FNOTO)  # smalls kicker: 10px made #9 touch the pill (0.3px gap)
F_PILL = font("NotoSans-Bold.ttf", 8, FNOTO)
F_SRC = font("NotoSans-Bold.ttf", 9, FNOTO)
F_STAMP = font("NotoSans-Black.ttf", 12, FNOTO)  # v30: the BANNED stamp, big + bold like the user's reference
F_HEAD = font("LiberationSerif-Bold.ttf", 20, FLIB)
F_HEAD_S = font("LiberationSerif-Bold.ttf", 16, FLIB)
F_DECK = font("LiberationSerif-Regular.ttf", 12, FLIB)
F_DECK_S = font("LiberationSerif-Regular.ttf", 11, FLIB)
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
     "90 minutes, then a 'Declaration on Peace'. Trump and Putin talked Ukraine alone for 40 minutes; Kyiv not in the room.",
     "", "", "summit"),
    (2, "THE HAGUE", "LAW", "ICJ", "REPORTED",
     "World Court: Myanmar committed genocide",
     "First state held liable; 9\u20136, 10,000 killed, reparations ordered.",
     "MYANMAR GUILTY", "9\u20136 \u00b7 FIRST STATE HELD LIABLE", "icj"),
    (3, "ANTALYA", "CLIMATE", "UNFCCC", "REPORTED",
     "COP31 draft drops fossil fuels and $120bn aid goal",
     "Ministers take over for the final 48 hours; $120bn is gone from the draft text.",
     "COP31", "DRAFT DROPS FOSSIL FUELS · $120BN", "cop31"),
    (4, "NEW YORK", "GAMES", "SENSOR TOWER", "REPORTED",
     "GTA VI out after a 13-year wait",
     "Unlocks at midnight, New Zealand first; 15.9m pre-orders.",
     "GTA VI", "METACRITIC 99 \u00b7 $79.99", "gta"),
    (5, "NASDAQ", "MARKETS", "SEC \u00b7 REUTERS", "REPORTED",
     "Anthropic IPO debuts, biggest on record",
     "Priced at $83; $81.3bn tops SpaceX's $75bn record.",
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
     "", "", "greenland"),
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
     "", "", "marathon"),
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
    (31, "Seoul", "551,864 sit exam; flights paused 35 min"),
    (32, "Washington", "Liu Yuming takes House Dem chair"),
    (33, "Brussels", "EU delays methane rules two years"),
    (34, "Benghazi", "cocaine and millions of pills seized"),
    (35, "Paris", "Greens back Mélenchon; left splits"),
    (36, "La Paz", "Bolivia El Niño emergency; 78,000 hit"),
]

STATS = [
    ("3", "presidents, one table"),
    ("$81.3bn", "Anthropic IPO, a record"),
    ("9\u20136", "ICJ genocide vote"),
    ("730,000+", "Rohingya fled in 2017"),
    ("109\u20130", "Danish Arctic vote"),
    ("204,070", "listed to move"),
    ("551,864", "Suneung sitters"),
    ("13 yrs", "since GTA V"),
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
    34: (20.1, 32.1), 35: (2.4, 48.9), 36: (-68.1, -16.5),
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
    """Big short text inside the art: white bold on a dark scrim, bottom-left.
    (v34: if both strings are empty, draw nothing — the Greenland pact
    document already carries its own title, flags and score, so its scrim
    would only cover the red 109-0 box.)"""
    if not big and not small:
        return
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
        cw, ch = w * 0.4, h * 0.55
        d.rectangle([x, y, x + cw, y + ch], fill=(30, 50, 120))
        # (v37 fix: the stars used a FIXED 7px/6px grid that did not scale
        # with the flag — on the small 20x12 Greenland flag the stars
        # spilled out of the canton and covered the whole flag, which is
        # why they looked wrong. Now the stars scale with the canton and
        # stay inside it.)
        r = max(1.0, min(cw, ch) * 0.09)
        for sy in range(3):
            for sx in range(4):
                scx = x + cw * (0.14 + sx * 0.24)
                scy = y + ch * (0.2 + sy * 0.3)
                d.ellipse([scx - r, scy - r, scx + r, scy + r], fill="white")
    elif kind == "cn":
        d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        d.ellipse([x + 3, y + 3, x + 11, y + 11], fill=(255, 222, 0))
        for sx, sy in [(16, 4), (20, 9), (16, 14)]:
            d.ellipse([x + sx, y + sy, x + sx + 4, y + sy + 4], fill=(255, 222, 0))
    elif kind == "ru":
        d.rectangle([x, y, x + w, y + h / 3], fill="white")
        d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 60, 180))
        d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(200, 20, 30))


def stamp(img, x, y, text, angle=-15, font=None):
    """Diagonal red rubber-stamp label (the #1 entry's signature device).

    Draws `text` in red bold caps inside a red outline box on a small
    RGBA tile, rotates it, and pastes it onto `img` at (x, y).
    The text is centred in the box (anchor "mm") — v30 fix: it used to
    sit top-left, so CUT and BANNED read as off-centre in their boxes.
    """
    if font is None:
        font = F_SRC
    tmp = Image.new("RGBA", (1, 1))
    td = ImageDraw.Draw(tmp)
    bbox = td.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad = 4
    sw, sh = tw + pad * 2 + 4, th + pad * 2 + 4
    s = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    sd = ImageDraw.Draw(s)
    # (v29: the user's BANNED-stamp reference has a THICK border, not a
    # hairline — the outline is now 3px, like the reference.)
    sd.rectangle([2, 2, sw - 3, sh - 3], outline=(200, 16, 46, 255), width=3)
    sd.text((sw / 2, sh / 2), text, font=font, fill=(200, 16, 46, 255),
            anchor="mm")
    s = s.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(s, (x, y), s)


def art_image(key, w, h):
    """Flat-vector picture for one front story, drawn in code."""
    img = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(img)
    if key == "summit":
        # (v36: TOTAL rebuild of the people. The v35 leaders were too small
        # and the skyline + big "SHENZHEN 12:45" text squeezed them — the
        # user said they still don't look like the top-1. Now the art is
        # just the three men, big like the top-1: plain dark-blue bg, no
        # skyline, no clock, no focal text (the kicker strip already says
        # SHENZHEN), large flags on gold poles, a thin white table.)
        d.rectangle([0, 0, w, h], fill=(22, 52, 110))
        # three large flags on GOLD poles, centred behind each leader
        for i in range(3):
            cx = int(w * (0.22 + i * 0.28))
            d.line([cx - 35, 6, cx - 35, 78], fill=GOLD, width=3)
            d.ellipse([cx - 38, 2, cx - 32, 8], fill=GOLD)
        _flag(d, 52, 8, 70, 44, "us")
        _flag(d, 163, 8, 70, 44, "cn")
        _flag(d, 274, 8, 70, 44, "ru")
        # a thin white table at the very bottom (v36 fix 2: the first
        # rebuild put the table at y82, too low for the 16px nameplate
        # text — it clipped at the art's bottom edge. The table is back
        # at y72 so the nameplates + text fit inside the 90px art.)
        d.rectangle([w * 0.06, h - 18, w * 0.94, h - 6], fill="white")
        d.line([w * 0.06, h - 18, w * 0.94, h - 18], fill=GOLD, width=2)
        for i in range(3):
            cx = int(w * (0.22 + i * 0.28))
            # broad navy suit — shoulders wider than the head, tall enough
            # to read as a chest, not a stick (v36 fix: the first rebuild
            # hid the body behind the big head + the table)
            d.polygon([(cx - 28, h - 18), (cx + 28, h - 18), (cx + 16, 48),
                       (cx - 16, 48)], fill=(25, 50, 110))
            # white shirt collar + coloured tie
            d.polygon([(cx - 6, 48), (cx + 6, 48), (cx, 56)], fill="white")
            tie_col = ((200, 16, 46) if i == 0 else
                       ((180, 30, 30) if i == 1 else (100, 120, 140)))
            d.polygon([(cx - 3, 52), (cx + 3, 52), (cx, 66)], fill=tie_col)
            # BIG round head (36px, like top-1)
            d.ellipse([cx - 18, 12, cx + 18, 48], fill=(230, 200, 160))
            # dot eyes + a small smile
            d.ellipse([cx - 8, 30, cx - 4, 34], fill=(20, 20, 20))
            d.ellipse([cx + 4, 30, cx + 8, 34], fill=(20, 20, 20))
            d.arc([cx - 5, 36, cx + 5, 42], 0, 180, fill=(20, 20, 20),
                  width=2)
            # hair, big and unmistakable: Trump gold quiff, Xi black cap,
            # Putin grey buzz
            if i == 0:
                d.ellipse([cx - 18, 8, cx + 18, 22], fill=(232, 190, 60))
                d.ellipse([cx - 4, 4, cx + 18, 20], fill=(232, 190, 60))
            elif i == 1:
                d.ellipse([cx - 18, 8, cx + 4, 24], fill=(20, 20, 20))
            else:
                d.ellipse([cx - 18, 8, cx + 18, 20], fill=(150, 150, 150))
        # nameplates on the table front, gold like the top-1 entry
        for i, name in enumerate(("TRUMP", "XI", "PUTIN")):
            cx = int(w * (0.22 + i * 0.28))
            d.rectangle([cx - 18, h - 17, cx + 18, h - 7], fill=GOLD)
            d.text((cx, h - 16), name, font=F_LABEL, fill=INK, anchor="ma")
    elif key == "gta":
        for i in range(h):
            t = i / h
            d.line([0, i, w, i], fill=(int(88 + 120 * t), int(40 + 60 * t),
                                       int(140 - 60 * t)))
        # sun, CENTRE: a full disc in the middle of the sky, like a sunset
        # (v33: the user asked for the sun in the middle, not clipped at
        # the right edge)
        d.ellipse([72, 24, 124, 76], fill=(255, 190, 60))
        # palm fronds silhouetted across the sun
        for py in (34, 41, 48):
            d.line([78, py, 118, py], fill=(40, 20, 60), width=1)
        _skyline(d, w, h, h, (10, 5, 20), 11)
        # palm trees, silhouetted against the sunset (v30: the old ones
        # were straight lines radiating from a point — a starburst, not a
        # palm. Now a curved trunk and fronds that arch out and droop.)
        for px in (14, w - 22):
            d.line([(px, h - 15), (px + 2, h - 30), (px + 5, h - 45),
                    (px + 8, h - 58)], fill=(10, 30, 10), width=3)
            cx, cy = px + 8, h - 58
            for dx, dy in ((-19, -8), (-14, -14), (-2, -17), (12, -14),
                           (19, -6), (16, 4)):
                mx, my = cx + dx // 2, cy + dy // 2 - 3
                d.line([(cx, cy), (mx, my), (cx + dx, cy + dy)],
                       fill=(10, 30, 10), width=2)
        # NZ midnight: gold clock top left, PS5 box, 2 fans with hair (not 4 dots)
        d.ellipse([8, 8, 28, 28], fill=GOLD)
        d.line([18, 18, 18, 10], fill=NAVY, width=2)
        d.line([18, 18, 23, 14], fill=NAVY, width=2)
        d.rectangle([173, 58, 195, 72], fill=(10, 10, 30), outline="white", width=1)
        d.text((184, 65), "PS5", font=F_SRC, fill="white", anchor="mm")
        # fan 1: buzz cut (dark cap on the head)
        cx = 118
        d.ellipse([cx - 5, 62, cx + 5, 72], fill=(230, 200, 160))
        d.ellipse([cx - 5, 60, cx + 5, 66], fill=(40, 30, 20))
        d.rectangle([cx - 7, 72, cx + 7, 80], fill=(20, 20, 40))
        # fan 2: long hair (dark shape behind the head, visible at the sides)
        cx = 146
        d.ellipse([cx - 6, 60, cx + 6, 76], fill=(40, 30, 20))
        d.ellipse([cx - 5, 62, cx + 5, 72], fill=(230, 200, 160))
        d.rectangle([cx - 7, 72, cx + 7, 80], fill=(20, 20, 40))
    elif key == "anthropic":
        d.rectangle([0, 0, w, h], fill=(246, 242, 233))
        for gy in range(0, h, 14):
            d.line([0, gy, w, gy], fill=(180, 190, 210), width=1)
        # (v27: the gold bars + arrow read like any chart. The story is the
        # RECORD — $81.3bn topping SpaceX's $75bn — so show the two bars
        # side by side, Anthropic's taller.)
        # Anthropic's record bar, gold, with its number above and name inside
        d.rectangle([45, 22, 85, 70], fill=GOLD)
        d.text((65, 14), "$81.3BN", font=F_ART2_S, fill=RED, anchor="mm")
        d.text((65, 30), "ANT", font=F_ART2_S, fill="white", anchor="mm")
        # SpaceX's bar, shorter, navy, with its number above and name inside
        d.rectangle([115, 34, 155, 70], fill=NAVY)
        d.text((135, 26), "$75BN", font=F_ART2_S, fill=(20, 20, 20),
               anchor="mm")
        d.text((135, 42), "SPACEX", font=F_SRC, fill="white", anchor="mm")
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
        # red divider between the 9 paper and 6 ink columns (the 9-6 vote)
        d.line([213, 40, 213, 74], fill=(179, 34, 44), width=3)
        # Myanmar flag top left (yellow/green/red + white star), white outline
        d.rectangle([12, 8, 38, 13], fill=(254, 203, 0))
        d.rectangle([12, 13, 38, 18], fill=(0, 140, 60))
        d.rectangle([12, 18, 38, 24], fill=(220, 40, 40))
        d.rectangle([12, 8, 38, 24], outline="white", width=1)
        _star(d, 25, 16, 5, 2)
        # gold scales of justice, left, below the flag (the recognisable object)
        d.line([60, 34, 60, 58], fill=GOLD, width=2)
        d.line([44, 38, 76, 38], fill=GOLD, width=2)
        d.polygon([(48, 38), (56, 38), (52, 48)], fill=GOLD)
        d.polygon([(64, 38), (72, 38), (68, 48)], fill=GOLD)
        d.ellipse([56, 58, 64, 64], fill=GOLD)
    elif key == "cop31":
        d.rectangle([0, 0, w, h], fill=(11, 110, 110))
        # THE DRAFT ITSELF: a white document with the two cuts struck through.
        # (v26: the hourglass/globe/thermometer read as abstract symbols;
        # the document says "draft drops" at a glance. v27: every line of
        # text centred in the box, as the user asked.)
        d.rectangle([16, 6, 180, 52], fill="white", outline=(120, 110, 95))
        d.text((98, 10), "COP31 DRAFT", font=F_SRC, fill=(20, 20, 20),
               anchor="ma")
        # (v28 fix: the grey rule lines used to cross the title and the
        # strike lines sat at the text's bottom edge, reading as underlines.
        # The strike lines now run through the MIDDLE of each word.)
        # FOSSIL FUELS struck through in red, centred (73px wide)
        d.text((98, 27), "FOSSIL FUELS", font=F_ART2_S, fill=RED,
               anchor="mm")
        d.line([60, 27, 136, 27], fill=RED, width=2)
        # $120BN struck through in red, centred (41.5px wide)
        d.text((98, 39), "$120BN", font=F_ART2_S, fill=RED, anchor="mm")
        d.line([75, 39, 121, 39], fill=RED, width=2)
        # diagonal CUT stamp on the document, clear of the centred text
        stamp(img, 140, 6, "CUT")
        # a BIG globe + a thermometer, like the top-1 entry (v35: the user
        # asked for both — the planet the deal is about, and the heat it
        # measures. The globe is blue ocean + green continents now, much
        # bigger than the old green disc; the thermometer stands beside it)
        d.ellipse([204, 6, 266, 68], fill=(30, 120, 200),
                  outline=(20, 20, 20), width=2)
        d.ellipse([216, 16, 236, 32], fill=(60, 180, 90))
        d.ellipse([236, 38, 256, 54], fill=(60, 180, 90))
        d.ellipse([214, 44, 226, 56], fill=(60, 180, 90))
        # thermometer: white tube, red fill rising, round bulb, tick marks
        d.rectangle([274, 8, 284, 58], fill="white", outline=(20, 20, 20))
        d.rectangle([276, 24, 282, 58], fill=(220, 30, 40))
        d.ellipse([270, 56, 290, 76], fill=(220, 30, 40),
                  outline=(20, 20, 20))
        for ty in (14, 22, 30, 38, 46, 54):
            d.line([284, ty, 289, ty], fill=(20, 20, 20), width=1)
    elif key == "akvan":
        d.rectangle([0, 0, w, h], fill=(12, 70, 160))
        # (v29: the top-down spiral read as a target. The user's reference
        # is a TORNADO seen from the side — a wide disc on top, a twisting
        # funnel narrowing down to a cloud base. That is the storm now.)
        # the wide disc on top (the cloud top), with an inner oval
        d.ellipse([65, 6, 145, 16], outline="white", width=2)
        d.ellipse([84, 9, 126, 13], outline="white", width=1)
        # the twisting funnel: stacked rings, narrowing as they fall, each
        # offset a little so the funnel reads as turning
        for ry, rw, ro in ((16, 72, 0), (24, 58, 3), (32, 44, -3),
                           (40, 32, 3), (48, 22, -2), (56, 14, 0)):
            cx = 105 + ro
            d.ellipse([cx - rw // 2, ry, cx + rw // 2, ry + 8],
                      outline="white", width=2)
        # the cloud base the funnel touches down into
        for bx, by, bw, bh in ((65, 60, 34, 12), (85, 58, 36, 14),
                               (108, 60, 34, 12)):
            d.ellipse([bx, by, bx + bw, by + bh], fill=(240, 240, 245))
        # the Odisha coast at the bottom; two houses and a yellow arrow
        # showing people moving inland, away from the sea
        d.polygon([(0, 80), (0, 68), (60, 66), (120, 68), (196, 66),
                   (196, 80)], fill=(8, 40, 90))
        for hx in (155, 178):
            d.rectangle([hx, 56, hx + 14, 66], fill=(240, 230, 210))
            d.polygon([(hx, 56), (hx + 14, 56), (hx + 7, 50)],
                      fill=(180, 60, 40))
        d.line([166, 64, 166, 48], fill=YELLOW, width=3)
        d.polygon([(166, 44), (160, 52), (172, 52)], fill=YELLOW)
        # red warning triangle top right
        d.polygon([(179, 4), (189, 24), (169, 24)], fill=RED,
                  outline=(20, 20, 20))
        d.text((179, 14), "!", font=F_ART2_S, fill=YELLOW, anchor="mm")
    elif key == "kerch":
        d.rectangle([0, 0, w, h], fill=(14, 30, 80))
        # (v29: the user's bridge-silhouette reference — a proper suspension
        # bridge: pointed towers, a sagging main cable, vertical suspenders.
        # The middle span is still blown out below it.)
        # water at the bottom
        d.rectangle([0, 64, w, h], fill=(10, 22, 60))
        d.line([0, 68, w, 68], fill=(30, 60, 110), width=1)
        d.line([0, 74, w, 74], fill=(30, 60, 110), width=1)
        # two WIDE flat-topped towers with a crossbeam, like the reference
        # suspension bridge (v32: the v31 spires were still thin and wispy —
        # the reference bridges are BOLD solid silhouettes, so the towers
        # are 12px wide now, the cable is a thick band, the deck is thick)
        for tx in (34, 166):
            d.rectangle([tx, 6, tx + 12, 44], fill=(225, 225, 225))
            d.rectangle([tx - 3, 14, tx + 15, 18], fill=(225, 225, 225))
        # the main suspension cable: side spans + a deep sagging span
        # between the tower tops (lowest at the middle, y32) — a THICK
        # white band now, so it reads as part of the silhouette
        d.line([(8, 42), (40, 6)], fill="white", width=4)
        d.line([(40, 6), (56, 18), (70, 26), (84, 30), (98, 32),
                (112, 30), (126, 26), (140, 18), (156, 10), (172, 6)],
               fill="white", width=4)
        d.line([(172, 6), (188, 42)], fill="white", width=4)
        # vertical suspenders from the cable down to the intact deck
        for sx, sy in ((56, 18), (70, 26), (84, 30), (98, 32), (180, 24)):
            d.line([sx, sy, sx, 40], fill="white", width=2)
        # gold deck, left and right of the blown-out middle span — thicker
        d.rectangle([8, 40, 120, 47], fill=(255, 205, 40))
        d.rectangle([160, 40, 188, 47], fill=(255, 205, 40))
        # the blown-out span, collapsed into the water (dark red, jagged)
        d.polygon([(120, 40), (160, 40), (150, 52), (140, 62), (130, 52)],
                  fill=(120, 30, 30))
        d.line([120, 40, 140, 62], fill=(200, 60, 40), width=2)
        d.line([160, 40, 140, 62], fill=(200, 60, 40), width=2)
        # explosion burst + smoke rising from the break
        d.ellipse([132, 34, 148, 50], fill=(255, 160, 40))
        d.ellipse([136, 38, 144, 46], fill=(255, 220, 80))
        d.ellipse([138, 22, 150, 34], fill=(200, 200, 200))
        d.ellipse([148, 12, 162, 26], fill=(220, 220, 220))
        d.ellipse([158, 4, 172, 18], fill=(235, 235, 235))
        # halted 3-car train on the left deck, headlight on, + a figure by the gap
        d.rectangle([20, 34, 36, 40], fill=(180, 30, 30))
        d.rectangle([38, 32, 54, 40], fill=(200, 40, 40))
        d.rectangle([56, 34, 72, 40], fill=(180, 30, 30))
        d.ellipse([50, 35, 54, 39], fill=GOLD)
        d.ellipse([110, 32, 114, 36], fill=(230, 200, 160))
        d.line([112, 36, 112, 40], fill=(20, 20, 20), width=2)
    elif key == "han":
        d.rectangle([0, 0, w, h], fill=NAVY)
        # the overturned sentence, big and unmistakable: "15 YEARS" with a
        # red PROHIBITION sign over it (v30: the user's circular-BANNED
        # reference — a thick red ring + diagonal bar — replaces the red X;
        # the X hid the digits, the ring frames them)
        # (v28 fix: the X was drawn OVER the text, so its thick arms hid the
        # "1" and the "YEARS". The ring + bar are drawn first and the text
        # sits on top of them — fully readable, still cancelled.)
        d.ellipse([6, 2, 52, 48], outline=RED, width=4)
        d.line([13, 9, 45, 41], fill=RED, width=4)
        d.text((16, 10), "15", font=F_ART, fill=(11, 27, 51))
        d.text((14, 8), "15", font=F_ART, fill="white")
        d.text((14, 34), "YEARS", font=F_ART2_S, fill="white")
        # (v31: the OVERTURNED stamp is gone — the user found its red box
        # and red text distracting and unclear. The prohibition ring over
        # "15 YEARS" already says the sentence is cancelled.)
        # (v32: the art looked empty after the stamp went, so the space now
        # holds the South Korean flag (Taegeukgi) — the news is about a
        # South Korean ex-PM. White field, red-over-blue taegeuk, four
        # black trigrams in the corners.)
        d.rectangle([62, 6, 132, 30], fill="white")
        d.pieslice([89, 10, 105, 26], 180, 360, fill=(205, 33, 52))
        d.pieslice([89, 10, 105, 26], 0, 180, fill=(0, 71, 140))
        d.ellipse([93, 14, 101, 22], fill=(205, 33, 52))
        d.ellipse([93, 14, 101, 22], fill=(0, 71, 140))
        for bx, by in ((66, 9), (122, 9), (66, 22), (122, 22)):
            d.rectangle([bx, by, bx + 8, by + 2], fill=(20, 20, 20))
        # a BIG gold gavel as the court's symbol, top right: head + long
        # handle + striking block (v27: the scales were clutter, removed)
        d.rectangle([140, 30, 168, 36], fill=(91, 58, 30))
        d.line([140, 30, 168, 30], fill=(138, 97, 54), width=1)
        d.rectangle([148, 8, 172, 18], fill=GOLD)
        d.line([160, 18, 148, 30], fill=GOLD, width=4)
    elif key == "greenland":
        # (v36: TOTAL REBUILD. The document + flanking icebergs never read
        # as a scene — the user said rebuild it entirely. Now it is the
        # top-1's scene, our own arrangement: pale sky, a big white
        # mountain, two flags on poles, a red 109-0 box, a small globe.
        # No document, no title box, no scrim — the headline below the art
        # already says "Arctic pact".)
        d.rectangle([0, 0, w, h], fill=(190, 215, 235))
        # navy sea band, waterline at y62
        d.rectangle([0, 62, w, h], fill=NAVY)
        # a smaller mountain behind, left, for depth
        d.polygon([(30, 80), (60, 35), (90, 80)], fill=(220, 230, 240))
        # the BIG white mountain, centre
        d.polygon([(55, 80), (95, 15), (135, 80)], fill="white")
        d.polygon([(95, 15), (135, 80), (120, 80)], fill=(191, 227, 242))
        # Danish flag (left) and US flag (right) on dark poles, top-left
        d.line([10, 8, 10, 32], fill=(20, 20, 20), width=2)
        d.rectangle([12, 10, 32, 22], fill=(200, 20, 40))
        d.rectangle([12, 15, 32, 17], fill="white")
        d.rectangle([20, 10, 22, 22], fill="white")
        d.line([38, 8, 38, 32], fill=(20, 20, 20), width=2)
        _flag(d, 40, 10, 20, 12, "us")
        # the vote, white text in a RED box, top-right (v37: the user asked
        # for "VOTE" to be spelled out — the box now says 109-0 on top and
        # VOTE underneath, so the count reads as a vote at a glance)
        d.rectangle([142, 6, 192, 32], fill=RED)
        d.text((167, 14), "109-0", font=F_ART2_S, fill="white", anchor="mm")
        d.text((167, 26), "VOTE", font=F_SRC, fill="white", anchor="mm")
        # small globe below the vote box, blue + white grid lines
        d.ellipse([160, 36, 180, 56], fill=(30, 120, 200),
                  outline=(20, 20, 20), width=1)
        d.line([170, 36, 170, 56], fill="white", width=1)
        d.line([160, 46, 180, 46], fill="white", width=1)
    elif key == "marathon":
        # (v37: the user said v36 still felt flat — a lone runner + a stamp
        # on plain tan. Now it has a RACE around it: a crowd stand at the
        # top, track lanes under the runner, and speed lines behind him.
        # The "3 YEARS" box + Kenyan flag + big BANNED stamp stay.)
        d.rectangle([0, 0, w, h], fill=(228, 200, 150))
        # crowd stand: a dark band across the top, heads in a row
        d.rectangle([0, 0, w, 16], fill=(40, 40, 60))
        for hx in range(95, 190, 13):
            d.ellipse([hx, 5, hx + 7, 12], fill=(230, 200, 160))
        for hx in range(102, 190, 13):
            d.ellipse([hx, 8, hx + 6, 14], fill=(120, 80, 50))
        # track lanes under the runner
        d.line([0, 48, w, 48], fill=(222, 62, 48), width=2)
        d.line([0, 64, w, 64], fill=(222, 62, 48), width=2)
        # speed lines behind the runner — he is moving fast
        for sy in (30, 40, 50):
            d.line([8, sy, 58, sy], fill="white", width=2)
        # Kenyan flag, small, top-left (on the crowd band)
        d.rectangle([8, 6, 32, 10], fill=(20, 20, 20))
        d.rectangle([8, 10, 32, 11], fill="white")
        d.rectangle([8, 11, 32, 15], fill=(200, 30, 30))
        d.rectangle([8, 15, 32, 16], fill="white")
        d.rectangle([8, 16, 32, 20], fill=(30, 140, 60))
        # the ban, spelled out in a red box, text centred in it
        d.rectangle([36, 6, 84, 20], fill=RED)
        d.text((60, 13), "3 YEARS", font=F_ART2_S, fill="white", anchor="mm")
        # ONE big runner, mid-stride to the right, centre-left
        SKIN = (120, 80, 50)
        d.ellipse([70, 24, 90, 44], fill=SKIN)
        d.ellipse([70, 22, 90, 32], fill=(20, 20, 20))
        d.polygon([(72, 44), (88, 44), (86, 60), (74, 60)], fill=(200, 30, 30))
        d.rectangle([74, 60, 86, 66], fill=(20, 20, 20))
        d.line([74, 46, 62, 38], fill=SKIN, width=4)
        d.line([86, 46, 98, 54], fill=SKIN, width=4)
        d.line([82, 66, 96, 78], fill=SKIN, width=4)
        d.line([78, 66, 64, 78], fill=SKIN, width=4)
        d.rectangle([76, 50, 84, 56], fill="white")
        # ONE big diagonal BANNED stamp, right, like the top-1's
        stamp(img, 118, 16, "BANNED", font=F_STAMP)
    elif key == "riyadh":
        d.rectangle([0, 0, w, h], fill=(10, 20, 50))
        _skyline(d, w, h, h - 30, (6, 12, 34), 11)
        # (v28: the missile now sits right against a tall tower, a split
        # second before impact, with the explosion already starting around
        # it — the interceptor caught it at the building.)
        # a tall tower on the right, the missile's target (lit windows)
        d.rectangle([150, 14, 172, 70], fill=(8, 16, 40))
        for wy in (22, 32, 42, 52, 62):
            for wx in (154, 162):
                d.rectangle([wx, wy, wx + 4, wy + 4], fill=(255, 215, 154))
        # the interceptor's red trail, launched from the ground, bottom-left,
        # climbing all the way to the missile's tail (v33: the user asked
        # for the red line to reach the rocket — it used to stop short)
        d.polygon([(24, 79), (60, 52), (128, 34), (132, 38), (64, 56),
                   (28, 79)], fill=RED)
        # the Houthi missile, SMALL now (v32: the v31 missile was far too
        # big) — about 1/4 the size, and DIAGONAL, its tail following the
        # red interceptor trail's direction (climbing up-right toward the
        # tower), not horizontal. Nose at the tower wall, flame trailing
        # down-left along the red line.
        d.polygon([(150, 22), (143, 25), (143, 30)], fill=(220, 220, 220))
        d.polygon([(143, 25), (145, 30), (133, 36), (131, 31)],
                  fill=(220, 220, 220))
        d.polygon([(133, 31), (129, 27), (135, 33)], fill=(180, 180, 180))
        d.polygon([(133, 36), (129, 40), (135, 35)], fill=(180, 180, 180))
        d.polygon([(132, 33), (118, 40), (133, 36)], fill=(255, 140, 40))
        d.polygon([(132, 33), (124, 37), (133, 35)], fill=(255, 220, 80))
        # the explosion starting around the missile nose: orange burst,
        # yellow core, sparks, smoke and debris
        d.ellipse([140, 12, 160, 32], fill=(255, 140, 40))
        d.ellipse([145, 17, 155, 27], fill=(255, 220, 80))
        for a in range(0, 360, 30):
            d.line([150, 22, 150 + int(12 * math.cos(math.radians(a))),
                    22 + int(12 * math.sin(math.radians(a)))],
                   fill=YELLOW, width=2)
        d.ellipse([132, 6, 144, 16], fill=(200, 200, 200))
        d.ellipse([160, 2, 172, 12], fill=(180, 180, 180))
        for dx, dy in ((126, 16), (168, 34), (134, 36), (164, 38)):
            d.rectangle([dx, dy, dx + 2, dy + 2], fill=(255, 200, 100))
        # small warm city dots along the base
        for dx in (30, 70, 110, 150, 180):
            d.ellipse([dx, 74, dx + 2, 76], fill=(255, 215, 154))
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
        # (v26: a static row of figures did not say "march". Now they walk,
        # in stride, down a road, carrying the PARO NACIONAL banner.)
        # road at the bottom, with a dashed centre line
        d.rectangle([0, 66, w, h], fill=(120, 110, 100))
        for dx in range(6, w, 20):
            d.line([dx, 73, dx + 10, 73], fill="white", width=2)
        # the PARO NACIONAL banner, carried on two poles at the front:
        # wider (96px) so the 75px text has real breathing room, and the
        # text placed by exact measurement so it is pixel-centred (v27)
        d.line([108, 10, 108, 34], fill=(60, 40, 20), width=2)
        d.line([188, 10, 188, 34], fill=(60, 40, 20), width=2)
        d.rectangle([100, 10, 196, 28], fill="white", outline=RED, width=2)
        d.text((148, 19), "PARO NACIONAL", font=F_SRC, fill=RED,
               anchor="mm")
        # FECODE banner, top-left, widened the same way
        d.rectangle([8, 8, 70, 24], fill=NAVY)
        d.text((39, 16), "FECODE", font=F_SRC, fill="white", anchor="mm")
        # five marchers walking right, in stride, shirts in varied colours
        skins = [(200, 140, 90), (220, 180, 140), (180, 120, 80),
                 (210, 160, 110), (190, 130, 85)]
        shirts = [(40, 90, 160), (200, 40, 40), (30, 140, 80),
                  (220, 170, 40), (90, 60, 140)]
        for i, x in enumerate((18, 52, 86, 120, 154)):
            d.ellipse([x, 34, x + 12, 46], fill=skins[i])
            d.ellipse([x + 3, 39, x + 5, 41], fill=(20, 20, 20))
            d.ellipse([x + 7, 39, x + 9, 41], fill=(20, 20, 20))
            d.rectangle([x + 1, 46, x + 11, 58], fill=shirts[i])
            # stride: one leg forward, one back
            d.line([x + 4, 58, x + 10, 68], fill=(20, 20, 20), width=2)
            d.line([x + 8, 58, x + 2, 68], fill=(20, 20, 20), width=2)
            # marchers 2 and 4 hold a placard up on a stick
            if i in (1, 3):
                d.line([x + 10, 50, x + 14, 34], fill=(60, 40, 20), width=2)
                d.rectangle([x + 6, 26, x + 20, 36], fill="white",
                            outline=INK)
    elif key == "australia":
        d.rectangle([0, 0, w, h], fill=(245, 240, 228))
        # (v26: four abstract bars did not say "people lost jobs". Now the
        # rate is a big red number, and a row of people — two in red — are
        # the ones who lost their jobs.)
        # the jobless rate, big and red, top-left (like top 1's "4.9%")
        d.text((8, 4), "4.9%", font=F_ART, fill=RED)
        # -44,000 in a bold red box, top-right
        d.rectangle([140, 4, 190, 20], fill=RED)
        d.text((165, 12), "-44,000", font=F_SRC, fill="white", anchor="mm")
        # red arrow climbing (the rate rising), clear of the big number
        d.line([(70, 50), (180, 26)], fill=RED, width=3)
        d.polygon([(180, 26), (162, 24), (174, 38)], fill=RED)
        # a row of six people; the 3rd and 5th are in red (job losses)
        for i, x in enumerate((16, 44, 72, 100, 128, 156)):
            col = RED if i in (2, 4) else NAVY
            d.ellipse([x, 52, x + 10, 62], fill=(200, 140, 90))
            d.rectangle([x + 1, 62, x + 9, 74], fill=col)
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
    sw6 = (W - 24) / len(STATS)
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

    # ---- heroes 192-378: lead 396 wide, rails 294; each card boxed like top 1 ----
    hy = 192
    hws = [396, 294, 294]
    for i, (num, reg, topic, src, status, head, deck, big, small, key) in enumerate(FRONT[:3]):
        hw = hws[i]
        cx = 12 + sum(hws[:i]) + 8 * i
        im = art_image(key, hw, 90)
        idd = ImageDraw.Draw(im)
        if key == "summit":
            focal_text(idd, 0, 0, hw, 90, big, small, F_FOC23, F_FOC23_S, "YELLOW", True)
        elif key == "gta":
            focal_text(idd, 0, 0, hw, 90, big, small, F_FOC, F_FOC_S, "WHITE", True)
        else:
            art_text(im, idd, 0, 0, hw, 90, big, small, F_LBL, F_LBL_S)
        img.paste(im, (cx, hy))
        d.rectangle([cx, hy + 90, cx + hw, hy + 106], fill=NAVY)
        pw = d.textlength(status, font=F_PILL) + 10
        d.rounded_rectangle([cx + 8, hy + 93, cx + 8 + pw, hy + 103],
                            radius=2, fill=PILL_COL[status])
        d.text((cx + 13, hy + 92), status, font=F_PILL, fill="white")
        d.text((cx + 14 + pw, hy + 91), "%d. %s \u00b7 %s" % (num, reg, topic),
               font=F_KICK, fill="white")
        sw = d.textlength(src, font=F_SRC)
        d.text((cx + hw - 8 - sw, hy + 91), src, font=F_SRC, fill=GOLD)
        lines = wrap(d, head, F_HEAD, hw - 16, max_lines=2)
        for j, ln in enumerate(lines):
            d.text((cx + 8, hy + 110 + j * 22), ln, font=F_HEAD, fill=INK)
        dlines = wrap(d, deck, F_DECK, hw - 16, max_lines=2)
        for j, ln in enumerate(dlines):
            d.text((cx + 8, hy + 110 + len(lines) * 22 + 2 + j * 14),
                   ln, font=F_DECK, fill=(60, 60, 60))
        # box around the whole card, like top 1 (1px ink, fixed bottom per row)
        d.rectangle([cx, hy, cx + hw, hy + 186], outline=INK, width=1)

    # ---- smalls 384-711 (2 rows x 5, image 196x80); each card boxed like top 1 ----
    sw_ = 196
    for r in range(2):
        for c in range(5):
            k = 3 + r * 5 + c
            num, reg, topic, src, status, head, deck, big, small, key = FRONT[k]
            cx = 12 + c * (sw_ + 8)
            cy = 384 + r * 166
            im = art_image(key, sw_, 80)
            idd = ImageDraw.Draw(im)
            art_text(im, idd, 0, 0, sw_, 80, big, small, F_LBL2, F_LBL2_S)
            img.paste(im, (cx, cy))
            d.rectangle([cx, cy + 80, cx + sw_, cy + 95], fill=NAVY)
            d.text((cx + 4, cy + 81), "%d. %s \u00b7 %s" % (num, reg, topic),
                   font=F_KICK_S, fill="white")
            pw = d.textlength(status, font=F_PILL) + 10
            d.rounded_rectangle([cx + sw_ - 4 - pw, cy + 82, cx + sw_ - 4, cy + 92],
                                radius=2, fill=PILL_COL[status])
            d.text((cx + sw_ + 1 - pw, cy + 81), status, font=F_PILL, fill="white")
            lines = wrap(d, head, F_HEAD_S, sw_ - 16, max_lines=2)
            for j, ln in enumerate(lines):
                d.text((cx + 8, cy + 99 + j * 17), ln, font=F_HEAD_S, fill=INK)
            dlines = wrap(d, deck + " \u2014 " + src, F_DECK_S, sw_ - 16, max_lines=2)
            for j, ln in enumerate(dlines):
                d.text((cx + 8, cy + 99 + len(lines) * 17 + 1 + j * 13),
                       ln, font=F_DECK_S, fill=(60, 60, 60))
            d.rectangle([cx, cy, cx + sw_, cy + 161], outline=INK, width=1)

    # ---- map + also 716-956 (map taller, also-list roomier) ----
    my = 716
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
