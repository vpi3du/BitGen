#!/usr/bin/env python3
import os
from dataclasses import dataclass
from typing import List, Tuple

try:
    import cairosvg  # type: ignore
except Exception:
    cairosvg = None

OUTPUT_DIR = "/workspace/frank_stickers/output"
ASSETS_DIR = "/workspace/frank_stickers"

# Base colors (from brief)
COLOR_BEIGE = "#E7D3B5"
COLOR_SEDLE = "#B99B72"
COLOR_MASK = "#3A2E2A"
COLOR_NOSE = "#1E1A19"
COLOR_EYE = "#2B201D"
COLOR_OUTLINE = "#1B1716"
COLOR_TONGUE = "#E67C73"
COLOR_TONGUE_HIGHLIGHT = "#F6B1A9"
ACCENT_YELLOW = "#FFC857"
ACCENT_BLUE = "#7EC8E3"
ACCENT_LIME = "#A7E07E"

SVG_SIZE = 512  # px
PADDING = int(SVG_SIZE * 0.06)


def ensure_dirs() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def svg_header() -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_SIZE}" height="{SVG_SIZE}" viewBox="0 0 {SVG_SIZE} {SVG_SIZE}">\n'


def svg_footer() -> str:
    return "</svg>\n"


def outline(style: str = "") -> str:
    base = f"stroke:{COLOR_OUTLINE};stroke-width:6;stroke-linecap:round;stroke-linejoin:round;fill:none;{style}"
    return base


def fill_outline(fill: str) -> str:
    return f"fill:{fill};stroke:{COLOR_OUTLINE};stroke-width:6;stroke-linecap:round;stroke-linejoin:round;"


def small_outline(fill: str) -> str:
    return f"fill:{fill};stroke:{COLOR_OUTLINE};stroke-width:3;stroke-linecap:round;stroke-linejoin:round;"


@dataclass
class StickerSpec:
    slug: str
    label: str
    accessories: List[str]
    # simple flags to tweak expression/pose
    tongue_out: bool = False
    asleep: bool = False
    wink: bool = False
    head_tilt: int = 0  # degrees
    snow: bool = False
    rope: bool = False
    car_window: bool = False


SPECS: List[StickerSpec] = [
    StickerSpec("01_hi", "гав-привет", ["party_hat"], head_tilt=10),
    StickerSpec("02_stop", "Остань, кожаная", ["paw_stop"]),
    StickerSpec("03_hug", "Хочу обнимашки", ["paws_up"], head_tilt=-8),
    StickerSpec("04_food", "Сыпь корм и уходи", ["bowl"]),
    StickerSpec("05_sleep", "Работа идёт, работник спит", ["helmet"], asleep=True),
    StickerSpec("06_reflect", "Сияю как зарплата", ["reflective_jacket"], tongue_out=True),
    StickerSpec("07_snow", "Зима — норм", [], snow=True, tongue_out=True),
    StickerSpec("08_rope", "За канат — до конца!", [], rope=True),
    StickerSpec("09_taxi", "Уже подъезжаю", [], car_window=True),
    StickerSpec("10_kiss", "Чмок-чмок!", ["hearts"], tongue_out=True),
    StickerSpec("11_yawn", "Трудно быть лапочкой", [], wink=True),
    StickerSpec("12_business", "Связи решают", ["bowtie", "mustache_heart"]),
]


# Geometry helpers

def group(transform: str, content: str) -> str:
    return f'<g transform="{transform}">{content}</g>'


def text(x: int, y: int, content: str) -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="DejaVu Sans, Arial, sans-serif" '
        f'font-size="36" font-weight="700" text-anchor="middle" '
        f'fill="{COLOR_OUTLINE}" stroke="white" stroke-width="0">{content}</text>'
    )


# Core pug drawing

def draw_pug(core_scale: float = 1.0, head_tilt: int = 0, tongue_out: bool = False, asleep: bool = False, wink: bool = False) -> str:
    # Positioned roughly center
    cx, cy = SVG_SIZE // 2, SVG_SIZE // 2 + 20
    scale = core_scale
    parts: List[str] = []

    # Body
    body = (
        f'<ellipse cx="{cx}" cy="{cy + 70}" rx="{160*scale}" ry="{120*scale}" style="{fill_outline(COLOR_BEIGE)}"/>'
        f'<path d="M {cx-140*scale},{cy+20} Q {cx},{cy-20} {cx+140*scale},{cy+20}" style="{fill_outline(COLOR_SEDLE)}"/>'
    )
    parts.append(body)

    # Tail (curl)
    tail = f'<path d="M {cx+160*scale},{cy+40} q 40,-20 20,-60 q -30,-40 -70,-5" style="{outline()}"/>'
    parts.append(tail)

    # Head group with tilt
    head: List[str] = []
    # Head base
    head.append(f'<ellipse cx="0" cy="0" rx="130" ry="110" style="{fill_outline(COLOR_BEIGE)}"/>')
    # Mask
    head.append(f'<path d="M -85,0 q 85,-70 170,0 q -35,80 -135,80 q -35,-25 -50,-80 z" style="{fill_outline(COLOR_MASK)}"/>')
    # Wrinkles
    head.append(f'<path d="M -70,-40 q 70,-30 140,0" style="{outline()}"/>')
    head.append(f'<path d="M -60,-20 q 60,-20 120,0" style="{outline()}"/>')

    # Ears
    head.append(f'<path d="M -90,-60 q -40,40 0,70 q 20,5 40,-10 q -15,-20 -10,-60 z" style="{fill_outline(COLOR_MASK)}"/>')
    head.append(f'<path d="M 90,-60 q 40,40 0,70 q -20,5 -40,-10 q 15,-20 10,-60 z" style="{fill_outline(COLOR_MASK)}"/>')

    # Eyes
    if asleep:
        head.append(f'<path d="M -40,-5 q 20,15 40,0" style="{outline()}"/>')
        head.append(f'<path d="M 40,-5 q -20,15 -40,0" style="{outline()}"/>')
    else:
        # Left eye
        head.append(f'<circle cx="-35" cy="-5" r="18" style="{small_outline(COLOR_EYE)}"/>')
        head.append('<circle cx="-30" cy="-10" r="6" fill="#FFFFFF"/>')
        # Right eye (wink if needed)
        if wink:
            head.append(f'<path d="M 15,-5 q 20,8 40,0" style="{outline()}"/>')
        else:
            head.append(f'<circle cx="35" cy="-5" r="18" style="{small_outline(COLOR_EYE)}"/>')
            head.append('<circle cx="30" cy="-10" r="6" fill="#FFFFFF"/>')

    # Nose & mouth
    head.append(f'<ellipse cx="0" cy="20" rx="26" ry="20" style="{small_outline(COLOR_NOSE)}"/>')
    head.append(f'<path d="M 0,40 q -15,10 -30,0" style="{outline()}"/>')
    head.append(f'<path d="M 0,40 q 15,10 30,0" style="{outline()}"/>')

    if tongue_out and not asleep:
        head.append(f'<path d="M -15,44 q 15,26 30,0 q 5,22 -15,30 q -20,-8 -15,-30 z" style="{small_outline(COLOR_TONGUE)}"/>')
        head.append(f'<circle cx="0" cy="64" r="4" fill="{COLOR_TONGUE_HIGHLIGHT}"/>')

    head_group = group(f"translate({cx},{cy-60}) rotate({head_tilt})", "".join(head))
    parts.append(head_group)

    # Front paws
    paws = (
        f'<ellipse cx="{cx-70}" cy="{cy+150}" rx="36" ry="22" style="{fill_outline(COLOR_BEIGE)}"/>'
        f'<ellipse cx="{cx+70}" cy="{cy+150}" rx="36" ry="22" style="{fill_outline(COLOR_BEIGE)}"/>'
    )
    parts.append(paws)

    return "".join(parts)


# Accessories and scene elements

def draw_party_hat(cx: int, cy: int) -> str:
    hat = []
    hat.append(f'<path d="M {cx-30},{cy-210} L {cx},{cy-300} L {cx+30},{cy-210} Z" style="{fill_outline(ACCENT_BLUE)}"/>')
    # simple butterflies as colored shapes
    hat.append(f'<circle cx="{cx}" cy="{cy-250}" r="6" fill="{ACCENT_YELLOW}"/>')
    hat.append(f'<rect x="{cx-12}" y="{cy-240}" width="24" height="10" fill="{ACCENT_LIME}" transform="rotate(-20 {cx} {cy-235})"/>')
    return "".join(hat)


def draw_stop_paw(cx: int, cy: int) -> str:
    return f'<g><ellipse cx="{cx+160}" cy="{cy+90}" rx="30" ry="22" style="{fill_outline(COLOR_BEIGE)}"/><text x="{cx+160}" y="{cy+98}" font-family="DejaVu Sans" font-size="18" text-anchor="middle">✋</text></g>'


def draw_paws_up(cx: int, cy: int) -> str:
    return (
        f'<ellipse cx="{cx-120}" cy="{cy+60}" rx="28" ry="20" style="{fill_outline(COLOR_BEIGE)}"/>'
        f'<ellipse cx="{cx+120}" cy="{cy+60}" rx="28" ry="20" style="{fill_outline(COLOR_BEIGE)}"/>'
    )


def draw_bowl(cx: int, cy: int) -> str:
    return f'<g><ellipse cx="{cx}" cy="{cy+180}" rx="80" ry="26" style="{fill_outline(ACCENT_YELLOW)}"/><text x="{cx}" y="{cy+188}" font-family="DejaVu Sans" font-size="18" text-anchor="middle">🍖</text></g>'


def draw_helmet(cx: int, cy: int) -> str:
    return f'<path d="M {cx-70},{cy-130} q 70,-50 140,0 l 0,20 l -140,0 z" style="{fill_outline(ACCENT_YELLOW)}"/>'


def draw_reflective_jacket(cx: int, cy: int) -> str:
    jacket = []
    jacket.append(f'<path d="M {cx-150},{cy+40} q 150,-40 300,0 l 0,120 l -300,0 z" style="{fill_outline("#F0F0F0")}"/>')
    jacket.append(f'<path d="M {cx-140},{cy+70} L {cx+140},{cy+70}" style="{outline("stroke-width:2; stroke:#888;")}"/>')
    jacket.append(f'<path d="M {cx-120},{cy+100} L {cx+120},{cy+100}" style="{outline("stroke-width:2; stroke:#888;")}"/>')
    return "".join(jacket)


def draw_snow(cx: int, cy: int) -> str:
    return f'<g><ellipse cx="{cx}" cy="{cy+210}" rx="220" ry="40" fill="#FFFFFF" opacity="0.9"/><circle cx="{cx-100}" cy="{cy+120}" r="6" fill="#FFFFFF"/><circle cx="{cx+80}" cy="{cy+110}" r="6" fill="#FFFFFF"/></g>'


def draw_rope(cx: int, cy: int) -> str:
    return f'<path d="M {cx-140},{cy+20} C {cx-60},{cy+10} {cx+60},{cy+10} {cx+140},{cy+20}" style="stroke:#A87C4F; stroke-width:10; fill:none; stroke-linecap:round; stroke-dasharray:6 6"/>'


def draw_car_window(cx: int, cy: int) -> str:
    x, y = cx-200, cy-40
    return f'<g><rect x="{x}" y="{y}" width="400" height="120" rx="16" ry="16" fill="#B7C7D3" opacity="0.45" stroke="#6A7B86" stroke-width="4"/></g>'


def draw_hearts(cx: int, cy: int) -> str:
    return f'<g fill="#FF6B6B" stroke="{COLOR_OUTLINE}" stroke-width="2"><path d="M {cx-140},{cy-40} c -12,-16 8,-36 24,-20 c 16,-16 36,4 24,20 c -10,12 -24,18 -24,18 c 0,0 -14,-6 -24,-18 z"/><path d="M {cx+140},{cy-40} c -12,-16 8,-36 24,-20 c 16,-16 36,4 24,20 c -10,12 -24,18 -24,18 c 0,0 -14,-6 -24,-18 z"/></g>'


def draw_bowtie(cx: int, cy: int) -> str:
    return f'<g><path d="M {cx-30},{cy+40} l -40,20 l 40,20 z" style="{fill_outline(ACCENT_BLUE)}"/><rect x="{cx-10}" y="{cy+45}" width="20" height="30" style="{fill_outline(ACCENT_YELLOW)}"/><path d="M {cx+30},{cy+40} l 40,20 l -40,20 z" style="{fill_outline(ACCENT_BLUE)}"/></g>'


def draw_mustache_heart(cx: int, cy: int) -> str:
    return f'<g stroke="{COLOR_OUTLINE}" stroke-width="4" fill="none"><path d="M {cx-50},{cy+30} q 30,30 50,0"/><path d="M {cx+50},{cy+30} q -30,30 -50,0"/><circle cx="{cx}" cy="{cy+28}" r="5" fill="#FF6B6B" stroke="none"/></g>'


def assemble_svg(spec: StickerSpec, with_text: bool) -> str:
    cx, cy = SVG_SIZE // 2, SVG_SIZE // 2
    parts: List[str] = [svg_header()]

    parts.append(draw_pug(head_tilt=spec.head_tilt, tongue_out=spec.tongue_out, asleep=spec.asleep, wink=spec.wink))

    # accessories
    if "party_hat" in spec.accessories:
        parts.append(draw_party_hat(cx, cy-20))
    if "paw_stop" in spec.accessories:
        parts.append(draw_stop_paw(cx, cy))
    if "paws_up" in spec.accessories:
        parts.append(draw_paws_up(cx, cy))
    if "bowl" in spec.accessories:
        parts.append(draw_bowl(cx, cy))
    if "helmet" in spec.accessories:
        parts.append(draw_helmet(cx, cy))
    if "reflective_jacket" in spec.accessories:
        parts.append(draw_reflective_jacket(cx, cy))
    if spec.snow:
        parts.append(draw_snow(cx, cy))
    if spec.rope:
        parts.append(draw_rope(cx, cy))
    if spec.car_window:
        parts.append(draw_car_window(cx, cy))
    if "hearts" in spec.accessories:
        parts.append(draw_hearts(cx, cy))
    if "bowtie" in spec.accessories:
        parts.append(draw_bowtie(cx, cy))
    if "mustache_heart" in spec.accessories:
        parts.append(draw_mustache_heart(cx, cy))

    if with_text and spec.label:
        parts.append(text(cx, SVG_SIZE - PADDING, spec.label))

    parts.append(svg_footer())
    return "".join(parts)


def save_svg(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def export_png(svg_path: str, png_path: str, png_size: int = 512) -> None:
    global cairosvg
    if cairosvg is None:
        return
    with open(svg_path, "rb") as f:
        svg_bytes = f.read()
    cairosvg.svg2png(bytestring=svg_bytes, write_to=png_path, output_width=png_size, output_height=png_size, background_color=None)


def main() -> None:
    ensure_dirs()
    for spec in SPECS:
        for with_text in (True, False):
            suffix = "" if with_text else "_nt"
            svg_name = f"frank_{spec.slug}{suffix}.svg"
            png_name = f"frank_{spec.slug}{suffix}.png"
            svg_path = os.path.join(OUTPUT_DIR, svg_name)
            png_path = os.path.join(OUTPUT_DIR, png_name)
            svg_content = assemble_svg(spec, with_text)
            save_svg(svg_path, svg_content)
            export_png(svg_path, png_path, png_size=512)

    # Cover icons from first sticker
    first_png = os.path.join(OUTPUT_DIR, "frank_01_hi.png")
    if os.path.exists(first_png) and cairosvg is not None:
        # Re-render to 100 and 96 via svg for crispness
        first_svg = os.path.join(OUTPUT_DIR, "frank_01_hi.svg")
        export_png(first_svg, os.path.join(OUTPUT_DIR, "cover_icon_100.png"), png_size=100)
        export_png(first_svg, os.path.join(OUTPUT_DIR, "cover_icon_96.png"), png_size=96)

    print(f"Generated stickers into {OUTPUT_DIR}")


if __name__ == "__main__":
    main()