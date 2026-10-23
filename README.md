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

## Kako radimo (da ne trošimo Netlify kredite)
- **`main`** = pravi sajt. Svaka objava na `main` troši 15 Netlify kredita (besplatno je 300 mesečno).
- **`izmene`** = grana za rad. Sve izmene idu ovde.
- Za granu `izmene` postoji otvoren Pull Request ka `main`. Netlify za njega pravi **Deploy Preview** (besplatno), a link za pregled se osvežava posle svake izmene.
- Kad je sve provereno i spremno, PR se spoji (Merge) u `main` i tek tada se menja pravi sajt (jedna objava = 15 kredita).
