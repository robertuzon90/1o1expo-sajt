"""Idempotent: turn the 'Trade fairs' / 'Messen' item in the main header nav into a dropdown
listing every fair page. Runs on EN pages (before build.py, so DE pages inherit it translated)
and on the hand-edited de/index.html."""
import re, glob, os
SITE = '/home/claude/1o1expo-sajt/'
FAIRS = [  # hub order (chronological)
    ('ambiente-frankfurt', 'ambiente-frankfurt', 'Ambiente Frankfurt', 'Ambiente Frankfurt', '29 Jan – 2 Feb 2027', '29. Jan. – 2. Feb. 2027'),
    ('mwc-barcelona', 'mwc-barcelona', 'MWC Barcelona', 'MWC Barcelona', '1–4 Mar 2027', '1.–4. März 2027'),
    ('reneo-budapest', 'reneo-budapest', 'RENEO Budapest', 'RENEO Budapest', 'Apr 2027 (TBC)', 'Apr. 2027 (offen)'),
    ('hannover-messe', 'hannover-messe', 'Hannover Messe', 'Hannover Messe', '5–8 Apr 2027', '5.–8. Apr. 2027'),
    ('intersolar-europe', 'intersolar-europe-muenchen', 'Intersolar Europe Munich', 'Intersolar Europe München', '8–10 Jun 2027', '8.–10. Juni 2027'),
    ('eurobike-frankfurt', 'eurobike-frankfurt', 'Eurobike Frankfurt', 'Eurobike Frankfurt', '30 Jun – 2 Jul 2027', '30. Juni – 2. Juli 2027'),
    ('gamescom-cologne', 'gamescom-koeln', 'gamescom Cologne', 'gamescom Köln', '23–29 Aug 2027', '23.–29. Aug. 2027'),
    ('ifa-berlin', 'ifa-berlin', 'IFA Berlin', 'IFA Berlin', '3–7 Sep 2027', '3.–7. Sept. 2027'),
    ('sbc-summit-lisbon', 'sbc-summit-lissabon', 'SBC Summit Lisbon', 'SBC Summit Lissabon', '21–23 Sep 2027', '21.–23. Sept. 2027'),
    ('cphi-frankfurt', 'cphi-frankfurt', 'CPHI Frankfurt', 'CPHI Frankfurt', '9–11 Nov 2027', '9.–11. Nov. 2027'),
]
CSS = ('<style id="fdd-css">.fdd{position:relative;display:flex;align-items:center}'
       '.fdd>a::after{content:"";display:inline-block;width:6px;height:6px;margin-left:8px;border-right:1.6px solid currentColor;border-bottom:1.6px solid currentColor;transform:translateY(-3px) rotate(45deg);transition:transform .2s}'
       '.fdd:hover>a::after,.fdd:focus-within>a::after{transform:translateY(0) rotate(225deg)}'
       '.fdd-m{position:absolute;left:-22px;top:100%;padding-top:14px;z-index:60;opacity:0;visibility:hidden;transform:translateY(-4px);transition:opacity .18s,transform .18s,visibility .18s}'
       '.fdd:hover .fdd-m,.fdd:focus-within .fdd-m{opacity:1;visibility:visible;transform:none}'
       '.fdd-p{display:flex;flex-direction:column;width:330px;background:#FFFFFF;border:1px solid #D8D1C5;box-shadow:0 18px 40px rgba(28,26,23,.12);padding:8px}'
       '.fdd-p a{display:flex;justify-content:space-between;align-items:baseline;gap:16px;padding:9px 12px;color:#1C1A17!important;text-decoration:none;font-size:15px;font-weight:500!important}'
       '.fdd-p a:hover,.fdd-p a:focus-visible{background:#DDF4EA}'
       '.fdd-p a .fdd-d{flex:none;font-size:13px;color:#6B665F;font-weight:400}'
       '.fdd-p a.fdd-all{color:#13704D!important;font-weight:600!important;border-bottom:1px solid #E6E0D6;margin-bottom:4px;padding-bottom:11px}'
       '</style>')
ANCHOR = re.compile(r'<a href="([^"]*)"((?: aria-current="page")?) style="([^"]*)">(Trade fairs|Messen)</a>')
OLD = re.compile(r'<div class="fdd">(<a [^>]*>(?:Trade fairs|Messen)</a>)<div class="fdd-m">.*?<i class="fdd-x"></i></span></div></div>', re.S)

def block(m, de):
    base, cur, style, label = m.group(1), m.group(2), m.group(3), m.group(4)
    if de:
        items = ''.join(f'<a href="/de/messen/{d}/"><span>{nd}</span><span class="fdd-d">{dd}</span></a>' for _, d, _, nd, _, dd in FAIRS)
        allt = 'Alle Messen&nbsp;→'
    else:
        items = ''.join(f'<a href="{base}{e}/"><span>{ne}</span><span class="fdd-d">{de_}</span></a>' for e, _, ne, _, de_, _ in FAIRS)
        allt = 'All trade fairs&nbsp;→'
    return (f'<div class="fdd"><a href="{base}"{cur} style="{style}">{label}</a><div class="fdd-m"><span class="fdd-p">'
            f'<a href="{base}" class="fdd-all">{allt}</a>{items}<i class="fdd-x"></i></span></div></div>')

def run(path, de=False):
    s = open(path).read()
    s = OLD.sub(r'\1', s)
    h = s.find('<nav class="hide-sm" aria-label="Main"')
    if h < 0: return False
    e = s.find('</nav>', h)
    nav = s[h:e]
    nav2 = ANCHOR.sub(lambda m: block(m, de), nav, count=1)
    if nav2 == nav: return False
    s = s[:h] + nav2 + s[e:]
    s = re.sub(r'<style id="fdd-css">.*?</style>', '', s, flags=re.S)
    s = s.replace('</head>', CSS + '\n</head>', 1)
    open(path, 'w').write(s)
    return True

if __name__ == '__main__':
    en = [p for p in glob.glob(SITE + '**/*.html', recursive=True) if '/de/' not in p and '/tools/' not in p]
    n = sum(run(p) for p in en)
    d = run(SITE + 'de/index.html', de=True)
    print('en', n, 'de/index', d)
