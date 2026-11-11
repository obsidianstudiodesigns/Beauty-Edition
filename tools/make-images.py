"""Builds every site image from the originals in _source/ (kept out of git).
Run: python tools/make-images.py"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_source"
OUT = ROOT / "assets/img"
INK = (30, 24, 27)
PORCELAIN = (250, 244, 243)
BLUSH = (236, 205, 203)


def save_webp(im, name, widths, quality=80):
    for w in widths:
        h = round(im.height * w / im.width)
        im.resize((w, h), Image.LANCZOS).save(OUT / f"{name}-{w}.webp", "WEBP", quality=quality, method=6)


def tint_alpha(gray, color, gain=1.0):
    """Turn dark ink on white into a solid colour with alpha from the ink."""
    a = np.array(gray, dtype=np.float32)
    # paper (and JPEG noise) above ~232 becomes fully transparent
    alpha = np.clip((232 - a) * 255 / 232 * gain, 0, 255).astype(np.uint8)
    layer = Image.new("RGBA", gray.size, color + (0,))
    layer.putalpha(Image.fromarray(alpha))
    return layer


def logo():
    (OUT / "brand").mkdir(parents=True, exist_ok=True)
    src = Image.open(SRC / "facebook/logo.jpg").convert("L")
    full = src.crop((100, 110, 860, 512))
    full = ImageOps.autocontrast(full, cutoff=1)
    # upscale before thresholding the alpha so the strokes stay smooth at 2x
    big = full.resize((full.width * 2, full.height * 2), Image.LANCZOS)
    for name, col in (("logo-ink", INK), ("logo-light", PORCELAIN)):
        tint_alpha(big, col, 1.25).save(OUT / f"brand/{name}.png", optimize=True)
        im = tint_alpha(big, col, 1.25)
        im.save(OUT / f"brand/{name}.webp", "WEBP", quality=92, method=6)
    mark = ImageOps.autocontrast(src.crop((100, 110, 372, 512)), cutoff=1)
    ImageDraw.Draw(mark).rectangle((258, 150, mark.width, mark.height), fill=255)  # start of the script B
    mark = mark.resize((mark.width * 2, mark.height * 2), Image.LANCZOS)
    tint_alpha(mark, INK, 1.25).save(OUT / "brand/mark-ink.png", optimize=True)
    return mark


def icons(mark):
    """Favicons: the line-art face on a blush disc, strokes thickened for small sizes."""
    def make(size, pad=0.12, round_bg=True, bold=1):
        canvas = Image.new("RGBA", (size * 4, size * 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(canvas)
        if round_bg:
            d.ellipse((0, 0, size * 4 - 1, size * 4 - 1), fill=BLUSH + (255,))
        else:
            d.rectangle((0, 0, size * 4, size * 4), fill=BLUSH + (255,))
        inner = int(size * 4 * (1 - 2 * pad))
        m = mark.copy()
        m.thumbnail((inner, inner), Image.LANCZOS)
        # thicken: min filter on the gray darkens strokes
        k = max(3, int(round(bold * size * 4 / 128)) | 1)
        m = m.filter(ImageFilter.MinFilter(k))
        layer = tint_alpha(m, INK, 1.6)
        x = (size * 4 - layer.width) // 2 + int(size * 0.06)
        y = (size * 4 - layer.height) // 2 + int(size * 0.1)
        canvas.alpha_composite(layer, (x, y))
        return canvas.resize((size, size), Image.LANCZOS)

    root = ROOT
    make(16, pad=0.06, bold=2.4).save(root / "favicon-16.png")
    make(32, pad=0.07, bold=2.2).save(root / "favicon-32.png")
    make(48, pad=0.08, bold=1.8).save(root / "favicon-48.png")
    make(96, pad=0.1, bold=1.4).save(root / "favicon-96.png")
    make(192, pad=0.11, bold=1.1).save(root / "icon-192.png")
    make(512, pad=0.11, bold=1.0).save(root / "icon-512.png")
    make(180, pad=0.12, round_bg=False, bold=1.1).convert("RGB").save(root / "apple-touch-icon.png")
    make(512, pad=0.2, round_bg=False, bold=1.0).save(root / "icon-maskable-512.png")
    ico = [make(s, pad=0.07, bold=2.2) for s in (16, 32, 48)]
    ico[2].save(root / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[:2])


def photos():
    g = SRC / "gen"
    hero = Image.open(g / "hero.png").convert("RGB")
    save_webp(hero, "hero", [1920, 1440, 960], quality=82)
    # separate portrait shot for phones
    save_webp(Image.open(g / "hero-tall.png").convert("RGB"), "hero-tall", [1024, 640], quality=82)
    save_webp(Image.open(g / "artist.png").convert("RGB"), "artist", [900, 600])
    save_webp(Image.open(g / "studio.png").convert("RGB"), "studio", [1536, 960, 640])
    save_webp(Image.open(g / "microneedling.png").convert("RGB"), "microneedling", [960, 640])
    save_webp(Image.open(g / "tools.png").convert("RGB"), "tools", [1200, 720])
    for n in ("classic", "hybrid", "volume"):
        save_webp(Image.open(g / f"{n}.png").convert("RGB"), n, [800, 520])
    # real before and after from the Facebook page: split, turn upright, crop to the eyes
    ba = Image.open(SRC / "facebook/p3-summertime.jpg").convert("RGB")
    # windows centred on each eye line (the photo is upside down), so the slider lines up
    # The after shot is tilted further and sits a touch further away, so it is turned
    # 11.5 degrees and scaled to put both pairs of eyes on the same line.
    b = ba.crop((0, 0, 632, ba.height)).rotate(180)
    before = b.crop((298 - 260, 444 - 195, 298 + 260, 444 + 195))
    a = ba.crop((636, 0, ba.width, ba.height)).rotate(180)
    a = a.rotate(-11.5, center=(326, 537), resample=Image.BICUBIC)
    after = a.crop((326 - 254, 537 - 191, 326 + 254, 537 + 191)).resize((520, 390), Image.LANCZOS)
    for name, im in (("before", before), ("after", after)):
        im = im.resize((1040, 780), Image.LANCZOS)
        save_webp(im, name, [1040, 640], quality=86)


def og():
    """1200x630 share image for WhatsApp, Facebook and search previews."""
    (OUT / "og").mkdir(exist_ok=True)
    hero = Image.open(SRC / "gen/hero.png").convert("RGB")
    hero = hero.resize((1200, round(hero.height * 1200 / hero.width)), Image.LANCZOS)
    top = (hero.height - 630) // 2
    im = hero.crop((0, top, 1200, top + 630)).convert("RGBA")
    # soften the left side so the logo reads cleanly
    fade = Image.new("L", (1200, 1))
    fade.putdata([int(max(0, 215 * (1 - x / 640))) if x < 640 else 0 for x in range(1200)])
    wash = Image.new("RGBA", (1200, 630), PORCELAIN + (0,))
    wash.putalpha(fade.resize((1200, 630)))
    im.alpha_composite(wash)
    logo_im = Image.open(OUT / "brand/logo-ink.png")
    logo_im.thumbnail((520, 300), Image.LANCZOS)
    im.alpha_composite(logo_im, (60, (630 - logo_im.height) // 2))
    im.convert("RGB").save(OUT / "og/home.jpg", quality=88, optimize=True, progressive=True)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    m = logo()
    icons(m)
    photos()
    og()
    print("images done")
