#!/usr/bin/env python3
import base64
import os
from pathlib import Path

SRC = Path("/workspace/frank_stickers/output_12")
DST = Path("/workspace/frank_stickers/gallery_embedded.html")

TITLES = {
    "frank_01_hi.png": "01 — гав‑привет",
    "frank_02_stop.png": "02 — Остань, кожаная",
    "frank_03_hug.png": "03 — Хочу обнимашки",
    "frank_04_food.png": "04 — Сыпь корм и уходи",
    "frank_05_sleep.png": "05 — Работа идёт, работник спит",
    "frank_06_reflect.png": "06 — Сияю как зарплата",
    "frank_07_snow.png": "07 — Зима — норм",
    "frank_08_rope.png": "08 — За канат — до конца!",
    "frank_09_taxi.png": "09 — Уже подъезжаю",
    "frank_10_kiss.png": "10 — Чмок‑чмок!",
    "frank_11_yawn.png": "11 — Трудно быть лапочкой",
    "frank_12_business.png": "12 — Связи решают",
}

def make_img_row(path: Path) -> str:
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    title = TITLES.get(path.name, path.name)
    return f'<div class="card"><img src="data:image/png;base64,{b64}" alt="{path.name}"/><div class="name">{title}</div></div>'


def main() -> None:
    files = sorted([p for p in SRC.glob("*.png")])
    cards = "\n".join(make_img_row(p) for p in files)
    html = f"""<!DOCTYPE html>
<html lang=\"ru\">
<head>
<meta charset=\"utf-8\" />
<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\" />
<title>Стикерпак Фрэнк — галерея (вшитые изображения)</title>
<style>
  body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 24px; background:#f6f7f9; }}
  h1 {{ margin: 0 0 16px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 16px; }}
  .card {{ background: #fff; border-radius: 12px; padding: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); text-align:center; }}
  .card img {{ width: 100%; height: auto; image-rendering: -webkit-optimize-contrast; }}
  .name {{ font-weight: 700; margin-top: 8px; font-size: 14px; color:#222; }}
  .hint {{ color:#666; font-size: 14px; margin-bottom: 16px; }}
</style>
</head>
<body>
  <h1>Стикерпак Фрэнк — 12 PNG</h1>
  <p class=\"hint\">Этот файл самодостаточный: просто откройте его в браузере — интернет и сервер не нужны.</p>
  <div class=\"grid\">{cards}</div>
</body>
</html>"""
    DST.write_text(html, encoding="utf-8")
    print(f"Wrote {DST}")

if __name__ == "__main__":
    main()