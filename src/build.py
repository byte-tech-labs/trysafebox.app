import json, os, sys
from html import escape as e
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "content"))
from content_en_fr import EN, FR
from content_es_pt import ES, PT
from content_hi_ja import HI, JA
from content_de_nl_pl import DE, NL, PL
from content_it_ru_uk import IT, RU, UK
from content_tr_id_vi import TR, ID, VI
from content_ar_th import AR, TH
from content_ko_zh import KO, ZH_HANS, ZH_HANT

OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "_site"))
DOMAIN = "trysafebox.app"
BASE = f"https://{DOMAIN}/"
STORE = "https://apps.apple.com/app/id1577066512"
POLICY = BASE + "privacy/"
TERMS = BASE + "terms/"
MAIL = "bytetechlabs@gmail.com"
LANGS = [EN, FR, ES, PT, DE, IT, NL, PL, RU, UK, TR, AR, HI, TH, VI, ID, JA, KO, ZH_HANS, ZH_HANT]

ICONS = {
    "photo": '<rect x="3" y="5" width="18" height="14" rx="3"/><circle cx="9" cy="10" r="1.6"/><path d="M4 17l5-5 4 4 3-3 4 4"/>',
    "camera": '<path d="M4 8h3l2-2.5h6L17 8h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
    "doc": '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M10 12h5M10 16h5"/>',
    "card": '<rect x="3" y="6" width="18" height="13" rx="2.5"/><circle cx="8.5" cy="12" r="2"/><path d="M6 16.5c.6-1.3 1.5-2 2.5-2s1.9.7 2.5 2M14 11h4M14 14h3"/>',
    "note": '<rect x="5" y="3" width="14" height="18" rx="2.5"/><path d="M9 8h6M9 12h6M9 16h3"/>',
    "mask": '<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/><circle cx="12" cy="10.5" r="2"/><path d="M12 12.5V16"/>',
    "lock": '<rect x="5" y="10" width="14" height="10" rx="2.5"/><path d="M8 10V7.5a4 4 0 018 0V10"/><path d="M12 14v2.5"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5 5"/>',
    "cloud": '<path d="M7 18h10a4 4 0 00.5-8 5.5 5.5 0 00-10.7 1.3A3.4 3.4 0 007 18z"/><rect x="10" y="12" width="4" height="3.5" rx=".8"/><path d="M10.8 12v-1a1.2 1.2 0 012.4 0v1"/>',
    "devices": '<rect x="3" y="4" width="13" height="16" rx="2"/><rect x="15" y="9" width="6" height="11" rx="1.5"/>',
}

def icon(k):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICONS[k]}</svg>'

def url(L): return BASE + L["path"]

def jsonld(L):
    app = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "SafeBox",
        "alternateName": "SafeBox: Secret Photo Vault",
        "description": L["desc"],
        "url": url(L),
        "inLanguage": L["hreflang"],
        "operatingSystem": "iOS 18.0 or later, iPadOS 18.0 or later",
        "applicationCategory": "SecurityApplication",
        "downloadUrl": STORE,
        "installUrl": STORE,
        "sameAs": STORE,
        "image": f"{BASE}images/{L['img']}/hero.jpg",
        "screenshot": [f"{BASE}images/{L['img']}/{k}.jpg" for k, _ in L["shots"]],
        "featureList": [f[1] for f in L["features"]],
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "category": "free", "url": STORE},
        "author": {"@type": "Organization", "name": "Byte Tech Labs", "email": MAIL},
        "publisher": {"@type": "Organization", "name": "Byte Tech Labs", "email": MAIL},
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "inLanguage": L["hreflang"],
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in L["faq"]],
    }
    dump = lambda o: json.dumps(o, ensure_ascii=False, indent=1).replace("</", "<\\/")
    return f'<script type="application/ld+json">\n{dump(app)}\n</script>\n<script type="application/ld+json">\n{dump(faq)}\n</script>'

def page(L):
    up = "../" if L["path"] else ""
    img = f"{up}images/{L['img']}"
    alts = "\n".join(f'<link rel="alternate" hreflang="{x["hreflang"]}" href="{url(x)}">' for x in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{BASE}">'
    og_alt = "\n".join(f'<meta property="og:locale:alternate" content="{x["og_locale"]}">' for x in LANGS if x is not L)
    switch = " ".join(
        (f'<a href="{up}{x["path"] or "./"}" hreflang="{x["hreflang"]}" lang="{x["html_lang"]}"' + (' aria-current="page"' if x is L else '') + f'>{e(x["name"])}</a>')
        for x in LANGS)
    feats = "\n".join(
        f'<li class="feature"><span class="ficon">{icon(k)}</span><h3>{e(t)}'
        + (f' <span class="badge">{e(p if isinstance(p, str) else L["plus"])}</span>' if p else "")
        + f'</h3><p>{e(b)}</p></li>'
        for k, t, b, p in L["features"])
    shots = "\n".join(
        f'<figure><img src="{img}/{k}.jpg" width="540" height="1174" loading="lazy" decoding="async" alt="{e(a)}"><figcaption>{e(a)}</figcaption></figure>'
        for k, a in L["shots"])
    privacy = "\n".join(f"<li>{e(x)}</li>" for x in L["privacy"])
    free = "\n".join(f"<li>{e(x)}</li>" for x in L["free"])
    plus = "\n".join(f"<li>{e(x)}</li>" for x in L["plus_list"])
    faq = "\n".join(f'<details><summary><h3>{e(q)}</h3></summary><p>{e(a)}</p></details>' for q, a in L["faq"])
    n = L["nav"]
    return f'''<!doctype html>
<html lang="{L["html_lang"]}" dir="{L.get("dir", "ltr")}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(L["title"])}</title>
<meta name="description" content="{e(L["desc"])}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#F5F6F3" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0A0E0D" media="(prefers-color-scheme: dark)">
<meta name="apple-itunes-app" content="app-id=1577066512">
<link rel="canonical" href="{url(L)}">
{alts}
<link rel="icon" type="image/png" href="{up}favicon.png">
<link rel="apple-touch-icon" href="{up}images/icon-192.png">
<link rel="stylesheet" href="{up}style.css">
<meta property="og:type" content="website">
<meta property="og:site_name" content="SafeBox">
<meta property="og:title" content="{e(L["title"])}">
<meta property="og:description" content="{e(L["desc"])}">
<meta property="og:url" content="{url(L)}">
<meta property="og:image" content="{BASE}images/{L["img"]}/hero.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="514">
<meta property="og:image:alt" content="{e(L["hero_alt"])}">
<meta property="og:locale" content="{L["og_locale"]}">
{og_alt}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(L["title"])}">
<meta name="twitter:description" content="{e(L["desc"])}">
<meta name="twitter:image" content="{BASE}images/{L["img"]}/hero.jpg">
{jsonld(L)}
</head>
<body>
<a class="skip" href="#main">{e(L["skip"])}</a>
<header class="top">
<div class="wrap bar">
<a class="brand" href="{up}{L["path"] or "./"}"><img src="{up}images/icon-192.png" width="32" height="32" alt="">SafeBox</a>
<nav aria-label="SafeBox"><a href="#features">{e(n[0])}</a><a href="#privacy">{e(n[1])}</a><a href="#plans">{e(n[2])}</a><a href="#faq">{e(n[3])}</a></nav>
<a class="btn btn-sm" href="{STORE}">{e(L["cta"])}</a>
</div>
</header>
<main id="main">
<section class="hero">
<div class="wrap">
<h1>{e(L["h1"])}</h1>
<p class="lede">{e(L["intro"])}</p>
<p><a class="btn" href="{STORE}">{e(L["cta"])}</a></p>
<p class="meta">{e(L["meta_line"])}</p>
</div>
<img class="hero-img" src="{img}/hero.jpg" width="1200" height="514" fetchpriority="high" alt="{e(L["hero_alt"])}">
</section>

<section id="features" class="wrap section">
<h2>{e(L["features_h"])}</h2>
<p class="sub">{e(L["features_intro"])}</p>
<ul class="features">
{feats}
</ul>
<div class="shots">
{shots}
</div>
</section>

<section id="privacy" class="section band">
<div class="wrap narrow">
<h2>{e(L["privacy_h"])}</h2>
<p class="sub">{e(L["privacy_intro"])}</p>
<ul class="checks">
{privacy}
</ul>
</div>
</section>

<section id="plans" class="wrap section">
<h2>{e(L["plans_h"])}</h2>
<div class="plans">
<div class="plan"><h3>{e(L["free_h"])}</h3><ul class="checks">
{free}
</ul></div>
<div class="plan plan-plus"><h3>{e(L["plus_h"])}</h3><ul class="checks">
{plus}
</ul></div>
</div>
<p class="note">{e(L["plans_note"])}</p>
</section>

<section id="faq" class="section band">
<div class="wrap narrow">
<h2>{e(L["faq_h"])}</h2>
<div class="faq">
{faq}
</div>
<p class="center"><a class="btn" href="{STORE}">{e(L["cta"])}</a></p>
</div>
</section>
</main>
<footer class="foot">
<div class="wrap">
<p class="langs"><span>{e(L["footer_lang"])}:</span> {switch}</p>
<p><a href="{POLICY}">{e(L["footer_privacy"])}</a> · {e(L["footer_support"])}: <a href="mailto:{MAIL}">{MAIL}</a> · <a href="{STORE}">App Store</a></p>
<p class="small">{e(L["footer_made"])} © 2026 Byte Tech Labs. iPhone, iPad, iCloud, Face ID and App Store are trademarks of Apple Inc.</p>
</div>
</footer>
</body>
</html>
'''

import shutil
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
shutil.copytree(os.path.join(HERE, "static"), OUT)
shutil.copytree(os.path.join(HERE, "legal"), OUT, dirs_exist_ok=True)
with open(os.path.join(OUT, "CNAME"), "w") as f:
    f.write(DOMAIN + "\n")
open(os.path.join(OUT, ".nojekyll"), "w").close()

for L in LANGS:
    d = os.path.join(OUT, L["path"])
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w") as f:
        f.write(page(L))

# sitemap
alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{x["hreflang"]}" href="{url(x)}"/>' for x in LANGS)
alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}"/>'
urls = "".join(f'\n  <url>\n    <loc>{url(L)}</loc>\n    <lastmod>2026-11-27</lastmod>{alts}\n  </url>' for L in LANGS)
urls += "".join(f'\n  <url>\n    <loc>{u}</loc>\n    <lastmod>2026-11-27</lastmod>\n  </url>' for u in (POLICY, TERMS))
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">{urls}\n</urlset>\n')

bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "Claude-SearchBot", "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot", "Applebot-Extended", "Bingbot", "Googlebot"]
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write("# SafeBox website: every crawler, including AI assistants and AI search, is welcome.\n\n")
    for b in bots:
        f.write(f"User-agent: {b}\nAllow: /\n\n")
    f.write("User-agent: *\nAllow: /\n\n")
    f.write(f"Sitemap: {BASE}sitemap.xml\n")
print("ok")
