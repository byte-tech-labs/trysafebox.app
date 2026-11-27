# trysafebox.app

The SafeBox website: the product page in 20 languages, the Privacy Policy and the Terms of Use.
Served by GitHub Pages at https://trysafebox.app (custom domain, HTTPS).

## Layout

| Path | What |
|---|---|
| `src/build.py` | Generates every page, `sitemap.xml`, `robots.txt` and `CNAME` into `_site/` |
| `src/content/content_*.py` | Page copy, one dict per language (`EN` is the source; the others mirror its keys) |
| `src/static/` | `style.css`, favicon, images (`images/<lang>/` come from the App Store screenshots) |
| `src/legal/privacy/`, `src/legal/terms/` | Privacy Policy and Terms of Use, copied as-is |
| `.github/workflows/pages.yml` | Builds and deploys on every push to `main` |

## Build locally

```bash
python3 -I src/build.py          # writes _site/
python3 -m http.server -d _site 8000
```

## Adding a language

1. Copy the `EN` dict into a new `src/content/content_<code>.py`, translate every string, keep the keys,
   list lengths, icon/shot keys and `False` badges. Right-to-left languages add `dir="rtl"`.
2. Add `images/<code>/` (hero 1200×514, four shots 540×1174).
3. Import it in `build.py` and add it to `LANGS`.

## URLs

- `/` English, `/<lang>/` the other languages
- `/privacy/` Privacy Policy (the app's `PrivacyPolicyURL`) · `/terms/` Terms of Use
- The old `byte-tech-labs.github.io/safebox/`, `/privacy-policy-terms/` and `/terms-of-use/` redirect here.

Copy rules: never claim every file is encrypted; no iCloud-sync claims until it ships to everyone; no "SafeBox 2".
