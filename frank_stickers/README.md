# Frank Sticker Pack

This folder contains a Python generator that builds a 12-sticker set for Frank the pug as SVG and PNG with transparent backgrounds.

## Generate

```bash
python3 -m pip install -r /workspace/frank_stickers/requirements.txt
python3 /workspace/frank_stickers/generate_frank_stickers.py
```

Output is written to `/workspace/frank_stickers/output` as 512×512 PNG and SVG files. For each sticker there are `_nt` variants without text. Icons `cover_icon_100.png` and `cover_icon_96.png` are generated for Telegram/WhatsApp.

## Import
- Telegram: use the `@stickers` bot (or `@stickers` in-app) and upload the 12 PNGs (with or without text). Size: 512×512, transparent, <512 KB each.
- WhatsApp: use any sticker maker app or `web.whatsapp.com` sticker upload; 512×512 PNG with padding is acceptable. Use the `_nt` versions if you want to add captions in-app.

## Customizing
If you want to tweak captions or add more poses, edit `generate_frank_stickers.py` in the `SPECS` list.