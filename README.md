# 1o1 expo – sajt

Statični sajt za 1o1 expo. Netlify ga automatski objavljuje kad se nešto promeni u `main` grani.

## Fajlovi
- `index.html` – ceo sajt (jedna strana)
- `thanks.html` – strana koja se prikaže posle slanja upita
- `img/` – fotografije i favicon
- `logo/` – logo u SVG formatu (tamni, beli, samo ikonica)
- `robots.txt` – sajt je skriven od Google-a dok ne krene zvanično

## Pre zvaničnog pokretanja
- Ukloniti `<meta name="robots" content="noindex, nofollow">` iz `index.html` i `thanks.html`
- U `robots.txt` promeniti `Disallow: /` u `Allow: /`
- Uključiti obaveštenja mejlom za formu „quote“ u Netlify → Forms
