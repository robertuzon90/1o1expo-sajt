import sys;sys.path.insert(0,'/home/claude/de-build')
from build import PAGES,en_url,de_url,SITE
pairs=[('/','/de/')]+[(en_url(p),de_url(p)) for p in PAGES if p not in ('404.html','review.html','review-thanks.html')]
D='2026-10-29'
rows=[]
for e,d in pairs:
    alt=f'<xhtml:link rel="alternate" hreflang="en" href="https://1o1expo.com{e}"/><xhtml:link rel="alternate" hreflang="de" href="https://1o1expo.com{d}"/><xhtml:link rel="alternate" hreflang="x-default" href="https://1o1expo.com{e}"/>'
    for u in (e,d): rows.append(f'  <url><loc>https://1o1expo.com{u}</loc><lastmod>{D}</lastmod>{alt}</url>')
open(SITE+'sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'+'\n'.join(rows)+'\n</urlset>\n')
print(len(rows))
