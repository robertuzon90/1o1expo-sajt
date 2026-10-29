"""Idempotent: point EN language switches at the DE counterpart, add hreflang to EN pages,
and point links in de/index.html (and de/danke.html) at the German pages."""
import sys, re
sys.path.insert(0, '/home/claude/de-build')
from build import PAGES, en_url, de_url, map_path, SITE
pairs = [(p, en_url(p), de_url(p)) for p in PAGES]
for p, ue, ud in pairs:
    f = SITE + p; s = open(f).read()
    s = re.sub(r'<a href="[^"]*de/" hreflang="de" lang="de">DE</a>', f'<a href="{ud}" hreflang="de" lang="de">DE</a>', s, count=1)
    s = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', '', s)
    alt = f'<link rel="alternate" hreflang="en" href="https://1o1expo.com{ue}">\n<link rel="alternate" hreflang="de" href="https://1o1expo.com{ud}">\n<link rel="alternate" hreflang="x-default" href="https://1o1expo.com{ue}">\n'
    s = s.replace('</head>', alt + '</head>', 1)
    open(f, 'w').write(s)

# German homepage
f = SITE + 'de/index.html'; s = open(f).read()
rep = [('href="../about.html"', 'href="/de/ueber-uns.html"'), ('href="../guides/"', 'href="/de/ratgeber/"'),
       ('href="../legal.html"', 'href="/de/impressum.html"'), ('href="../privacy.html"', 'href="/de/datenschutz.html"'),
       ('href="../fairs/"', 'href="/de/messen/"'), ('href="../guides/trade-fair-calendar-2027/"', 'href="/de/ratgeber/messekalender-2027/"')]
for a, b in rep: s = s.replace(a, b)
# nav "Messen" -> fairs hub
s = s.replace('<a href="#fairs" style="color: #1C1A17; text-decoration: none">Messen</a>', '<a href="/de/messen/" style="color: #1C1A17; text-decoration: none">Messen</a>')
# map pins + city chips -> fairs hub filtered by city (English city keys, as on the EN page)
CITY_EN = {'München': 'Munich', 'Köln': 'Cologne', 'Mailand': 'Milan', 'Lissabon': 'Lisbon'}
def pin(m):
    cls, city = m.group(1), m.group(2)
    return f'href="/de/messen/?city={city}" class="{cls}" data-city="{city}"'
s = re.sub(r'href="(?:#quote|/de/messen/\?city=[A-Za-z]+)" class="(mcity|cchip)" data-city="([A-Za-z]+)"', pin, s)
# stand cards -> German stand types guide
for en, de, lab in [('row', 'Reihenstand', 'Reihenstände im Detail'), ('corner', 'Eckstand', 'Eckstände im Detail'), ('peninsula', 'Kopfstand', 'Kopfstände im Detail'), ('island', 'Inselstand', 'Inselstände im Detail')]:
    m = re.search(r'<a href="[^"]*" class="stype"(.*?)</a>', s[s.find(f'aria-label="{de}') - 3000 if f'aria-label="{de}' in s else 0:], re.S)
blocks = list(re.finditer(r'<a href="[^"]*" class="stype".*?</a>', s, re.S))
labs = {'Reihenstand': ('row', 'Reihenstände im Detail'), 'Eckstand': ('corner', 'Eckstände im Detail'), 'Kopfstand': ('peninsula', 'Kopfstände im Detail'), 'Inselstand': ('island', 'Inselstände im Detail')}
for b in blocks:
    blk = b.group(0)
    name = next((k for k in labs if f'aria-label="{k}' in blk), None)
    if not name: continue
    anc, lab = labs[name]
    nb = re.sub(r'^<a href="[^"]*"', f'<a href="/de/ratgeber/standtypen/#{anc}"', blk)
    nb = re.sub(r'(Passt dieser Typ zu Ihnen\?|[A-ZÄÖÜa-zäöü]+ im Detail)&nbsp;→', lab + '&nbsp;→', nb)
    s = s.replace(blk, nb, 1)
# "See trade fair pages" line under the fairs intro
old = 'Nach diesen Messen fragen Aussteller uns am häufigsten:</p>'
if old in s:
    s = s.replace(old, 'Nach diesen Messen fragen Aussteller uns am häufigsten. <a href="/de/messen/" style="color: #13704D; font-weight: 600; white-space: nowrap">Zu unseren Messeseiten&nbsp;→</a> oder zum <a href="/de/ratgeber/messekalender-2027/" style="color: #13704D; white-space: nowrap">Messekalender&nbsp;2027</a>.</p>')
# footer: add Messen link after Ratgeber in the Unternehmen column if missing
i = s.find('<footer')
if i > 0 and '/de/messen/" style="color: #1C1A17; text-decoration: none">Messen</a></div>' not in s[i:]:
    s = s[:i] + re.sub(r'(<a href="/de/ratgeber/" style="color: #1C1A17; text-decoration: none">Ratgeber</a>)(</div>)', r'\1<a href="/de/messen/" style="color: #1C1A17; text-decoration: none">Messen</a>\2', s[i:], count=1)
open(f, 'w').write(s)
print('ok')
