"""Idempotent: the floating WhatsApp button becomes a card with the founder's photo,
'Chat with Robert' and 'on WhatsApp'. Runs on hand-edited EN pages and de/index.html;
generated pages inherit it from guides/stand-cost (fairs.py, pages.py, build.py)."""
import re, glob, sys
SITE = '/home/claude/1o1expo-sajt/'
CSS = ('<style id="wa-pill-css">.wa-pill{width:auto!important;height:auto!important;border-radius:0!important;background:#FCFAF6!important;border:0!important;padding:7px 16px 7px 7px;gap:11px;justify-content:flex-start!important;text-decoration:none}'
       '.wa-ph{position:relative;width:42px;height:42px;flex:none}.wa-ph img{width:42px;height:42px;border-radius:50%;object-fit:cover;display:block}'
       '.wa-pill .wa-ph svg{position:absolute;right:-5px;bottom:-5px;width:20px!important;height:20px!important;padding:2px;background:#5ED3A2;border-radius:50%;box-sizing:border-box}'
       '.wa-t{display:flex;flex-direction:column;line-height:1.2;color:#12100E;font-family:"DM Sans",sans-serif;white-space:nowrap}.wa-t b{font-size:15px;font-weight:600}.wa-t span{font-size:13px}'
       '.wa-pill .wa-tip{display:none}.wa-pill:hover,.wa-pill:focus-visible{transform:translateY(-2px)!important}'
       '@media (max-width:700px){.wa-pill{right:16px!important;bottom:16px!important}.foot-legal{padding-bottom:72px}}</style>')
A = re.compile(r'<a href="([^"]*)" class="wa-link wa-float(?: wa-pill)?" aria-label="[^"]*">(.*?)</a>', re.S)
def run(path, de=False):
    s = open(path).read(); o = s
    m = A.search(s)
    if not m: return False
    svg = re.search(r'<svg.*?</svg>', m.group(2), re.S).group(0)
    t1, t2, al = ('Mit Robert chatten', 'auf WhatsApp', 'Mit Robert auf WhatsApp chatten') if de else ('Chat with Robert', 'on WhatsApp', 'Chat with Robert on WhatsApp')
    new = (f'<a href="{m.group(1)}" class="wa-link wa-float wa-pill" aria-label="{al}"><span class="wa-ph"><img src="/img/founder.jpg" alt="" width="42" height="42">{svg}</span>'
           f'<span class="wa-t" aria-hidden="true"><b>{t1}</b><span>{t2}</span></span></a>')
    s = s[:m.start()] + new + s[m.end():]
    s = re.sub(r'<style id="wa-pill-css">.*?</style>\n?', '', s, flags=re.S)
    s = s.replace('</body>', CSS + '\n</body>', 1)
    if s != o: open(path, 'w').write(s)
    return s != o
if __name__ == '__main__':
    en = [p for p in glob.glob(SITE + '**/*.html', recursive=True) if '/de/' not in p and '/tools/' not in p]
    print('en', sum(run(p) for p in en), 'de', run(SITE + 'de/index.html', de=True) if '--de' in sys.argv else 'skipped')
