"""Idempotent: the dark green site footer (logo, Stands, Company, Contact with icons and a
call button, legal row with EN | DE). Runs on EN pages; run gen/fairs.py, gen/pages.py and
gen/notfound.py afterwards so generated pages pick it up from guides/stand-cost."""
import re, glob
SITE = '/home/claude/1o1expo-sajt/'
BOOK = 'https://bookings.cloud.microsoft/bookwithme/user/a20ad59f87524954acb3bec7ebf8fafe@1o1expo.com/meetingtype/E-M3e0osO02kEq45CkuijQ2?anonymous'
I_MAIL = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round" aria-hidden="true" style="flex: none"><rect x="3" y="5.5" width="18" height="13"/><path d="M3.5 6.5l8.5 6.5 8.5-6.5"/></svg>'
I_WA = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round" aria-hidden="true" style="flex: none"><path d="M12 2.6a9.4 9.4 0 0 0-8.1 14.1L2.6 21.4l4.8-1.3A9.4 9.4 0 1 0 12 2.6z"/><path d="M8.8 8.2c.4 2.9 3.3 5.9 6.6 6.8" stroke-linecap="round"/></svg>'
I_CAL = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true" style="flex: none"><rect x="3.5" y="5" width="17" height="15"/><path d="M3.5 9.5h17M8 3v4M16 3v4"/></svg>'
CSS = ('<style id="ft-css">.ft a{text-decoration:none}.ft .ft-l a:hover{color:#5ED3A2!important}.ft .ft-c a:hover span{text-decoration:underline}'
       '.ft .lsw a,.ft .lsw span{color:rgba(255,255,255,.7)!important}.ft .lsw [aria-current]{color:#FFFFFF!important}.ft .lsw .lsw-sep{color:rgba(255,255,255,.35)!important}'
       '.ft-call:hover{background:#7FE0B8!important}@media (max-width:900px){.ft-g{grid-template-columns:1fr 1fr!important}.ft-g>div:first-child{grid-column:1/-1}}'
       '@media (max-width:520px){.ft-g>div:last-child{grid-column:1/-1}}@media (min-width:701px){.ft .foot-legal{padding-right:230px}}</style>')

def footer(pre, home, logo, lsw):
    ix = '' if home else pre + 'index.html'
    L = lambda h, t: f'<a href="{h}" style="color: #FFFFFF; font-size: 16px">{t}</a>'
    col = lambda t, items: f'<div class="ft-l" style="display: flex; flex-direction: column; gap: 10px"><span style="font-size: 12px; letter-spacing: 0.08em; font-weight: 700; color: #5ED3A2">{t}</span>' + ''.join(L(h, x) for h, x in items) + '</div>'
    stands = col('STANDS', [(f'{pre}stands/row/', 'Row stands'), (f'{pre}stands/corner/', 'Corner stands'), (f'{pre}stands/peninsula/', 'Peninsula stands'), (f'{pre}stands/island/', 'Island stands'), (f'{pre}own-design/', 'Your own design')])
    company = col('COMPANY', [(f'{pre}quote/', 'Get a quote'), (f'{ix}#offer', 'Your offer'), (f'{ix}#faq', 'FAQ'), (f'{pre}about.html', 'About us'), (f'{pre}guides/', 'Guides'), (f'{pre}fairs/', 'Trade fairs')])
    contact = (f'<div class="ft-c" style="display: flex; flex-direction: column; gap: 12px"><span style="font-size: 12px; letter-spacing: 0.08em; font-weight: 700; color: #5ED3A2">CONTACT</span>'
               f'<a href="mailto:robert@1o1expo.com" style="display: inline-flex; align-items: center; gap: 10px; color: #FFFFFF; font-size: 16px"><span style="color: #5ED3A2; display: inline-flex">{I_MAIL}</span><span>robert@1o1expo.com</span></a>'
               f'<a href="{pre}quote/" class="wa-link" style="display: inline-flex; align-items: center; gap: 10px; color: #FFFFFF; font-size: 16px"><span style="color: #5ED3A2; display: inline-flex">{I_WA}</span><span>WhatsApp</span></a>'
               f'<a href="{BOOK}" target="_blank" rel="noopener" class="ft-call" style="margin-top: 6px; align-self: flex-start; display: inline-flex; align-items: center; gap: 10px; min-height: 48px; padding: 0 20px; background: #5ED3A2; color: #12100E; font-weight: 600; font-size: 16px; white-space: nowrap">{I_CAL}Book a 30-min call</a></div>')
    brand = f'<div style="display: flex; flex-direction: column; gap: 14px">{logo}<span style="color: rgba(255,255,255,.7); font-size: 15px; line-height: 1.55; max-width: 22em">Exhibition stands for trade fairs across Europe. Designed, built and ready on opening&nbsp;day.</span></div>'
    return (f'<footer class="ft" style="background: #0E3B2B; color: #FFFFFF"><div style="max-width: 1240px; margin: 0 auto; padding: 64px 24px 28px; display: flex; flex-direction: column; gap: 48px">'
            f'<div class="ft-g" style="display: grid; grid-template-columns: 1.3fr 1fr 1fr 1.2fr; gap: 40px">{brand}{stands}{company}{contact}</div>'
            f'<div class="foot-legal" style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 12px 24px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,.18); font-size: 13px; color: rgba(255,255,255,.65)">'
            f'<span>©&nbsp;2026&nbsp;1o1&nbsp;expo</span><span style="display: flex; flex-wrap: wrap; align-items: center; gap: 18px 24px">{lsw}<a href="{pre}legal.html" style="color: rgba(255,255,255,.65); text-decoration: underline">Legal notice</a><a href="{pre}privacy.html" style="color: rgba(255,255,255,.65); text-decoration: underline">Privacy policy</a></span></div></div></footer>')

def run(path):
    s = open(path).read(); o = s
    m = re.search(r'<footer[^>]*>.*?</footer>', s, re.S)
    if not m: return False
    old = m.group(0)
    a = re.search(r'href="([^"]*)about\.html"', old)
    if not a or 'class="ft"' not in old and 'Legal notice' not in old: return False
    pre = a.group(1)
    home = path.endswith('/index.html') and path[len(SITE):] == 'index.html'
    lg = re.search(r'<svg data-flogo.*?</svg>', old, re.S) or re.search(r'<svg[^>]*aria-label="1o1 expo".*?</svg>', old, re.S)
    logo = lg.group(0).replace('fill="#1C1A17"', 'fill="#FFFFFF"').replace('fill="#12100E"', 'fill="#FFFFFF"')
    ls = re.search(r'<div class="lsw".*?</div>', s, re.S)
    lsw = ls.group(0) if ls else ''
    s = s[:m.start()] + footer(pre, home, logo, lsw) + s[m.end():]
    s = re.sub(r'<style id="ft-css">.*?</style>\n?', '', s, flags=re.S)
    s = s.replace('</body>', CSS + '\n</body>', 1)
    if s != o: open(path, 'w').write(s)
    return s != o

if __name__ == '__main__':
    en = [p for p in glob.glob(SITE + '**/*.html', recursive=True) if '/de/' not in p and '/tools/' not in p]
    print('en', sum(run(p) for p in en))
