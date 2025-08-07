#!/usr/bin/env python3
import base64
from pathlib import Path

BASE = Path("/workspace/frank_stickers")
FILES = [
    (BASE / "frank_pack_12.zip", "frank_pack_12.zip", "12 PNG стикеров"),
    (BASE / "../frank_all_assets.zip").resolve(),
]

def to_link(path: Path, label: str) -> str:
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    return f'<p><a download="{path.name}" href="data:application/zip;base64,{b64}">Скачать — {label} ({path.name})</a></p>'


def main() -> None:
    link12 = to_link(BASE / "frank_pack_12.zip", "12 PNG с подписями")
    linkAll = to_link((BASE / "../frank_all_assets.zip").resolve(), "Все материалы: PNG, SVG, без текста, галереи")
    html = f"""<!doctype html>
<html lang=\"ru\"><meta charset=\"utf-8\"><title>Скачать стикеры Фрэнка</title>
<style>body{{font-family:system-ui,Arial,sans-serif;padding:24px;}} a{{display:inline-block;background:#222;color:#fff;padding:10px 14px;border-radius:8px;text-decoration:none;margin:8px 0;}}</style>
<h1>Скачать стикеры Фрэнка</h1>
{link12}
{linkAll}
<p>Подсказка: если загрузка не начинается в превью редактора, кликните правой кнопкой по ссылке и выберите «Сохранить ссылку как…».</p>
"""
    (BASE / "download_links.html").write_text(html, encoding="utf-8")
    print("Wrote", BASE / "download_links.html")

if __name__ == "__main__":
    main()