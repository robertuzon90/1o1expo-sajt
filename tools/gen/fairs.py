import re, json, os, urllib.parse
SITE = '/home/claude/1o1expo-sajt/'
L = open(SITE + 'guides/stand-cost/index.html').read().split('\n')
HEAD0 = '\n'.join(L[:118])
TAIL0 = '\n'.join(L[132:])

MF_BUILD = 'https://builder.messefrankfurt.com/frankfurt/en/event-specific-information/cphi.html'
FAIRS = [
 dict(slug='ambiente-frankfurt', name='Ambiente', full='Ambiente Frankfurt', city='Frankfurt', venue='Messe Frankfurt', organiser='Messe Frankfurt',
      dates='29 January – 2 February 2027', dshort='29 Jan – 2 Feb 2027', start='2027-01-29', brief='As soon as possible', sector='Consumer goods', img='fair-ambiente.jpg',
      about=["Ambiente is Messe Frankfurt's international trade fair for consumer goods: tableware, kitchen and household, interiors, gifts and products for the workplace. It runs alongside Christmasworld, the trade fair for seasonal decorations.",
             "In 2026, Ambiente, Christmasworld and Creativeworld together brought 4,636 exhibitors and participants from 170 countries and around 140,000 visitors to Frankfurt."],
      src=[('Messe Frankfurt final report 2026', 'https://christmasworld.messefrankfurt.com/content/dam/messefrankfurt-redaktion/ambiente/2026/press/press-releases/12-ambcw-crw-finalreport-en.pdf')],
      tips=['<b>Let visitors touch the products.</b> Buyers at Ambiente want to pick things up, so we plan open shelves and tables at a comfortable height, not only glass cases.',
            '<b>Light for products, not just for the stand.</b> Glass, ceramics and textiles look very different under good spotlights.',
            '<b>A table for orders.</b> A quieter corner where buyers can sit down, go through the catalogue and place an order.',
            '<b>Storage for stock and packaging.</b> Spare samples, boxes and order forms need a place out of sight.']),
 dict(slug='mwc-barcelona', name='MWC Barcelona', full='MWC Barcelona', city='Barcelona', venue='Fira Gran Via', organiser='GSMA',
      dates='1–4 March 2027', dshort='1–4 Mar 2027', start='2027-03-01', brief='Now', sector='Mobile and connectivity', img='fair-mwc.jpg',
      about=["MWC Barcelona, organised by the GSMA, is the largest annual event of the mobile and connectivity industry. It takes place at Fira de Barcelona's Gran Via venue.",
             "The 2026 edition welcomed nearly 105,000 attendees from 207 countries and territories, with 2,900 exhibitors, sponsors and partners."],
      src=[('GSMA press release, MWC26', 'https://www.gsma.com/newsroom/press-release/gsma-mwc26-barcelona-closes-20th-anniversary-edition')],
      tips=['<b>Meeting rooms.</b> Much of MWC happens in scheduled meetings, so closed rooms with a table, screen and good acoustics are often the heart of the stand.',
            '<b>Demos that always work.</b> Demo stations with power and internet where you need them, ordered with the organiser in time.',
            '<b>Clean cable routing.</b> Screens and devices need power everywhere; we plan it into the floor and walls so nothing is in the way.',
            '<b>A clear message from the aisle.</b> Halls are big and busy; visitors should see in seconds what you offer.']),
 dict(slug='hannover-messe', name='Hannover Messe', full='Hannover Messe', city='Hannover', venue='Hannover Exhibition Grounds', organiser='Deutsche Messe',
      dates='5–8 April 2027', dshort='5–8 Apr 2027', start='2027-04-05', brief='November 2026', sector='Industrial technology', img='fair-hannover.jpg',
      about=["Hannover Messe, organised by Deutsche Messe, is one of the world's leading trade fairs for industrial technology: automation, digitalisation, energy and engineering. From 2027 it runs from Monday to Thursday, and the 2027 partner country is Spain.",
             "In 2026, Hannover Messe welcomed around 110,000 visitors, about 40 percent of them from abroad."],
      src=[('IEN Europe, Hannover Messe 2026 report', 'https://www.ien.eu/article/industry-points-the-way-to-a-competitive-future-at-hannover-messe-2026/')],
      tips=['<b>Plan around your exhibits.</b> Heavy machines and demonstrators decide the layout, floor and access, so we start from what you bring.',
            '<b>Power and media in time.</b> High power, compressed air or water for live demos are ordered from the organiser and planned into the stand early.',
            '<b>Space to explain.</b> Technical buyers ask detailed questions, so a meeting area next to the exhibits works better than one hidden at the back.',
            '<b>Robust materials.</b> Four busy days and heavy equipment call for floors and surfaces that take it.']),
 dict(slug='intersolar-europe', name='Intersolar Europe', full='Intersolar Europe Munich', city='Munich', venue='Messe München', organiser='The smarter E Europe organisers',
      dates='8–10 June 2027', dshort='8–10 Jun 2027', start='2027-06-08', brief='January 2027', sector='Solar and energy', img='fair-intersolar.jpg',
      about=["Intersolar Europe is a leading exhibition for the solar industry and part of The smarter E Europe, an alliance of energy exhibitions at Messe München. The Intersolar Europe Conference runs on 7–8 June 2027 at ICM München.",
             "For its latest edition, The smarter E Europe projected more than 2,600 exhibitors and more than 100,000 visitors, with about 1,170 exhibitors at Intersolar Europe."],
      src=[('Intersolar Europe, at a glance', 'https://www.intersolar.de/en/about')],
      tips=['<b>Show the product at full size.</b> Modules, inverters and storage systems need solid walls and plinths that carry their weight.',
            '<b>Make specs easy to compare.</b> Visitors compare efficiency, capacity and warranties; clear graphics next to each product save a lot of talking.',
            '<b>Room for technical talks.</b> A meeting area where installers and buyers can sit down with your engineers.',
            '<b>Power for live systems.</b> If something should run on the stand, we plan the electricity order with you early.']),
 dict(slug='eurobike-frankfurt', name='Eurobike', full='Eurobike Frankfurt', city='Frankfurt', venue='Messe Frankfurt', organiser='fairnamic',
      dates='30 June – 2 July 2027', dshort='30 Jun – 2 Jul 2027', start='2027-06-30', brief='January 2027', sector='Bicycles and mobility', img='fair-eurobike.jpg',
      about=["Eurobike is the international trade fair of the bicycle and cycling industry, organised by fairnamic at the Messe Frankfurt exhibition grounds. After an earlier plan to move the 2027 show to September, the organiser confirmed it stays in summer and remains an annual event.",
             "The 2026 edition had about 800 exhibitors from 44 countries."],
      src=[('Bicycle Retailer, Eurobike 2027 dates', 'https://www.bicycleretailer.com/industry-news/2026/09/01/eurobike-reverses-earlier-date-change-will-remain-summer-show'), ('Interempresas, Eurobike 2026 figures', 'https://www.interempresas.net/Ciclismo/651275-Eurobike-2026-datos-y-fotos-de-una-edicion-complicada.html')],
      tips=['<b>Bikes at eye level.</b> Wall and floor racks so every model can be seen, and the key ones can be taken down and handled.',
            '<b>Easy in and out.</b> Bikes are wheeled on and off the stand all day, so we keep entrances wide and floors hard-wearing.',
            '<b>Good light on details.</b> Frames, components and finishes sell on close inspection.',
            '<b>A place for dealers.</b> A table where dealers and distributors can talk terms away from the busy aisle.']),
 dict(slug='gamescom-cologne', name='gamescom', full='gamescom Cologne', city='Cologne', venue='Koelnmesse', organiser='Koelnmesse and game',
      dates='23–29 August 2027', dshort='23–29 Aug 2027', start='2027-08-23', brief='March 2027', sector='Games', img='fair-gamescom.jpg',
      about=["gamescom in Cologne is one of the world's largest events for computer and video games, organised by Koelnmesse and game, the German games industry association. The 2027 gamescom week runs from 23 to 29 August, opening with gamescom dev on 23–24 August; the public days start on 26 August.",
             "In 2026, gamescom welcomed 368,000 visitors from 131 countries and 1,743 exhibiting companies from 66 countries, with more than 36,000 trade visitors."],
      src=[('CGMagazine, gamescom 2026 figures and 2027 dates', 'https://www.cgmagonline.com/news/gamescom-2026-ends-368000-visitors/')],
      tips=['<b>Business area or entertainment area?</b> They need very different stands: meeting cabins for business, play stations and queues for the public halls.',
            '<b>Plan for queues.</b> In the entertainment area, popular games draw long lines; space for them keeps the aisle and your neighbours happy.',
            '<b>Sound and screens.</b> Big screens and audio need careful planning so your demo is heard without drowning out the stand next door.',
            '<b>Secure storage.</b> Consoles, PCs and merchandise need a lockable room.']),
 dict(slug='ifa-berlin', name='IFA', full='IFA Berlin', city='Berlin', venue='Messe Berlin', organiser='IFA Management',
      dates='3–7 September 2027', dshort='3–7 Sep 2027', start='2027-09-03', brief='April 2027', sector='Consumer electronics', img='fair-ifa.jpg',
      about=["IFA Berlin is one of the world's leading trade shows for consumer electronics and home appliances, organised by IFA Management at the Messe Berlin grounds.",
             "In 2025, IFA brought together over 1,900 exhibitors from 49 countries and around 220,000 visitors from 140 countries."],
      src=[('IFA Berlin press release, 2025 figures and 2027 dates', 'https://www.ifa-berlin.com/press-releases/ifa-berlin-looks-back-on-a-strong-2025-112025')],
      tips=['<b>Products people can try.</b> Live demos need power and network at every display, planned into the stand from the start.',
            '<b>Secure displays.</b> With trade and public visitors in the halls, valuable devices need secure mounting and lockable storage.',
            '<b>Light that flatters screens.</b> Too much light washes out displays; we balance stand lighting with your screens.',
            '<b>Space for trade meetings.</b> A quieter area for retailers and partners, away from the demo crowd.']),
 dict(slug='sbc-summit-lisbon', name='SBC Summit', full='SBC Summit Lisbon', city='Lisbon', venue='FIL and MEO Arena', organiser='SBC',
      dates='21–23 September 2027', dshort='21–23 Sep 2027', start='2027-09-21', brief='April 2027', sector='Betting and gaming', img='fair-sbc.jpg',
      about=["SBC Summit is a major B2B event for the betting and gaming industry, organised by SBC. It takes place in Lisbon at the Feira Internacional de Lisboa (FIL) and the MEO Arena, and SBC has confirmed Lisbon as its home through 2030.",
             "The 2026 edition welcomed 40,000 attendees, with 800 sponsors and exhibitors."],
      src=[('G3 Newswire, SBC Summit 2026', 'https://g3newswire.com/sbc-summit-2026-closes-record-lisbon-week-with-40000-attendees/'), ('SBC Americas, 2027 dates', 'https://sbcamericas.com/2025/11/05/sbc-summit-dates-2026-2027/')],
      tips=['<b>Meetings first.</b> Deals at SBC are made in conversations, so comfortable seating and a few semi-private areas matter.',
            '<b>Screens for your product.</b> Platforms and games are shown on screens, so we plan their size, height and power early.',
            '<b>A hospitality point.</b> A bar counter or coffee point gives visitors a reason to stop and talk, if it fits your brand.',
            '<b>Strong presence from a distance.</b> A header or hanging element helps visitors find you in a busy hall.']),
 dict(slug='reneo-budapest', name='RENEO', full='RENEO Budapest', city='Budapest', venue='HUNGEXPO Budapest', organiser='HUNGEXPO',
      dates='April 2027 (dates to be confirmed)', dshort='Apr 2027 (TBC)', start='2027-04-01', brief='November 2026', sector='Renewable energy', img='fair-reneo.jpg',
      about=["RENEO is the international trade exhibition for renewable energies at HUNGEXPO Budapest, held alongside CONSTRUMA, Hungary's major construction and home-building exhibition. It features solar energy and energy-efficient products.",
             "The organiser has not yet published the 2027 dates for RENEO. CONSTRUMA 2027 is scheduled for 8–11 April 2027, so check the HUNGEXPO site for the final RENEO dates before you plan."],
      src=[('HUNGEXPO, RENEO', 'https://hungexpo.hu/en/events/reneo/'), ('HUNGEXPO, CONSTRUMA 2027', 'https://hungexpo.hu/wp-content/uploads/CONSTRUMA2027_kiallitoi_prezi_EN.pdf')],
      tips=['<b>Products at real size.</b> Panels, heat pumps and storage systems need solid walls and plinths.',
            '<b>Clear benefits on the wall.</b> Savings, efficiency and warranties, easy to read for installers and homeowners alike.',
            '<b>A place to talk.</b> Visitors often come with a concrete project, so a table for advice pays off.',
            '<b>Bilingual graphics.</b> Hungarian and English, so both local and international visitors understand you.']),
 dict(slug='cphi-frankfurt', name='CPHI Frankfurt', full='CPHI Frankfurt', city='Frankfurt', venue='Messe Frankfurt', organiser='Informa Markets',
      dates='9–11 November 2027', dshort='9–11 Nov 2027', start='2027-11-09', brief='June 2027', sector='Pharmaceuticals', img='fair-cphi.jpg',
      about=["CPHI Frankfurt is one of the largest meeting points of the pharmaceutical supply chain: ingredients and APIs, contract development and manufacturing, machinery, packaging and services. It is organised by Informa Markets and takes place at Messe Frankfurt.",
             "For the 2025 edition, the organiser expected more than 60,000 visitors and more than 2,000 exhibitors. With that many stands in the halls, a stand that is easy to read from the aisle and comfortable to meet on makes a real&nbsp;difference."],
      src=[('cphi.com (2027 dates)', 'https://www.cphi.com/europe/cphi-frankfurt-2027-book-your-stand-form/'), ('PharmTech (2025 figures)', 'https://www.pharmtech.com/view/cphi-frankfurt-expected-draw-more-than-60-000-attendees-october')],
      buildup=('In 2025, build-up at Messe Frankfurt ran for four days before the fair opened, and dismantling began on the evening of the last day.', [('Messe Frankfurt, information for stand builders (2025)', MF_BUILD)]),
      tips=['<b>A place to talk.</b> A closed meeting room or a few quieter tables, so conversations can go deeper than the aisle allows.',
            '<b>Say what you make, from the aisle.</b> Visitors scan quickly, so your offer, such as APIs, CDMO services or packaging, should be readable from a few metres away.',
            '<b>Storage.</b> A small lockable room for samples, brochures, coats and bags keeps the stand tidy through three busy days.',
            "<b>Good light and power where you need it.</b> For screens, a coffee machine and charging, planned with the organiser's electricity order."]),
]
BY = {f['slug']: f for f in FAIRS}

P = '<p style="margin: 0">'
def H2(id_, t): return f'<section id="{id_}" style="scroll-margin-top: 24px; display: flex; flex-direction: column; gap: 20px; padding-top: 40px; border-top: 1px solid #D8D1C5"><h2 style="margin: 0; font-size: 32px; line-height: 1.1; letter-spacing: -0.02em; font-weight: 600">{t}</h2>'
def SRC(items): return '<p style="margin: 0; font-size: 14px; color: #5B5650">' + ('Sources: ' if len(items) > 1 else 'Source: ') + ' · '.join(f'<a href="{u}" target="_blank" rel="noopener" style="color: #13704D">{t}</a>' for t, u in items) + '</p>'
TICK = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true" style="flex: none; margin-top: 5px"><circle cx="12" cy="12" r="11" fill="#13704D"/><path d="M7 12.5l3.2 3.2L17 9" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def ul(items): return '<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 12px">' + ''.join(f'<li style="display: flex; gap: 12px; align-items: flex-start">{TICK}<span>{re.sub(r"^<b>([^<]*</b>) ", r'<b style="display: block; margin-bottom: 2px">\1', x)}</span></li>' for x in items) + '</ul>'
NB = lambda s: s.replace('&nbsp;', ' ')

def head(title, desc, url, depth_current_fairs=True):
    h = HEAD0
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', h)
    h = h.replace('https://1o1expo.com/guides/stand-cost/', url)
    h = re.sub(r'<meta property="og:type" content="article">\n<meta property="article:published_time" content="[^"]*">\n<meta property="article:modified_time" content="[^"]*">', '<meta property="og:type" content="website">', h)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', h)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', h)
    h = h.replace('https://1o1expo.com/img/guide-cost-buildup.jpg', 'https://1o1expo.com/img/og-image.jpg').replace('<meta property="og:image:width" content="1672">', '<meta property="og:image:width" content="1200">').replace('<meta property="og:image:height" content="941">', '<meta property="og:image:height" content="630">')
    h = re.sub(r'<meta property="og:image:alt" content="[^"]*">', f'<meta property="og:image:alt" content="{title}">', h)
    h = re.sub(r'<title>[^<]*</title>', f"<title>{title} | 1o1 expo</title>", h)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', h)
    h = h.replace('<a href="../" aria-current="page" style="color: #13704D; text-decoration: none; font-weight: 600">Guides</a>', '<a href="../../guides/" style="color: #1C1A17; text-decoration: none">Guides</a>')
    h = h.replace('<a href="../../fairs/" style="color: #1C1A17; text-decoration: none">Trade fairs</a>', '<a href="../../fairs/" aria-current="page" style="color: #13704D; text-decoration: none; font-weight: 600">Trade fairs</a>')
    return h

def tail(quote):
    t = TAIL0.replace('href="../../index.html#quote" style="display: inline-flex', f'href="{quote}" style="display: inline-flex', 1)
    return t.replace('href="../"', 'href="../../guides/"')

def ld(objs, h): return h.replace('</head>', ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in objs) + '</head>')

def render(F):
    yr = '2027'
    quote = '../../index.html?fair=' + urllib.parse.quote(f"{F['full']} {yr}") + '#quote'
    title = f"Exhibition stands for {F['full']} {yr}"
    desc = f"Custom exhibition stands for {F['full']} {yr} ({F['dshort']}, {F['venue']}): design, production, transport, build-up and dismantling in one all-inclusive price."
    url = f"https://1o1expo.com/fairs/{F['slug']}/"
    late = F['brief'] in ('Now', 'As soon as possible')
    faq = [
        (f"When should we contact you for {F['name']} {yr}?", ("Now. For a custom stand, about five months ahead is comfortable, and that point has already passed or is close. Tell us your date in your brief and we tell you honestly whether we can still build it&nbsp;well." if late else f"For a custom stand, about five months ahead is comfortable, so by {F['brief']}. Later is often still possible: tell us your date in your brief and we tell you honestly whether we can still build it&nbsp;well.")),
        ("Does your price include the floor space?", "No. You book and pay the space, electricity, water and other venue services directly with the organiser. Our all-inclusive price covers the stand itself: design, production, graphics, transport, build-up and&nbsp;dismantling."),
        ("Who handles the organiser's technical forms?", "You book the space and the organiser's services. We help you with the technical forms for the stand itself, such as the stand drawings the organiser asks&nbsp;for."),
        ("Is someone from your team at the fair?", "Yes. Our team is on site throughout the fair, so if anything on the stand needs attention, it is handled&nbsp;quickly."),
    ]
    h = head(title, desc, url)
    h = ld([
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "1o1 expo", "item": "https://1o1expo.com/"},
            {"@type": "ListItem", "position": 2, "name": "Trade fairs", "item": "https://1o1expo.com/fairs/"},
            {"@type": "ListItem", "position": 3, "name": F['full'], "item": url}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": NB(q), "acceptedAnswer": {"@type": "Answer", "text": NB(a)}} for q, a in faq]},
    ], h)
    facts = [('Dates', F['dates']), ('Venue', F['venue']), ('Brief us by', F['brief'])]
    fx = ''.join(f'<div style="display: flex; flex-direction: column; gap: 4px; padding: 0 28px; border-left: 1px solid rgba(255,255,255,.22)"><span style="font-size: 12px; letter-spacing: .08em; font-weight: 700; color: #5ED3A2">{k.upper()}</span><b style="font-size: 18px; font-weight: 600">{v}</b></div>' for k, v in facts)
    hero = f'''</header><section style="background: #0E3B2B; color: #FFFFFF"><div class="fh" style="max-width: 1240px; margin: 0 auto; padding: 56px 24px 56px; display: grid; grid-template-columns: minmax(0,1.15fr) minmax(0,.85fr); gap: 48px; align-items: center"><div style="display: flex; flex-direction: column; gap: 22px">
<nav aria-label="Breadcrumb" style="font-size: 15px; color: rgba(255,255,255,.7)"><a href="../" style="color: #5ED3A2; text-decoration: none; font-weight: 600">Trade fairs</a> <span aria-hidden="true">/</span> {F['full']}</nav>
<span style="font-size: 12px; letter-spacing: .08em; font-weight: 700; color: #5ED3A2">{F['sector'].upper()} · {F['city'].upper()}</span>
<h1 style="margin: 0; max-width: 18em; font-size: clamp(34px, 4.6vw, 56px); line-height: 1.05; letter-spacing: -0.03em; font-weight: 600; text-wrap: balance">Exhibition stands for {F['full']}&nbsp;{yr}</h1>
<p style="margin: 0; max-width: 38em; font-size: 19px; line-height: 1.6; color: rgba(255,255,255,.85)">Send us your hall, stand number and a few notes. Within 7 working days you get a design and one all-inclusive price, and our team takes care of production, transport, build-up and dismantling at {F['venue']}.</p>
<div class="fx" style="display: flex; flex-wrap: wrap; gap: 16px 0; margin: 6px 0 0 -28px">{fx}</div>
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 14px 22px; margin-top: 10px"><a href="{quote}" style="display: inline-flex; align-items: center; gap: 10px; min-height: 54px; padding: 0 24px; background: #5ED3A2; color: #12100E; font-weight: 600; font-size: 17px; text-decoration: none">Get a quote for {F['name']} <span aria-hidden="true">→</span></a><span style="font-size: 15px; color: rgba(255,255,255,.7)">Free and without obligation.</span></div>
</div><figure class="fh-img" style="margin: 0; position: relative"><img src="../../img/{F['img']}" alt="Concept visualisation of an exhibition stand" width="1200" height="900" style="display: block; width: 100%; height: auto; aspect-ratio: 4 / 3.4; object-fit: cover; box-shadow: 0 24px 48px rgba(0,0,0,.28)"><figcaption style="margin-top: 10px; font-size: 13px; color: rgba(255,255,255,.65)">Concept visualisation</figcaption></figure></div></section>'''
    toc_items = [('about', f"About {F['name']}"), ('timeline', 'Your timeline'), ('stand', 'What works on the stand'), ('price', 'What our price covers'), ('questions', 'Common questions')]
    toc = '<nav class="toc" aria-label="On this page" style="position: sticky; top: 24px; display: flex; flex-direction: column; font-size: 15px"><span style="font-size: 12px; letter-spacing: .08em; font-weight: 700; color: #5B5650; padding-bottom: 8px">ON THIS&nbsp;PAGE</span>' + ''.join(f'<a href="#{i}" style="color: #1C1A17; text-decoration: none; padding: 6px 0; border-bottom: 1px solid #E6E0D6">{t}</a>' for i, t in toc_items) + '</nav>'
    about = H2('about', f"About {F['full']}").replace('; padding-top: 40px; border-top: 1px solid #D8D1C5', '', 1) + ''.join(P + p + '</p>' for p in F['about']) + SRC(F['src']) + '</section>'
    bu = F.get('buildup')
    steps = [
        ('Now' if late else f"Now to {F['brief']}", 'Brief us', 'Your hall, stand number, size and open sides, plus what visitors should remember. A phone photo of the floor plan is fine.'),
        ('About 6–8 weeks before build-up', "Organiser's deadlines", "Stand drawings and service orders are usually due around here. The exact dates are in the organiser's exhibitor manual, so check it as soon as you get access."),
        ('The days before opening', 'Build-up', (bu[0] + ' ' if bu else 'Build-up usually takes a few days before the fair opens; the organiser publishes the exact days and hours. ') + 'We build, and you check the finished stand before the doors open.'),
        (F['dates'], 'The fair', 'You meet your visitors. Our team is on site throughout the fair.'),
        ('After the fair closes', 'Dismantling', 'We take the stand down and out of the hall within the organiser\'s dismantling times.'),
    ]
    tl = ''.join(f'<div style="display: grid; grid-template-columns: 44px minmax(0,1fr); gap: 14px; padding: 16px 0{"; border-top: 1px solid #E6E0D6" if i else ""}"><span style="width: 34px; height: 34px; border-radius: 50%; background: {"#5ED3A2" if i==3 else "#0E3B2B"}; color: {"#0E3B2B" if i==3 else "#FFFFFF"}; display: inline-flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 700">{i+1}</span><div style="display: flex; flex-direction: column; gap: 4px"><span style="font-size: 12px; letter-spacing: .08em; font-weight: 700; color: #13704D">{w.upper()}</span><b style="font-size: 19px; font-weight: 600">{t}</b><span style="font-size: 16px; line-height: 1.6; color: #3F3B36">{d}</span></div></div>' for i, (w, t, d) in enumerate(steps))
    timeline = H2('timeline', f"Your {F['name']} {yr} timeline") + P + f"Working back from opening day. Dates come from the organiser and can change, so always check the exhibitor manual.</p>" + f'<div class="rv" style="background: #FFFFFF; border: 1px solid #D8D1C5; padding: 6px 24px 8px">{tl}</div>' + (SRC(bu[1]) if bu else '') + '</section>'
    stand = H2('stand', (f"What works on an {F['name']} stand" if F['name'][:3] in ("Amb","IFA","Int","MWC","SBC") else f"What works on a {F['name']} stand")) + P + "A few things we plan for on almost every stand at this fair:</p>" + ul(F['tips']) + P + 'Not sure what fits your space? Read our guide to <a href="../../guides/stand-types/">stand types</a> or <a href="../../guides/stand-brief/">what to put in your brief</a>.</p></section>'
    inc = ['Stand design and visuals', 'Walls, flooring and furniture', 'Lighting and electrics on the stand', 'Printed graphics and branding', 'Transport to the venue', 'Build-up and dismantling']
    price = H2('price', 'What our price covers') + P + "One all-inclusive price for the whole stand, agreed before anything is made. Every change is priced before you approve&nbsp;it.</p>" + f'<div class="pc2" style="display: grid; grid-template-columns: 1fr 1fr; border-top: 1.5px solid #1C1A17; border-bottom: 1px solid #D8D1C5"><div style="padding: 18px 24px 20px 0"><span style="display: block; font-size: 12px; letter-spacing: .08em; font-weight: 700; color: #13704D; margin-bottom: 10px">IN OUR PRICE</span>{ul(inc)}</div><div class="pc2-r" style="padding: 18px 0 20px 24px; border-left: 1px solid #D8D1C5"><span style="display: block; font-size: 12px; letter-spacing: .08em; font-weight: 700; color: #8A6A1E; margin-bottom: 10px">BOOKED WITH THE ORGANISER</span><p style="margin: 0; font-size: 17px; line-height: 1.6">Floor space, electricity and water connections, internet, cleaning and other venue services. You book and pay these directly with the organiser, and we tell you which ones your stand&nbsp;needs.</p></div></div>' + P + 'More on this in <a href="../../guides/stand-cost/">What drives the cost of an exhibition stand</a>.</p></section>'
    sib = [x for x in FAIRS if x['city'] == F['city'] and x['slug'] != F['slug']]
    also = (f'Also in {F["city"]}: ' + ', '.join(f'<a href="../{x["slug"]}/">{x["full"]}</a>' for x in sib) + '. ') if sib else ''
    faqh = H2('questions', 'Common&nbsp;questions') + '<div style="display: flex; flex-direction: column; gap: 10px">' + ''.join(f'<details class="gq" style="background: #FFFFFF; border: 1px solid #D8D1C5"><summary style="list-style: none; cursor: pointer; display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 18px 20px; font-weight: 600; font-size: 17px"><span>{q}</span><span class="gq-plus" aria-hidden="true" style="flex: none; width: 28px; height: 28px; border-radius: 50%; border: 1.5px solid #1C1A17; display: flex; align-items: center; justify-content: center; transition: transform .2s">+</span></summary><p style="margin: 0; padding: 0 20px 20px; font-size: 16px; line-height: 1.6; color: #3F3B36">{a}</p></details>' for q, a in faq) + '</div>'
    faqh += f'<p style="margin: 8px 0 0; font-size: 16px; color: #3F3B36">{also}See <a href="../">all trade fairs</a> or the dates in our <a href="../../guides/trade-fair-calendar-2027/">trade fair calendar 2027</a>.</p></section>'
    body = f'''<section style="max-width: 1240px; margin: 0 auto; padding-left: 24px; padding-right: 24px; padding-top: clamp(48px, 6vw, 80px)"><div class="art" style="display: grid; grid-template-columns: 240px minmax(0, 1fr); gap: 64px; align-items: start">
{toc}
<article style="display: flex; flex-direction: column; gap: 32px; font-size: 18px; line-height: 1.7; max-width: 760px">
{about}
{timeline}
{stand}
{price}
{faqh}
</article></div></section>
<style>@media (max-width:960px){{.fh{{grid-template-columns:minmax(0,1fr)!important}}.fh-img{{display:none}}}}@media (max-width:900px){{.art{{grid-template-columns:minmax(0,1fr)!important;gap:24px!important}}.toc{{position:static!important}}}}@media (max-width:700px){{.pc2{{grid-template-columns:1fr!important}}.pc2-r{{border-left:0!important;padding-left:0!important;border-top:1px solid #D8D1C5}}.fx>div{{padding:0 18px!important}}}}</style>'''
    os.makedirs(SITE + f"fairs/{F['slug']}", exist_ok=True)
    open(SITE + f"fairs/{F['slug']}/index.html", 'w').write(h + '\n' + hero + '\n' + body + '\n' + tail(quote))

def hub():
    title = 'Exhibition stands at trade fairs across Europe'
    desc = 'Custom exhibition stands for Hannover Messe, Ambiente, CPHI, MWC, Intersolar, Eurobike, gamescom, IFA, SBC Summit and RENEO: dates, venues and what works on the stand.'
    h = head(title, desc, 'https://1o1expo.com/fairs/')
    h = h.replace('href="../../', 'href="../').replace('src="../../', 'src="../')
    order = sorted(FAIRS, key=lambda x: x['start'])
    cards = ''.join(f'''<a href="{f['slug']}/" class="gcard fcard" data-city="{f['city']}" style="text-decoration: none; color: #1C1A17; display: flex; flex-direction: column; background: #FFFFFF; border: 1px solid #E6E0D6"><span style="display: block; overflow: hidden"><img src="../img/{f['img']}" alt="" width="1200" height="900" loading="lazy" style="display: block; width: 100%; height: auto; aspect-ratio: 16 / 10; object-fit: cover"></span><span style="padding: 18px 22px 22px; display: flex; flex-direction: column; gap: 8px"><span style="font-size: 12px; letter-spacing: .08em; font-weight: 700; color: #13704D">{f['sector'].upper()} · {f['city'].upper()}</span><span class="gt" style="font-size: 21px; font-weight: 600; line-height: 1.2">{f['full']}</span><span style="font-size: 15px; color: #3F3B36">{f['dshort']} · {f['venue']}</span><span class="gread" style="margin-top: 6px; font-weight: 600">Stands for {f['name']}&nbsp;→</span></span></a>''' for f in order)
    hero = f'''</header><section style="background: #0E3B2B; color: #FFFFFF"><div style="max-width: 1240px; margin: 0 auto; padding: 56px 24px 56px; display: flex; flex-direction: column; gap: 18px">
<span style="font-size: 12px; letter-spacing: .08em; font-weight: 700; color: #5ED3A2">TRADE FAIRS · 2027</span>
<h1 style="margin: 0; max-width: 18em; font-size: clamp(34px, 4.6vw, 56px); line-height: 1.05; letter-spacing: -0.03em; font-weight: 600; text-wrap: balance">Exhibition stands at trade fairs across&nbsp;Europe</h1>
<p style="margin: 0; max-width: 40em; font-size: 19px; line-height: 1.6; color: rgba(255,255,255,.85)">The fairs exhibitors ask us about most, with dates, venues and what works on the stand. Your fair is not listed? We build at trade fairs anywhere in&nbsp;Europe.</p></div></section>
<section style="max-width: 1240px; margin: 0 auto; padding: 56px 24px 0"><div id="fcity" hidden style="flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px 24px; background: #DDF4EA; border: 1px solid #9FD8BF; padding: 16px 22px; margin-bottom: 24px; font-size: 17px"><span id="fcity-t"></span><a href="./" id="fcity-all" style="font-weight: 600; color: #13704D">Show all trade fairs&nbsp;→</a></div><div class="fgrid" style="display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 24px">{cards}</div>
<p style="margin: 28px 0 0; font-size: 16px; color: #3F3B36">Dates come from each organiser and can change. See all dates in our <a href="../guides/trade-fair-calendar-2027/">trade fair calendar 2027</a>.</p></section>
<style>.fcard{{transition:box-shadow .2s,border-color .2s}}.fcard:hover{{border-color:#5ED3A2!important;box-shadow:0 10px 24px rgba(28,26,23,.08)}}@media (max-width:1000px){{.fgrid{{grid-template-columns:repeat(2,minmax(0,1fr))!important}}}}@media (max-width:620px){{.fgrid{{grid-template-columns:1fr!important}}}}</style><script>(function(){{try{{var c=new URLSearchParams(location.search).get("city");if(!c)return;var cards=[].slice.call(document.querySelectorAll(".fcard")),hit=cards.filter(function(e){{return e.dataset.city.toLowerCase()===c.toLowerCase()}});var box=document.getElementById("fcity"),t=document.getElementById("fcity-t");var safe=c.replace(/[^A-Za-zÀ-ž \-]/g,"").slice(0,30);box.hidden=false;box.style.display="flex";if(hit.length){{cards.forEach(function(e){{if(hit.indexOf(e)<0)e.style.display="none"}});t.innerHTML="";t.appendChild(document.createTextNode("Trade fairs in "+safe+" with their own page."))}}else{{t.innerHTML="";t.appendChild(document.createTextNode("We build at fairs in "+safe+" too. Tell us which fair and we will send you a design and a price. "));var a=document.createElement("a");a.href="../index.html?fair="+encodeURIComponent(safe)+"#quote";a.textContent="Get a quote →";a.style.fontWeight="600";a.style.color="#13704D";t.appendChild(a)}}}}catch(e){{}}}})();</script>'''
    t = tail('../index.html#quote').replace('href="../../', 'href="../').replace('src="../../', 'src="../').replace('href="../guides/"', 'href="../guides/"')
    h = h.replace('href="../fairs/" aria-current', 'href="./" aria-current')
    open(SITE + 'fairs/index.html', 'w').write(h + '\n' + hero + '\n' + t)

for f in FAIRS: render(f)
hub()
print('ok', len(FAIRS))
