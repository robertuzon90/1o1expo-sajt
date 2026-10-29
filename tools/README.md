# Build tools (not part of the website)

Do not upload this folder to the web server.

## German pages (`tools/de/`)
German pages under `/de/` (except `de/index.html` and `de/danke.html`) are generated from the English pages.
After changing English text on a translated page:

1. `python3 tools/de/extract.py` lists new or changed English strings in `todo.txt`.
2. Add German translations for them to `tr.json` (English → German, keep `{0}`, `{1}` placeholders = HTML tags).
3. `python3 tools/de/build.py --check --write` rebuilds all German pages (`missing.json` must be empty).
4. `python3 tools/de/link_lang.py` updates the EN/DE switch and hreflang links, `python3 tools/de/sitemap.py` the sitemap.

Paths in the scripts point to /home/claude/... – adjust `SITE` and the json paths if run elsewhere.

## Fair pages and 404 (`tools/gen/`)
`fairs.py` builds `/fairs/` and the ten fair pages, `notfound.py` builds `404.html`. Run `link_lang.py` afterwards.
