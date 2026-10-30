import re
SITE = '/home/claude/1o1expo-sajt/'
s = open(SITE + 'fairs/index.html').read()
i = s.find('</header>'); j = s.find('class="cta-box'); k = s.rfind('<section', 0, j)
head, tail = s[:i], s[k:]
# drop the closing CTA section, keep everything after it (footer, scripts)
end_cta = tail.find('</section>') + len('</section>')
tail = tail[end_cta:]

def absol(x):
    x = re.sub(r'(href|src)="\.\./', r'\1="/', x)
    x = x.replace('href="./"', 'href="/fairs/"')
    return x
head, tail = absol(head), absol(tail)
head = head.replace('aria-current="page" style="color: #13704D; text-decoration: none; font-weight: 600">Trade fairs', 'style="color: #1C1A17; text-decoration: none">Trade fairs')
head = re.sub(r'<title>[^<]*</title>', '<title>Page not found | 1o1 expo</title>', head)
head = re.sub(r'<meta name="description" content="[^"]*">\n?', '', head)
head = re.sub(r'<link rel="canonical"[^>]*>\n?', '', head)
head = re.sub(r'<meta property="og:[^>]*>\n?', '', head)
head = re.sub(r'<meta name="twitter:[^>]*>\n?', '', head)
head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head)
head = head.replace('<meta name="robots" content="noindex, nofollow">', '<meta name="robots" content="noindex, follow"><!-- keep noindex on this page after launch -->')

ARROW = '<span aria-hidden="true">→</span>'
links = [('/fairs/', 'Trade fairs', 'Stands for Hannover Messe, CPHI, MWC, gamescom and more'),
         ('/guides/', 'Guides', 'Stand types, briefs, costs and your trade fair timeline'),
         ('/guides/trade-fair-calendar-2027/', 'Trade fair calendar 2027', 'Dates of the major European fairs'),
         ('/about.html', 'About us', 'Who we are and how we work')]
cards = ''.join(f'<a href="{h}" class="nf-c"><b>{t}&nbsp;→</b><span>{d}</span></a>' for h, t, d in links)
body = f'''</header><section style="background: #0E3B2B; color: #FFFFFF"><div class="nf" style="max-width: 1240px; margin: 0 auto; padding: 72px 24px 80px; display: grid; grid-template-columns: minmax(0,1fr) 360px; gap: 48px; align-items: center">
<div style="display: flex; flex-direction: column; gap: 20px">
<span style="font-size: 12px; letter-spacing: .08em; font-weight: 700; color: #5ED3A2">ERROR 404</span>
<h1 style="margin: 0; font-size: clamp(36px, 5vw, 60px); line-height: 1.04; letter-spacing: -0.03em; font-weight: 600">This stand isn't&nbsp;here.</h1>
<p style="margin: 0; max-width: 34em; font-size: 19px; line-height: 1.6; color: rgba(255,255,255,.85)">The page you are looking for doesn't exist, or it has moved. Let's get you back on the right&nbsp;aisle.</p>
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 14px 24px; margin-top: 8px"><a href="/" style="display: inline-flex; align-items: center; gap: 10px; min-height: 54px; padding: 0 24px; background: #5ED3A2; color: #12100E; font-weight: 600; font-size: 17px; text-decoration: none">Back to the homepage {ARROW}</a><a href="/index.html#quote" style="color: #FFFFFF; font-weight: 600; font-size: 17px; text-decoration: none; padding-bottom: 4px; background: linear-gradient(#5ED3A2,#5ED3A2) left bottom / 100% 2px no-repeat">or get your quote</a></div>
<p lang="de" style="margin: 6px 0 0; font-size: 15px; color: rgba(255,255,255,.65)">Seite nicht gefunden. <a href="/de/" style="color: #5ED3A2">Zur deutschen Startseite&nbsp;→</a></p>
</div>
<svg class="nf-art" viewBox="0 0 360 300" width="360" height="300" aria-hidden="true">
<g stroke="#5ED3A2" stroke-opacity=".25" stroke-width="1">{''.join(f'<line x1="{x}" y1="40" x2="{x}" y2="260"/>' for x in range(20, 361, 40))}{''.join(f'<line x1="0" y1="{y}" x2="360" y2="{y}"/>' for y in range(40, 261, 40))}</g>
<rect x="100" y="80" width="160" height="120" fill="#5ED3A2" fill-opacity=".08" stroke="#5ED3A2" stroke-width="2.5" stroke-dasharray="10 8"/>
<text x="180" y="132" text-anchor="middle" font-family="DM Sans, sans-serif" font-size="40" font-weight="700" fill="#5ED3A2">404</text>
<text x="180" y="160" text-anchor="middle" font-family="DM Sans, sans-serif" font-size="12" font-weight="700" letter-spacing="1.6" fill="#BDECD7">STAND NOT FOUND</text>
<text x="180" y="236" text-anchor="middle" font-family="DM Sans, sans-serif" font-size="11" font-weight="700" letter-spacing="1.6" fill="#7FA897">AISLE</text>
</svg></div></section>
<section style="max-width: 1240px; margin: 0 auto; padding: 56px 24px 104px"><h2 style="margin: 0 0 20px; font-size: 26px; letter-spacing: -0.01em; font-weight: 600">Popular pages</h2><div class="nf-g">{cards}</div></section>
<style>.nf-g{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}}.nf-c{{display:flex;flex-direction:column;gap:6px;padding:20px 22px;background:#fff;border:1px solid #E6E0D6;text-decoration:none;color:#1C1A17;transition:border-color .2s,box-shadow .2s}}.nf-c b{{font-size:18px;font-weight:600}}.nf-c span{{font-size:15px;line-height:1.5;color:#3F3B36}}.nf-c:hover{{border-color:#5ED3A2;box-shadow:0 10px 24px rgba(28,26,23,.08)}}@media (max-width:1000px){{.nf{{grid-template-columns:minmax(0,1fr)!important}}.nf-art{{display:none}}.nf-g{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}@media (max-width:560px){{.nf-g{{grid-template-columns:1fr}}}}</style>'''
open(SITE + '404.html', 'w').write(head + body + tail)
print('ok')
