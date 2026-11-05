"""Idempotent: 'Stand types' / 'Standtypen' in the header nav becomes a dropdown with the four stand
pages, FAQ leaves the header nav, and footer 'STANDS' links point at the stand pages.
Runs on EN pages (before build.py) and on the hand-edited de/index.html and de/danke.html."""
import re, glob
SITE = '/home/claude/1o1expo-sajt/'
STANDS = [('row', 'reihenstand', 'Row stand', 'Reihenstand', '1 open side', '1 offene Seite', 'Row stands', 'Reihenstände'),
          ('corner', 'eckstand', 'Corner stand', 'Eckstand', '2 open sides', '2 offene Seiten', 'Corner stands', 'Eckstände'),
          ('peninsula', 'kopfstand', 'Peninsula stand', 'Kopfstand', '3 open sides', '3 offene Seiten', 'Peninsula stands', 'Kopfstände'),
          ('island', 'inselstand', 'Island stand', 'Inselstand', '4 open sides', '4 offene Seiten', 'Island stands', 'Inselstände')]
ANCHOR = re.compile(r'<a href="([^"]*?)(?:index\.html)?#stands"((?: aria-current="page")?) style="([^"]*)">(Stand types|Standtypen)</a>')
OLD = re.compile(r'<div class="fdd">(<a [^>]*>(?:Stand types|Standtypen)</a>)<div class="fdd-m">.*?<i class="fdd-x"></i></span></div></div>', re.S)

def block(m, de):
    pre, cur, style, label = m.group(1), m.group(2), m.group(3), m.group(4)
    top = (pre + 'index.html#stands') if pre not in ('', '/de/') else ('#stands' if pre == '' else '/de/#stands')
    if de:
        items = ''.join(f'<a href="/de/messestand/{d}/"><span>{nd}</span><span class="fdd-d">{od}</span></a>' for _, d, _, nd, _, od, _, _ in STANDS)
        allt = '<a href="/de/ratgeber/standtypen/" class="fdd-all">Standtypen vergleichen&nbsp;→</a>'
    else:
        items = ''.join(f'<a href="{pre}stands/{e}/"><span>{ne}</span><span class="fdd-d">{oe}</span></a>' for e, _, ne, _, oe, _, _, _ in STANDS)
        allt = f'<a href="{pre}guides/stand-types/" class="fdd-all">Compare stand types&nbsp;→</a>'
    return (f'<div class="fdd"><a href="{top}"{cur} style="{style}">{label}</a><div class="fdd-m"><span class="fdd-p">'
            f'{allt}{items}<i class="fdd-x"></i></span></div></div>')

def run(path, de=False, pre=None):
    s = open(path).read(); o = s
    s = OLD.sub(r'\1', s)
    h = s.find('<nav class="hide-sm" aria-label="Main"')
    if h >= 0:
        e = s.find('</nav>', h); nav = s[h:e]
        nav = ANCHOR.sub(lambda m: block(m, de), nav, count=1)
        nav = re.sub(r'\s*<a href="[^"]*#faq" style="[^"]*">FAQ</a>', '', nav)
        s = s[:h] + nav + s[e:]
    # footer stand links
    i = s.find('<footer')
    if i > 0:
        f = s[i:]
        for e_, d_, _, _, _, _, pe, pd in STANDS:
            if de: f = re.sub(rf'<a href="[^"]*"( style="[^"]*")?>{pd}</a>', rf'<a href="/de/messestand/{d_}/"\1>{pd}</a>', f)
            else:
                p = pre
                f = re.sub(rf'<a href="[^"]*"( style="[^"]*")?>{pe}</a>', rf'<a href="{p}stands/{e_}/"\1>{pe}</a>', f)
        s = s[:i] + f
    if s != o: open(path, 'w').write(s)
    return s != o

def prefix(path):
    rel = path[len(SITE):]
    return '../' * rel.count('/')

if __name__ == '__main__':
    en = [p for p in glob.glob(SITE + '**/*.html', recursive=True) if '/de/' not in p and '/tools/' not in p]
    n = sum(run(p, pre=('/' if p.endswith('/404.html') else prefix(p))) for p in en)
    d = run(SITE + 'de/index.html', de=True) + run(SITE + 'de/danke.html', de=True)
    print('en', n, 'de', d)
