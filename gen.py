# gen.py — renders entry.png for news-image-20261126 (b176, numbers)
# Thursday 26 November 2026. 1024x1024, 50 stories, 10 regions.
# Layout (fresh variant): masthead + DATE CHECK strip; 3 hero columns;
# timeline strip; 10 cards 5x2; bottom split ALSO (left) + world map (right).
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
FD = "/usr/share/fonts/truetype/dejavu"

def font(sz, bold=False):
    return ImageFont.truetype(os.path.join(FD, "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), sz)

def tw(draw, s, f):
    b = draw.textbbox((0, 0), s, font=f)
    return b[2] - b[0], b[3] - b[1]

def wrap(draw, s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if tw(draw, t, f)[0] <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines

def rects_overlap(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])

def draw_lines(draw, lines, f, x, y, fill, lh, maxw=None, box=None):
    """Draw wrapped lines; assert text stays inside box with >=2px margin."""
    yy = y
    for ln in lines:
        w, h = tw(draw, ln, f)
        if maxw is not None:
            assert w <= maxw, "line too wide: %r (%d > %d)" % (ln, w, maxw)
        if box is not None:
            assert x >= box[0] + 2 and x + w <= box[2] - 2, "text x outside box: %r" % ln
            assert yy >= box[1] + 2 and yy + h <= box[3] - 2, "text y outside box: %r" % ln
        draw.text((x, yy), ln, font=f, fill=fill)
        yy += lh
    return yy

# ---- palette ----
NAVY = (13, 27, 62)
NAVY2 = (24, 48, 96)
GOLD = (201, 162, 39)
GOLD_BG = (246, 226, 150)
INK = (18, 18, 18)
PAPER = (250, 248, 242)
CARD = (255, 255, 255)
RED = (178, 34, 34)
BLUE = (23, 84, 160)
TEAL = (14, 110, 110)
GREY = (90, 90, 90)
LINE = (200, 200, 200)
LAND = (196, 214, 176)
SEA = (168, 205, 225)

# ---- content ----
HEROES = [
    dict(kicker="NEW YORK \u00b7 [C]", tag="[C]",
         head=["MACY'S 100TH PARADE", "POSTPONED BY STORM"],
         deck="Thanksgiving parade delayed by high winds, a first in its 100-year history.",
         why="WHY IT MATTERS: America's most iconic Thanksgiving parade moves to Saturday, and balloon safety rules face a rethink.",
         stat="100TH EDITION \u00b7 SAT 28 NOV 08:30 ET \u00b7 60 MPH",
         art="balloon", accent=RED),
    dict(kicker="STRAIT OF HORMUZ \u00b7 [CL]", tag="[CL]",
         head=["IRGC CLAIMS TWO TANKERS", "HIT BY MINES"],
         deck="Iran claims two tankers exploded after striking mines in the strait; one supertanker carried over 2 million barrels.",
         why="WHY IT MATTERS: The claim widens the Iran war to the world's key oil chokepoint, and Brent crude rose to $93.8 a barrel.",
         stat="2M BARRELS \u00b7 BRENT $93.8 \u00b7 [CL] UNVERIFIED",
         art="tanker", accent=(150, 60, 10)),
    dict(kicker="GLOBAL MARKETS \u00b7 [C]", tag="[C]",
         head=["TRUMP TARIFFS:", "MARKETS REBOUND"],
         deck="European and Asian stocks rose as the tariff salvo looked milder than feared.",
         why="WHY IT MATTERS: The rebound eases fears of a global trade shock from duties on 14 partners, with China facing 20%.",
         stat="STOXX +1.6% \u00b7 MSCI +0.4% \u00b7 14 PARTNERS",
         art="chart", accent=TEAL),
]

CARDS = [
    ("GAZA", "[C]", "HAMAS EDUCATION DEPUTY KILLED IN GAZA STRIKE",
     "Israeli strike on Deir al-Balah kills Abu Nada and his wife.",
     "DEIR AL-BALAH \u00b7 OVERNIGHT"),
    ("KYIV", "[C]", "BALLISTIC MISSILE HITS KYIV MALL",
     "Russian strike on Desnianskyi mall wounds 7 as 113 drones hit.",
     "7 HURT \u00b7 113 DRONES"),
    ("BOGOR", "[C]", "BOGOR MINE FLOOD: 13 DEAD, 13 MISSING",
     "Illegal gold mine floods in Bogor after heavy rain, trapping miners.",
     "13 DEAD \u00b7 13 MISSING"),
    ("JERUSALEM", "[R]", "JUDGE URGES NETANYAHU BRIBERY CHARGE DROPPED",
     "Judge urges prosecutors to drop Case 4000, the bribery count.",
     "CASE 4000 \u00b7 WEDNESDAY"),
    ("PYONGYANG", "[R]", "KIM TOURS NUCLEAR PLANT, PUSHES TACTICAL NUKES",
     "Kim visits a nuclear-materials plant, urges tactical nukes.",
     "KCNA \u00b7 THURSDAY"),
    ("WASHINGTON", "[C]", "FCC CLEARS SPACEX 1M SATELLITE DATA NETWORK",
     "US approves SpaceX Starmind, up to one million orbital modules.",
     "APPROVED 25 NOV \u00b7 FCC"),
    ("LONDON", "[C]", "UK NET MIGRATION FALLS TO 77,000",
     "Net migration falls to 77,000, lowest since 1997, ONS says.",
     "77,000 \u00b7 LOWEST SINCE 1997"),
    ("MOSCOW", "[R]", "RUSSIA APPROVES RECORD MILITARY BUDGET",
     "Moscow signs off its biggest post-Soviet defence budget.",
     "RECORD POST-SOVIET BUDGET"),
    ("BANGKOK", "[C]", "BANGKOK OIL DEPOT BLAST HURTS 7",
     "Explosion at a Bangkok oil depot injures seven, triggers evacuation.",
     "7 HURT \u00b7 FIRE OUT IN ~30 MIN"),
    ("COLOGNE", "[C]", "2 HELD OVER GERMAN SYNAGOGUE PLOT",
     "Two Iraqi suspects held in Cologne and Heidelberg over a plot.",
     "COLOGNE + HEIDELBERG"),
]

ALSO = [
    "Philadelphia parade cancelled in storm [C]",
    "NYC bars balloons over 23 mph sustained wind [C]",
    "Two Italians killed in Iranian drone attack in Kuwait [C]",
    "UN rights chief Turk warns of Gaza atrocities [R]",
    "Couple aged 37 and 38 killed in Kharkiv flat [C]",
    "18 wounded in Kryvyi Rih strike [C]",
    "Ukraine hits Savasleyka base; 5 jets damaged [R]",
    "Subkhankulovo pumping station ablaze in Bashkortostan [R]",
    "Cargo ship near Odesa reportedly hit [R]",
    "Eisenkot seals first Israel coalition deal [R]",
    "Merz warns Russia aims beyond Ukraine [R]",
    "UK on alert over drone threat to airbases [R]",
    "Norse Atlantic halts all flights, warns of bankruptcy [C]",
    "Poundland in administration; 11,000 jobs at risk [C]",
    "Malaysia sues Google for $146m [C]",
    "Kenya court halts US-backed Ebola facility [C]",
    "Belarus offers to fly Zelensky to Moscow; he declines [R]",
    "Kushner calls Putin 'grandmaster of politics' [C]",
    "Estonia decides to close border [C]",
    "Copernicus confirms longest stretch above 2C warming [C]",
    "Nvidia halts AI server shipments to 4 countries [R]",
    "Bitcoin funds post record $4.94bn monthly outflows [C]",
    "Jazan refinery hit by projectile; 1 Nepal worker killed [C]",
    "Trump urges Putin to 'pull back all military aggression' [C]",
    "Slavyansk-ECO refinery hit by drone; serious damage [R]",
    "UKMTO 222-26: blast 50 nm west of Dubai, 25 Nov [CL]",
    "UKMTO 223-26: tanker hit 18 nm east of Khasab, 25 Nov [CL]",
    "Houthi claim strike on Ras Tanura refinery, 25 Nov [CL]",
    "Tariff hearings set 25 Jan; duties will not stack on July tariffs [R]",
    "Wall Street shut for Thanksgiving; futures up 0.5% [C]",
    "Russia claims drone sites hit in Kyiv strike [CL]",
    "Guinea-Bissau delays elections to 2028 [C]",
    "Starmind modules carry AI chips in orbit [C]",
    "Netanyahu recommendation came on Wednesday [R]",
    "Gold $3,572 an ounce, down 0.2% Thursday [C]",
    "German synagogue plot targeted late March [C]",
    "Strikes go on despite year-old Gaza ceasefire [C]",
]
assert len(ALSO) == 37, len(ALSO)

DATE_L1 = "DATE CHECK \u2014 NOT 26 NOV: COP31 failed (22 Nov) \u00b7 Shenzhou-24 launch (25 Nov) \u00b7 Cairo tanker, 31 dead (25 Nov)"
DATE_L2 = "Cartagena hostages freed (25 Nov) \u00b7 Australia\u2013Solomon pact (25 Nov) \u00b7 UK energy +26% (25 Nov) \u00b7 Huawei convicted (24 Nov)"

# ---- world map: lon/lat polygons, equirectangular lon -170..190, lat 75..-55 ----
N_AMER = [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66), (-80, 73),
          (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35), (-80, 32), (-85, 30),
          (-90, 21), (-95, 19), (-100, 16), (-105, 20), (-110, 23), (-115, 28), (-120, 34),
          (-125, 40), (-125, 48), (-135, 58), (-150, 60), (-165, 60)]
GREENLAND = [(-58, 64), (-45, 60), (-40, 64), (-32, 68), (-25, 70), (-20, 74), (-30, 76),
             (-45, 76), (-58, 74)]
S_AMER = [(-80, 10), (-75, 11), (-62, 10), (-52, 5), (-50, 0), (-40, -5), (-35, -8),
          (-40, -20), (-48, -28), (-55, -35), (-62, -41), (-68, -50), (-70, -55), (-73, -50),
          (-73, -40), (-72, -30), (-70, -18), (-77, -12), (-80, -5)]
EUROPE = [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (3, 53), (8, 57), (10, 59),
          (5, 60), (12, 62), (18, 69), (25, 71), (30, 70), (40, 68), (48, 66), (48, 60),
          (40, 55), (35, 50), (30, 46), (28, 44), (23, 40), (22, 37), (26, 38), (30, 36),
          (36, 36), (33, 41), (28, 45), (23, 44), (19, 42), (15, 44), (12, 45), (8, 44),
          (3, 42), (0, 40), (-2, 37), (-6, 36)]
AFRICA = [(-17, 15), (-16, 20), (-10, 31), (-5, 35), (0, 36), (10, 37), (11, 34), (20, 32),
          (30, 31), (32, 31), (35, 28), (37, 22), (40, 15), (43, 11), (48, 11), (51, 10),
          (46, 5), (40, -2), (40, -10), (36, -18), (32, -26), (28, -33), (20, -35),
          (16, -28), (12, -18), (12, -8), (9, 4), (4, 6), (-8, 5), (-13, 8), (-17, 12)]
ASIA = [(38, 70), (50, 68), (60, 66), (68, 68), (75, 72), (85, 74), (95, 76), (105, 76),
        (115, 73), (125, 71), (135, 71), (145, 71), (155, 69), (160, 66), (162, 60),
        (158, 55), (150, 59), (142, 55), (140, 50), (138, 45), (134, 43), (130, 42),
        (127, 40), (126, 38), (122, 37), (120, 34), (121, 30), (120, 26), (116, 23),
        (110, 20), (108, 15), (105, 9), (103, 7), (100, 6), (98, 9), (95, 15), (92, 21),
        (89, 22), (86, 20), (83, 18), (80, 14), (77, 8), (75, 12), (72, 20), (68, 23),
        (66, 25), (61, 25), (58, 25), (56, 26), (53, 27), (50, 29), (48, 30), (45, 29),
        (42, 29), (39, 28), (37, 27), (35, 29), (34, 31), (35, 36), (36, 36), (33, 40),
        (30, 44), (28, 48), (30, 55), (32, 60), (34, 65), (36, 68)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)]
JAPAN = [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (140, 39), (141, 41),
         (142, 44), (140, 45), (138, 40), (136, 37), (133, 35), (131, 33)]
SUMATRA = [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (104, -5), (100, -1), (97, 3)]
JAVA = [(105, -5), (108, -6), (111, -6), (114, -7), (114, -10), (111, -9), (108, -9), (105, -7)]
BORNEO = [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (113, -4), (110, -3)]
SULAWESI = [(119, 0), (121, 1), (123, 0), (121, -2), (120, -4), (119, -2)]
NEWGUINEA = [(131, -1), (136, -2), (141, -3), (146, -6), (147, -8), (142, -8), (137, -6), (132, -4)]
AUSTRALIA = [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
             (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
             (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
             (136, -12), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)]
NZ = [(167, -45), (170, -43), (174, -41), (176, -38), (174, -36), (172, -40), (168, -44)]
MADAG = [(44, -16), (47, -15), (50, -16), (49, -20), (47, -25), (44, -25), (43, -20)]
ARABIA = [(44, 29), (41, 27), (39, 24), (38, 20), (36, 16), (34, 13), (36, 12),
          (40, 13), (44, 13), (48, 14), (52, 15), (56, 17), (59, 22), (60, 24),
          (58, 26), (56, 27), (53, 27), (50, 28), (48, 29), (46, 29)]
CONTINENTS = [N_AMER, GREENLAND, S_AMER, EUROPE, AFRICA, ASIA, ARABIA, UK, JAPAN,
              SUMATRA, JAVA, BORNEO, SULAWESI, NEWGUINEA, AUSTRALIA, NZ, MADAG]

# pins: (num, label, lon, lat, true-lon, true-lat or None) — offset pins get leader lines
PINS = [
    (1, "NEW YORK \u2014 Macy's parade", -74, 40.7, None, None),
    (2, "LONDON \u2014 UK migration", -3, 54, -0.1, 51.5),
    (3, "COLOGNE \u2014 synagogue plot", 12, 54, 7, 50.9),
    (4, "KYIV \u2014 mall missile", 28, 49, 30.5, 50.4),
    (5, "MOSCOW \u2014 military budget", 42, 58, 37.6, 55.7),
    (6, "GAZA \u2014 Hamas official killed", 34.5, 31.5, None, None),
    (7, "KHASAB \u2014 Hormuz mines claim", 56.3, 26.2, None, None),
    (8, "JAZAN \u2014 refinery attack", 42.5, 16.9, None, None),
    (9, "BANGKOK \u2014 oil depot blast", 100.5, 13.7, None, None),
    (10, "BOGOR \u2014 mine flood", 106.8, -6.6, None, None),
    (11, "NAIROBI \u2014 Ebola facility halt", 36.8, -1.3, None, None),
    (12, "KRASNODAR \u2014 refinery drone hit", 43, 47, 39, 45.1),
]

def project(lon, lat, mx, my, mw, mh):
    x = mx + (lon + 170.0) / 360.0 * mw
    y = my + (75.0 - lat) / 130.0 * mh
    return x, y

# ---- hero art, drawn on a layer clipped to the art box (never touches text) ----
def art_balloon(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(135, 178, 214))
    d.rectangle((x0, y1 - 14, x1, y1), fill=(52, 58, 64))  # street
    for bx in (x0 + 12, x0 + 78, x0 + 150, x0 + 216, x0 + 282):
        d.rectangle((bx, y1 - 62, bx + 34, y1 - 14), fill=(70, 76, 84))
        for wy in range(y1 - 56, y1 - 18, 12):
            d.rectangle((bx + 5, wy, bx + 13, wy + 6), fill=(250, 220, 90))
            d.rectangle((bx + 20, wy, bx + 28, wy + 6), fill=(250, 220, 90))
    # clouds
    for cx, cy in ((x0 + 40, y0 + 14), (x0 + 250, y0 + 24), (x0 + 170, y0 + 8)):
        d.ellipse((cx, cy, cx + 46, cy + 12), fill=(255, 255, 255))
    # balloon: big red envelope + basket
    d.ellipse((x0 + 108, y0 + 4, x0 + 222, y0 + 72), fill=(198, 40, 40))
    d.ellipse((x0 + 128, y0 + 4, x0 + 202, y0 + 72), fill=(220, 70, 50))
    d.line((x0 + 150, y0 + 68, x0 + 146, y0 + 80), fill=(60, 60, 60), width=2)
    d.line((x0 + 180, y0 + 68, x0 + 184, y0 + 80), fill=(60, 60, 60), width=2)
    d.rectangle((x0 + 142, y0 + 80, x0 + 188, y0 + 100), fill=(120, 72, 30))
    d.ellipse((x0 + 30, y0 + 44, x0 + 82, y0 + 80), fill=(40, 90, 160))  # small balloon

def art_tanker(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(30, 38, 52))
    d.rectangle((x0, y1 - 34, x1, y1), fill=(18, 60, 84))  # sea
    for i in range(5):
        d.arc((x0 + 10 + i * 64, y1 - 44, x0 + 50 + i * 64, y1 - 16), 180, 360, fill=(120, 180, 210))
    d.polygon([(x0 + 30, y1 - 34), (x0 + 300, y1 - 34), (x0 + 285, y1 - 60), (x0 + 45, y1 - 60)],
              fill=(90, 30, 26))  # hull
    d.rectangle((x0 + 200, y1 - 92, x0 + 252, y1 - 60), fill=(210, 210, 200))  # superstructure
    d.rectangle((x0 + 214, y1 - 108, x0 + 224, y1 - 92), fill=(180, 180, 170))
    # flames + smoke, kept inside box
    for fx, fh in ((x0 + 70, 34), (x0 + 120, 46), (x0 + 165, 28)):
        d.polygon([(fx, y1 - 60), (fx + 14, y1 - 60 - fh), (fx + 28, y1 - 60)], fill=(240, 140, 20))
        d.polygon([(fx + 7, y1 - 60), (fx + 14, y1 - 60 - fh + 14), (fx + 21, y1 - 60)], fill=(250, 210, 60))
    d.ellipse((x0 + 96, y0 + 6, x0 + 128, y0 + 30), fill=(120, 120, 120))
    d.ellipse((x0 + 150, y0 + 2, x0 + 186, y0 + 26), fill=(100, 100, 100))
    # mine in water
    d.ellipse((x0 + 262, y1 - 26, x0 + 282, y1 - 6), fill=(20, 20, 20))
    for dx, dy in ((-8, 0), (8, 0), (0, -8), (-6, -6), (6, -6)):
        d.line((x0 + 272 + dx, y1 - 16 + dy, x0 + 272, y1 - 16), fill=(20, 20, 20), width=2)

def art_chart(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(232, 240, 244))
    for gy in range(y0 + 18, y1 - 10, 22):
        d.line((x0 + 8, gy, x1 - 8, gy), fill=(200, 210, 216), width=1)
    bars = [34, 30, 36, 28, 32, 40, 38, 46, 52, 60]
    bw = (x1 - x0 - 24) // len(bars)
    for i, v in enumerate(bars):
        bx = x0 + 12 + i * bw
        col = (180, 60, 50) if v < 34 else (20, 120, 90)
        d.rectangle((bx + 2, y1 - 12 - v, bx + bw - 2, y1 - 12), fill=col)
    pts = [(x0 + 12 + i * bw + bw // 2, y1 - 14 - v) for i, v in enumerate(bars)]
    d.line(pts, fill=(23, 84, 160), width=3)
    for px, py in pts:
        d.ellipse((px - 3, py - 3, px + 3, py + 3), fill=(23, 84, 160))
    d.polygon([(x1 - 62, y0 + 8), (x1 - 40, y0 + 8), (x1 - 40, y0 + 30), (x1 - 62, y0 + 30)],
              fill=(20, 120, 90))
    d.text((x1 - 58, y0 + 12), "+1.6%", font=font(11, True), fill=(255, 255, 255))

ARTS = {"balloon": art_balloon, "tanker": art_tanker, "chart": art_chart}

# ---- render ----
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle((0, 0, W, 62), fill=NAVY)
    d.rectangle((0, 58, W, 62), fill=GOLD)
    d.text((12, 8), "THE WORLD IN ONE DAY", font=font(30, True), fill=(255, 255, 255))
    d.text((12, 42), "50 STORIES  \u00b7  10 REGIONS  \u00b7  ALL FROM THURSDAY 26 NOVEMBER 2026",
           font=font(11, True), fill=GOLD)
    r = d.textbbox((0, 0), "THURSDAY 26 NOVEMBER 2026", font=font(15, True))
    d.text((W - 12 - (r[2] - r[0]), 12), "THURSDAY 26 NOVEMBER 2026", font=font(15, True),
           fill=(255, 255, 255))
    d.text((W - 12 - tw(d, "news-image-20261126", font(11))[0], 40),
           "news-image-20261126", font=font(11), fill=(180, 190, 210))
    # DATE CHECK strip (2 lines)
    d.rectangle((0, 62, W, 98), fill=GOLD_BG)
    d.rectangle((0, 62, W, 98), outline=GOLD, width=1)
    for i, ln in enumerate((DATE_L1, DATE_L2)):
        w, h = tw(d, ln, font(11, True))
        assert w <= W - 16, "DATE CHECK line too wide: %d" % w
        d.text((8, 65 + i * 15), ln, font=font(11, True), fill=(90, 60, 0))
    dc = (DATE_L1 + " " + DATE_L2)
    for need in ("COP31", "Shenzhou-24", "Cairo", "31 dead", "Cartagena",
                 "Australia", "Solomon", "+26%", "Huawei", "24 Nov", "22 Nov"):
        assert need in dc, "DATE CHECK missing: %s" % need
    assert "Ras Tanura" not in dc and "Riyadh" not in dc
    assert "Trump tariffs announced 25 Nov" not in dc

    # heroes: 3 columns
    hero_boxes = []
    for i, hro in enumerate(HEROES):
        x = 8 + i * 336
        y = 104
        box = (x, y, x + 330, y + 268)
        hero_boxes.append(box)
        d.rectangle(box, fill=CARD, outline=LINE, width=1)
        art_box = (x + 1, y + 1, x + 329, y + 119)
        layer = Image.new("RGBA", (328, 118), (0, 0, 0, 0))
        ARTS[hro["art"]](ImageDraw.Draw(layer), (0, 0, 328, 118))
        img.paste(layer, (x + 1, y + 1), layer)
        # kicker badge line (text, below art)
        kick = hro["kicker"]
        kw, kh = tw(d, kick, font(11, True))
        assert kw <= 318
        d.text((x + 8, y + 124), kick, font=font(11, True), fill=hro["accent"])
        # headline (exactly 2 lines, stored)
        yy = draw_lines(d, hro["head"], font(17, True), x + 8, y + 142, INK, 20,
                        maxw=314, box=box)
        assert yy <= y + 184, "hero headline overflow"
        deck_lines = wrap(d, hro["deck"], font(11), 314)
        assert len(deck_lines) <= 2, "hero deck >2 lines: %r" % deck_lines
        deck_top = y + 186
        deck_rect = (x + 8, deck_top, x + 8 + max(tw(d, ln, font(11))[0] for ln in deck_lines),
                     deck_top + 14 * len(deck_lines))
        kick_rect = (x + 8, y + 124, x + 8 + kw, y + 124 + kh)
        assert not rects_overlap(deck_rect, kick_rect), "deck overlaps badge"
        draw_lines(d, deck_lines, font(11), x + 8, deck_top, (40, 40, 40), 14,
                   maxw=314, box=box)
        # WHY IT MATTERS (2 lines, complete sentences)
        why_lines = wrap(d, hro["why"], font(10), 314)
        assert len(why_lines) <= 2, "hero WHY >2 lines: %r" % why_lines
        assert hro["why"].rstrip().endswith("."), "WHY must end with a full stop"
        draw_lines(d, why_lines, font(10), x + 8, y + 218, (60, 60, 60), 13,
                   maxw=314, box=box)
        # stat band (solid, below all text)
        d.rectangle((x + 1, y + 250, x + 329, y + 267), fill=hro["accent"])
        sw, sh = tw(d, hro["stat"], font(11, True))
        assert sw <= 322, "hero stat too wide: %d" % sw
        d.text((x + 8, y + 253), hro["stat"], font=font(11, True), fill=(255, 255, 255))
        # art-vs-text: art box ends y+119, first text starts y+124
        assert y + 119 < y + 124

    # timeline strip
    d.rectangle((8, 378, 1016, 402), fill=NAVY2)
    tl = "OVERNIGHT  Kyiv hit  \u00b7  MORNING  Markets rebound  \u00b7  MIDDAY  Hormuz claim  \u00b7  AFTERNOON  Parade moved to Sat  \u00b7  EVENING  Tariff details"
    twl, _ = tw(d, tl, font(10, True))
    assert twl <= 1000
    d.text(((W - twl) // 2, 385), tl, font=font(10, True), fill=(255, 255, 255))

    # cards: 5 cols x 2 rows
    card_boxes = []
    accents = [RED, BLUE, TEAL, (120, 60, 140), (150, 60, 10),
               (20, 120, 90), (23, 84, 160), (90, 90, 90), (178, 34, 34), TEAL]
    for i, (loc, tag, head, deck, stat) in enumerate(CARDS):
        cx = 8 + (i % 5) * 203
        cy = 408 + (i // 5) * 132
        box = (cx, cy, cx + 197, cy + 124)
        card_boxes.append(box)
        d.rectangle(box, fill=CARD, outline=LINE, width=1)
        # mini art band (no text inside it)
        d.rectangle((cx + 1, cy + 1, cx + 196, cy + 29), fill=accents[i])
        for k in range(4):
            bx = cx + 14 + k * 46
            d.rectangle((bx, cy + 18, bx + 26, cy + 29), fill=(255, 255, 255, 90))
        d.ellipse((cx + 168, cy + 7, cx + 188, cy + 27), fill=(255, 255, 255))
        # kicker with literal tag
        kick = "%s \u00b7 %s" % (loc, tag)
        d.text((cx + 8, cy + 33), kick, font=font(10, True), fill=accents[i])
        head_lines = wrap(d, head, font(11, True), 181)
        assert len(head_lines) <= 2, "card head >2 lines: %r" % head_lines
        draw_lines(d, head_lines, font(11, True), cx + 8, cy + 49, INK, 13,
                   maxw=181, box=box)
        deck_lines = wrap(d, deck, font(10), 181)
        assert len(deck_lines) <= 2, "card deck >2 lines: %r" % deck_lines
        draw_lines(d, deck_lines, font(10), cx + 8, cy + 79, (40, 40, 40), 12,
                   maxw=181, box=box)
        sw, _ = tw(d, stat, font(9, True))
        assert sw <= 181, "card stat too wide: %r" % stat
        d.text((cx + 8, cy + 106), stat, font=font(9, True), fill=accents[i])
    return img, d, hero_boxes, card_boxes

def render_bottom(img, d, card_boxes):
    # ALSO panel (left) + map panel (right)
    also_box = (8, 670, 648, 986)
    map_box = (656, 670, 1016, 986)
    assert not rects_overlap(also_box, map_box)
    for cb in card_boxes:
        assert not rects_overlap(map_box, cb), "map overlaps a card"
        assert not rects_overlap(also_box, cb), "ALSO overlaps a card"
    d.rectangle(also_box, fill=CARD, outline=LINE, width=1)
    d.text((16, 676), "ALSO ON 26 NOVEMBER", font=font(12, True), fill=NAVY)
    d.line((16, 694, 640, 694), fill=GOLD, width=2)
    PREPS = {"in", "on", "at", "of", "to", "for", "by", "with", "from"}
    cols = [ALSO[i::3] for i in range(3)]  # 13 / 12 / 12
    assert sum(len(c) for c in cols) == 37
    for ci, col in enumerate(cols):
        cx = 16 + ci * 208
        for ri, item in enumerate(col):
            ry = 700 + ri * 22
            assert "[C]" in item or "[R]" in item or "[CL]" in item, "ALSO missing tag: %r" % item
            core = item.rsplit("[", 1)[0].strip()
            assert core.split()[-1].lower().strip(".,") not in PREPS, "ALSO ends with preposition: %r" % item
            if "25 Nov" in item:
                assert "[CL]" in item, "25 Nov ALSO item must be [CL]: %r" % item
            lines = wrap(d, "\u2022 " + item, font(10), 200)
            assert len(lines) <= 2, "ALSO >2 lines: %r" % item
            assert len(lines) >= 1
            yy = ry
            for ln in lines:
                w, _ = tw(d, ln, font(10))
                assert w <= 200, "ALSO line too wide: %r" % ln
                d.text((cx, yy), ln, font=font(10), fill=INK)
                yy += 11
    # map panel
    d.rectangle(map_box, fill=(255, 255, 255), outline=LINE, width=1)
    d.text((664, 676), "WORLD MAP \u2014 12 PINS", font=font(12, True), fill=NAVY)
    d.line((664, 694, 1008, 694), fill=GOLD, width=2)
    mx, my, mw, mh = 656, 700, 360, 190
    d.rectangle((mx, my, mx + mw, my + mh), fill=SEA)
    mask = Image.new("L", (mw, mh), 0)
    md = ImageDraw.Draw(mask)
    for poly in CONTINENTS:
        pts = [project(lon, lat, mx, my, mw, mh) for lon, lat in poly]
        rel = [(px - mx, py - my) for px, py in pts]
        md.polygon(rel, fill=255)
        d.polygon(pts, fill=LAND, outline=(120, 150, 110))
    # Java drawn thick so it stays visible
    jx0, jy0 = project(105, -7.5, mx, my, mw, mh)
    jx1, jy1 = project(114, -7.5, mx, my, mw, mh)
    d.line((jx0, jy0, jx1, jy1), fill=LAND, width=7)
    # pins
    PR = 6
    centers = []
    for num, label, lon, lat, tlon, tlat in PINS:
        px, py = project(lon, lat, mx, my, mw, mh)
        assert mx + 2 + PR <= px <= mx + mw - 2 - PR, "pin %d x outside panel" % num
        assert my + 2 + PR <= py <= my + mh - 2 - PR, "pin %d y outside panel" % num
        assert mask.getpixel((int(px - mx), int(py - my))) > 0, "pin %d not on land" % num
        centers.append((px, py))
        if tlon is not None:
            tx, ty = project(tlon, tlat, mx, my, mw, mh)
            d.line((px, py, tx, ty), fill=RED, width=1)
            d.ellipse((tx - 2, ty - 2, tx + 2, ty + 2), fill=RED)
        d.ellipse((px - PR, py - PR, px + PR, py + PR), fill=RED, outline=(255, 255, 255), width=1)
        s = str(num)
        sw, sh = tw(d, s, font(8, True))
        d.text((px - sw / 2, py - sh / 2 - 1), s, font=font(8, True), fill=(255, 255, 255))
    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            dx = centers[i][0] - centers[j][0]
            dy = centers[i][1] - centers[j][1]
            assert (dx * dx + dy * dy) ** 0.5 >= 2 * PR + 2, "pins %d/%d too close" % (i + 1, j + 1)
    # legend lists every pin
    for i, (num, label, lon, lat, tlon, tlat) in enumerate(PINS):
        lx = 664 + (i // 6) * 178
        ly = 898 + (i % 6) * 14
        s = "%d %s" % (num, label)
        w, _ = tw(d, s, font(9))
        assert w <= 174, "legend too wide: %r" % s
        d.text((lx, ly), s, font=font(9), fill=INK)
    # footer
    d.rectangle((0, 992, W, H), fill=NAVY)
    ft = "Sources: Reuters \u00b7 AP \u00b7 BBC \u00b7 CNN \u00b7 KCNA \u00b7 ONS \u00b7 FCC \u2014 All stories 26 Nov 2026 unless noted"
    fw, _ = tw(d, ft, font(9))
    assert fw <= W - 16
    d.text(((W - fw) // 2, 1002), ft, font=font(9), fill=(200, 205, 215))

if __name__ == "__main__":
    import hashlib
    img, d, hb, cb = render()
    render_bottom(img, d, cb)
    assert img.size == (1024, 1024)
    img.save(OUT, optimize=True)
    data = open(OUT, "rb").read()
    assert len(data) <= 1024 * 1024, "entry.png over 1 MiB: %d" % len(data)
    print("stories=%d regions=10" % (3 + len(CARDS) + len(ALSO)))
    print("entry.png %dx%d %d bytes sha256=%s" % (1024, 1024, len(data),
                                                  hashlib.sha256(data).hexdigest()))
