"""Writes every page, the sitemap, robots.txt and the manifest.
Run: python tools/build.py   (business details live in the constants below)"""
import json
import re
from html import escape as e
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://obsidianstudiodesigns.github.io/Beauty-Edition/"
NAME = "Beauty Edition"
FANCY = "\U0001d4d1\U0001d4ee\U0001d4ea\U0001d4fe\U0001d4fd\U0001d502 \U0001d4d4\U0001d4ed\U0001d4f2\U0001d4fd\U0001d4f2\U0001d4f8\U0001d4f7"
FULL = "Beauty Edition Lash Atelier"
TAGLINE = "Rediscover your beauty"
PHONE_LOCAL = "083 303 6393"
PHONE_INTL = "+27833036393"
WA = "https://wa.me/27833036393"
# beautyedition.co.za had no DNS (no website, no mail records) on 11 Nov 2026, so the
# address is hidden until it works. Set SHOW_EMAIL = True and rebuild to show it everywhere.
EMAIL = "lashes@beautyedition.co.za"
SHOW_EMAIL = False
IG = "https://www.instagram.com/beauty_edition_bm/"
TIKTOK = "https://www.tiktok.com/@beautyedition01"
FB = "https://www.facebook.com/profile.php?id=61577019053193"
CREDIT = "https://obsidianstudiodesigns.co.za/"
UPDATED = "11 November 2026"
ISO = "2026-11-11"
THEME = "#fbf6f5"
THEME_DARK = "#151113"

SETS = [
    # key, name, price, Black Friday price, line, image, alt
    ("classic", "Classic", 390, 350,
     "One extension on each natural lash. Clean, defined and natural, like your best mascara day.",
     "Close-up of a green eye wearing a natural classic lash set"),
    ("hybrid", "Hybrid", 460, 410,
     "Classic lashes blended with soft, airy fans for texture and a little more fullness.",
     "Close-up of a brown eye wearing a wispy hybrid lash set"),
    ("volume", "Volume", None, None,
     "Handmade fans of ultra-fine lashes for a plush, fluffy finish. Choose light or full.",
     "Close-up of a blue eye wearing a full, fluffy volume lash set"),
]
VOLUME = [("Light volume", 600, 540), ("Full volume", 700, 630)]

ICONS = {p.stem: p.read_text(encoding="utf8") for p in (ROOT / "tools/icons").glob("*.svg")}


def wa(text=None):
    return WA + ("?text=" + quote(text) if text else "")


def icon(name, cls="i"):
    svg = ICONS[name]
    inner = re.sub(r"^<svg[^>]*>|</svg>\s*$", "", svg.strip())
    return f'<svg class="{cls}" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true" focusable="false">{inner}</svg>'


def img(name, widths, ratio, sizes, alt, cls="", loading="lazy", priority=False):
    """ratio is (w, h) of the source so the browser can reserve space."""
    srcset = ", ".join(f"assets/img/{name}-{w}.webp {w}w" for w in widths)
    w = widths[0]
    h = round(w * ratio[1] / ratio[0])
    fetch = ' fetchpriority="high"' if priority else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="assets/img/{name}-{widths[-1]}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{e(alt)}" loading="{loading}" decoding="async"{fetch}>')


def logo(cls="logo", eager=False):
    load = "eager" if eager else "lazy"
    return (f'<picture class="{cls}"><source srcset="assets/img/brand/logo-light.webp" media="(prefers-color-scheme: dark)" width="1520" height="804">'
            f'<img src="assets/img/brand/logo-ink.webp" width="1520" height="804" alt="{FULL} logo" loading="{load}" decoding="async"></picture>')


def ld_business():
    offers = []
    for key, nm, price, _, line, _ in SETS:
        if price:
            offers.append((f"{nm} lash extension set", line, price))
    for nm, price, _ in VOLUME:
        offers.append((f"{nm} lash extension set", "Handmade volume fans for a plush, fluffy finish.", price))
    return {
        "@context": "https://schema.org",
        "@type": "BeautySalon",
        "@id": BASE + "#salon",
        "name": FULL,
        "alternateName": [NAME, FANCY],
        "slogan": TAGLINE,
        "description": "Custom lash extensions (classic, hybrid and volume) and microneedling in a private, appointment-only lash atelier in Cullinan, Gauteng.",
        "url": BASE,
        "logo": BASE + "assets/img/brand/logo-ink.png",
        "image": BASE + "assets/img/og/home.jpg",
        "telephone": PHONE_INTL,
        **({"email": EMAIL} if SHOW_EMAIL else {}),
        "priceRange": "R390 - R700",
        "currenciesAccepted": "ZAR",
        "address": {"@type": "PostalAddress", "addressLocality": "Cullinan", "addressRegion": "Gauteng", "postalCode": "1000", "addressCountry": "ZA"},
        "areaServed": [{"@type": "City", "name": n} for n in ("Cullinan", "Rayton", "Bronkhorstspruit", "Pretoria East")],
        "sameAs": [FB, IG, TIKTOK],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Lash extensions and skin",
            "itemListElement": [
                {"@type": "Offer", "price": str(p), "priceCurrency": "ZAR",
                 "itemOffered": {"@type": "Service", "name": n, "description": d}} for n, d, p in offers
            ] + [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Microneedling",
                                                      "description": "Collagen induction treatment for smoother texture, softer fine lines and scars, and brighter skin."}}],
        },
    }


FAQ = [
    ("Which lash set should I choose?",
     "Classic gives a natural, mascara-like look. Hybrid adds soft texture and a little more fullness. Volume is the fluffiest and most glamorous. Not sure? Send us a photo of a look you love and we will recommend a set that suits your eyes and natural lashes."),
    ("How long do lash extensions last?",
     "Extensions fall out with your natural lashes as they shed, so a set slowly thins over time. Most clients book a refill every two to three weeks to keep their lashes full."),
    ("How should I prepare for my appointment?",
     "Arrive with clean lashes and no mascara or eye makeup, and skip oily skincare around the eyes that day. Plan on about two hours for a new full set. You will lie back with your eyes closed the whole time, and many clients fall asleep."),
    ("How do I look after my lashes?",
     "Keep them dry for the first 24 hours. After that, cleanse them gently with a lash cleanser, brush them through each morning, sleep on your back if you can, and avoid oil-based products around your eyes. Never pull or pick at your extensions."),
    ("Is the deposit refundable?",
     "A 50% deposit secures your appointment and it is non-refundable. If you need to move your booking, please let us know as early as you can."),
    ("What should I expect after microneedling?",
     "Your skin may look pink and feel warm or tight for a day or two, a bit like mild sunburn. We will talk you through preparation and aftercare when you book, including keeping out of the sun and using a good SPF."),
]


def ld_faq():
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ],
    }


def head(title, desc, path, lds=(), robots="index,follow,max-image-preview:large", extra=""):
    url = BASE + path
    og = f"{BASE}assets/img/og/home.jpg"
    scripts = "".join(f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>\n' for d in lds)
    return f"""<!doctype html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script>document.documentElement.classList.add("js")</script>
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="{THEME}" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="{THEME_DARK}" media="(prefers-color-scheme: dark)">
<meta name="author" content="{FULL}">
<meta name="geo.region" content="ZA-GP">
<meta name="geo.placename" content="Cullinan">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{FANCY}">
<meta property="og:locale" content="en_ZA">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:secure_url" content="{og}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{FULL}, lash extensions in Cullinan">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og}">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="icon" type="image/png" sizes="96x96" href="favicon-96.png">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="assets/fonts/CormorantGaramond-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/Jost-normal.woff2" as="font" type="font/woff2" crossorigin>
{extra}<link rel="stylesheet" href="assets/css/style.css">
{scripts}</head>
"""


NAV = [("#lashes", "Lashes"), ("#results", "Results"), ("#microneedling", "Microneedling"), ("#studio", "Studio"), ("#faq", "FAQ")]


def header(home=True):
    pre = "" if home else "index.html"
    links = "".join(f'<a href="{pre}{h}">{t}</a>' for h, t in NAV)
    sheet = "".join(f'<a href="{pre}{h}">{t}</a>' for h, t in NAV)
    return f"""<body class="{'home' if home else 'sub'}">
<a class="skip" href="#main">Skip to content</a>
<header class="nav" data-nav>
  <div class="nav__in">
    <a class="nav__brand" href="{'#top' if home else 'index.html'}" aria-label="{FULL}, home">{logo('logo', eager=True)}</a>
    <nav class="nav__links" aria-label="Main">{links}</nav>
    <a class="btn btn--sm nav__cta" href="{pre}#book">Book on WhatsApp</a>
    <button class="nav__menu" type="button" aria-expanded="false" aria-controls="sheet" data-menu>
      <span class="sr">Menu</span>{icon('list', 'i i--open')}{icon('x', 'i i--close')}
    </button>
  </div>
</header>
<div class="sheet" id="sheet" data-sheet hidden>
  <nav aria-label="Mobile">{sheet}</nav>
  <a class="btn" href="{pre}#book">{icon('whatsapp-logo')}Book on WhatsApp</a>
  <p class="sheet__meta"><a href="tel:{PHONE_INTL}">{PHONE_LOCAL}</a><span>Cullinan, Gauteng</span></p>
</div>
"""


def footer():
    return f"""<footer class="foot">
  <div class="foot__in">
    <div class="foot__brand">
      <img class="foot__logo" src="assets/img/brand/logo-light.webp" width="1520" height="804" alt="{FULL} logo" loading="lazy" decoding="async">
      <p class="foot__tag">{TAGLINE}.</p>
    </div>
    <div class="foot__col">
      <h2>Visit</h2>
      <p>Cullinan, Gauteng<br>By appointment only</p>
      <p class="foot__soft">Welcoming clients from Cullinan, Rayton, Bronkhorstspruit and Pretoria East.</p>
    </div>
    <div class="foot__col">
      <h2>Contact</h2>
      <p><a href="{wa()}" target="_blank" rel="noopener">WhatsApp {PHONE_LOCAL}</a></p>
      <p><a href="tel:{PHONE_INTL}">Call {PHONE_LOCAL}</a></p>
      {f'<p><a href="mailto:{EMAIL}">{EMAIL}</a></p>' if SHOW_EMAIL else ''}
    </div>
    <div class="foot__col">
      <h2>Follow</h2>
      <p class="foot__social">
        <a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{icon('instagram-logo')}</a>
        <a href="{TIKTOK}" target="_blank" rel="noopener" aria-label="TikTok">{icon('tiktok-logo')}</a>
        <a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook">{icon('facebook-logo')}</a>
      </p>
      <p class="foot__soft">@beauty_edition_bm</p>
    </div>
  </div>
  <div class="foot__end">
    <span>&copy; 2026 {FULL}</span>
    <span class="foot__legal"><a href="privacy.html">Privacy policy</a><a href="terms.html">Terms of use</a></span>
    <a class="foot__credit" href="{CREDIT}" target="_blank" rel="noopener">Website designed by <strong>Obsidian Studio Designs</strong></a>
  </div>
</footer>
"""


def wa_float():
    return f'<a class="wa-float" href="{wa("Hi Beauty Edition, I would like to book a lash appointment.")}" target="_blank" rel="noopener" aria-label="Book on WhatsApp" data-float>{icon("whatsapp-logo")}</a>\n'


def scripts():
    return '<script src="assets/js/main.js" defer></script>\n</body>\n</html>\n'


def price(amount, bf):
    if not amount:
        return ""
    bf_attr = f' data-bf="R{bf}"' if bf else ""
    return f'<span class="price"{bf_attr}><span class="price__now">R{amount}</span></span>'


def page_home():
    title = f"{NAME} Lash Atelier | Lash Extensions in Cullinan"
    desc = "Classic, hybrid and volume lash extensions plus microneedling in a private lash atelier in Cullinan, Gauteng. Sets from R390. Book on WhatsApp 083 303 6393."
    h = head(title, desc, "", lds=(ld_business(), ld_faq()),
             extra='<link rel="preload" as="image" href="assets/img/hero-1440.webp" imagesrcset="assets/img/hero-960.webp 960w, assets/img/hero-1440.webp 1440w, assets/img/hero-1920.webp 1920w" imagesizes="100vw" media="(min-width: 768px)">\n'
                   '<link rel="preload" as="image" href="assets/img/hero-tall-640.webp" imagesrcset="assets/img/hero-tall-640.webp 640w, assets/img/hero-tall-1024.webp 1024w" imagesizes="100vw" media="(max-width: 767px)">\n')

    benefits = [("feather", "Lightweight and comfortable"), ("eye", "Shaped to your natural eyes"),
                ("clock", "No mascara, no morning fuss"), ("hourglass-medium", "Long lasting, low maintenance")]
    ben = "".join(f'<li>{icon(i)}<span>{t}</span></li>' for i, t in benefits)

    tiles = []
    for idx, (key, nm, p, bf, line, alt) in enumerate(SETS):
        if key == "volume":
            prices = "".join(f'<li><span>{n}</span>{price(a, b)}</li>' for n, a, b in VOLUME)
            meta = f'<ul class="set__tiers">{prices}</ul>'
        else:
            meta = f'<p class="set__price">Full set {price(p, bf)}</p>'
        tiles.append(f"""<article class="set set--{key}" data-reveal style="--d:{idx}">
      <div class="set__img">{img(key, [800, 520], (1024, 1280), "(min-width: 1024px) 30vw, (min-width: 640px) 45vw, 90vw", alt)}</div>
      <div class="set__body">
        <h3>{nm}</h3>
        <p>{line}</p>
        {meta}
      </div>
    </article>""")

    faq = "".join(f"""<details class="qa"{' open' if i == 0 else ''}>
        <summary><span>{e(q)}</span>{icon('plus', 'i qa__i')}</summary>
        <div class="qa__a"><p>{e(a)}</p></div>
      </details>""" for i, (q, a) in enumerate(FAQ))

    services = [("Classic set (R390)", "Classic lash set"), ("Hybrid set (R460)", "Hybrid lash set"),
                ("Light volume set (R600)", "Light volume lash set"), ("Full volume set (R700)", "Full volume lash set"),
                ("Lash refill", "Lash refill"), ("Microneedling", "Microneedling"), ("Not sure yet", "Not sure yet, please advise")]
    opts = "".join(f'<option value="{e(v)}">{e(t)}</option>' for t, v in services)

    body = f"""<main id="main">
<section class="hero" id="top" aria-labelledby="hero-h">
  <div class="hero__media">
    <picture>
      <source media="(max-width: 767px)" srcset="assets/img/hero-tall-640.webp 640w, assets/img/hero-tall-1024.webp 1024w" sizes="100vw" width="1024" height="1536">
      {img("hero", [1920, 1440, 960], (1920, 1080), "100vw", "A woman resting on blush silk with long, fluffy volume lash extensions", "hero__img", loading="eager", priority=True)}
    </picture>
  </div>
  <div class="hero__in">
    <h1 id="hero-h" class="hero__h"><span class="ln">Rediscover</span> <span class="ln">your <em>beauty</em></span></h1>
    <p class="hero__p">Custom lash extensions and microneedling, by appointment in a private atelier in Cullinan.</p>
    <div class="hero__cta">
      <a class="btn" href="#book">{icon('whatsapp-logo')}Book on WhatsApp</a>
      <a class="link" href="#lashes">See the lash menu{icon('arrow-right')}</a>
    </div>
  </div>
</section>

<section class="intro" aria-labelledby="intro-h">
  <figure class="intro__fig arch" data-reveal>
    {img("artist", [900, 600], (1024, 1536), "(min-width: 1024px) 38vw, 88vw", "A lash artist in black gloves placing a single extension with fine tweezers")}
  </figure>
  <div class="intro__txt">
    <h2 id="intro-h" class="statement" data-reveal>Lashes designed around <em>your</em> eyes, never a template.</h2>
    <p class="lede" data-reveal>Every set is mapped to your eye shape, your natural lashes and the look you love, then applied one extension at a time. Lightweight, comfortable and made to last.</p>
    <ul class="benefits" data-reveal>{ben}</ul>
  </div>
</section>

<section class="menu" id="lashes" aria-labelledby="menu-h">
  <header class="menu__head" data-reveal>
    <p class="eyebrow">Lash extensions</p>
    <h2 id="menu-h" class="h2">The lash menu</h2>
  </header>
  <div class="menu__grid">
    {''.join(tiles)}
  </div>
  <p class="menu__note" data-reveal>Prices are for a new full set. Ask about refills when you book. <span class="bf-note" data-bf-note hidden>Black Friday pricing runs from 20 to 30 November.</span></p>
</section>

<section class="results" id="results" aria-labelledby="results-h">
  <div class="results__head" data-reveal>
    <h2 id="results-h" class="h2">Before and after</h2>
    <p>A Beauty Edition client, photographed before and after her appointment. Drag to compare.</p>
  </div>
  <div class="compare" data-compare data-reveal style="--pos:50%">
    {img("before", [1040, 640], (1040, 780), "(min-width: 1024px) 860px, 94vw", "A client's natural lashes before her appointment", "compare__img")}
    <div class="compare__after">
      {img("after", [1040, 640], (1040, 780), "(min-width: 1024px) 860px, 94vw", "The same client after her lash extensions", "compare__img")}
    </div>
    <span class="compare__tag compare__tag--l" aria-hidden="true">Before</span>
    <span class="compare__tag compare__tag--r" aria-hidden="true">After</span>
    <span class="compare__line" aria-hidden="true"><span class="compare__knob">{icon('arrows-left-right')}</span></span>
    <input class="compare__range" type="range" min="0" max="100" value="50" aria-label="Compare before and after">
  </div>
</section>

<section class="skin" id="microneedling" aria-labelledby="skin-h">
  <div class="skin__in">
    <div class="skin__txt">
      <p class="eyebrow" data-reveal>Skin</p>
      <h2 id="skin-h" class="h2" data-reveal>Microneedling, now at the atelier</h2>
      <p class="lede" data-reveal>Fine, controlled micro-channels wake up your skin's own collagen response. The result is smoother texture and a brighter, more even glow.</p>
      <ul class="ticks" data-reveal>
        <li>{icon('sparkle')}Boosts collagen</li>
        <li>{icon('drop')}Improves skin texture</li>
        <li>{icon('feather')}Softens fine lines and scars</li>
        <li>{icon('sun')}Brightens and rejuvenates</li>
      </ul>
      <a class="btn btn--line" data-reveal href="{wa('Hi Beauty Edition, I would like to book a microneedling treatment.')}" target="_blank" rel="noopener">{icon('whatsapp-logo')}Book on WhatsApp</a>
    </div>
    <figure class="skin__fig arch" data-reveal>
      {img("microneedling", [960, 640], (1024, 1280), "(min-width: 1024px) 34vw, 88vw", "A relaxed client receiving a microneedling treatment on her cheek")}
    </figure>
  </div>
</section>

<section class="studio" id="studio" aria-labelledby="studio-h">
  <figure class="studio__wide" data-reveal>
    {img("studio", [1536, 960, 640], (1536, 1024), "100vw", "A calm lash room with a white lash bed, blush throw and soft daylight")}
  </figure>
  <div class="studio__card" data-reveal>
    <h2 id="studio-h" class="h2">A quiet room, just for you</h2>
    <p>Beauty Edition is a private, appointment-only lash atelier in Cullinan. One client at a time, never rushed, with spotless tools and premium lash products for every set.</p>
    <p class="studio__area">{icon('map-pin')}Cullinan, Rayton, Bronkhorstspruit and Pretoria East</p>
  </div>
  <figure class="studio__detail" data-reveal>
    {img("tools", [1200, 720], (1536, 1024), "(min-width: 1024px) 30vw, 70vw", "Lash trays, rose gold tweezers and a lash cleanser on blush satin")}
  </figure>
</section>

<section class="book" id="book" aria-labelledby="book-h">
  <div class="book__in">
    <div class="book__steps">
      <h2 id="book-h" class="h2" data-reveal>Book your set</h2>
      <ol class="steps">
        <li data-reveal><h3>Send a message</h3><p>Tell us the set you would like and a day that suits you. Slots are limited, so book early.</p></li>
        <li data-reveal><h3>Secure your slot</h3><p>A 50% non-refundable deposit confirms your appointment.</p></li>
        <li data-reveal><h3>Arrive lash-ready</h3><p>Clean lashes, no mascara or eye makeup. Then lie back and relax.</p></li>
      </ol>
      <p class="book__direct" data-reveal>Prefer to call? <a href="tel:{PHONE_INTL}">{PHONE_LOCAL}</a></p>
    </div>
    <form class="form" data-form novalidate data-reveal>
      <div class="field">
        <label for="f-name">Your name</label>
        <input id="f-name" name="name" type="text" autocomplete="name" required>
        <p class="field__err" id="f-name-err" hidden>Please add your name.</p>
      </div>
      <div class="field">
        <label for="f-service">Treatment</label>
        <select id="f-service" name="service" required>
          <option value="" selected disabled>Choose a treatment</option>
          {opts}
        </select>
        <p class="field__err" id="f-service-err" hidden>Please choose a treatment.</p>
      </div>
      <div class="field-row">
        <div class="field">
          <label for="f-date">Preferred date</label>
          <input id="f-date" name="date" type="date">
        </div>
        <div class="field">
          <label for="f-time">Time of day</label>
          <select id="f-time" name="time">
            <option value="">Any time</option>
            <option>Morning</option>
            <option>Midday</option>
            <option>Afternoon</option>
          </select>
        </div>
      </div>
      <div class="field">
        <label for="f-notes">Anything we should know? <span class="opt">(optional)</span></label>
        <textarea id="f-notes" name="notes" rows="3"></textarea>
      </div>
      <button class="btn btn--block" type="submit">{icon('whatsapp-logo')}Book on WhatsApp</button>
      <p class="form__help">This opens WhatsApp with your message ready to send. Nothing is stored on this website.</p>
    </form>
  </div>
</section>

<section class="faq" id="faq" aria-labelledby="faq-h">
  <h2 id="faq-h" class="h2" data-reveal>Good to know</h2>
  <div class="faq__list" data-reveal>
    {faq}
  </div>
</section>
</main>
"""
    return h + header(True) + body + footer() + wa_float() + scripts()


def legal(path, title, desc, h1, content):
    h = head(f"{title} | {FULL}", desc, path)
    return h + header(False) + f"""<main id="main" class="legal">
<h1>{h1}</h1>
<p class="legal__date">Last updated {UPDATED}</p>
{content}
</main>
""" + footer() + scripts()


def page_privacy():
    content = f"""
<p>This policy explains how {FULL} (&ldquo;we&rdquo;, &ldquo;us&rdquo;) collects, uses and protects your personal information when you use this website, contact us or book a treatment, in line with the Protection of Personal Information Act 4 of 2013 (POPIA).</p>
<h2>Who we are</h2>
<dl class="facts">
  <div><dt>Business</dt><dd>{FULL}</dd></div>
  <div><dt>Location</dt><dd>Cullinan, Gauteng, South Africa</dd></div>
  <div><dt>Phone and WhatsApp</dt><dd><a href="tel:{PHONE_INTL}">{PHONE_LOCAL}</a></dd></div>
  {f'<div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>' if SHOW_EMAIL else ''}
</dl>
<h2>What we collect</h2>
<p>This website has no accounts, no online payments and no visitor database. We only receive personal information when you choose to contact us by WhatsApp, phone or social media. That can include your name, phone number, the treatment and date you ask about, and anything else you write in your message.</p>
<p>The booking form on this website does not store or send anything by itself. It prepares a message in WhatsApp on your own device, and nothing reaches us unless you press send there.</p>
<p>When you come in for a treatment we may ask about allergies, sensitivities, skin conditions or medication that could affect your lash or skin treatment. This is health information, and we only collect it with your consent and use it to keep you safe.</p>
<h2>Why we use it</h2>
<ul>
  <li>To answer your questions and arrange, confirm or move your appointments.</li>
  <li>To record your deposit and payments.</li>
  <li>To choose products and techniques that are safe and suitable for you.</li>
  <li>To keep the business records we are required to keep by law.</li>
</ul>
<p>We will not send you marketing messages unless you ask us to, and you can ask us to stop at any time.</p>
<h2>Photographs</h2>
<p>We only take or share before and after photos of you with your permission. You can withdraw that permission at any time and we will remove the photos from our website and social media.</p>
<h2>Cookies and tracking</h2>
<p>This website does not use analytics, advertising trackers or cookies. Our fonts and images are served from this website itself.</p>
<h2>Other services</h2>
<p>This website is hosted on GitHub Pages, which may keep standard technical logs such as IP addresses to keep the service secure. Links to WhatsApp, Instagram, TikTok and Facebook take you to those services, and their own privacy policies apply once you are there.</p>
<h2>Sharing your information</h2>
<p>We do not sell or rent your personal information. We only share it when the law requires us to, or when you have asked us to.</p>
<h2>How long we keep it</h2>
<p>We keep client notes for as long as you are a client and for a reasonable time afterwards, and financial records for as long as the law requires. After that we delete them securely.</p>
<h2>Your rights</h2>
<p>Under POPIA you may ask whether we hold personal information about you, ask for a copy, ask us to correct or delete it, and object to how we use it. To do so, contact us on <a href="tel:{PHONE_INTL}">{PHONE_LOCAL}</a>{f' or <a href="mailto:{EMAIL}">{EMAIL}</a>' if SHOW_EMAIL else ''}.</p>
<p>If you are unhappy with how we handled your information, you may complain to the Information Regulator of South Africa at <a href="https://inforegulator.org.za/" target="_blank" rel="noopener">inforegulator.org.za</a>.</p>
<h2>Changes to this policy</h2>
<p>We may update this policy from time to time. The date at the top shows when it last changed.</p>
"""
    return legal("privacy.html", "Privacy Policy", f"How {FULL} collects, uses and protects your personal information under POPIA.", "Privacy policy", content)


def page_terms():
    content = f"""
<p>These terms apply when you use this website or book a treatment with {FULL}. By using the website or making a booking, you agree to them.</p>
<h2>About us</h2>
<p>This website is run by {FULL}, a lash atelier in Cullinan, Gauteng, South Africa. You can reach us on <a href="tel:{PHONE_INTL}">{PHONE_LOCAL}</a>{f' or <a href="mailto:{EMAIL}">{EMAIL}</a>' if SHOW_EMAIL else ''}. This information is provided in line with section 43 of the Electronic Communications and Transactions Act 25 of 2002.</p>
<h2>Bookings and deposits</h2>
<p>Appointments are confirmed once your deposit of 50% of the treatment price has been received. The deposit is non-refundable. If you need to move your appointment, please give us as much notice as possible so we can offer the slot to someone else. The balance is payable at your appointment.</p>
<h2>Prices</h2>
<p>Prices on this website are in South African rand and may change without notice. The price that applies is the one we confirm when you book. Specials apply only for the dates shown.</p>
<h2>Your treatment</h2>
<p>Please tell us about any allergies, sensitivities, eye or skin conditions, recent procedures or medication before your treatment. We may decline or postpone a treatment if we believe it is not safe for you. Results vary from person to person, and the life of your lash extensions depends on your natural lash cycle and on following the aftercare advice we give you.</p>
<h2>Photographs and images</h2>
<p>The before and after photos on this website show a real Beauty Edition client and are shared with permission. Other images on this website are illustrative and may not show actual clients, results or our studio.</p>
<h2>Copyright</h2>
<p>The {NAME} name, logo, photographs and content on this website belong to {FULL} or are used with permission. You may share links to this website, but you may not copy or reuse its content without our written permission.</p>
<h2>Links to other services</h2>
<p>We link to WhatsApp, Instagram, TikTok and Facebook for your convenience. We are not responsible for those services or their content.</p>
<h2>Liability</h2>
<p>We work to keep the information on this website accurate, but it may change. To the extent the law allows, we are not liable for loss that results from using this website or relying on its content. Nothing in these terms limits your rights under the Consumer Protection Act 68 of 2008.</p>
<h2>Governing law and changes</h2>
<p>These terms are governed by the laws of South Africa. We may update them from time to time, and the date at the top shows when they last changed.</p>
"""
    return legal("terms.html", "Terms of Use", f"Booking, deposit and website terms for {FULL} in Cullinan.", "Terms of use", content)


def page_404():
    h = head(f"Page not found | {FULL}", "This page could not be found.", "404.html", robots="noindex").replace(
        "<head>\n", '<head>\n<base href="/Beauty-Edition/">\n', 1)
    return h + header(False) + f"""<main id="main" class="legal notfound">
{logo('logo notfound__logo')}
<h1>This page has wandered off</h1>
<p>The link may be old, or the page may have moved.</p>
<p><a class="btn" href="index.html">Back to the home page</a></p>
</main>
""" + footer() + scripts()


PAGES = {
    "index.html": page_home,
    "privacy.html": page_privacy,
    "terms.html": page_terms,
    "404.html": page_404,
}

if __name__ == "__main__":
    for name, fn in PAGES.items():
        html = fn()
        visible = re.sub(r'<script type="application/ld\+json">.*?</script>', "", html, flags=re.S)
        bad = [c for c in ("—", "–") if c in visible]
        if bad:
            raise SystemExit(f"{name} contains a banned dash")
        (ROOT / name).write_text(html, encoding="utf8", newline="\n")

    pages = [p for p in PAGES if p != "404.html"]
    prio = {"index.html": "1.0"}
    urls = "\n".join(
        f"<url><loc>{BASE}{'' if p == 'index.html' else p}</loc><lastmod>{ISO}</lastmod><priority>{prio.get(p, '0.3')}</priority></url>"
        for p in pages)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf8", newline="\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: {BASE}sitemap.xml\n", encoding="utf8", newline="\n")
    manifest = {
        "name": FULL, "short_name": NAME, "description": f"{TAGLINE}. Lash extensions and microneedling in Cullinan.",
        "start_url": "./", "scope": "./", "display": "standalone", "background_color": THEME, "theme_color": THEME,
        "icons": [
            {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }
    (ROOT / "site.webmanifest").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf8", newline="\n")
    print("built", len(PAGES), "pages")
