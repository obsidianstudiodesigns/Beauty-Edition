# 𝓑𝓮𝓪𝓾𝓽𝔂 𝓔𝓭𝓲𝓽𝓲𝓸𝓷 Lash Atelier

Website for Beauty Edition Lash Atelier: custom lash extensions (classic, hybrid, volume) and microneedling in Cullinan, Gauteng. Rediscover your beauty.

Live: https://obsidianstudiodesigns.github.io/Beauty-Edition/

Static site hosted on GitHub Pages from `main`. No build step is needed to serve it; the Python tools only run on your machine.

## Update details
- Phone, WhatsApp, social links, prices and FAQ answers are constants at the top of `tools/build.py`. Edit them, run `python tools/build.py`, then commit and push.
- Black Friday prices (20 to 30 November 2026) switch on and off by themselves in `assets/js/main.js`. Change the dates there for the next special.
- The email address is hidden because `beautyedition.co.za` has no DNS yet. Once mail works, set `SHOW_EMAIL = True` in `tools/build.py` and rebuild.

## Rebuild images
`python tools/make-images.py` rebuilds every image, the favicons and the share image (`assets/img/og/home.jpg`). It needs the originals in `_source/`, which are kept out of the repository.

## To confirm with the client
- A working email address (the domain on Facebook does not resolve).
- Refill prices, and microneedling price, if they want them shown.
- Typical appointment length (the FAQ says about two hours for a new full set) and the aftercare wording.
- Permission to use the before and after photo from the Facebook page on the website.
- Whether to show a street address or area for Google Maps. Right now only "Cullinan, Gauteng" is shown.
- Real photos of the studio and their work, to replace the illustrative images (lash menu eyes, studio, artist, microneedling, hero).

Site by [Obsidian Studio Designs](https://obsidianstudiodesigns.co.za/).
