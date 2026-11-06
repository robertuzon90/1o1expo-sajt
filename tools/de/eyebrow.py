"""Idempotent: small uppercase labels above headings get the marker style
(black text on a half-height #5ED3A2 bar; on dark green: black text on a full bar).
Run on EN pages after gen/fairs.py and gen/pages.py."""
import re, glob
SITE = '/home/claude/1o1expo-sajt/'
CSS = ('<style id="eyb-css">.eyb{color:#1C1A17!important;background:linear-gradient(transparent 48%,rgba(94,211,162,.5) 48%)!important;padding:2px 5px 3px!important;margin-left:-5px!important;line-height:1.2!important;align-self:flex-start}'
       '.eyb-w{color:#5ED3A2!important;background:linear-gradient(transparent 48%,#236B4F 48%)!important;padding:2px 5px 3px!important;margin-left:-5px!important;line-height:1.2!important;align-self:flex-start}'
       '.eyb-d,.hero-photo .hero-left>span:first-child{color:#12100E!important;background:#5ED3A2!important;padding:3px 6px!important;margin-left:-6px!important;line-height:1.2!important;align-self:flex-start}</style>')
SPAN = re.compile(r'<span(?: class="(tag|eyb|eyb-d|eyb-w)")? style="([^"]*font-size: ?12px[^"]*color: ?#(1F845B|5ED3A2)[^"]*)">([^<]{2,80})</span>(?!\s*<b )', re.I)
def run(path):
    s = open(path).read(); o = s
    fi = s.find('<footer'); tail = s[fi:] if fi >= 0 else ''; s = s[:fi] if fi >= 0 else s
    s = SPAN.sub(lambda m: f'<span class="{"eyb-w" if m.group(1) == "eyb-w" else ("eyb" if m.group(3).upper() == "1F845B" else "eyb-d")}" style="{m.group(2)}">{m.group(4)}</span>', s)
    tail = re.sub(r'<span class="eyb(?:-d|-w)?" (style="[^"]*">(?:STANDS|COMPANY|CONTACT)</span>)', r'<span \1', tail)
    s = s + tail
    if 'class="eyb' in s or 'hero-photo' in s:
        s = re.sub(r'<style id="eyb-css">.*?</style>\n?', '', s, flags=re.S)
        s = s.replace('</body>', CSS + '\n</body>', 1)
    if s != o: open(path, 'w').write(s)
    return s != o
if __name__ == '__main__':
    en = [p for p in glob.glob(SITE + '**/*.html', recursive=True) if '/de/' not in p and '/tools/' not in p]
    print('en', sum(run(p) for p in en))
