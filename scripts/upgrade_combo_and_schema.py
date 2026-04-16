#!/usr/bin/env python3
"""
Upgrade combo pages (borough+service) and add Service schema to borough pages.

Combo pages (160 total):
  - Title: "24/7 {Service} in {Borough} | From {price} | FixMyTyreNow"
  - Meta desc: unique per service+borough (postcode + price + USP)
  - Expand nearby-areas from 3 to 5 with varied anchor text
  - Add Review schema to <head>

Borough pages (32 total):
  - Add Service schema (hasOfferCatalog) to existing AutomotiveBusiness block
"""

import os
import re
import json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AREAS_DIR = os.path.join(BASE, 'areas')

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
BOROUGH_NAMES = {
    'barking-and-dagenham': 'Barking and Dagenham',
    'barnet':               'Barnet',
    'bexley':               'Bexley',
    'brent':                'Brent',
    'bromley':              'Bromley',
    'camden':               'Camden',
    'city-of-westminster':  'City of Westminster',
    'croydon':              'Croydon',
    'ealing':               'Ealing',
    'enfield':              'Enfield',
    'greenwich':            'Greenwich',
    'hackney':              'Hackney',
    'hammersmith-and-fulham': 'Hammersmith and Fulham',
    'haringey':             'Haringey',
    'harrow':               'Harrow',
    'havering':             'Havering',
    'hillingdon':           'Hillingdon',
    'hounslow':             'Hounslow',
    'islington':            'Islington',
    'kensington-and-chelsea': 'Kensington and Chelsea',
    'kingston-upon-thames': 'Kingston upon Thames',
    'lambeth':              'Lambeth',
    'lewisham':             'Lewisham',
    'merton':               'Merton',
    'newham':               'Newham',
    'redbridge':            'Redbridge',
    'richmond-upon-thames': 'Richmond upon Thames',
    'southwark':            'Southwark',
    'sutton':               'Sutton',
    'tower-hamlets':        'Tower Hamlets',
    'waltham-forest':       'Waltham Forest',
    'wandsworth':           'Wandsworth',
}

BOROUGH_POSTCODES = {
    'barking-and-dagenham': 'IG11, RM8, RM9, RM10',
    'barnet':               'EN4, EN5, N2, N3, N11',
    'bexley':               'DA1, DA5, DA6, DA7, DA14, SE2',
    'brent':                'HA0, HA9, NW2, NW6, NW10',
    'bromley':              'BR1, BR2, BR3, BR5, BR6, SE20',
    'camden':               'NW1, NW3, NW5, WC1, WC2',
    'city-of-westminster':  'W1, W2, WC1, WC2, SW1',
    'croydon':              'CR0, CR2, CR7, SE25',
    'ealing':               'W5, W7, W13, UB1, UB2',
    'enfield':              'EN1, EN2, EN3, N13, N14, N21',
    'greenwich':            'SE3, SE7, SE9, SE10, SE18',
    'hackney':              'E2, E5, E8, E9, N16',
    'hammersmith-and-fulham': 'W6, W12, SW6',
    'haringey':             'N4, N8, N15, N17, N22',
    'harrow':               'HA1, HA2, HA3, HA7',
    'havering':             'RM1, RM2, RM11, RM12, RM14',
    'hillingdon':           'UB3, UB4, UB8, UB9, UB10',
    'hounslow':             'TW3, TW4, TW5, TW13, W4',
    'islington':            'N1, N4, N5, N7, EC1',
    'kensington-and-chelsea': 'W8, W10, W11, SW3, SW5',
    'kingston-upon-thames': 'KT1, KT2, KT3',
    'lambeth':              'SE1, SE11, SE24, SW2, SW4, SW9',
    'lewisham':             'SE4, SE6, SE12, SE13, SE23',
    'merton':               'SW19, SW20, CR4, SM4',
    'newham':               'E6, E7, E12, E13, E15, E16',
    'redbridge':            'IG1, IG2, IG4, IG5, IG6, IG7',
    'richmond-upon-thames': 'TW1, TW2, TW9, TW10, TW11',
    'southwark':            'SE1, SE5, SE15, SE17, SE21, SE22',
    'sutton':               'SM1, SM2, SM3, SM5, SM6',
    'tower-hamlets':        'E1, E2, E3, E14',
    'waltham-forest':       'E4, E10, E11, E17',
    'wandsworth':           'SW11, SW12, SW17, SW18',
}

NEARBY = {
    'barking-and-dagenham': ['newham', 'havering', 'redbridge', 'greenwich', 'tower-hamlets'],
    'barnet':               ['enfield', 'haringey', 'camden', 'brent', 'harrow'],
    'bexley':               ['greenwich', 'bromley', 'lewisham', 'havering', 'southwark'],
    'brent':                ['barnet', 'harrow', 'ealing', 'hammersmith-and-fulham', 'camden'],
    'bromley':              ['lewisham', 'greenwich', 'croydon', 'bexley', 'southwark'],
    'camden':               ['islington', 'city-of-westminster', 'barnet', 'haringey', 'brent'],
    'city-of-westminster':  ['camden', 'kensington-and-chelsea', 'islington', 'lambeth', 'tower-hamlets'],
    'croydon':              ['bromley', 'lewisham', 'southwark', 'sutton', 'merton'],
    'ealing':               ['brent', 'hillingdon', 'hounslow', 'hammersmith-and-fulham', 'harrow'],
    'enfield':              ['barnet', 'haringey', 'waltham-forest', 'hackney', 'islington'],
    'greenwich':            ['lewisham', 'southwark', 'bexley', 'newham', 'tower-hamlets'],
    'hackney':              ['tower-hamlets', 'islington', 'haringey', 'newham', 'waltham-forest'],
    'hammersmith-and-fulham': ['ealing', 'hounslow', 'wandsworth', 'kensington-and-chelsea', 'brent'],
    'haringey':             ['barnet', 'enfield', 'hackney', 'islington', 'camden'],
    'harrow':               ['barnet', 'brent', 'ealing', 'hillingdon', 'hammersmith-and-fulham'],
    'havering':             ['barking-and-dagenham', 'redbridge', 'bexley', 'newham', 'greenwich'],
    'hillingdon':           ['harrow', 'ealing', 'hounslow', 'brent', 'hammersmith-and-fulham'],
    'hounslow':             ['ealing', 'hillingdon', 'richmond-upon-thames', 'hammersmith-and-fulham', 'wandsworth'],
    'islington':            ['camden', 'hackney', 'tower-hamlets', 'city-of-westminster', 'haringey'],
    'kensington-and-chelsea': ['city-of-westminster', 'hammersmith-and-fulham', 'wandsworth', 'brent', 'camden'],
    'kingston-upon-thames': ['merton', 'richmond-upon-thames', 'sutton', 'wandsworth', 'hounslow'],
    'lambeth':              ['wandsworth', 'southwark', 'lewisham', 'city-of-westminster', 'merton'],
    'lewisham':             ['greenwich', 'bromley', 'southwark', 'lambeth', 'bexley'],
    'merton':               ['wandsworth', 'kingston-upon-thames', 'sutton', 'croydon', 'lambeth'],
    'newham':               ['tower-hamlets', 'hackney', 'waltham-forest', 'barking-and-dagenham', 'greenwich'],
    'redbridge':            ['waltham-forest', 'havering', 'barking-and-dagenham', 'hackney', 'newham'],
    'richmond-upon-thames': ['hounslow', 'kingston-upon-thames', 'wandsworth', 'merton', 'hammersmith-and-fulham'],
    'southwark':            ['lambeth', 'lewisham', 'greenwich', 'tower-hamlets', 'city-of-westminster'],
    'sutton':               ['merton', 'kingston-upon-thames', 'croydon', 'wandsworth', 'lambeth'],
    'tower-hamlets':        ['hackney', 'newham', 'greenwich', 'southwark', 'islington'],
    'waltham-forest':       ['hackney', 'redbridge', 'newham', 'enfield', 'haringey'],
    'wandsworth':           ['lambeth', 'merton', 'richmond-upon-thames', 'kingston-upon-thames', 'hammersmith-and-fulham'],
}

SERVICES = {
    'emergency-tyre-replacement': {
        'name': 'Emergency Tyre Replacement',
        'price_str': 'From £69',
        'price_num': '69',
        'duration': '30 mins',
        'usp': 'Fastest callout. We aim to reach you within 20 minutes, any time of day or night.',
    },
    'standard-tyre-fitting': {
        'name': 'Standard Tyre Fitting',
        'price_str': 'From £65',
        'price_num': '65',
        'duration': '45 mins',
        'usp': 'Full tyre replacement at your location. No garage visit needed.',
    },
    'puncture-repair': {
        'name': 'Puncture Repair',
        'price_str': 'From £25',
        'price_num': '25',
        'duration': '30 mins',
        'usp': 'Most punctures repaired on the spot in under 30 minutes.',
    },
    'wheel-balancing': {
        'name': 'Wheel Balancing',
        'price_str': 'From £15',
        'price_num': '15',
        'duration': '30 mins',
        'usp': 'Precision mobile wheel balancing using portable equipment at your location.',
    },
    'run-flat-replacement': {
        'name': 'Run-Flat Replacement',
        'price_str': 'From £110',
        'price_num': '110',
        'duration': '45 mins',
        'usp': 'Specialist run-flat replacement for BMW, Mercedes, Range Rover and more.',
    },
}

# Anchor text variants for nearby links (cycles through 5)
ANCHOR_VARIANTS = [
    'Mobile Tyre Fitting in {borough}',
    'Same-Day Tyre Fitting in {borough}',
    '24/7 Tyre Service in {borough}',
    'Emergency Tyre Fitting in {borough}',
    'Mobile Tyre Fitter in {borough}',
]

# Review quotes per borough (reuse from upgrade script)
REVIEWS = {
    'barking-and-dagenham': ('James T., Dagenham', 'Tyre went flat at 8pm near the A13. They were with me in 18 minutes. Brilliant service.'),
    'barnet': ('Sarah M., Finchley', 'Flat tyre outside my house at 7am. Fitter arrived in 22 minutes and I still made it to work on time.'),
    'bexley': ('Dave K., Sidcup', 'Got a flat on the A2 at night. Called FixMyTyreNow and the fitter was there in under 20 minutes. Excellent.'),
    'brent': ('Marcus O., Wembley', 'Parked near the stadium before a concert, came back to a flat. Fixed within 30 mins. Saved my night.'),
    'bromley': ('Helen R., Orpington', 'Had a blowout on the A21. Called them and the fitter arrived quickly. Professional and calm under pressure.'),
    'camden': ('Tom B., Hampstead', 'Run-flat light came on in Hampstead. They arrived fast and sorted it on the street. No garage needed.'),
    'city-of-westminster': ('Fiona A., Mayfair', 'Flat tyre on a residents street at midnight. Fitter arrived in 19 minutes. Absolutely outstanding.'),
    'croydon': ('Priya S., Thornton Heath', 'Puncture on the way to work near East Croydon. They arrived in 17 minutes. Brilliant.'),
    'ealing': ('Arjun P., Southall', 'Got a flat outside the supermarket in Southall. Called and they came in 20 mins. Easy and affordable.'),
    'enfield': ('Chris H., Winchmore Hill', 'Flat at 6am before a long drive. Fitter arrived in under 20 minutes. Sorted and on the road by 6:45.'),
    'greenwich': ('Michelle T., Woolwich', 'Blowout near the A2 at night. They came fast, professional, sorted it in 35 minutes. Highly recommend.'),
    'hackney': ('Kezia N., Dalston', 'Puncture on my street at midnight. Fitter arrived in 18 minutes. So impressed with the service.'),
    'hammersmith-and-fulham': ('George W., Fulham', 'Flat tyre outside the flat in SW6 at 11pm. Fixed in 30 minutes flat. Will use again.'),
    'haringey': ('Danny F., Tottenham', 'Tyre blew near the Spurs stadium after a match. Fitter was there in 20 minutes in all that traffic. Incredible.'),
    'harrow': ('Lisa C., Pinner', 'Flat tyre at home early morning. Booked online, fitter arrived within 20 mins. Couldn\'t ask for more.'),
    'havering': ('Ray G., Hornchurch', 'A127 blowout on the way home. Safe pull-off, called FixMyTyreNow. There in 22 minutes. Excellent.'),
    'hillingdon': ('Amara J., Hayes', 'Flat outside my office near Heathrow. Fitter there in 19 minutes. Back on the road before my next meeting.'),
    'hounslow': ('Nadia K., Chiswick', 'Slow puncture on my way out in the morning. Called at 7:30am, fitter arrived by 7:52. Perfect.'),
    'islington': ('Ben A., Angel', 'Parked on my street, flat in the morning. Fitter arrived in 17 minutes. Great service, easy booking.'),
    'kensington-and-chelsea': ('Olivia B., Chelsea', 'Low profile tyre on my Porsche, needed specialist help at 10pm in SW3. They knew exactly what they were doing.'),
    'kingston-upon-thames': ('Claudia F., Surbiton', 'Slow puncture found at 7am. Booked online, fitter arrived by 8am. Back on the road for my commute.'),
    'lambeth': ('Jade L., Brixton', 'Flat tyre outside my house in Brixton at midnight. Arrived in 20 minutes. Friendly and professional.'),
    'lewisham': ('Owen P., Forest Hill', 'Noticed a flat at 8am on the street. Fitter arrived at 8:25. Sorted quickly and professionally.'),
    'merton': ('Alice M., Wimbledon', 'Tyre went flat outside the shops in Wimbledon. Fitter arrived quickly. Friendly service, fair price.'),
    'newham': ('Tunde A., Stratford', 'Blowout near Westfield car park. Called FixMyTyreNow and they were there in 18 minutes. Excellent.'),
    'redbridge': ('Mia B., Ilford', 'Flat at the shopping centre in Ilford. Fitter there in 20 minutes, car sorted in 40. Very happy.'),
    'richmond-upon-thames': ('Edward N., Richmond', 'Run-flat warning on the A316 at 7am. Fitter met me at a safe layby within 20 minutes. Brilliant.'),
    'southwark': ('Jordan K., Peckham', 'Puncture on my way home from work in Peckham. Called them and fitter arrived in 19 minutes. Ace.'),
    'sutton': ('Phil D., Cheam', 'Found a slow puncture at 7am. Called, booked, fitter arrived by 7:40. Home in time for the school run.'),
    'tower-hamlets': ('Steve T., Canary Wharf', 'Flat tyre in the car park at work in E14. They were there in 17 minutes. Back in the office without missing a beat.'),
    'waltham-forest': ('Yasmin O., Walthamstow', 'Tyre burst near the market at 6pm. They arrived in 21 minutes through the traffic. Fantastic service.'),
    'wandsworth': ('Sam H., Battersea', 'Flat tyre near the Power Station development. Called at 9pm, fitter arrived by 9:20. Couldn\'t believe it.'),
}


def build_review_schema(borough_slug, service_slug, service_name, borough_name):
    reviewer, review_text = REVIEWS.get(borough_slug, ('London Customer', 'Excellent fast service. Highly recommended.'))
    # reviewer = "John D., Barnet" → split at ", "
    parts = reviewer.split(', ')
    author_name = parts[0] if parts else reviewer
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Review",
        "itemReviewed": {
            "@type": "Service",
            "name": f"{service_name} in {borough_name}",
            "provider": {"@type": "LocalBusiness", "name": "FixMyTyreNow"}
        },
        "reviewRating": {
            "@type": "Rating",
            "ratingValue": "5",
            "bestRating": "5"
        },
        "author": {"@type": "Person", "name": author_name},
        "reviewBody": review_text
    }, ensure_ascii=False, separators=(',', ':'))


def build_service_schema_for_borough(borough_name, borough_slug):
    url = f"https://fixmytyrenow.com/areas/{borough_slug}/"
    schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": "Mobile Tyre Fitting",
        "name": f"Mobile Tyre Fitting {borough_name}",
        "provider": {
            "@type": "AutomotiveBusiness",
            "name": "FixMyTyreNow",
            "url": "https://fixmytyrenow.com",
            "telephone": "07340645595"
        },
        "areaServed": {
            "@type": "AdministrativeArea",
            "name": f"{borough_name}, London"
        },
        "url": url,
        "offers": [
            {"@type": "Offer", "name": "Emergency Tyre Replacement", "price": "69", "priceCurrency": "GBP", "availability": "https://schema.org/InStock"},
            {"@type": "Offer", "name": "Standard Tyre Fitting", "price": "65", "priceCurrency": "GBP", "availability": "https://schema.org/InStock"},
            {"@type": "Offer", "name": "Puncture Repair", "price": "25", "priceCurrency": "GBP", "availability": "https://schema.org/InStock"},
            {"@type": "Offer", "name": "Wheel Balancing", "price": "15", "priceCurrency": "GBP", "availability": "https://schema.org/InStock"},
            {"@type": "Offer", "name": "Run-Flat Replacement", "price": "110", "priceCurrency": "GBP", "availability": "https://schema.org/InStock"},
        ],
        "availableChannel": {
            "@type": "ServiceChannel",
            "serviceUrl": url,
            "availableLanguage": "en-GB"
        }
    }
    return json.dumps(schema, ensure_ascii=False, separators=(',', ':'))


def upgrade_combo_page(filepath, borough_slug, service_slug):
    borough_name = BOROUGH_NAMES.get(borough_slug, '')
    postcodes = BOROUGH_POSTCODES.get(borough_slug, '')
    svc = SERVICES.get(service_slug)
    if not borough_name or not svc:
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    svc_name = svc['name']
    price_str = svc['price_str']
    usp = svc['usp']
    new_title = f"{svc_name} in {borough_name} | 24/7, {price_str} | FixMyTyreNow"
    new_meta = f"{svc_name} in {borough_name}. {usp} Covers {postcodes}. Book with £10 deposit."

    # ── Title ──
    content = re.sub(r'<title>.*?</title>', f'<title>{new_title}</title>', content)

    # ── Meta descriptions ──
    content = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{new_meta}">', content)
    content = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{new_meta}">', content)
    content = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{new_meta}">', content)

    # ── og:title + twitter:title ──
    content = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{new_title}">', content)
    content = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{new_title}">', content)

    # ── Add Review schema (before </head>) ──
    if '"@type":"Review"' not in content:
        review_schema = build_review_schema(borough_slug, service_slug, svc_name, borough_name)
        content = content.replace(
            '</head>',
            f'<script type="application/ld+json">{review_schema}</script>\n</head>',
            1
        )

    # ── Expand nearby-areas to 5 with varied anchor text ──
    nearby = NEARBY.get(borough_slug, [])
    anchor_variants = ANCHOR_VARIANTS
    new_links = ['<div class="nearby-areas">', f'<h3>Also available in nearby areas</h3>', '<ul>']
    for i, n_slug in enumerate(nearby):
        n_name = BOROUGH_NAMES.get(n_slug, n_slug.replace('-', ' ').title())
        anchor_tmpl = anchor_variants[i % len(anchor_variants)]
        anchor_text = anchor_tmpl.format(borough=n_name)
        new_links.append(f'            <li><a href="../../{n_slug}/{service_slug}/">{anchor_text}</a></li>')
    new_links.append('        </ul>')
    new_links.append('        </div>')
    new_nearby_html = '\n'.join(new_links)

    content = re.sub(
        r'<div class="nearby-areas">.*?</div>',
        new_nearby_html,
        content,
        flags=re.DOTALL
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


def add_service_schema_to_borough_page(filepath, borough_slug):
    borough_name = BOROUGH_NAMES.get(borough_slug, '')
    if not borough_name:
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if '"serviceType"' in content:
        return False  # already has service schema

    service_schema = build_service_schema_for_borough(borough_name, borough_slug)
    # Insert before </head>
    content = content.replace(
        '</head>',
        f'<script type="application/ld+json">{service_schema}</script>\n</head>',
        1
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


def main():
    combo_ok = 0
    schema_ok = 0
    errors = 0

    # ── 1. Upgrade combo pages ──────────────────────────────────────────────
    print("=== Upgrading combo pages (borough+service) ===")
    for borough_slug in BOROUGH_NAMES:
        borough_dir = os.path.join(AREAS_DIR, borough_slug)
        if not os.path.isdir(borough_dir):
            continue
        for service_slug in SERVICES:
            filepath = os.path.join(borough_dir, service_slug, 'index.html')
            if not os.path.exists(filepath):
                continue
            try:
                upgrade_combo_page(filepath, borough_slug, service_slug)
                combo_ok += 1
            except Exception as e:
                print(f"  ERROR combo {borough_slug}/{service_slug}: {e}")
                errors += 1

    print(f"  Combo pages upgraded: {combo_ok}")

    # ── 2. Add Service schema to borough pages ──────────────────────────────
    print("\n=== Adding Service schema to borough pages ===")
    for borough_slug in BOROUGH_NAMES:
        filepath = os.path.join(AREAS_DIR, borough_slug, 'index.html')
        if not os.path.exists(filepath):
            continue
        try:
            if add_service_schema_to_borough_page(filepath, borough_slug):
                print(f"  Schema added: {borough_slug}")
                schema_ok += 1
        except Exception as e:
            print(f"  ERROR schema {borough_slug}: {e}")
            errors += 1

    print(f"\nDone. Combo: {combo_ok} upgraded, Schema: {schema_ok} added, Errors: {errors}")


if __name__ == '__main__':
    main()
