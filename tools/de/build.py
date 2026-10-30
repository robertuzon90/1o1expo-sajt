import sys, re, json, os, html, urllib.parse, posixpath
sys.path.insert(0, '/home/claude/de-build')
from units import split, runs, key_of
SITE = '/home/claude/1o1expo-sajt/'
TR = json.load(open('/home/claude/de-build/tr.json'))
TR.update(json.load(open('/home/claude/de-build/tr_extra.json')))
ATTR = json.load(open('/home/claude/de-build/attr.json'))
META = json.load(open('/home/claude/de-build/meta.json'))
FAIR_DE = {'ambiente-frankfurt': 'ambiente-frankfurt', 'mwc-barcelona': 'mwc-barcelona', 'hannover-messe': 'hannover-messe',
           'intersolar-europe': 'intersolar-europe-muenchen', 'eurobike-frankfurt': 'eurobike-frankfurt', 'gamescom-cologne': 'gamescom-koeln',
           'ifa-berlin': 'ifa-berlin', 'sbc-summit-lisbon': 'sbc-summit-lissabon', 'reneo-budapest': 'reneo-budapest', 'cphi-frankfurt': 'cphi-frankfurt'}
URLMAP = [('/index.html', '/de/'), ('/about.html', '/de/ueber-uns.html'), ('/legal.html', '/de/impressum.html'), ('/privacy.html', '/de/datenschutz.html'),
          ('/review-thanks.html', '/de/bewertung-danke.html'), ('/review.html', '/de/bewertung.html'), ('/thanks.html', '/de/danke.html'), ('/404.html', '/de/404.html'),
          ('/guides/stand-types/', '/de/ratgeber/standtypen/'), ('/guides/stand-brief/', '/de/ratgeber/standbriefing/'), ('/guides/stand-cost/', '/de/ratgeber/standkosten/'),
          ('/guides/trade-fair-timeline/', '/de/ratgeber/messe-zeitplan/'), ('/guides/trade-fair-calendar-2027/', '/de/ratgeber/messekalender-2027/'), ('/guides/', '/de/ratgeber/')]
URLMAP += [(f'/fairs/{k}/', f'/de/messen/{v}/') for k, v in FAIR_DE.items()] + [('/fairs/', '/de/messen/')]
PAGES = ['about.html', 'legal.html', 'privacy.html', '404.html', 'review.html', 'review-thanks.html', 'guides/index.html'] + \
        [f'guides/{g}/index.html' for g in ['stand-types', 'stand-brief', 'stand-cost', 'trade-fair-timeline', 'trade-fair-calendar-2027']] + \
        ['fairs/index.html'] + [f'fairs/{k}/index.html' for k in FAIR_DE]

def en_url(p):  # site path of an EN page
    return '/' + (p[:-len('index.html')] if p.endswith('index.html') else p)
def map_path(path):
    if path in ('/', ''): return '/de/'
    for a, b in URLMAP:
        if path == a or (a.endswith('/') and path.startswith(a) and path == a): return b
    for a, b in URLMAP:
        if path == a: return b
    return None
def de_url(p): return map_path(en_url(p))

def resolve(href, base):
    if re.match(r'^(https?:|mailto:|tel:|#|data:|javascript:)', href): return None
    u = urllib.parse.urlsplit(href)
    path = u.path
    if not path.startswith('/'):
        path = posixpath.normpath(posixpath.join(posixpath.dirname(base), path)) + ('/' if path.endswith('/') or path in ('', '.', './') else '')
        if path.startswith('//'): path = path[1:]
    if path == '/.': path = '/'
    return path, u.query, u.fragment

def rewrite_url(href, base, page):
    r = resolve(href, base)
    if r is None: return href
    path, q, frag = r
    if path.startswith('/de/'): return '/' + path[4:] if path != '/de/' else '/'   # EN link inside EN page pointing to DE (language switch) -> EN, fixed later
    m = map_path(path)
    if m is None:
        m = path  # assets: img, downloads, etc.
    out = m + (('?' + q) if q else '') + (('#' + frag) if frag else '')
    return out

def translate_runs(s, missing):
    parts, rs = runs(s)
    repl = {}
    for r in rs:
        k, tags, lead, trail = key_of(r)
        if k not in TR:
            missing.add(k); continue
        v = TR[k]
        out = re.sub(r'\{(\d+)\}', lambda m: tags[int(m.group(1))], v)
        idx = [i for i, _ in r]
        repl[idx[0]] = lead + out + trail
        for i in idx[1:]: repl[i] = ''
    return ''.join(repl.get(i, p) for i, p in enumerate(parts))

def translate_attrs(s, missing):
    def f(m):
        a, v = m.group(1), m.group(2)
        if not v.strip() or v in ('1o1 expo',): return m.group(0)
        if v in ATTR: return f'{a}="{ATTR[v]}"'
        missing.add('ATTR:' + v); return m.group(0)
    return re.sub(r'\b(alt|aria-label|placeholder|data-cap|data-alt)="([^"]*)"', f, s)

def translate_meta(s, missing):
    def f(m):
        pre, v = m.group(1), m.group(2)
        vn = v.replace('\xa0', ' ').replace('&nbsp;', ' ')
        if v in META: return f'{pre}"{META[v]}"'
        if vn in META: return f'{pre}"{META[vn]}"'
        missing.add('META:' + v); return m.group(0)
    s = re.sub(r'(<meta (?:name="description"|property="og:title"|property="og:description"|property="og:image:alt") content=)"([^"]*)"', f, s)
    return s

def ld_tr(obj, missing):
    norm = lambda x: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', x)).replace('\xa0', ' ')).strip()
    NT = {norm(k): norm(v) for k, v in TR.items() if '{' not in k}
    NT.update({norm(k): norm(v) for k, v in META.items()})
    NT.update({'Guides': 'Ratgeber', 'Trade fairs': 'Messen'})
    def walk(o, key=None):
        if isinstance(o, dict): return {k: walk(v, k) for k, v in o.items()}
        if isinstance(o, list): return [walk(v) for v in o]
        if isinstance(o, str):
            if o.startswith('https://1o1expo.com'):
                p = o[len('https://1o1expo.com'):] or '/'
                m = map_path(p); return 'https://1o1expo.com' + (m or p)
            if key in ('@context', '@type', 'url', 'item', 'datePublished', 'dateModified', 'image'):
                if key in ('url', 'item') and o.startswith('https://1o1expo.com'):
                    p = o[len('https://1o1expo.com'):] or '/'
                    m = map_path(p); return 'https://1o1expo.com' + (m or p)
                return o
            if key == 'inLanguage': return 'de'
            if key == 'name' and o in ('1o1 expo',): return o
            n = norm(o)
            if n in NT: return NT[n]
            missing.add('LD:' + o); return o
        return o
    return walk(obj)

def build(p, missing):
    s = open(SITE + p).read()
    base = en_url(p) if not p.endswith('/') else en_url(p)
    base_file = '/' + p
    url_de = de_url(p); url_en = en_url(p)
    # 1 JSON-LD
    def ldf(m):
        try: obj = json.loads(m.group(2))
        except Exception: return m.group(0)
        return m.group(1) + json.dumps(ld_tr(obj, missing), ensure_ascii=False) + '</script>'
    s = re.sub(r'(<script type="application/ld\+json">)(.*?)</script>', ldf, s, flags=re.S)
    # 2 text + attrs + meta
    s = translate_runs(s, missing)
    s = translate_attrs(s, missing)
    s = translate_meta(s, missing)
    # 3 urls (href, src, action, data-src)
    s = re.sub(r'\b(href|src|action|data-src)="([^"]*)"', lambda m: f'{m.group(1)}="{rewrite_url(m.group(2), base_file, p)}"', s)
    # absolute site urls (canonical, og:url, share links)
    def absu(m):
        path = m.group(1) or '/'
        mp = map_path(path)
        return 'https://1o1expo.com' + (mp or path)
    s = re.sub(r'https://1o1expo\.com(/[^"\s&<]*)?(?=["\s&<])', absu, s)
    enc_en = urllib.parse.quote('https://1o1expo.com' + url_en, safe='')
    enc_de = urllib.parse.quote('https://1o1expo.com' + url_de, safe='')
    s = s.replace(enc_en, enc_de)
    # mailto subject -> German h1
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    if h1:
        subj = urllib.parse.quote(html.unescape(re.sub(r'<[^>]+>', '', h1.group(1))).replace('\xa0', ' ').strip())
        s = re.sub(r'mailto:\?subject=[^&"]*', 'mailto:?subject=' + subj, s)
    # 4 lang + hreflang
    s = s.replace('<html lang="en">', '<html lang="de">', 1)
    s = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', '', s)
    alt = f'<link rel="alternate" hreflang="en" href="https://1o1expo.com{url_en}">\n<link rel="alternate" hreflang="de" href="https://1o1expo.com{url_de}">\n<link rel="alternate" hreflang="x-default" href="https://1o1expo.com{url_en}">\n'
    s = s.replace('</head>', alt + '<style>@media (max-width:700px){h1,h2,h3,td,th{-webkit-hyphens:auto;hyphens:auto;overflow-wrap:break-word}table{font-size:14px!important}th,td{padding:10px 8px!important}article,.art>*{min-width:0}h1 span[style*=nowrap]{white-space:normal!important}div[style*="overflow-x: auto"]{max-width:calc(100vw - 48px)}}</style>\n</head>', 1)
    # 5 language switch
    s = re.sub(r'<div class="lsw" role="group" aria-label="[^"]*">.*?</div>',
               f'<div class="lsw" role="group" aria-label="Sprache"><a href="{url_en}" hreflang="en" lang="en">EN</a><span class="lsw-sep" aria-hidden="true">|</span><span aria-current="true" lang="de">DE</span></div>', s, count=1, flags=re.S)
    # 6 JS strings
    js = [('m="Hi 1o1 expo, I\'m planning a stand for this fair: "', 'm="Hallo 1o1 expo, ich plane einen Stand für diese Messe: "'),
          ('"Link copied"', '"Link kopiert"'), ('"Copy link"', '"Link kopieren"'), ('"Copied"', '"Kopiert"'), ('"Copy failed"', '"Kopieren fehlgeschlagen"'), ('"Copy as text"', '"Als Text kopieren"'),
          ("e.textContent='now'", "e.textContent='jetzt'"), ("sp.firstChild.textContent='Brief us '", "sp.firstChild.textContent='Briefing: '"),
          ('"Trade fairs in "+safe+" with their own page."', '"Messen in "+safe+" mit eigener Seite."'),
          ('"We build at fairs in "+safe+" too. Tell us which fair and we will send you a design and a price. "', '"Wir bauen auch auf Messen in "+safe+". Sagen Sie uns, welche Messe, und Sie erhalten einen Entwurf und einen Preis. "'),
          ('var safe=c.replace(', 'var N={Munich:"München",Cologne:"Köln",Milan:"Mailand",Lisbon:"Lissabon"};var safe=c.replace('),
          ('"Messen in "+safe+"', '"Messen in "+(N[safe]||safe)+"'), ('"Wir bauen auch auf Messen in "+safe+"', '"Wir bauen auch auf Messen in "+(N[safe]||safe)+"'),
          ('a.textContent="Get a quote →"', 'a.textContent="Angebot anfragen →"'), ('a.href="../index.html?fair="', 'a.href="/de/?fair="')]
    for a, b in js: s = s.replace(a, b)
    s = s.replace('<p lang="de" style="margin: 6px 0 0; font-size: 15px; color: rgba(255,255,255,.65)">Page not found', '<p lang="en" style="margin: 6px 0 0; font-size: 15px; color: rgba(255,255,255,.65)">Page not found')
    # fairs hub city param links: /index.html?fair=.. already mapped by href rewrite; quote links in fairs -> /de/?fair=
    return s, url_de

if __name__ == '__main__':
    missing = set(); out = {}
    for p in PAGES:
        s, u = build(p, missing)
        dest = SITE + u.lstrip('/') + ('index.html' if u.endswith('/') else '')
        out[dest] = s
    if '--check' in sys.argv or missing:
        json.dump(sorted(missing), open('/home/claude/de-build/missing.json', 'w'), ensure_ascii=False, indent=0)
        print('missing', len(missing))
    if '--write' in sys.argv:
        for d, s in out.items():
            os.makedirs(os.path.dirname(d), exist_ok=True); open(d, 'w').write(s)
        print('written', len(out))
