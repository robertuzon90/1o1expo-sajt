"""Builds the stand type pages (/stands/<type>/), the quote page (/quote/) and the
'your own design' page (/own-design/). Run after any header/footer change on the guides,
then tools/de/build.py, link_lang.py and sitemap.py for the German versions."""
import re, json, os, urllib.parse
SITE = '/home/claude/1o1expo-sajt/'
_T = open(SITE + 'guides/stand-cost/index.html').read()
_T = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', '', _T)
HEAD0 = _T[:_T.find('</header>')].rstrip('\n')
TAIL0 = _T[_T.rfind('<section', 0, _T.find('class="cta-box')):]
INDEX = open(SITE + 'index.html').read()
FORM0 = INDEX[INDEX.index('<form name="quote"'):INDEX.index('</form>', INDEX.index('<form name="quote"')) + 7]
BOOK = 'https://bookings.cloud.microsoft/bookwithme/user/a20ad59f87524954acb3bec7ebf8fafe@1o1expo.com/meetingtype/E-M3e0osO02kEq45CkuijQ2?anonymous'

P = '<p style="margin: 0">'
NB = lambda s: s.replace('&nbsp;', ' ')
def H2(id_, t, first=False):
    st = '' if first else '; padding-top: 40px; border-top: 1px solid #D8D1C5'
    return f'<section id="{id_}" style="scroll-margin-top: 24px; display: flex; flex-direction: column; gap: 20px{st}"><h2 style="margin: 0; font-size: 32px; line-height: 1.1; letter-spacing: -0.02em; font-weight: 600">{t}</h2>'
TICK = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true" style="flex: none; margin-top: 5px"><circle cx="12" cy="12" r="11" fill="#13704D"/><path d="M7 12.5l3.2 3.2L17 9" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
WARN = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true" style="flex: none; margin-top: 5px"><circle cx="12" cy="12" r="11" fill="#8A6A1E"/><path d="M12 6.5v7M12 17v.5" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/></svg>'
BOLD = '<b style="display: block; margin-bottom: 2px">'
def _lead(x): return re.sub(r"^<b>([^<]*</b>) ?", lambda m: BOLD + m.group(1), x)
def ul(items, ico=TICK, size=''):
    return f'<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 12px{size}">' + ''.join(f'<li style="display: flex; gap: 12px; align-items: flex-start">{ico}<span>{_lead(x)}</span></li>' for x in items) + '</ul>'
def faq_html(faq):
    return '<div style="display: flex; flex-direction: column; gap: 10px">' + ''.join(f'<details class="gq" style="background: #FFFFFF; border: 1px solid #D8D1C5"><summary style="list-style: none; cursor: pointer; display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 18px 20px; font-weight: 600; font-size: 17px"><span>{q}</span><span class="gq-plus" aria-hidden="true" style="flex: none; width: 28px; height: 28px; border-radius: 50%; border: 1.5px solid #1C1A17; display: flex; align-items: center; justify-content: center; transition: transform .2s">+</span></summary><p style="margin: 0; padding: 0 20px 20px; font-size: 16px; line-height: 1.6; color: #3F3B36">{a}</p></details>' for q, a in faq) + '</div>'
def faq_ld(faq): return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": NB(re.sub('<[^>]+>', '', q)), "acceptedAnswer": {"@type": "Answer", "text": NB(re.sub('<[^>]+>', '', a))}} for q, a in faq]}
def crumbs(items): return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}
def ld(objs, h): return h.replace('</head>', ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in objs) + '</head>')

def head(title, desc, url, img='https://1o1expo.com/img/og-image.jpg'):
    h = HEAD0
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', h)
    h = h.replace('https://1o1expo.com/guides/stand-cost/', url)
    h = re.sub(r'<meta property="og:type" content="article">\n<meta property="article:published_time" content="[^"]*">\n<meta property="article:modified_time" content="[^"]*">', '<meta property="og:type" content="website">', h)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', h)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', h)
    h = h.replace('https://1o1expo.com/img/guide-cost-buildup.jpg', img).replace('<meta property="og:image:width" content="1672">', '<meta property="og:image:width" content="1200">').replace('<meta property="og:image:height" content="941">', '<meta property="og:image:height" content="630">')
    h = re.sub(r'<meta property="og:image:alt" content="[^"]*">', f'<meta property="og:image:alt" content="{title}">', h)
    h = re.sub(r'<title>[^<]*</title>', f"<title>{title} | 1o1 expo</title>", h)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', h)
    h = h.replace('<a href="../" aria-current="page" style="color: #13704D; text-decoration: none; font-weight: 600">Guides</a>', '<a href="../../guides/" style="color: #1C1A17; text-decoration: none">Guides</a>')
    return h

def tail(quote):
    t = TAIL0.replace('href="../../quote/" style="display: inline-flex', f'href="{quote}" style="display: inline-flex', 1)
    return t.replace('href="../"', 'href="../../guides/"')

def write(path, s):
    os.makedirs(os.path.dirname(SITE + path), exist_ok=True)
    open(SITE + path, 'w').write(s)

STEPS = [('Tell us about your fair', 'Your fair, hall, stand size and what visitors should remember. Rough notes and a phone photo of the floor plan are&nbsp;fine.'),
         ('Get your offer within 7 working days', 'A design for your space and the full price for the whole stand, so you see what you pay for before you&nbsp;decide.'),
         ('Approve the design', 'We adjust it with you until it fits. Every change is priced before you approve, and nothing is produced before your&nbsp;yes.'),
         ('We produce, deliver and build', 'The stand is made, shipped to the venue and built before the fair opens. When the fair closes, we take it&nbsp;down.')]
def steps_html(steps):
    return '<div style="background: #FFFFFF; border: 1px solid #D8D1C5; padding: 6px 24px 8px">' + ''.join(f'<div style="display: grid; grid-template-columns: 44px minmax(0,1fr); gap: 14px; padding: 16px 0{"; border-top: 1px solid #E6E0D6" if i else ""}"><span style="width: 34px; height: 34px; border-radius: 50%; background: #0E3B2B; color: #FFFFFF; display: inline-flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 700">{i+1}</span><div style="display: flex; flex-direction: column; gap: 4px"><b style="font-size: 19px; font-weight: 600">{t}</b><span style="font-size: 16px; line-height: 1.6; color: #3F3B36">{d}</span></div></div>' for i, (t, d) in enumerate(steps)) + '</div>'

INC = ['Stand design and visuals', 'Walls, flooring and furniture', 'Lighting and electrics on the stand', 'Printed graphics and branding', 'Transport to the venue', 'Build-up and dismantling']
def price_html(inc, intro, more=True):
    return (P + intro + '</p>' + f'<div class="pc2" style="display: grid; grid-template-columns: 1fr 1fr; border-top: 1.5px solid #1C1A17; border-bottom: 1px solid #D8D1C5"><div style="padding: 18px 24px 20px 0"><span style="display: block; font-size: 12px; letter-spacing: .08em; font-weight: 700; color: #13704D; margin-bottom: 10px">IN OUR PRICE</span>{ul(inc)}</div><div class="pc2-r" style="padding: 18px 0 20px 24px; border-left: 1px solid #D8D1C5"><span style="display: block; font-size: 12px; letter-spacing: .08em; font-weight: 700; color: #8A6A1E; margin-bottom: 10px">BOOKED WITH THE ORGANISER</span><p style="margin: 0; font-size: 17px; line-height: 1.6">Floor space, electricity and water connections, internet, cleaning and other venue services. You book and pay these directly with the organiser, and we tell you which ones your stand&nbsp;needs.</p></div></div>'
            + (P + 'More on this in <a href="../../guides/stand-cost/">What drives the cost of an exhibition stand</a>.</p>' if more else ''))

def toc_html(items):
    return '<nav class="toc" aria-label="On this page" style="position: sticky; top: 24px; display: flex; flex-direction: column; font-size: 15px"><span style="font-size: 12px; letter-spacing: .08em; font-weight: 700; color: #5B5650; padding-bottom: 8px">ON THIS&nbsp;PAGE</span>' + ''.join(f'<a href="#{i}" style="color: #1C1A17; text-decoration: none; padding: 6px 0; border-bottom: 1px solid #E6E0D6">{t}</a>' for i, t in items) + '</nav>'

def hero_side(crumb, eyebrow, h1, lead, facts, cta_href, cta_text, img, alt, note='Free and without obligation.', caption='Concept visualisation'):
    fx = ''.join(f'<div style="display: flex; flex-direction: column; gap: 4px; padding: 0 28px; border-left: 1px solid rgba(255,255,255,.22)"><span style="font-size: 12px; letter-spacing: .08em; font-weight: 700; color: #5ED3A2">{k.upper()}</span><b style="font-size: 18px; font-weight: 600">{v}</b></div>' for k, v in facts)
    return f'''</header><section style="background: #0E3B2B; color: #FFFFFF"><div class="fh" style="max-width: 1240px; margin: 0 auto; padding: 56px 24px 56px; display: grid; grid-template-columns: minmax(0,1.15fr) minmax(0,.85fr); gap: 48px; align-items: center"><div style="display: flex; flex-direction: column; gap: 22px">
<nav aria-label="Breadcrumb" style="font-size: 15px; color: rgba(255,255,255,.7)">{crumb}</nav>
<span style="font-size: 12px; letter-spacing: .08em; font-weight: 700; color: #5ED3A2; margin-bottom: -10px">{eyebrow}</span>
<h1 style="margin: 0; max-width: 18em; font-size: clamp(34px, 4.6vw, 56px); line-height: 1.05; letter-spacing: -0.03em; font-weight: 600; text-wrap: balance">{h1}</h1>
<p style="margin: 0; max-width: 38em; font-size: 19px; line-height: 1.6; color: rgba(255,255,255,.85)">{lead}</p>
<div class="fx" style="display: flex; flex-wrap: wrap; gap: 16px 0; margin: 6px 0 0 -28px">{fx}</div>
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 14px 22px; margin-top: 10px"><a href="{cta_href}" style="display: inline-flex; align-items: center; gap: 10px; min-height: 54px; padding: 0 24px; background: #5ED3A2; color: #12100E; font-weight: 600; font-size: 17px; text-decoration: none">{cta_text} <span aria-hidden="true">→</span></a><span style="font-size: 15px; color: rgba(255,255,255,.7)">{note}</span></div>
</div><figure class="fh-img" style="margin: 0; position: relative; display: flex; flex-direction: column; gap: 10px"><img src="{img}" alt="{alt}" width="1200" height="900" style="display: block; width: 100%; height: auto; aspect-ratio: 4 / 3.4; object-fit: cover; box-shadow: 0 24px 48px rgba(0,0,0,.28)"><figcaption style="font-size: 13px; color: rgba(255,255,255,.65)">{caption}</figcaption></figure></div></section>'''

def body_html(toc, sections, extra=''):
    return (f'''<section style="max-width: 1240px; margin: 0 auto; padding-left: 24px; padding-right: 24px; padding-top: clamp(48px, 6vw, 80px)"><div class="art" style="display: grid; grid-template-columns: 240px minmax(0, 1fr); gap: 64px; align-items: start">
{toc}
<article style="display: flex; flex-direction: column; gap: 32px; font-size: 18px; line-height: 1.7; max-width: 760px">
''' + '\n'.join(sections) + f'''
</article></div></section>{extra}
<style>@media (max-width:960px){{.fh{{grid-template-columns:minmax(0,1fr)!important}}.fh-img{{display:none!important}}}}@media (max-width:900px){{.art{{grid-template-columns:minmax(0,1fr)!important;gap:24px!important}}.toc{{position:static!important}}}}@media (max-width:700px){{.pc2,.cg2{{grid-template-columns:1fr!important}}.pc2-r{{border-left:0!important;padding-left:0!important;border-top:1px solid #D8D1C5}}.fx{{margin-left:0!important;flex-direction:column;gap:12px!important}}.fx>div{{padding:0!important;border-left:0!important}}}}.ocard{{transition:border-color .2s}}.ocard:hover{{border-color:#5ED3A2!important}}</style>''')

# ---------------------------------------------------------------- stand types
STANDS = [
 dict(slug='row', alt='Row stand in the middle of a row, closed on three sides and open to the aisle', name='Row stand', plural='Row stands', art='a row stand', open=1, sides='1 open side', best='Graphics and storage', rent='Base rate',
      what="A row stand stands between two neighbours: closed at the back and on both sides, open to one aisle. It is the most common stand type at most trade&nbsp;fairs.",
      lead='Walls on three sides, one side open to the aisle. We design and build your row stand at any trade fair in Europe, for one all-inclusive&nbsp;price.',
      good=['Usually the lowest space rent per m²', 'Lots of wall space for graphics, screens and shelving', 'Easy to add a small storage room'],
      watch=['Visitors can only reach you from one aisle', 'Less visible from a distance, so your back wall has to work hard'],
      fit='A row stand suits you if most of your message fits on one strong back wall and you want to keep the space rent low. It is less suited to large products that people need to walk around, or to many meetings at&nbsp;once.',
      bestfor='Exhibitors with a smaller budget, a clear product range and a strong brand&nbsp;wall.',
      tips=['<b>Make the back wall work from the aisle.</b> Visitors see you from one side only, so your logo and one clear message go high on the back wall, within the organiser\'s height limit.',
            '<b>Keep the front open.</b> A counter or table set back from the aisle edge invites people in instead of blocking the way.',
            '<b>Storage behind a wall.</b> A small lockable room for coats, stock and brochures fits behind the back or a side wall.',
            '<b>Side walls for the details.</b> Product graphics, shelves or a screen go on the side walls, for visitors who are already on the stand.'],
      faq=[('Is a row stand enough for us?', 'Often, yes. If your stand is mainly a brand wall, a few products and a counter, a row stand does the job at the lowest space rent. If you need room for meetings or large products, look at a <a href="../corner/">corner</a> or <a href="../peninsula/">peninsula</a>&nbsp;stand.'),
           ('Can a row stand have a storage room?', 'Yes. A small lockable room behind the back wall or along a side wall is easy to add on a row stand, as long as the stand is big enough to keep a welcoming&nbsp;front.')]),
 dict(slug='corner', alt='Corner stand with two walls, open to two aisles', name='Corner stand', plural='Corner stands', art='a corner stand', open=2, sides='2 open sides', best='Two-way visibility', rent='Often higher',
      what="Your stand sits at the end of a row, with two walls and two sides open to the aisles, so two streams of visitors pass&nbsp;it.",
      lead='Open on two sides, so visitors reach you from two aisles. We design and build your corner stand at any trade fair in Europe, for one all-inclusive&nbsp;price.',
      good=['Visitors reach you from two aisles', 'More visibility than a row stand for a modest step up in space rent', 'Still has two walls for graphics and storage'],
      watch=['Both open sides need to invite people in, so the layout takes more planning', 'Many organisers charge a supplement for corner space'],
      fit='A corner stand suits you if you want visitors from two aisles without paying for a peninsula or island. The layout has to welcome people from both sides, so it takes a little more planning than a row&nbsp;stand.',
      bestfor='Exhibitors who want more foot traffic without the space rent of a peninsula or&nbsp;island.',
      tips=['<b>Two ways in.</b> Both aisles should lead onto the stand, so we keep high walls and counters away from the open sides.',
            '<b>Brand where the walls meet.</b> The closed corner is seen from both aisles, which makes it the natural place for your logo and main message.',
            '<b>A clear route through.</b> Whichever aisle visitors come from, they should see where to go: a product, a screen or someone to talk to.',
            '<b>Storage in the back corner.</b> The closed corner also takes a small storage room without blocking either open side.'],
      faq=[('Where should the counter go on a corner stand?', 'Usually not right on the corner. A counter there blocks both entrances. We place it so visitors can step onto the stand from either aisle first, and then find someone to talk&nbsp;to.'),
           ('Can a corner stand have a storage room?', 'Yes. The closed corner, where the two walls meet, takes a small lockable room without blocking either open&nbsp;side.')]),
 dict(slug='peninsula', alt='Peninsula stand with one back wall, open on three sides', name='Peninsula stand', plural='Peninsula stands', art='a peninsula stand', open=3, sides='3 open sides', best='A strong brand wall', rent='Higher again',
      what="Your stand sits at the head of a row, with one back wall and three sides open, so visitors come from three&nbsp;directions.",
      lead='Open on three sides with one strong back wall. We design and build your peninsula stand at any trade fair in Europe, for one all-inclusive&nbsp;price.',
      good=['Very visible, with visitors coming from three directions', 'One strong back wall for your brand and a storage room', 'Room for product displays, a meeting area and a reception desk'],
      watch=["The back wall is shared with the neighbour behind you, so its height and finish follow the organiser's rules", 'The layout has to work from three directions'],
      fit="A peninsula stand suits you if you want to be seen from three directions and still keep one wall for your brand and storage. That wall faces a neighbour, so the organiser's rules for it come&nbsp;first.",
      bestfor='Mid-size and larger exhibitors who want presence and a clear brand&nbsp;wall.',
      tips=["<b>One back wall that carries the brand.</b> It is seen from far down the aisle in front of it, so it holds your logo and one clear message.",
            "<b>Check the back wall rules first.</b> The neighbour behind you shares the wall, so its height and finish follow the organiser's rules. We check them before we design.",
            '<b>A reason to step in from each side.</b> Products, screens and the reception are placed so all three open sides invite people in.',
            '<b>Meetings and storage at the back.</b> A meeting area or a small room along the back wall stays out of the main flow of visitors.'],
      faq=[('Can a peninsula stand have a meeting room?', 'Yes, usually along the back wall, where it stays out of the main flow of visitors. How big it can be depends on your stand&nbsp;size.'),
           ('Who decides how high the back wall can be?', "The organiser. The technical guidelines of each fair set the maximum height and how the side facing your neighbour must be finished. Send us the guidelines with your brief, or tell us the fair and we look them&nbsp;up.")]),
 dict(slug='island', alt='Island stand seen from above, open on all four sides', name='Island stand', plural='Island stands', art='an island stand', open=4, sides='4 open sides', best='Maximum visibility', rent='Usually the highest',
      what="An island stand stands on its own, with aisles on all four sides and no neighbour touching it. It is seen from every aisle and has the biggest presence in the&nbsp;hall.",
      lead='Open on all four sides and seen from every aisle. We design and build your island stand at any trade fair in Europe, for one all-inclusive&nbsp;price.',
      good=['The biggest presence in the hall, visible from every aisle', 'Full freedom in the layout, including closed meeting rooms', 'Can be built as a double-deck stand where the hall allows it'],
      watch=['The most complex to plan, and usually the highest space rent per m²', 'Height limits, hanging points and double-deck structures need organiser approval and often structural calculations'],
      fit='An island stand suits you if you want the strongest presence in the hall, with room for meetings, demos or hospitality. It is the most complex to plan, and approvals for height, hanging points or a second floor come&nbsp;first.',
      bestfor='Larger exhibitors who want the strongest presence and room for meetings, demos and&nbsp;hospitality.',
      tips=['<b>No back side.</b> Visitors walk all the way around, so every side has to look finished and give people a reason to stop.',
            '<b>Seen from across the hall.</b> A hanging sign or a tall element shows where you are from far away. Hanging points need the organiser\'s approval, so we plan them early.',
            '<b>Rooms in the middle.</b> Meeting rooms and storage in the core of the stand keep the outer edges open to the aisles.',
            '<b>Approvals first.</b> Height, hanging points and double-deck structures need organiser approval and often structural calculations, so they come first in the schedule.'],
      faq=[('Can an island stand have a second floor?', "It can, if the hall and the organiser allow it. For a second floor the organiser asks for approval and structural calculations, and some fairs charge the upper floor as extra space. We check your fair's rules before we start the&nbsp;design."),
           ('Who handles the organiser approvals?', "You book the space and the organiser's services. We help you with the technical forms for the stand itself, such as the stand drawings the organiser asks for. For hanging points and double-deck structures, these are part of our&nbsp;planning.")]),
]
COMMON_FAQ = [
    ('What do you need from us to start?', 'The fair, your stand size and the open sides, plus your email. A phone photo of the floor plan helps. Anything missing we sort out&nbsp;together.'),
    ('Do we pay anything before we approve the design?', 'No. Your design and your price are free and come with no obligation. You only commit once you have seen both and said&nbsp;yes.'),
]
TYPE_OPT = {'row': 'Row stand (1 open side)', 'corner': 'Corner stand (2 open sides)', 'peninsula': 'Peninsula stand (3 open sides)', 'island': 'Island stand (4 open sides)'}

def stand(S):
    url = f"https://1o1expo.com/stands/{S['slug']}/"
    quote = f"../../quote/?type={S['slug']}"
    title = f"{S['plural']} for trade fairs in Europe"
    desc = f"{S['plural']} ({S['sides']}) designed and built for any trade fair in Europe: design, production, transport, build-up and dismantling in one all-inclusive price."
    faq = S['faq'] + COMMON_FAQ
    h = head(title, desc, url, f"https://1o1expo.com/img/concept-{S['slug']}-1.jpg")
    h = h.replace('<meta property="og:image:height" content="630">', '<meta property="og:image:height" content="900">')
    h = ld([crumbs([('1o1 expo', 'https://1o1expo.com/'), ('Stand types', 'https://1o1expo.com/#stands'), (S['plural'], url)]), faq_ld(faq)], h)
    h = h.replace('<a href="../../index.html#stands" style="color: #1C1A17; text-decoration: none">Stand types</a>', '<a href="../../index.html#stands" aria-current="page" style="color: #13704D; text-decoration: none; font-weight: 600">Stand types</a>')
    crumb = f'<a href="../../index.html#stands" style="color: #5ED3A2; text-decoration: none; font-weight: 600">Stand types</a> <span aria-hidden="true">/</span> {S["plural"]}'
    hero = hero_side(crumb, S['sides'].upper(), f"{S['plural']} for trade fairs in&nbsp;Europe", S['lead'],
                     [('Open sides', str(S['open'])), ('Best for', S['best']), ('Space rent', S['rent'])],
                     quote, f"Get a quote for {S['art']}", f"../../img/concept-{S['slug']}-1.jpg", f"Concept visualisation of {S['art']}")
    toc = toc_html([('what', f"What {S['art']} is"), ('fit', 'Is it right for you?'), ('plan', 'What we plan for'), ('designs', 'Concept designs'), ('price', 'What our price covers'), ('process', 'How it works'), ('questions', 'Common questions')])
    what = (H2('what', f"What {S['art']} is", first=True) + P + S['what'] + '</p>'
            + f'<figure style="margin: 0; display: flex; flex-direction: column; gap: 10px"><img src="../../img/stand-type-{S["slug"]}.jpg" alt="{S["alt"]}" width="1000" height="747" loading="lazy" style="display: block; width: 100%; height: auto; border: 1px solid #D8D1C5"><figcaption style="font-size: 14px; color: #5B5650">{S["name"]}: {S["sides"]}. The organiser sets the open sides when you book your&nbsp;space.</figcaption></figure>'
            + '<p style="margin: 0; padding: 16px 20px; background: #DDF4EA; border: 1.5px solid #1C1A17; font-size: 17px">Not sure which type you booked? Send us your space confirmation or the floor plan with your brief and we check it. <a href="../../quote/" style="color: #13704D; font-weight: 600; white-space: nowrap">Send your floor plan&nbsp;→</a></p></section>')
    fit = (H2('fit', f"Is {S['art']} right for you?") + P + S['fit'] + '</p>'
           + P + 'Compare all four types side by side, including how the space rent changes, in our guide to <a href="../../guides/stand-types/">stand types</a>.</p></section>')
    plan = H2('plan', f"What we plan for on {S['art']}") + P + 'A few things we plan for on almost every stand of this&nbsp;type:</p>' + ul(S['tips']) + '</section>'
    imgs = ''.join(f'<figure style="margin: 0; display: flex; flex-direction: column; gap: 8px"><img src="../../img/concept-{S["slug"]}-{i}.jpg" alt="Concept visualisation of {S["art"]}, design {i}" width="1200" height="900" loading="lazy" style="display: block; width: 100%; height: auto; aspect-ratio: 4 / 3; object-fit: cover; border: 1px solid #D8D1C5"><figcaption style="font-size: 14px; color: #5B5650">Concept visualisation</figcaption></figure>' for i in (1, 2))
    designs = H2('designs', 'Concept designs') + P + 'Two concepts for this stand type. Yours is drawn from scratch for your hall, your size and your open&nbsp;sides.</p>' + f'<div class="cg2" style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px">{imgs}</div></section>'
    price = H2('price', 'What our price covers') + price_html(INC, 'One all-inclusive price for the whole stand, agreed before anything is made. The stand type does not change our price; size, design, materials and finish&nbsp;do.') + '</section>'
    process = H2('process', 'How it works') + P + 'You always know what happens next, and nothing is produced before you say&nbsp;yes.</p>' + steps_html(STEPS) + '</section>'
    others = ''.join(f'<a href="../{o["slug"]}/" class="ocard" style="display: flex; flex-direction: column; gap: 4px; padding: 16px 18px; background: #FFFFFF; border: 1px solid #D8D1C5; color: #1C1A17; text-decoration: none"><span style="font-size: 12px; letter-spacing: .08em; font-weight: 700; color: #13704D">{o["sides"].upper()}</span><b style="font-size: 18px; font-weight: 600">{o["plural"]}&nbsp;→</b></a>' for o in STANDS if o is not S)
    qs = H2('questions', 'Common&nbsp;questions') + faq_html(faq) + f'<span style="margin-top: 12px; font-size: 12px; letter-spacing: .08em; font-weight: 700; color: #5B5650">OTHER STAND TYPES</span><div class="cg3" style="display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 12px">{others}</div></section>'
    body = body_html(toc, [what, fit, plan, designs, price, process, qs]).replace('</style>', '@media (max-width:700px){.cg3{grid-template-columns:1fr!important}}</style>')
    write(f"stands/{S['slug']}/index.html", h + '\n' + hero + '\n' + body + '\n' + tail(quote))

# ---------------------------------------------------------------- quote page
def quote_page():
    url = 'https://1o1expo.com/quote/'
    title = 'Get your stand quote'
    desc = 'Tell us about your trade fair. Within 7 working days you get a design for your space and one all-inclusive price. Free and without obligation.'
    h = head(title, desc, url)
    h = re.sub(r'\s*<nav class="hide-sm".*?</nav>', '', h, flags=re.S)                     # no menu on the conversion page
    h = re.sub(r'(<div class="lsw".*?</div>)\s*<a href="[^"]*" style="[^"]*">Get&nbsp;your&nbsp;quote</a>', r'\1', h, count=1, flags=re.S)
    h = h.replace('<meta name="robots" content="noindex, nofollow">', '<meta name="robots" content="noindex, nofollow">')
    form = FORM0.replace('action="/thanks.html"', 'action="/thanks.html"').replace('class="quote-form" style="background: #FBFAF6; border-left: 1.5px solid #1C1A17;', 'class="quote-form" style="background: #FBFAF6; border: 1.5px solid #1C1A17;')
    ico = lambda p: f'<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#13704D" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" style="flex: none">{p}</svg>'
    i_mail = ico('<rect x="3" y="5.5" width="18" height="13"/><path d="M3.5 6.5l8.5 6.5 8.5-6.5"/>')
    i_wa = ico('<path d="M12 2.6a9.4 9.4 0 0 0-8.1 14.1L2.6 21.4l4.8-1.3A9.4 9.4 0 1 0 12 2.6z"/>')
    i_cal = ico('<rect x="3.5" y="5" width="17" height="15"/><path d="M3.5 9.5h17M8 3v4M16 3v4"/>')
    def card(href, extra, icon, label, main, cls='qc'):
        return (f'<a href="{href}"{extra} class="{cls}" style="display: grid; grid-template-columns: 48px minmax(0, 1fr); gap: 14px; align-items: center; padding: 12px 16px 12px 12px; border: 1.5px solid #1C1A17; background: #FFFFFF; color: #12100E; text-decoration: none">'
                f'<span style="width: 48px; height: 48px; display: flex; align-items: center; justify-content: center; background: #DDF4EA">{icon}</span>'
                f'<span style="display: flex; flex-direction: column; gap: 2px; min-width: 0"><span style="font-size: 14px; color: #5B5650">{label}</span><span style="font-size: 17px; font-weight: 600; overflow-wrap: anywhere">{main}</span></span></a>')
    cards = ('<div style="display: flex; flex-direction: column; gap: 10px">' + card('mailto:robert@1o1expo.com', '', i_mail, 'Write to us directly', 'robert@1o1expo.com')
             + card('#quote', '', i_wa, 'Prefer to chat?', 'Message us on WhatsApp', 'qc wa-link') + card(BOOK, ' target="_blank" rel="noopener"', i_cal, 'Want to talk it through?', 'Book a 30-min call') + '</div>')
    nxt = [('We read your brief', 'and reply within 1 working day, with questions if anything is&nbsp;unclear.'),
           ('Within 7 working days', 'you get a design for your space, the full price and every date up to opening&nbsp;day.'),
           ('You decide.', 'Nothing is produced before your yes, and the design and price are free either&nbsp;way.')]
    nx = '<ol style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 14px">' + ''.join(f'<li style="display: grid; grid-template-columns: 34px minmax(0,1fr); gap: 12px; align-items: start"><span style="width: 30px; height: 30px; border-radius: 50%; background: #0E3B2B; color: #FFFFFF; display: inline-flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700">{i+1}</span><span style="font-size: 17px; line-height: 1.55"><b>{t}</b> {d}</span></li>' for i, (t, d) in enumerate(nxt)) + '</ol>'
    faq = [('Is the quote really free?', 'Yes. Your design and your price are free and come with no obligation. You only commit once you have seen both and said&nbsp;yes.'),
           ('What if we have no floor plan yet?', 'Send what you have: the fair, the date and roughly how much space you booked. Missing details are fine, we sort them out together. Not sure which stand type you booked? Send the booking confirmation and we&nbsp;check.'),
           ('We already have a stand design. Can you build it?', 'Yes. Attach your drawings or renders in the form below, or read how we <a href="../own-design/">build your own design</a> first.'),
           ('What if our fair is only a few weeks away?', 'Tell us the date in the form. Within one working day, we tell you honestly whether we can still build it&nbsp;well.')]
    h = ld([faq_ld(faq)], h)
    main = f'''</header><section id="quote" style="max-width: 1240px; margin: 0 auto; padding: clamp(40px, 6vw, 72px) 24px 0"><div class="qp" style="display: grid; grid-template-columns: minmax(0, .85fr) minmax(0, 1.15fr); grid-template-areas: 'intro form' 'aside form'; gap: 24px 48px; align-items: start">
<div style="grid-area: intro; display: flex; flex-direction: column; gap: 24px">
<span style="align-self: flex-start; font-size: 12px; letter-spacing: 0.08em; font-weight: 700; color: #1F845B; margin-bottom: -12px">YOUR QUOTE</span>
<h1 style="margin: 0; font-size: clamp(34px, 4.4vw, 52px); line-height: 1.04; letter-spacing: -0.03em; font-weight: 600; text-wrap: balance">A design and one price for your&nbsp;stand.</h1>
<p style="margin: 0; font-size: 19px; line-height: 1.6; color: #3F3B36">Only your fair and your email are required. The rest takes two minutes, and missing details are&nbsp;fine.</p>
</div>
<div style="grid-area: aside; display: flex; flex-direction: column; gap: 24px">
<div style="display: flex; flex-direction: column; gap: 14px; padding: 22px 24px; background: #DDF4EA; border: 1.5px solid #1C1A17"><span style="font-size: 12px; letter-spacing: .08em; font-weight: 700; color: #13704D">WHAT HAPPENS NEXT</span>{nx}</div>
{cards}
</div>
<div class="qp-f" style="grid-area: form">{form}</div>
</div></section>
<section style="max-width: 1240px; margin: 0 auto; padding: 72px 24px 104px"><div style="max-width: 760px; display: flex; flex-direction: column; gap: 20px"><h2 style="margin: 0; font-size: 32px; line-height: 1.1; letter-spacing: -0.02em; font-weight: 600">Before you&nbsp;send</h2>{faq_html(faq)}</div></section>
<style>.qp-f .qf-grid{{grid-template-columns:repeat(2,minmax(0,1fr))!important}}@media (max-width:960px){{.qp{{grid-template-columns:minmax(0,1fr)!important;grid-template-areas:'intro' 'form' 'aside'!important;gap:28px!important}}}}@media (max-width:520px){{.qp-f .qf-grid{{grid-template-columns:minmax(0,1fr)!important}}}}.qc{{transition:background .2s}}.qc:hover{{background:#F5FBF8!important}}</style>
<script>(function(){{try{{var q=new URLSearchParams(location.search),f=q.get("fair"),t=q.get("type"),T={json.dumps(TYPE_OPT)};var i=document.querySelector('input[name="fair"]');if(f&&i&&!i.value)i.value=f.slice(0,120);var s=document.querySelector('select[name="stand-type"]');if(t&&s&&T[t]){{[].forEach.call(s.options,function(o){{if(o.text===T[t])s.value=o.value||o.text}})}}if(q.get("own")!==null){{var l=document.getElementById("q-plan");if(l)l.closest("label").style.outline="2px solid #5ED3A2"}}}}catch(e){{}}}})();</script>'''
    t = TAIL0[TAIL0.find('<footer'):]
    t = re.sub(r'<footer.*?</footer>', '<footer style="border-top: 1px solid #D8D1C5"><div style="max-width: 1240px; margin: 0 auto; padding: 24px; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px; font-size: 14px; color: #5B5650"><span>©&nbsp;2026&nbsp;1o1&nbsp;expo</span><span style="display: flex; gap: 20px"><a href="../legal.html" style="color: #5B5650">Legal notice</a><a href="../privacy.html" style="color: #5B5650">Privacy policy</a></span></div></footer>', t, count=1, flags=re.S)
    out = (h + '\n' + main + '\n' + t)
    out = out.replace('href="../../', 'href="../').replace('src="../../', 'src="../')
    out = re.sub(r'<a href="[^"]*" class="wa-link wa-float".*?</a>\n?', '', out, count=1, flags=re.S)
    write('quote/index.html', out)

# ---------------------------------------------------------------- own design
def own_design():
    url = 'https://1o1expo.com/own-design/'
    quote = '../quote/?own'
    title = 'We build your own stand design'
    desc = 'Already have a stand design? Send us your drawings or renders and get one all-inclusive price to build it: production, transport, build-up and dismantling.'
    faq = [('Can you change our design?', 'Only if you want us to. If something can be built more simply or at a lower cost, or does not fit the organiser\'s rules, we tell you and suggest a change. You&nbsp;decide.'),
           ('Our design was made for another fair or size. Can you adapt it?', 'Yes. Tell us the new fair, the size and the open sides, and we adapt the layout and price it for the new&nbsp;space.'),
           ('Do we pay anything before we approve the price?', 'No. Your price is free and comes with no obligation. You only commit once you have seen it and said&nbsp;yes.'),
           ('What if our files are incomplete?', 'Send what you have. A render, a sketch with sizes or photos of your last stand are a good start, and we ask for anything we are&nbsp;missing.')]
    h = head(title, desc, url, 'https://1o1expo.com/img/concept-island-2.jpg')
    h = h.replace('<meta property="og:image:height" content="630">', '<meta property="og:image:height" content="900">')
    h = ld([crumbs([('1o1 expo', 'https://1o1expo.com/'), ('Your own design', url)]), faq_ld(faq)], h)
    h = h.replace('href="../../', 'href="../').replace('src="../../', 'src="../')
    crumb = '<a href="../index.html" style="color: #5ED3A2; text-decoration: none; font-weight: 600">1o1&nbsp;expo</a> <span aria-hidden="true">/</span> Your own design'
    hero = hero_side(crumb, 'YOU HAVE THE DESIGN · WE BUILD IT', 'Already have a stand design? We build&nbsp;it.',
                     'Send us your drawings or renders, or the design from your last fair. You get one price to build it: production, transport, build-up and dismantling, at any trade fair in&nbsp;Europe.',
                     [('You send', 'Drawings or renders'), ('You get', 'One price to build it'), ('Before you pay', 'Nothing produced')],
                     quote, 'Send your design', '../img/concept-island-2.jpg', 'Concept visualisation of a double-deck island stand')
    toc = toc_html([('who', 'Who this is for'), ('send', 'What to send'), ('check', 'What we check'), ('price', 'What our price covers'), ('process', 'How it works'), ('questions', 'Common questions')])
    who = (H2('who', 'Who this is for', first=True) + P + 'You already know what your stand should look like, and you need someone to build it well and on time. For&nbsp;example:</p>'
           + ul(['<b>Your agency or in-house team designed it.</b> You have the design, but no builder in the city of the fair.',
                 '<b>You want to reuse your last stand design.</b> The same look at a new fair, often in a different size.',
                 '<b>You have a render from a competition or a supplier.</b> You want a second, all-inclusive price to build it.']) + '</section>')
    send = (H2('send', 'What to send') + P + 'The more you send, the more exact the price. Missing files are fine, we ask for what we&nbsp;need.</p>'
            + ul(['<b>Your design.</b> Drawings, renders or photos of your last stand, ideally with sizes.',
                  '<b>The fair and your space.</b> Fair name, dates, hall and stand number, stand size and open sides, or the floor plan from your booking.',
                  "<b>The organiser's technical guidelines</b>, if you have them: maximum height, hanging points and approval deadlines.",
                  '<b>Graphics and logo files,</b> if they are ready: your logo as a vector file (AI, EPS, SVG or PDF).'])
            + P + 'More in our guide on <a href="../guides/stand-brief/">what to send a stand builder</a>.</p></section>')
    check = (H2('check', 'What we check before we price it') + P + 'A design that looks good on screen still has to work in the hall. Before you get a price, we go&nbsp;through:</p>'
             + ul(["<b>The organiser's rules.</b> Height, back walls facing neighbours, hanging points and what needs approval at your fair.",
                   '<b>Materials and finish.</b> What each surface is made of, so the price is complete and nothing is left open.',
                   '<b>Transport and build-up.</b> That the stand can be shipped, carried in and built within the official build-up days.',
                   '<b>Where it can be simpler.</b> If something can be built more simply or at a lower cost without changing the look, we suggest it.'])
             + '</section>')
    price = H2('price', 'What our price covers') + price_html(['Production of walls, flooring and furniture', 'Lighting and electrics on the stand', 'Printed graphics from your files', 'Transport to the venue', 'Build-up and dismantling'], 'One all-inclusive price to build your design, agreed before anything is made. Every change is priced before you approve&nbsp;it.') + '</section>'
    steps = [('Send your design', 'Your files, your fair and your space, through the form. A short call works&nbsp;too.'), ('Get your price within 7 working days', 'The full price to build it and every date up to opening day, with any suggestions we&nbsp;have.'),
             ('Approve', 'Nothing is produced before your yes. Once you approve, the price only changes if you change the&nbsp;stand.'), ('We produce, deliver and build', 'Made, shipped to the venue and built before the fair opens. When it closes, we take it&nbsp;down.')]
    process = H2('process', 'How it works') + steps_html(steps) + '</section>'
    qs = H2('questions', 'Common&nbsp;questions') + faq_html(faq) + P + 'No design yet? We design it for you: see our <a href="../index.html#stands">stand types</a> or <a href="../quote/">ask for a design and a price</a>.</p></section>'
    body = body_html(toc, [who, send, check, price, process, qs]).replace('href="../../', 'href="../')
    t = tail(quote).replace('href="../../', 'href="../').replace('src="../../', 'src="../').replace('href="../../guides/"', 'href="../guides/"')
    t = t.replace('>Get your quote <span aria-hidden="true">→</span></a>', '>Send your design <span aria-hidden="true">→</span></a>', 1).replace('Tell us about it. You get a design and one all-inclusive price within 7&nbsp;working&nbsp;days.', 'Send us your design. You get one all-inclusive price to build it within 7&nbsp;working&nbsp;days.', 1).replace('Planning a stand for your next&nbsp;fair?', 'Ready to get your design&nbsp;built?', 1)
    write('own-design/index.html', h + '\n' + hero + '\n' + body + '\n' + t)

if __name__ == '__main__':
    for S in STANDS: stand(S)
    quote_page(); own_design()
    print('ok')
