# 1o1 expo – sajt

Statični sajt za 1o1 expo. Netlify ga automatski objavljuje kad se nešto promeni u `main` grani.

## Fajlovi
- `index.html` – ceo sajt (jedna strana)
- `thanks.html` – strana koja se prikaže posle slanja upita
- `guides/` – svi vodiči i kalendar, svaki u svom folderu (`guides/naziv/index.html`, adresa `/guides/naziv/`)
- `_redirects` – stare adrese vodiča (`guide-*.html`) vode na nove

## Novi vodič

1. Kopirati folder postojećeg vodiča u `guides/novi-naziv/`.
2. Promeniti naslov, opis, canonical, og:url, og:image, JSON-LD (headline, datumi, slika, mainEntityOfPage, BreadcrumbList) i share linkove.
3. Dodati karticu na `guides/index.html` i po potrebi u "Your next read" drugih vodiča.
4. Dodati adresu u `sitemap.xml`.
- `img/` – fotografije i favicon
- `logo/` – logo u SVG formatu (tamni, beli, samo ikonica)
- `robots.txt` – sajt je skriven od Google-a dok ne krene zvanično

## Pre zvaničnog pokretanja
- Ukloniti `<meta name="robots" content="noindex, nofollow">` iz `index.html` i `thanks.html`
- U `robots.txt` promeniti `Disallow: /` u `Allow: /`
- Uključiti obaveštenja mejlom za formu „quote“ u Netlify → Forms

## Kako radimo (da ne trošimo Netlify kredite)
- **`main`** = pravi sajt. Svaka objava na `main` troši 15 Netlify kredita (besplatno je 300 mesečno).
- **`izmene`** = grana za rad. Sve izmene idu ovde.
- Za granu `izmene` postoji otvoren Pull Request ka `main`. Netlify za njega pravi **Deploy Preview** (besplatno), a link za pregled se osvežava posle svake izmene.
- Kad je sve provereno i spremno, PR se spoji (Merge) u `main` i tek tada se menja pravi sajt (jedna objava = 15 kredita).
