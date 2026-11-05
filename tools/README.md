# Build tools (not part of the website)

Do not upload this folder to the web server.

## German pages (`tools/de/`)
German pages under `/de/` (except `de/index.html` and `de/danke.html`) are generated from the English pages.
After changing English text on a translated page:

1. `python3 tools/de/extract.py` lists new or changed English strings in `todo.txt`.
2. Add German translations for them to `tr.json` (English → German, keep `{0}`, `{1}` placeholders = HTML tags).
3. `python3 tools/de/navdd.py` (header dropdown with all fairs; run before the build so German pages inherit it, it also updates `de/index.html`).
4. `python3 tools/de/build.py --check --write` rebuilds all German pages (`missing.json` must be empty).
5. `python3 tools/de/link_lang.py` updates the EN/DE switch and hreflang links, `python3 tools/de/sitemap.py` the sitemap.

Paths in the scripts point to /home/claude/... – adjust `SITE` and the json paths if run elsewhere.

## Stand, quote and own-design pages (`tools/gen/pages.py`)
`pages.py` builds `/stands/<type>/`, `/quote/` and `/own-design/` from the header and footer of `guides/stand-cost/`. `tools/de/navstands.py` adds the Stand types dropdown to the header nav and points the footer stand links at the stand pages. German text for these pages is in `tr_extra.json`, `attr.json` and `meta.json` (source list: `tr_new.py`).

Order after a header or footer change: `navdd.py`, `navstands.py`, `footer.py`, `gen/fairs.py`, `gen/pages.py`, `gen/notfound.py`, then `footer.py` (site footer), `eyebrow.py` (marker style for section labels) and `wapill.py` (floating WhatsApp button), then the German build, `link_lang.py` and `sitemap.py`.

## Fair pages and 404 (`tools/gen/`)
`fairs.py` builds `/fairs/` and the ten fair pages, `notfound.py` builds `404.html`. Run `navdd.py`, then the German build and `link_lang.py` afterwards.
When a fair is added, also add it to the list in `tools/de/navdd.py`.
