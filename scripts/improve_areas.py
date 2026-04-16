#!/usr/bin/env python3
"""
Improve /areas/ pages for Google #1 rankings.
- Replaces thin borough intro content with rich, unique, borough-specific content
- Adds visible FAQ section to borough pages
- Fixes em-dashes (U+2014) everywhere in areas pages
- Updates meta descriptions to remove em-dashes
"""

import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AREAS_DIR = os.path.join(BASE, 'areas')

# ---------------------------------------------------------------------------
# Borough data: unique content for each of the 32 London boroughs
# ---------------------------------------------------------------------------
BOROUGHS = {
    'barking-and-dagenham': {
        'name': 'Barking and Dagenham',
        'postcodes': ['IG11', 'RM8', 'RM9', 'RM10'],
        'intro': (
            "Barking and Dagenham is one of East London's most industrious boroughs, "
            "with a proud working heritage that stretches back to the Ford Dagenham plant "
            "and beyond. The borough covers a wide area from the Thames-side docks at "
            "Barking to the residential streets of Chadwell Heath and Rush Green. "
            "Major roads including the A13 and A406 North Circular carry heavy traffic "
            "through the area daily, making tyre wear and roadside incidents a genuine "
            "concern for local drivers."
        ),
        'coverage': (
            "Our mobile tyre fitters cover every corner of Barking and Dagenham, "
            "including Barking town centre, Becontree, Dagenham, Chadwell Heath, "
            "Rush Green, and Marks Gate. Whether you are parked near Barking station "
            "or dealing with a flat on the A13, we reach you fast. We serve postcodes "
            "IG11, RM8, RM9, and RM10 with the same reliable 20-minute response time "
            "available across Greater London."
        ),
        'why_us': (
            "Drivers in Barking and Dagenham benefit from our fully equipped mobile "
            "vans that stock a wide range of tyre sizes to suit everything from family "
            "hatchbacks to commercial vehicles. With same-day slots and 24/7 emergency "
            "cover, there is never a wrong time to call. Our fitters know the local "
            "roads and can reach you at home, at work, or on the roadside without delay."
        ),
        'faq': [
            ("Which postcodes in Barking and Dagenham do you cover?",
             "We cover IG11, RM8, RM9, and RM10 throughout Barking and Dagenham, "
             "reaching Barking town centre, Becontree, Dagenham, Chadwell Heath, and surrounding areas."),
            ("Can you help me if my tyre blows on the A13?",
             "Yes. The A13 runs through Barking and Dagenham and our fitters respond to "
             "roadside callouts there regularly. Call us and a technician will be with you "
             "in around 20 minutes."),
            ("Do you stock tyres for vans and larger vehicles?",
             "Yes, our mobile vans carry tyre stock for cars, SUVs, and light commercial "
             "vehicles. If you drive a van or larger car common in Barking and Dagenham, "
             "we are well prepared to fit the right tyre on the spot."),
            ("How quickly can you reach me in Dagenham?",
             "Our average arrival time across the borough is under 20 minutes. We dispatch "
             "the nearest available fitter directly to your location."),
            ("Do you offer emergency tyre fitting at night in Barking and Dagenham?",
             "Yes. Our emergency service runs 24 hours a day, 7 days a week. "
             "Call us any time of day or night and we will send a fitter to you."),
        ],
    },
    'barnet': {
        'name': 'Barnet',
        'postcodes': ['EN4', 'EN5', 'EN6', 'N2', 'N3', 'N11'],
        'intro': (
            "Barnet is one of North London's largest and most varied boroughs, "
            "stretching from the suburban avenues of High Barnet and Hadley Wood "
            "in the north to the busy residential streets of East Finchley and "
            "Friern Barnet in the south. The borough is home to a wide mix of "
            "drivers, from commuters using the A1 and A41 corridors into central "
            "London to families navigating local roads through Whetstone, "
            "New Barnet, and East Barnet."
        ),
        'coverage': (
            "Our mobile tyre fitting team covers all of Barnet, including High Barnet, "
            "East Barnet, New Barnet, Whetstone, Friern Barnet, Finchley, "
            "East Finchley, Totteridge, Mill Hill, and Edgware. We serve postcodes "
            "EN4, EN5, EN6, N2, N3, and N11, reaching every residential street and "
            "major road in the borough within around 20 minutes of your call."
        ),
        'why_us': (
            "Barnet drivers trust FixMyTyreNow for fast, professional mobile tyre "
            "fitting that fits around busy schedules. Whether you need a tyre changed "
            "at home in Totteridge, at an office in Finchley, or on the roadside "
            "near the A1, our fully equipped vans arrive quickly with the right tyre "
            "in stock. We offer same-day and emergency cover seven days a week."
        ),
        'faq': [
            ("Which parts of Barnet do you cover?",
             "We cover all of Barnet including High Barnet, East Barnet, New Barnet, "
             "Whetstone, Friern Barnet, Finchley, East Finchley, Totteridge, Mill Hill, "
             "and Edgware. Postcodes served include EN4, EN5, EN6, N2, N3, and N11."),
            ("Can you come to me on the A1 if I have a breakdown?",
             "Yes. The A1 is one of the main routes through Barnet and we respond to "
             "roadside callouts along it regularly. Call us and a fitter will reach you "
             "in approximately 20 minutes."),
            ("Do you offer same-day tyre fitting in Barnet?",
             "Yes. Same-day appointments are available throughout Barnet seven days a "
             "week. For emergencies, we operate 24 hours a day."),
            ("How long does mobile tyre fitting take?",
             "Most tyre fittings take between 30 and 45 minutes from when our fitter "
             "arrives. We carry equipment for balancing and pressure checks on the spot."),
            ("Do I need to visit a garage for tyre fitting in Barnet?",
             "No. We are a fully mobile service and come directly to you. "
             "There is no need to visit a garage or tyre centre at any point."),
        ],
    },
    'bexley': {
        'name': 'Bexley',
        'postcodes': ['DA1', 'DA5', 'DA6', 'DA7', 'DA14', 'DA15', 'DA16', 'DA17', 'SE2'],
        'intro': (
            "Bexley is a South-East London borough that stretches from the Thames at "
            "Erith and Abbey Wood east to the rural fringes of Crayford and Swanley Village. "
            "It is a commuter-friendly area with good road connections via the A2 and A20, "
            "making it popular with families who drive regularly into and through London. "
            "Bexleyheath, Sidcup, and Welling form the commercial heart of the borough "
            "while quieter villages like Old Bexley and Foots Cray sit to the south."
        ),
        'coverage': (
            "We cover the entire borough of Bexley including Bexleyheath, Sidcup, "
            "Welling, Crayford, Erith, Abbey Wood, Thamesmead, Belvedere, "
            "New Eltham, and Old Bexley. Postcodes served include DA1, DA5, DA6, "
            "DA7, DA14, DA15, DA16, DA17, and SE2. We reach you within 20 minutes "
            "across the whole borough, from the riverside to the southern outskirts."
        ),
        'why_us': (
            "Bexley drivers benefit from our rapid response to both planned and emergency "
            "tyre requests. The A2 and A20 corridors see heavy use from Bexley commuters "
            "and our fitters know these routes well. We carry tyres to suit the large "
            "number of family SUVs and estates popular in the borough, and we offer "
            "same-day fitting seven days a week with no garage visit needed."
        ),
        'faq': [
            ("Which postcodes in Bexley do you serve?",
             "We cover DA1, DA5, DA6, DA7, DA14, DA15, DA16, DA17, and SE2, "
             "reaching Bexleyheath, Sidcup, Welling, Crayford, Erith, and all surrounding areas."),
            ("Can you reach me if my tyre fails on the A2?",
             "Yes. The A2 is a key road through Bexley and we respond to roadside "
             "callouts along it frequently. Our average arrival time is around 20 minutes."),
            ("Do you fit run-flat tyres in Bexley?",
             "Yes. We carry run-flat tyres for a wide range of vehicles and can fit them "
             "at your home, workplace, or on the roadside anywhere in Bexley."),
            ("Is same-day mobile tyre fitting available in Bexley?",
             "Yes. Same-day fitting is available seven days a week. Emergency cover "
             "operates 24 hours a day throughout the borough."),
            ("How do I book a mobile tyre fitter in Bexley?",
             "You can book online in under 60 seconds with a 10 pound deposit, or call us "
             "directly. We confirm your appointment and dispatch the nearest available fitter."),
        ],
    },
    'brent': {
        'name': 'Brent',
        'postcodes': ['HA0', 'HA9', 'NW2', 'NW6', 'NW10'],
        'intro': (
            "Brent is one of North-West London's most culturally diverse boroughs, "
            "encompassing well-known neighbourhoods from Wembley and Harlesden to "
            "Kilburn and Cricklewood. The borough sees constant traffic around Wembley "
            "stadium and along the North Circular A406 and A40, which carry thousands "
            "of vehicles through the area every day. Brent is also a densely populated "
            "borough where on-street parking is the norm, making mobile tyre fitting "
            "a practical and popular choice."
        ),
        'coverage': (
            "Our mobile tyre fitters serve all of Brent, including Wembley, Wembley Park, "
            "Harlesden, Willesden, Kilburn, Cricklewood, Kingsbury, Sudbury, "
            "Kensal Rise, and Neasden. Postcodes covered include HA0, HA9, NW2, NW6, "
            "and NW10. We reach you at home on a residential street or on a main road "
            "within approximately 20 minutes."
        ),
        'why_us': (
            "Brent's dense streets and busy roads mean tyre problems can happen at any "
            "time. FixMyTyreNow provides a fast, professional response with no need to "
            "drive to a garage. Our fitters carry a broad range of tyre sizes to cover "
            "the diverse mix of vehicles in Brent, from small city cars to large SUVs. "
            "We offer emergency 24/7 cover and same-day appointments every day of the week."
        ),
        'faq': [
            ("Which parts of Brent do you cover?",
             "We cover all of Brent including Wembley, Harlesden, Willesden, Kilburn, "
             "Cricklewood, Kingsbury, and Neasden. Postcodes include HA0, HA9, NW2, NW6, and NW10."),
            ("Can you fit tyres near Wembley Stadium on event days?",
             "Yes. We cover the entire Wembley area including on and around event days. "
             "Call or book online and we will come directly to your location."),
            ("How long will the fitter take to arrive in Brent?",
             "Our average arrival time across Brent is under 20 minutes. We dispatch "
             "the nearest available technician to your exact location."),
            ("Do you offer emergency tyre replacement at night in Brent?",
             "Yes. Emergency tyre replacement is available 24 hours a day throughout Brent. "
             "Call us any time and a fitter will be on the way."),
            ("Can you come to me at my home in Kilburn or Cricklewood?",
             "Absolutely. We come to residential addresses across the borough, including "
             "Kilburn, Cricklewood, Willesden, and all other Brent neighbourhoods."),
        ],
    },
    'bromley': {
        'name': 'Bromley',
        'postcodes': ['BR1', 'BR2', 'BR3', 'BR4', 'BR5', 'BR6', 'BR7', 'SE20'],
        'intro': (
            "Bromley is the largest London borough by area, covering a wide stretch of "
            "South-East London from Beckenham and Penge in the north to the rural outskirts "
            "of Orpington and Biggin Hill in the south. The borough has a strong commuter "
            "population and excellent road links via the A21 and A20, with the town centres "
            "of Bromley, Beckenham, Chislehurst, and West Wickham each serving distinct "
            "communities. The variety of urban and semi-rural roads means drivers cover "
            "longer distances than in many inner-London boroughs."
        ),
        'coverage': (
            "We serve the full extent of Bromley, including Bromley town centre, "
            "Beckenham, Penge, Orpington, Chislehurst, West Wickham, Hayes, "
            "Biggin Hill, Crystal Palace, and Anerley. Postcodes covered include "
            "BR1, BR2, BR3, BR4, BR5, BR6, BR7, and SE20. Whether you are in the "
            "town centre or a quieter residential road, we reach you within around 20 minutes."
        ),
        'why_us': (
            "As London's largest borough, Bromley presents unique coverage challenges "
            "that our mobile service handles with ease. We carry a comprehensive range "
            "of tyre sizes to suit the varied vehicle types driven across the borough, "
            "from compact town cars to larger family estates common on Bromley's wider "
            "suburban roads. Same-day and emergency cover is available seven days a week."
        ),
        'faq': [
            ("Do you cover the whole of Bromley including Orpington and Biggin Hill?",
             "Yes. We cover the full borough of Bromley from Penge and Beckenham in "
             "the north to Orpington and Biggin Hill in the south. All BR and SE20 postcodes are served."),
            ("Can you help if my tyre fails on the A21?",
             "Yes. The A21 is a main route through Bromley and we respond to roadside "
             "callouts along it regularly. Our fitters typically arrive within 20 minutes."),
            ("Is mobile tyre fitting available in Chislehurst and West Wickham?",
             "Yes. We cover all parts of Bromley, including Chislehurst, West Wickham, "
             "Hayes, and all surrounding residential areas."),
            ("Do you offer weekend tyre fitting in Bromley?",
             "Yes. We operate seven days a week including weekends and bank holidays, "
             "with emergency cover available 24 hours a day."),
            ("What tyre brands do you stock?",
             "We stock a full range of tyre brands including budget, mid-range, and "
             "premium options. Our fitters carry the most popular sizes for vehicles "
             "driven in Bromley."),
        ],
    },
    'camden': {
        'name': 'Camden',
        'postcodes': ['NW1', 'NW3', 'NW5', 'WC1', 'WC2'],
        'intro': (
            "Camden is one of central London's most distinctive boroughs, encompassing "
            "the iconic Camden Market, the elegant residential streets of Hampstead and "
            "Belsize Park, and the academic institutions of Bloomsbury. It is a densely "
            "populated, vibrant area with a constant flow of vehicles on major routes "
            "including the A1 Archway Road, A400, and the inner ring roads. "
            "Finding a garage in Camden can be difficult and expensive, making "
            "on-location mobile tyre fitting the logical choice for most drivers."
        ),
        'coverage': (
            "Our mobile tyre fitters cover all of Camden, including Camden Town, "
            "Hampstead, Belsize Park, Kentish Town, Bloomsbury, Holborn, Kilburn, "
            "Primrose Hill, and Swiss Cottage. Postcodes served include NW1, NW3, "
            "NW5, WC1, and WC2. We come to your exact location in under 20 minutes, "
            "saving you the difficulty of finding and travelling to a garage."
        ),
        'why_us': (
            "In a borough as busy and well-connected as Camden, tyre problems rarely "
            "come at a convenient time. FixMyTyreNow resolves the issue wherever you "
            "are, whether you are parked near the canal in Primrose Hill, outside "
            "an office in Bloomsbury, or stuck on the A1. Our fitters are experienced "
            "with central London parking restrictions and arrive with everything needed "
            "to complete the job on the spot."
        ),
        'faq': [
            ("Can you come to central Camden if parking is restricted?",
             "Yes. Our fitters are familiar with Camden's parking restrictions and "
             "controlled zones. We come to your exact location and work within "
             "whatever space is available."),
            ("Do you serve Hampstead and Belsize Park?",
             "Yes. We cover all of Camden including Hampstead, Belsize Park, "
             "Primrose Hill, Kentish Town, and all surrounding areas."),
            ("How quickly can you reach me near Camden Market?",
             "Our average arrival time across Camden is under 20 minutes. "
             "We dispatch the nearest available fitter to your exact location."),
            ("Is emergency tyre fitting available in Camden at night?",
             "Yes. Emergency tyre fitting is available 24 hours a day throughout Camden. "
             "Call us any time and we will send a fitter to you."),
            ("Do I need to move my car to a specific location for the fitting?",
             "No. We come to wherever your car is parked, including on residential "
             "streets, car parks, and workplace locations throughout Camden."),
        ],
    },
    'city-of-westminster': {
        'name': 'City of Westminster',
        'postcodes': ['W1', 'W2', 'WC1', 'WC2', 'SW1'],
        'intro': (
            "The City of Westminster is the historic and political heart of London, "
            "home to Buckingham Palace, the Houses of Parliament, Westminster Abbey, "
            "and some of the capital's most prestigious addresses. Its streets include "
            "the exclusive postcodes of Mayfair, Belgravia, and Knightsbridge alongside "
            "the busier areas of Soho, Fitzrovia, and Marylebone. Traffic in Westminster "
            "is constant and parking is tightly controlled, making mobile tyre fitting "
            "an essential service for residents and visitors alike."
        ),
        'coverage': (
            "We cover all of the City of Westminster, including Mayfair, Soho, "
            "Fitzrovia, Marylebone, Paddington, Bayswater, Pimlico, Victoria, "
            "Belgravia, Westminster, Covent Garden, and St James's. "
            "Postcodes served include W1, W2, WC1, WC2, and SW1. "
            "We navigate Westminster's one-way systems and parking zones to reach "
            "you at your exact location within approximately 20 minutes."
        ),
        'why_us': (
            "Westminster residents and drivers expect a premium level of service, "
            "and that is exactly what FixMyTyreNow provides. Our fitters are "
            "experienced in working within congestion charge zones and around "
            "Westminster's complex traffic management. We carry premium tyre brands "
            "as well as standard options, and complete every job to the highest "
            "standard without any need for you to leave your vehicle unattended."
        ),
        'faq': [
            ("Can you work within the Congestion Charge Zone in Westminster?",
             "Yes. Our mobile fitters are fully operational within the Congestion "
             "Charge Zone and ULEZ. We come to your location regardless of which "
             "zone you are in."),
            ("Do you cover Mayfair and Belgravia?",
             "Yes. We cover all of Westminster including Mayfair, Belgravia, "
             "Knightsbridge, Pimlico, Victoria, and all surrounding areas."),
            ("How long does a tyre fitting take in Westminster?",
             "Most fittings take 30 to 45 minutes from when our fitter arrives. "
             "We work efficiently to minimise any disruption in busy Westminster locations."),
            ("Can you fit tyres for luxury and premium vehicles?",
             "Yes. We stock tyres for a wide range of premium and luxury vehicles "
             "common in Westminster, including performance sizes and run-flat options."),
            ("Is there a 24-hour emergency tyre service in Westminster?",
             "Yes. Emergency tyre fitting is available around the clock throughout "
             "the City of Westminster. Call us any time."),
        ],
    },
    'croydon': {
        'name': 'Croydon',
        'postcodes': ['CR0', 'CR2', 'CR7', 'SE25'],
        'intro': (
            "Croydon is South London's largest commercial hub, with a busy town centre, "
            "major retail parks, and some of the best transport connections in Outer London. "
            "The borough stretches from the urban streets around East Croydon station "
            "south to the leafier suburbs of Purley, Coulsdon, and Sanderstead. "
            "Major roads including the A23 Brighton Road and A232 carry significant "
            "volumes of traffic through the area, and a large commuter population "
            "means tyres take a harder-than-average beating on Croydon's roads."
        ),
        'coverage': (
            "We cover all of Croydon, including Croydon town centre, Thornton Heath, "
            "Norbury, Selhurst, South Norwood, Addiscombe, Shirley, Purley, Coulsdon, "
            "Sanderstead, New Addington, and Kenley. Postcodes served include CR0, "
            "CR2, CR7, and SE25. Our mobile fitters reach all parts of the borough "
            "within approximately 20 minutes of your call."
        ),
        'why_us': (
            "Croydon drivers benefit from FixMyTyreNow's fast response and wide tyre "
            "stock. Whether you are stuck in traffic near East Croydon station or "
            "parked on a quiet residential road in Purley, our fitter comes to you "
            "and handles the job on the spot. We provide same-day and emergency "
            "cover throughout the borough, with no need to arrange transport to a garage."
        ),
        'faq': [
            ("Do you cover South Croydon, Purley, and Coulsdon?",
             "Yes. We cover the full extent of Croydon including Purley, Coulsdon, "
             "Sanderstead, South Croydon, and all surrounding areas within the borough."),
            ("Can you help with a tyre emergency on the A23?",
             "Yes. The A23 is a key route through Croydon and we regularly respond "
             "to roadside callouts along it. Our average arrival time is under 20 minutes."),
            ("Do you offer same-day tyre fitting in Croydon?",
             "Yes. Same-day fitting is available throughout Croydon seven days a "
             "week. Emergency cover operates 24 hours a day."),
            ("How do I book mobile tyre fitting in Croydon?",
             "Book online in under 60 seconds with a 10 pound deposit, or call us "
             "directly. We confirm your slot and send the nearest available fitter."),
            ("Can you fit tyres for vans and larger vehicles in Croydon?",
             "Yes. We stock tyres for a broad range of vehicle types, including "
             "light commercial vehicles and larger SUVs common in Croydon."),
        ],
    },
    'ealing': {
        'name': 'Ealing',
        'postcodes': ['W5', 'W7', 'W13', 'UB1', 'UB2'],
        'intro': (
            "Ealing is one of West London's most established and culturally rich boroughs, "
            "known for its leafy streets, vibrant town centres, and the famous studios "
            "that gave it the nickname the Queen of the Suburbs. From the upmarket "
            "restaurants and boutiques of Ealing Broadway to the lively markets of "
            "Southall, the borough serves a hugely diverse population. "
            "The A4020 Uxbridge Road is one of the busiest arterial roads in West London, "
            "running the entire length of the borough and seeing heavy tyre wear from "
            "the volume of daily traffic."
        ),
        'coverage': (
            "We cover all of Ealing, including Ealing Broadway, Southall, Hanwell, "
            "Greenford, Northolt, Perivale, West Ealing, Acton, and Norwood Green. "
            "Postcodes served include W5, W7, W13, UB1, and UB2. Our mobile fitters "
            "reach every part of the borough within approximately 20 minutes, "
            "whether you are on the A4020 or a quieter residential side street."
        ),
        'why_us': (
            "Ealing's mix of busy main roads and suburban streets means tyre issues "
            "can happen anywhere at any time. FixMyTyreNow provides a fast, "
            "convenient solution that comes directly to you. We carry a wide range "
            "of tyres to suit the diverse vehicle types across the borough, from "
            "small city cars to family SUVs and minivans. Same-day and emergency "
            "cover is available seven days a week across all of Ealing."
        ),
        'faq': [
            ("Do you cover Southall and Hanwell as well as Ealing Broadway?",
             "Yes. We cover the whole of Ealing, including Southall, Hanwell, "
             "Greenford, Northolt, Acton, and all other areas within the borough."),
            ("Can you respond to a tyre problem on the A4020 Uxbridge Road?",
             "Yes. The A4020 runs through the heart of Ealing and we regularly "
             "attend roadside callouts along it. We arrive in approximately 20 minutes."),
            ("Is same-day tyre fitting available in Ealing?",
             "Yes. Same-day appointments are available throughout Ealing every day "
             "of the week. For emergencies, we operate 24 hours a day."),
            ("How long does a mobile tyre fitting take in Ealing?",
             "Most fittings are completed within 30 to 45 minutes from when our "
             "fitter arrives at your location."),
            ("Do you need access to a garage or pit to fit tyres?",
             "No. Our fully equipped mobile vans carry all necessary equipment to "
             "fit and balance tyres at any location, including residential streets "
             "and car parks throughout Ealing."),
        ],
    },
    'enfield': {
        'name': 'Enfield',
        'postcodes': ['EN1', 'EN2', 'EN3', 'N9', 'N13', 'N14', 'N18', 'N21'],
        'intro': (
            "Enfield is a large North London borough with a character that shifts "
            "from the traditional market town of Enfield Town in its centre to the "
            "leafy residential streets of Winchmore Hill and Grange Park, and the "
            "more industrial areas of Ponders End and Edmonton to the south. "
            "The A10 Great Cambridge Road is the main arterial route through the "
            "borough and one of the busiest roads in North London, making Enfield "
            "a high-traffic area where tyre wear and punctures are everyday occurrences."
        ),
        'coverage': (
            "We cover the entire borough of Enfield, including Enfield Town, "
            "Edmonton, Palmers Green, Winchmore Hill, Southgate, Grange Park, "
            "Ponders End, Waltham Cross, and Forty Hill. Postcodes served include "
            "EN1, EN2, EN3, N9, N13, N14, N18, and N21. Our mobile fitters reach "
            "you at any location in the borough within approximately 20 minutes."
        ),
        'why_us': (
            "Enfield residents rely on their cars for daily commuting and local travel, "
            "and a flat tyre can cause significant disruption. FixMyTyreNow eliminates "
            "that disruption by coming directly to you. Our fitters know the local roads "
            "from the A10 through to the quieter streets of Winchmore Hill, and we "
            "carry a wide stock of tyres to cover the full range of vehicles in the borough."
        ),
        'faq': [
            ("Which postcodes in Enfield do you serve?",
             "We serve EN1, EN2, EN3, N9, N13, N14, N18, and N21, covering "
             "all of Enfield from Edmonton in the south to Grange Park and Enfield Town."),
            ("Can you reach me on the A10 Great Cambridge Road?",
             "Yes. The A10 is a key route through Enfield and we respond to "
             "roadside callouts along it regularly. Our average arrival time is around 20 minutes."),
            ("Do you cover the quieter residential areas like Winchmore Hill?",
             "Yes. We cover all of Enfield including Winchmore Hill, Grange Park, "
             "Southgate, Palmers Green, and all other residential areas."),
            ("Is mobile tyre fitting available at weekends in Enfield?",
             "Yes. We operate seven days a week including weekends and bank holidays, "
             "with 24-hour emergency cover throughout Enfield."),
            ("How do I book a tyre fitting in Enfield?",
             "You can book online with a 10 pound deposit or call us directly. "
             "We confirm your booking and dispatch the nearest available fitter."),
        ],
    },
    'greenwich': {
        'name': 'Greenwich',
        'postcodes': ['SE3', 'SE7', 'SE9', 'SE10', 'SE18'],
        'intro': (
            "Greenwich is a South-East London borough with a remarkable history, "
            "home to the Royal Observatory, the Cutty Sark, and the National Maritime "
            "Museum. Beyond its tourist landmarks, Greenwich is a large and varied "
            "borough covering the riverside areas of Woolwich and Charlton, "
            "the leafy residential streets of Eltham and Kidbrooke, and the "
            "suburban roads of Welling and Plumstead. The A2 Rochester Way and "
            "A206 carry heavy traffic through the borough, connecting it to the "
            "Dartford Crossing and central London."
        ),
        'coverage': (
            "We cover all of Greenwich, including Greenwich town, Woolwich, Charlton, "
            "Eltham, Kidbrooke, Plumstead, Abbey Wood, Thamesmead, and Blackheath. "
            "Postcodes served include SE3, SE7, SE9, SE10, and SE18. Our fitters "
            "reach every part of the borough within approximately 20 minutes, "
            "from the riverside attractions of Greenwich to the residential streets of Eltham."
        ),
        'why_us': (
            "Greenwich's mix of heritage streets, riverside roads, and suburban "
            "avenues creates varied driving conditions that can affect tyre wear. "
            "FixMyTyreNow provides a fast response to tyre problems anywhere in "
            "the borough. We carry stock to cover the wide range of vehicle types "
            "in Greenwich, and our fitters are experienced with the local road network. "
            "Same-day and emergency cover is available every day of the year."
        ),
        'faq': [
            ("Do you cover Woolwich, Eltham, and Charlton?",
             "Yes. We cover all of Greenwich, including Woolwich, Eltham, Charlton, "
             "Kidbrooke, Plumstead, Thamesmead, and all surrounding areas."),
            ("Can you help if my tyre fails on the A2?",
             "Yes. The A2 runs through Greenwich and we regularly attend roadside "
             "callouts along it. Our average arrival time is under 20 minutes."),
            ("Is there a 24-hour emergency tyre service in Greenwich?",
             "Yes. Emergency tyre fitting is available around the clock throughout "
             "the borough. Call us any time and we will dispatch a fitter immediately."),
            ("Do you offer tyre fitting near the Thames Barrier?",
             "Yes. We cover the riverside areas of Thamesmead and Woolwich, "
             "and can reach locations near the Thames Barrier and surrounding industrial areas."),
            ("How quickly can you reach Eltham?",
             "Our average arrival time across Greenwich, including Eltham, is "
             "under 20 minutes from your call."),
        ],
    },
    'hackney': {
        'name': 'Hackney',
        'postcodes': ['E2', 'E5', 'E8', 'E9', 'N16'],
        'intro': (
            "Hackney is one of East London's most dynamic and creative boroughs, "
            "encompassing the trendy streets of Shoreditch and Dalston, the open "
            "spaces of Victoria Park and London Fields, and the diverse communities "
            "of Stoke Newington and Homerton. It is a densely populated borough "
            "with a busy road network including the A10 Kingsland Road and A107. "
            "Parking in Hackney is competitive, and with many residents relying on "
            "street parking, a flat tyre can quickly become a complicated problem."
        ),
        'coverage': (
            "We cover all of Hackney, including Shoreditch, Dalston, Stoke Newington, "
            "Hackney Central, Homerton, Clapton, London Fields, Victoria Park, "
            "and Haggerston. Postcodes served include E2, E5, E8, E9, and N16. "
            "Our fitters navigate Hackney's busy streets and reach your location "
            "within approximately 20 minutes, working around on-street parking wherever needed."
        ),
        'why_us': (
            "In a borough as busy as Hackney, waiting at a garage is time no one "
            "can afford to spare. FixMyTyreNow sends a fitter directly to where your "
            "car is parked, whether that is a residential street in Stoke Newington "
            "or a side road in Shoreditch. We cover all common tyre sizes and offer "
            "same-day appointments and round-the-clock emergency cover every day of the week."
        ),
        'faq': [
            ("Do you cover Shoreditch and Dalston?",
             "Yes. We cover all of Hackney including Shoreditch, Dalston, Stoke Newington, "
             "Hackney Central, Homerton, and Clapton."),
            ("Can you come to a residential street in Hackney?",
             "Yes. We come to any residential street, car park, or roadside location "
             "throughout Hackney. You do not need to move your car to a specific spot."),
            ("How quickly can a mobile tyre fitter reach me in Hackney?",
             "Our average arrival time across Hackney is under 20 minutes. "
             "We dispatch the nearest available fitter to your exact address."),
            ("Is emergency tyre fitting available overnight in Hackney?",
             "Yes. We operate 24 hours a day throughout Hackney. "
             "Call us any time and a fitter will be with you."),
            ("Do you offer puncture repair as well as full tyre replacement in Hackney?",
             "Yes. We offer puncture repair from 25 pounds as well as full tyre "
             "replacement. Our fitter will assess the damage and recommend the best option."),
        ],
    },
    'hammersmith-and-fulham': {
        'name': 'Hammersmith and Fulham',
        'postcodes': ['W6', 'W12', 'SW6'],
        'intro': (
            "Hammersmith and Fulham is a West London borough with a distinctly "
            "riverside character, stretching from the Thames towpaths of Hammersmith "
            "and Fulham in the south to the busy commercial stretch of Shepherd's Bush "
            "in the north. The borough is home to a young professional population "
            "and sees substantial traffic on the A4 Great West Road, A316, and "
            "around the Hammersmith gyratory, one of West London's busiest junctions."
        ),
        'coverage': (
            "We cover all of Hammersmith and Fulham, including Hammersmith, Fulham, "
            "Shepherd's Bush, Parsons Green, Barons Court, Brook Green, and Ravenscourt Park. "
            "Postcodes served include W6, W12, and SW6. Our mobile fitters know "
            "the local road network well and reach your location within approximately "
            "20 minutes, including during busy rush-hour periods."
        ),
        'why_us': (
            "Hammersmith and Fulham residents increasingly prefer mobile services "
            "over visits to traditional garages. FixMyTyreNow fits tyres at your "
            "home, workplace, or roadside location without requiring you to arrange "
            "alternative transport. We carry a strong stock of the popular tyre "
            "sizes for hatchbacks and SUVs common in the borough, and we offer "
            "same-day and 24-hour emergency cover throughout."
        ),
        'faq': [
            ("Do you cover Fulham, Shepherd's Bush, and Hammersmith?",
             "Yes. We cover the full borough including Hammersmith, Fulham, "
             "Shepherd's Bush, Parsons Green, Barons Court, and Brook Green."),
            ("Can you come near the Hammersmith roundabout?",
             "Yes. Our fitters are familiar with the Hammersmith area and can "
             "reach locations around the gyratory and nearby streets quickly."),
            ("How long does a mobile tyre fitting take?",
             "Most fittings take 30 to 45 minutes from when our fitter arrives. "
             "We carry balancing equipment and pressure gauges to complete every job on the spot."),
            ("Is same-day tyre fitting available in Hammersmith and Fulham?",
             "Yes. Same-day appointments are available every day of the week. "
             "For urgent needs, emergency cover is available 24 hours a day."),
            ("Do you work on the A4 and A316 if I break down there?",
             "Yes. We respond to roadside callouts on the A4, A316, and other major "
             "roads through the borough. Our average arrival time is under 20 minutes."),
        ],
    },
    'haringey': {
        'name': 'Haringey',
        'postcodes': ['N4', 'N8', 'N15', 'N17', 'N22'],
        'intro': (
            "Haringey is a diverse North London borough that spans from the affluent "
            "streets of Muswell Hill and Crouch End in the west to the busier "
            "commercial areas of Tottenham and Wood Green in the east. "
            "The A10 Tottenham High Road is one of the main arteries of the borough "
            "and sees constant traffic, particularly around match days at the "
            "Tottenham Hotspur Stadium in N17. Haringey's mix of residential side "
            "streets and busy main roads creates an environment where tyre issues "
            "are a frequent and unpredictable occurrence."
        ),
        'coverage': (
            "We cover all of Haringey, including Tottenham, Wood Green, Hornsey, "
            "Muswell Hill, Crouch End, Finsbury Park, Stroud Green, Turnpike Lane, "
            "and Noel Park. Postcodes served include N4, N8, N15, N17, and N22. "
            "Our fitters reach every part of the borough within approximately 20 minutes, "
            "including the areas around the Tottenham Hotspur Stadium."
        ),
        'why_us': (
            "Haringey drivers benefit from a mobile tyre service that understands "
            "the borough's varied geography. Whether you live in a quiet street in "
            "Muswell Hill or drive regularly along the A10 through Tottenham, "
            "FixMyTyreNow sends a fitter directly to you. We carry stock for a "
            "wide range of vehicle types and offer same-day and emergency cover "
            "seven days a week."
        ),
        'faq': [
            ("Do you cover Tottenham, Wood Green, and Muswell Hill?",
             "Yes. We cover all of Haringey including Tottenham, Wood Green, Muswell Hill, "
             "Crouch End, Hornsey, Finsbury Park, and all surrounding areas."),
            ("Can you respond to a breakdown on the A10 Tottenham High Road?",
             "Yes. The A10 is a key route through Haringey and we attend roadside "
             "callouts along it regularly. Our average arrival time is under 20 minutes."),
            ("Is mobile tyre fitting available near the Tottenham Hotspur Stadium?",
             "Yes. We cover the N17 area including roads around the Tottenham Hotspur "
             "Stadium. We operate on match days and throughout the week."),
            ("How do I book emergency tyre fitting in Haringey?",
             "Call us directly or book online. We dispatch a fitter immediately "
             "and operate 24 hours a day throughout Haringey."),
            ("What tyre services do you offer in Haringey?",
             "We offer emergency tyre replacement, standard tyre fitting, puncture "
             "repair, wheel balancing, and run-flat tyre replacement across all of Haringey."),
        ],
    },
    'harrow': {
        'name': 'Harrow',
        'postcodes': ['HA1', 'HA2', 'HA3', 'HA7'],
        'intro': (
            "Harrow is a suburban North-West London borough best known for the "
            "hilltop landmark of Harrow-on-the-Hill and its prestigious school. "
            "The borough has a large and diverse population, with busy town centres "
            "at Harrow, Wealdstone, and Kenton, and quieter residential streets "
            "spreading through Pinner, Stanmore, and Hatch End. "
            "The A404 Harrow Road and A409 are the main arterial routes, "
            "carrying significant commuter traffic towards central London daily."
        ),
        'coverage': (
            "We cover all of Harrow, including Harrow town centre, Harrow-on-the-Hill, "
            "Wealdstone, Kenton, Pinner, Stanmore, Hatch End, Queensbury, "
            "and Rayners Lane. Postcodes served include HA1, HA2, HA3, and HA7. "
            "Our mobile fitters reach every part of the borough in approximately 20 minutes, "
            "ready to fit your tyre at home, work, or on the roadside."
        ),
        'why_us': (
            "Harrow's suburban character means most residents depend heavily on "
            "their car for daily travel. FixMyTyreNow provides the reassurance of "
            "a fast, professional tyre fitting service that comes to you. "
            "Whether you are in Pinner or Wealdstone, our fitters arrive quickly "
            "with the right tyres in stock. We offer same-day service every day "
            "and 24-hour emergency cover across the whole borough."
        ),
        'faq': [
            ("Which postcodes in Harrow do you cover?",
             "We cover HA1, HA2, HA3, and HA7, serving Harrow town, Wealdstone, "
             "Kenton, Pinner, Stanmore, Hatch End, and all surrounding areas."),
            ("Do you offer tyre fitting in Pinner and Stanmore?",
             "Yes. We cover the full extent of Harrow including Pinner, Stanmore, "
             "Hatch End, and Queensbury."),
            ("Can you fit tyres at my home in Harrow?",
             "Yes. We come to your home, workplace, or any roadside location "
             "throughout Harrow. No garage visit is required."),
            ("How quickly can you reach me in Harrow?",
             "Our average arrival time across Harrow is under 20 minutes. "
             "We dispatch the nearest available fitter to your exact location."),
            ("Is emergency tyre replacement available overnight in Harrow?",
             "Yes. Our emergency service operates 24 hours a day throughout Harrow. "
             "Call us any time and a fitter will be dispatched to you."),
        ],
    },
    'havering': {
        'name': 'Havering',
        'postcodes': ['RM1', 'RM2', 'RM11', 'RM12', 'RM14'],
        'intro': (
            "Havering is the easternmost London borough, a largely suburban and "
            "semi-rural area that stretches from Romford in the west to the "
            "historic village of Upminster and the rural parish of Havering-atte-Bower "
            "to the east. Romford is the commercial heart of the borough with one of "
            "East London's busiest market towns, while quieter residential areas "
            "extend through Hornchurch, Emerson Park, and Cranham. "
            "The A12 and A127 Southend Arterial are the main roads through the borough, "
            "serving a large population of car-dependent commuters."
        ),
        'coverage': (
            "We cover all of Havering, including Romford, Hornchurch, Upminster, "
            "Emerson Park, Cranham, Harold Wood, Gidea Park, Harold Hill, "
            "Rainham, and Elm Park. Postcodes served include RM1, RM2, RM11, "
            "RM12, and RM14. Our fitters reach you throughout the borough within "
            "approximately 20 minutes of your call."
        ),
        'why_us': (
            "In Havering's largely car-dependent communities, a reliable mobile "
            "tyre service saves significant time and inconvenience. FixMyTyreNow "
            "comes to you wherever you are in the borough, from the busy streets "
            "around Romford market to the quiet roads of Upminster. We carry a "
            "strong range of tyre sizes to cover the popular family vehicles "
            "driven across Havering, and we offer same-day and emergency cover "
            "every day of the week."
        ),
        'faq': [
            ("Do you cover Upminster, Hornchurch, and Romford?",
             "Yes. We cover all of Havering including Romford, Hornchurch, Upminster, "
             "Emerson Park, Harold Wood, Gidea Park, Rainham, and all surrounding areas."),
            ("Can you help with a tyre breakdown on the A12 or A127?",
             "Yes. Both the A12 and A127 run through Havering and we regularly "
             "attend roadside callouts on these roads. Our fitters arrive in under 20 minutes."),
            ("Is same-day tyre fitting available in Havering?",
             "Yes. Same-day fitting is available throughout Havering seven days a week. "
             "Emergency cover operates 24 hours a day."),
            ("Do you service semi-rural areas like Havering-atte-Bower?",
             "Yes. We cover the full extent of the borough including the more rural "
             "eastern areas. Our fitters travel to all Havering postcodes."),
            ("How do I pay for mobile tyre fitting in Havering?",
             "You pay a 10 pound deposit at the time of booking, with the balance "
             "due when the fitter completes the job. We accept secure digital payments."),
        ],
    },
    'hillingdon': {
        'name': 'Hillingdon',
        'postcodes': ['UB3', 'UB4', 'UB8', 'UB9', 'UB10'],
        'intro': (
            "Hillingdon is West London's largest borough by area, home to Heathrow "
            "Airport and stretching west to the semi-rural areas of Uxbridge, "
            "Ruislip, and West Drayton. It is an exceptionally well-connected "
            "borough with the M4 and M25 motorways, the A40 Western Avenue, "
            "and the A4020 Uxbridge Road all passing through. "
            "The constant flow of airport-related traffic alongside resident "
            "commuters and commercial vehicles makes Hillingdon's roads some "
            "of the busiest in Outer West London."
        ),
        'coverage': (
            "We cover all of Hillingdon, including Uxbridge, Hayes, Ruislip, "
            "Northolt, West Drayton, Yiewsley, Harlington, Harmondsworth, "
            "Ickenham, and Cowley. Postcodes served include UB3, UB4, UB8, "
            "UB9, and UB10. Our mobile fitters reach every part of the borough "
            "within approximately 20 minutes, including locations close to Heathrow."
        ),
        'why_us': (
            "With Heathrow at its heart and major motorways crossing the borough, "
            "Hillingdon drivers face some of the most demanding tyre conditions "
            "in London. FixMyTyreNow provides rapid mobile tyre fitting wherever "
            "you are in the borough, with a broad range of tyre sizes for "
            "passenger cars, SUVs, and light commercial vehicles. We offer "
            "same-day service and 24-hour emergency cover seven days a week."
        ),
        'faq': [
            ("Do you cover areas near Heathrow Airport in Hillingdon?",
             "Yes. We cover the full borough including Hayes, West Drayton, Harlington, "
             "and Harmondsworth near Heathrow. We can reach airport vicinity locations."),
            ("Can you respond to a tyre problem on the M4 or A40?",
             "For safety reasons we cannot work on live motorways, but we can reach "
             "you at the nearest safe stopping point, service station, or junction "
             "and assist from there."),
            ("Do you serve Uxbridge and Ruislip?",
             "Yes. We cover all of Hillingdon including Uxbridge, Ruislip, Ickenham, "
             "Northolt, and all other areas within the borough."),
            ("Is emergency tyre fitting available 24 hours in Hillingdon?",
             "Yes. Emergency cover operates around the clock throughout Hillingdon. "
             "Call us any time for immediate dispatch."),
            ("How long does a tyre fitting take in Hillingdon?",
             "Most fittings take 30 to 45 minutes from when the fitter arrives. "
             "We also perform wheel balancing and pressure checks on the spot."),
        ],
    },
    'hounslow': {
        'name': 'Hounslow',
        'postcodes': ['TW3', 'TW4', 'TW5', 'TW13', 'W4'],
        'intro': (
            "Hounslow is a West London borough sitting directly beneath the Heathrow "
            "flight path, stretching from the riverside at Chiswick and Brentford "
            "in the east to Feltham and Hanworth in the west. It is a busy, "
            "multi-ethnic borough with strong commercial centres at Hounslow town "
            "and Isleworth, and popular residential areas at Chiswick and Gunnersbury. "
            "The A4 Great West Road and A316 Richmond Road are the main arterial "
            "routes, carrying heavy traffic through the borough at all hours."
        ),
        'coverage': (
            "We cover all of Hounslow, including Hounslow town centre, Chiswick, "
            "Brentford, Isleworth, Feltham, Hanworth, Heston, Cranford, "
            "and Bedfont. Postcodes served include TW3, TW4, TW5, TW13, and W4. "
            "Our mobile fitters reach every part of the borough within approximately "
            "20 minutes from your call."
        ),
        'why_us': (
            "Hounslow's position next to Heathrow and its major road corridors "
            "mean tyre problems can strike at the most inconvenient moments. "
            "FixMyTyreNow provides a mobile solution that comes to you, saving the "
            "time and cost of arranging transport to a garage. We carry a "
            "wide range of tyres for all vehicle types and offer same-day "
            "and emergency cover every day of the year."
        ),
        'faq': [
            ("Do you cover Chiswick, Brentford, and Feltham?",
             "Yes. We cover the full borough of Hounslow including Chiswick, "
             "Brentford, Isleworth, Feltham, Heston, and all surrounding areas."),
            ("Can you help with a tyre problem on the A4 or A316?",
             "Yes. Both the A4 and A316 are major routes through Hounslow and we "
             "respond to roadside callouts along them regularly."),
            ("Is same-day tyre fitting available in Hounslow?",
             "Yes. Same-day slots are available every day of the week, with "
             "24-hour emergency cover across the whole borough."),
            ("How far in advance do I need to book?",
             "For same-day bookings, simply call or book online and we will "
             "confirm availability. For emergencies, we respond immediately."),
            ("Do you fit tyres for airport taxi and minicab drivers in Hounslow?",
             "Yes. We service all types of vehicles including private hire vehicles. "
             "We carry tyre sizes common to taxi fleets and minicab operators."),
        ],
    },
    'islington': {
        'name': 'Islington',
        'postcodes': ['N1', 'N4', 'N5', 'N7', 'EC1'],
        'intro': (
            "Islington is an inner North London borough with a vibrant mix of "
            "Victorian terraces, boutique shops, and some of the capital's best "
            "restaurants and bars along Upper Street and Essex Road. "
            "It is a densely built borough where most residents park on the street "
            "and roads can be congested at all hours. The A1 runs through the "
            "borough from Kings Cross northwards through Holloway, and the "
            "Highbury and Finsbury Park areas are key residential hubs. "
            "Parking, traffic, and tight streets make mobile tyre fitting "
            "a highly practical choice in Islington."
        ),
        'coverage': (
            "We cover all of Islington, including Islington village, Angel, "
            "Holloway, Highbury, Finsbury Park, Canonbury, Barnsbury, Clerkenwell, "
            "and Farringdon. Postcodes served include N1, N4, N5, N7, and EC1. "
            "Our fitters navigate Islington's busy streets and reach you within "
            "approximately 20 minutes, working wherever your car is parked."
        ),
        'why_us': (
            "In Islington's tight, busy streets, a mobile tyre fitter is far more "
            "practical than a traditional garage. FixMyTyreNow sends a technician "
            "directly to your street, your office, or wherever you are parked. "
            "We are experienced with central London parking conditions and "
            "carry a full range of popular tyre sizes for the hatchbacks and "
            "city cars common in the borough. Same-day and 24-hour emergency "
            "cover is available throughout Islington."
        ),
        'faq': [
            ("Can you work on residential streets with parking restrictions in Islington?",
             "Yes. Our fitters are familiar with Islington's permit zones and "
             "parking restrictions. We assess the available space and complete "
             "the job wherever your car is legally parked."),
            ("Do you serve Angel, Highbury, and Holloway?",
             "Yes. We cover all of Islington including Angel, Highbury, Holloway, "
             "Finsbury Park, Canonbury, and all surrounding areas."),
            ("How fast can you reach me in Islington?",
             "Our average arrival time across Islington is under 20 minutes. "
             "We dispatch the nearest fitter to your exact location."),
            ("Is 24-hour emergency tyre fitting available in Islington?",
             "Yes. We operate around the clock throughout Islington. "
             "Call us at any hour and a fitter will be dispatched immediately."),
            ("What if I cannot find a space to leave my car in Islington?",
             "We can assess the best approach when we arrive. Our fitters are experienced "
             "in working within the constraints of central London parking."),
        ],
    },
    'kensington-and-chelsea': {
        'name': 'Kensington and Chelsea',
        'postcodes': ['W8', 'W10', 'W11', 'SW3', 'SW5', 'SW10'],
        'intro': (
            "Kensington and Chelsea is one of London's most prestigious boroughs, "
            "home to the Royal Borough of Chelsea, Notting Hill's vibrant streets, "
            "the cultural institutions of South Kensington, and the upmarket "
            "residential streets of Holland Park and Earls Court. "
            "It is a compact but exceptionally dense borough with constant traffic, "
            "premium residential addresses, and a high proportion of expensive and "
            "luxury vehicles. Roads including the A4 and A3220 carry significant "
            "through-traffic alongside local journeys."
        ),
        'coverage': (
            "We cover all of Kensington and Chelsea, including Chelsea, Notting Hill, "
            "South Kensington, Kensington, Holland Park, Earls Court, North Kensington, "
            "Knightsbridge, Brompton, and World's End. Postcodes served include "
            "W8, W10, W11, SW3, SW5, and SW10. Our fitters reach you anywhere "
            "in the borough within approximately 20 minutes."
        ),
        'why_us': (
            "Kensington and Chelsea drivers expect the highest standards of service, "
            "and FixMyTyreNow delivers. We carry premium tyre brands alongside "
            "standard options and are experienced in fitting tyres on luxury and "
            "high-performance vehicles. Our fitters work discreetly and efficiently "
            "at your location, with no need to transport your vehicle to a garage. "
            "Same-day and 24-hour emergency cover is available throughout the borough."
        ),
        'faq': [
            ("Do you fit tyres for luxury and high-performance cars in Kensington and Chelsea?",
             "Yes. We stock tyres for a wide range of premium and performance vehicles, "
             "including low-profile and run-flat options for luxury cars common in the borough."),
            ("Do you cover Notting Hill and Chelsea?",
             "Yes. We cover the entire borough including Notting Hill, Chelsea, "
             "South Kensington, Kensington, Earls Court, and all surrounding areas."),
            ("Can you work within the Congestion Charge Zone?",
             "Yes. Our fitters are fully operational within the CCZ and ULEZ. "
             "We come to your exact location regardless of the zone."),
            ("How quickly can you reach me in Kensington and Chelsea?",
             "Our average arrival time across the borough is under 20 minutes. "
             "We dispatch the nearest available fitter immediately."),
            ("Is there an emergency tyre service available in Kensington and Chelsea?",
             "Yes. Emergency tyre fitting operates 24 hours a day throughout the borough. "
             "Call us any time and we will respond immediately."),
        ],
    },
    'kingston-upon-thames': {
        'name': 'Kingston upon Thames',
        'postcodes': ['KT1', 'KT2', 'KT3'],
        'intro': (
            "Kingston upon Thames is a historic South-West London borough with one "
            "of London's oldest market towns at its centre. The town is a busy retail "
            "and leisure destination with good transport links via the A3 and A308, "
            "and the River Thames provides a beautiful backdrop to the residential "
            "streets and parks of Kingston, Surbiton, and New Malden. "
            "The borough has a large commuter population who drive regularly "
            "into and through the A3 corridor towards central London."
        ),
        'coverage': (
            "We cover all of Kingston upon Thames, including Kingston town centre, "
            "Surbiton, New Malden, Tolworth, Chessington, Berrylands, and Canbury. "
            "Postcodes served include KT1, KT2, and KT3. Our mobile fitters reach "
            "every part of the borough within approximately 20 minutes, whether "
            "you are parked in the town centre or on a residential street in Surbiton."
        ),
        'why_us': (
            "Kingston upon Thames residents benefit from a mobile tyre service that "
            "comes to them, saving the time and inconvenience of a garage visit in "
            "a busy town centre area. FixMyTyreNow carries the popular tyre sizes "
            "for the family cars and SUVs driven across the borough and offers "
            "same-day fitting and 24-hour emergency cover throughout Kingston upon Thames."
        ),
        'faq': [
            ("Do you cover Surbiton, New Malden, and Tolworth?",
             "Yes. We cover the full borough of Kingston upon Thames including "
             "Kingston town, Surbiton, New Malden, Tolworth, Chessington, and Berrylands."),
            ("Can you help with a tyre problem on the A3?",
             "Yes. The A3 runs through Kingston upon Thames and we respond to "
             "roadside callouts along it. Our average arrival time is under 20 minutes."),
            ("Is same-day tyre fitting available in Kingston?",
             "Yes. Same-day appointments are available seven days a week throughout "
             "the borough. Emergency cover operates 24 hours a day."),
            ("Do you offer wheel balancing in Kingston upon Thames?",
             "Yes. Wheel balancing is available from 15 pounds per wheel. Our mobile "
             "units carry portable balancing equipment for on-location service."),
            ("How do I book mobile tyre fitting in Kingston?",
             "Book online in under 60 seconds with a 10 pound deposit, or call us "
             "directly. We confirm your slot and dispatch the nearest fitter."),
        ],
    },
    'lambeth': {
        'name': 'Lambeth',
        'postcodes': ['SE1', 'SE11', 'SE24', 'SW2', 'SW4', 'SW9'],
        'intro': (
            "Lambeth is a vibrant South London borough running along the south bank "
            "of the Thames from Waterloo and Lambeth North in the north to the "
            "residential streets of Streatham Hill and Tulse Hill in the south. "
            "Its neighbourhoods include the internationally known Brixton, the "
            "trendy Clapham, the cultural Stockwell, and the regenerating "
            "South Bank and Vauxhall areas. The A23 Brixton Road and A3 carry "
            "heavy traffic through the borough and roads around Brixton station "
            "and Clapham Junction are consistently congested."
        ),
        'coverage': (
            "We cover all of Lambeth, including Brixton, Clapham, Stockwell, Vauxhall, "
            "Waterloo, Lambeth North, Herne Hill, Tulse Hill, West Norwood, "
            "and Streatham. Postcodes served include SE1, SE11, SE24, SW2, SW4, and SW9. "
            "Our fitters navigate Lambeth's busy roads and reach you within "
            "approximately 20 minutes of your call."
        ),
        'why_us': (
            "Lambeth's busy streets and limited garage options make mobile tyre "
            "fitting the practical choice for most drivers in the borough. "
            "FixMyTyreNow sends a fitter to wherever your car is, whether that is "
            "a residential road in Brixton, a car park in Clapham, or the roadside "
            "on the A23. We offer same-day service and 24-hour emergency cover "
            "throughout Lambeth every day of the year."
        ),
        'faq': [
            ("Do you cover Brixton, Clapham, and Stockwell?",
             "Yes. We cover all of Lambeth including Brixton, Clapham, Stockwell, "
             "Vauxhall, Herne Hill, Tulse Hill, West Norwood, and Streatham."),
            ("Can you respond to a breakdown on the A23 in Lambeth?",
             "Yes. The A23 is one of Lambeth's main roads and we attend roadside "
             "callouts along it regularly. Our average arrival time is under 20 minutes."),
            ("Is emergency tyre fitting available at night in Lambeth?",
             "Yes. Emergency cover operates 24 hours a day throughout Lambeth. "
             "Call us any time and a fitter will be on the way to you."),
            ("Can you come to a flat in a residential street in Brixton?",
             "Yes. We come to any residential address throughout Lambeth. "
             "You do not need to arrange to meet us at a specific location."),
            ("Do you offer puncture repair in Lambeth?",
             "Yes. Puncture repair is available from 25 pounds. Our fitter will "
             "assess whether the tyre is repairable or needs to be replaced."),
        ],
    },
    'lewisham': {
        'name': 'Lewisham',
        'postcodes': ['SE4', 'SE6', 'SE12', 'SE13', 'SE14', 'SE23'],
        'intro': (
            "Lewisham is a South-East London borough with a diverse and energetic "
            "character, stretching from the urban streets around Lewisham station "
            "in the north to the green spaces of Hilly Fields and Sydenham Hill "
            "Wood in the south. Key neighbourhoods include Catford, Forest Hill, "
            "Lee Green, Ladywell, and Brockley, each with its own distinct identity. "
            "The A21 Lewisham High Street and A205 South Circular are the main "
            "routes through the borough, carrying heavy traffic throughout the day."
        ),
        'coverage': (
            "We cover all of Lewisham, including Lewisham town centre, Catford, "
            "Forest Hill, Lee Green, Ladywell, Brockley, Sydenham, Bellingham, "
            "and Hither Green. Postcodes served include SE4, SE6, SE12, SE13, "
            "SE14, and SE23. Our mobile fitters reach every part of the borough "
            "within approximately 20 minutes of your call."
        ),
        'why_us': (
            "Lewisham residents benefit from FixMyTyreNow's fast, reliable mobile "
            "service that covers the full borough without requiring a garage visit. "
            "Whether you are parked on a side street in Catford or on the A205 "
            "South Circular, we come to you. We carry a full range of popular "
            "tyre sizes and offer same-day fitting and 24-hour emergency cover "
            "seven days a week across all of Lewisham."
        ),
        'faq': [
            ("Do you cover Catford, Forest Hill, and Lee Green?",
             "Yes. We cover all of Lewisham including Catford, Forest Hill, Lee Green, "
             "Ladywell, Brockley, Sydenham, Bellingham, and Hither Green."),
            ("Can you help if my tyre fails on the A205 South Circular?",
             "Yes. The A205 runs through Lewisham and we respond to roadside callouts "
             "along it regularly. Our average arrival time is under 20 minutes."),
            ("Is same-day tyre fitting available in Lewisham?",
             "Yes. Same-day appointments are available throughout the borough seven "
             "days a week. Emergency cover operates 24 hours a day."),
            ("How do I book a mobile tyre fitter in Lewisham?",
             "Book online in under 60 seconds with a 10 pound deposit, or call us "
             "directly. We confirm your slot and send the nearest available fitter."),
            ("Do you offer wheel balancing in Lewisham?",
             "Yes. Wheel balancing is available from 15 pounds per wheel as part of "
             "our on-location mobile service across Lewisham."),
        ],
    },
    'merton': {
        'name': 'Merton',
        'postcodes': ['SW19', 'SW20', 'CR4', 'SM4'],
        'intro': (
            "Merton is a South London borough famous worldwide for Wimbledon and "
            "its tennis championships, but it is also home to the busy market town "
            "of Mitcham, the regenerating Colliers Wood, and the residential avenues "
            "of Morden and Raynes Park. The borough has excellent road links via the "
            "A24 Merton High Street and A217, connecting it to the A3 Kingston "
            "bypass and central London. Merton's mix of urban and suburban roads "
            "generates steady demand for reliable tyre services."
        ),
        'coverage': (
            "We cover all of Merton, including Wimbledon, South Wimbledon, "
            "Mitcham, Morden, Colliers Wood, Raynes Park, and Merton Park. "
            "Postcodes served include SW19, SW20, CR4, and SM4. Our mobile "
            "fitters reach every part of the borough within approximately 20 "
            "minutes, ready to fit your tyre at home, at work, or on the roadside."
        ),
        'why_us': (
            "Merton drivers trust FixMyTyreNow for a fast response and professional "
            "service that comes to them. Whether you are near Wimbledon town centre "
            "or parked on a residential road in Morden, our fitters arrive quickly "
            "with the right tyres in stock. We offer same-day and emergency cover "
            "throughout the borough every day of the week, including during "
            "the Wimbledon tennis fortnight."
        ),
        'faq': [
            ("Do you cover Wimbledon, Mitcham, and Morden?",
             "Yes. We cover all of Merton including Wimbledon, South Wimbledon, "
             "Mitcham, Morden, Colliers Wood, Raynes Park, and Merton Park."),
            ("Can you respond to a tyre problem on the A24 or A217?",
             "Yes. Both roads run through Merton and we attend roadside callouts "
             "along them regularly. Our average arrival time is under 20 minutes."),
            ("Is mobile tyre fitting available during the Wimbledon tournament?",
             "Yes. We operate throughout the year including during the Wimbledon "
             "tennis fortnight. We cover all roads in the SW19 area."),
            ("How quickly can you reach me in Merton?",
             "Our average arrival time across Merton is under 20 minutes. "
             "We dispatch the nearest available fitter to your exact location."),
            ("Is emergency tyre replacement available overnight in Merton?",
             "Yes. Our emergency service operates 24 hours a day throughout Merton. "
             "Call us at any time and a fitter will be dispatched."),
        ],
    },
    'newham': {
        'name': 'Newham',
        'postcodes': ['E6', 'E7', 'E12', 'E13', 'E15', 'E16'],
        'intro': (
            "Newham is an East London borough that has undergone remarkable "
            "transformation since hosting the 2012 Olympic Games. Stratford is "
            "now a major retail and cultural hub, while West Ham, Forest Gate, "
            "and Plaistow remain vibrant residential communities. "
            "The borough has excellent road links via the A13 and A406 North "
            "Circular, and the ongoing development around the Olympic Park "
            "has brought significant new commercial and residential areas "
            "to what was once largely industrial land."
        ),
        'coverage': (
            "We cover all of Newham, including Stratford, West Ham, Forest Gate, "
            "Plaistow, Green Street, East Ham, Manor Park, Upton Park, Canning Town, "
            "and Custom House. Postcodes served include E6, E7, E12, E13, E15, and E16. "
            "Our mobile fitters reach every part of the borough within approximately "
            "20 minutes of your call."
        ),
        'why_us': (
            "Newham's rapidly changing landscape includes new residential developments, "
            "busy commercial roads, and a large working population that relies on "
            "vehicles for daily travel. FixMyTyreNow provides fast, reliable mobile "
            "tyre fitting across all of Newham, with a wide stock of tyre sizes "
            "to cover the full range of vehicles in the borough. Same-day "
            "and 24-hour emergency cover is available every day."
        ),
        'faq': [
            ("Do you cover Stratford, West Ham, and Forest Gate?",
             "Yes. We cover all of Newham including Stratford, West Ham, Forest Gate, "
             "Plaistow, East Ham, Manor Park, Canning Town, and all surrounding areas."),
            ("Can you help with a tyre emergency on the A13?",
             "Yes. The A13 runs through Newham and we attend roadside callouts "
             "along it regularly. Our average arrival time is under 20 minutes."),
            ("Is same-day tyre fitting available in Newham?",
             "Yes. Same-day slots are available every day of the week. "
             "Emergency cover operates 24 hours a day throughout Newham."),
            ("How do I book mobile tyre fitting in Newham?",
             "You can book online in under 60 seconds with a 10 pound deposit, "
             "or call us directly. We confirm your slot and dispatch the nearest fitter."),
            ("Do you offer tyre fitting near the Olympic Park in Stratford?",
             "Yes. We cover all of Stratford including the E15 postcode and "
             "areas around the Olympic Park."),
        ],
    },
    'redbridge': {
        'name': 'Redbridge',
        'postcodes': ['IG1', 'IG2', 'IG4', 'IG5', 'IG6', 'IG7', 'IG8'],
        'intro': (
            "Redbridge is a North-East London borough with a predominantly suburban "
            "character, stretching from the vibrant commercial centre of Ilford in "
            "the west to the more rural fringes of Hainault Forest in the east. "
            "Key neighbourhoods include Seven Kings, Goodmayes, Gants Hill, "
            "Wanstead, and Woodford Green, each with strong residential communities. "
            "The A12 Eastern Avenue and A406 North Circular are the main roads "
            "through the borough, connecting Redbridge to the City and the M11."
        ),
        'coverage': (
            "We cover all of Redbridge, including Ilford, Seven Kings, Goodmayes, "
            "Gants Hill, Wanstead, Woodford Green, South Woodford, Barkingside, "
            "Newbury Park, Hainault, and Chigwell Row. Postcodes served include "
            "IG1, IG2, IG4, IG5, IG6, IG7, and IG8. Our fitters reach every "
            "part of the borough within approximately 20 minutes."
        ),
        'why_us': (
            "Redbridge's suburban roads and commuter-heavy population make a reliable "
            "mobile tyre service invaluable. FixMyTyreNow provides fast response to "
            "both planned tyre replacements and emergency callouts across the borough, "
            "coming directly to your home, workplace, or roadside location. "
            "We carry stock for the popular family vehicles driven across Redbridge "
            "and offer same-day and 24-hour emergency cover every day."
        ),
        'faq': [
            ("Which parts of Redbridge do you serve?",
             "We cover all of Redbridge including Ilford, Seven Kings, Wanstead, "
             "Woodford Green, Gants Hill, Barkingside, Newbury Park, and Hainault."),
            ("Can you respond to a breakdown on the A12 Eastern Avenue?",
             "Yes. The A12 runs through Redbridge and we attend roadside callouts "
             "along it regularly. Our average arrival time is under 20 minutes."),
            ("Do you offer same-day tyre fitting in Redbridge?",
             "Yes. Same-day fitting is available throughout Redbridge seven days a week. "
             "Emergency cover operates 24 hours a day."),
            ("Can you come to my home in Wanstead or Woodford?",
             "Yes. We come to any residential address throughout Redbridge, including "
             "Wanstead, Woodford Green, South Woodford, and all surrounding areas."),
            ("What services do you offer in Redbridge?",
             "We offer emergency tyre replacement, standard tyre fitting, puncture "
             "repair, wheel balancing, and run-flat tyre replacement across all of Redbridge."),
        ],
    },
    'richmond-upon-thames': {
        'name': 'Richmond upon Thames',
        'postcodes': ['TW1', 'TW2', 'TW9', 'TW10', 'TW11'],
        'intro': (
            "Richmond upon Thames is a beautiful South-West London borough set "
            "along a sweeping stretch of the Thames, known for Richmond Park, "
            "Kew Gardens, Twickenham Stadium, and some of the finest riverside "
            "scenery in the capital. The borough has a prosperous, family-oriented "
            "population and excellent road connections via the A316 and A307. "
            "Its roads include a mix of busy town centre streets in Richmond "
            "and Twickenham and quieter residential roads through Ham, "
            "Petersham, and East Twickenham."
        ),
        'coverage': (
            "We cover all of Richmond upon Thames, including Richmond, Twickenham, "
            "Kew, East Twickenham, St Margarets, Ham, Petersham, Whitton, "
            "Teddington, and Hampton. Postcodes served include TW1, TW2, TW9, "
            "TW10, and TW11. Our mobile fitters reach every part of the borough "
            "within approximately 20 minutes, from the riverside to the park."
        ),
        'why_us': (
            "Richmond upon Thames residents expect and receive a high quality of "
            "service, and FixMyTyreNow delivers exactly that. We come to your "
            "home, workplace, or roadside location anywhere in the borough, "
            "with a range of premium and standard tyre options to suit the "
            "upmarket vehicles common in the area. Same-day and emergency "
            "cover is available throughout Richmond upon Thames every day of the week."
        ),
        'faq': [
            ("Do you cover Kew, Twickenham, and Richmond?",
             "Yes. We cover the full borough including Richmond, Twickenham, Kew, "
             "Ham, Petersham, Teddington, Hampton, and all surrounding areas."),
            ("Can you help near Richmond Park or Kew Gardens?",
             "Yes. We cover all roads in and around Richmond Park and Kew. "
             "Our fitters reach you at your exact location within 20 minutes."),
            ("Do you fit tyres for premium vehicles in Richmond upon Thames?",
             "Yes. We stock premium tyre brands and sizes for the luxury and "
             "performance vehicles common in Richmond upon Thames."),
            ("Is emergency tyre fitting available overnight in Richmond?",
             "Yes. Emergency tyre fitting operates 24 hours a day throughout "
             "the borough. Call us any time for an immediate response."),
            ("How do I book mobile tyre fitting in Richmond upon Thames?",
             "Book online in under 60 seconds with a 10 pound deposit, or call us "
             "directly. We confirm your slot and dispatch the nearest available fitter."),
        ],
    },
    'southwark': {
        'name': 'Southwark',
        'postcodes': ['SE1', 'SE5', 'SE15', 'SE17', 'SE21', 'SE22'],
        'intro': (
            "Southwark is a South London borough with an extraordinary range of "
            "character, from the world-famous attractions of the South Bank and "
            "Borough Market to the regenerated docklands of Bermondsey and the "
            "diverse communities of Peckham and Nunhead. "
            "The A2 Old Kent Road and A3 Brixton Road are major routes through "
            "the borough, carrying substantial volumes of both commuter and "
            "commercial traffic. Southwark's density and varied road network "
            "make it an area where mobile tyre fitting is consistently in demand."
        ),
        'coverage': (
            "We cover all of Southwark, including Bermondsey, Peckham, Nunhead, "
            "Dulwich, Forest Hill, Herne Hill, East Dulwich, Camberwell, "
            "Borough, and Waterloo. Postcodes served include SE1, SE5, SE15, "
            "SE17, SE21, and SE22. Our mobile fitters navigate Southwark's streets "
            "and reach you within approximately 20 minutes."
        ),
        'why_us': (
            "Southwark's busy streets and limited on-street parking in central "
            "areas make mobile tyre fitting the sensible choice. FixMyTyreNow "
            "sends a fitter directly to wherever your car is located, saving "
            "you the time and difficulty of reaching a traditional garage. "
            "We cover all of Southwark with same-day and 24-hour emergency "
            "service every day of the year."
        ),
        'faq': [
            ("Do you cover Peckham, Bermondsey, and Dulwich?",
             "Yes. We cover all of Southwark including Peckham, Bermondsey, "
             "Dulwich, East Dulwich, Camberwell, Nunhead, and all surrounding areas."),
            ("Can you respond to a breakdown on the A2 Old Kent Road?",
             "Yes. The A2 runs through Southwark and we regularly attend roadside "
             "callouts along it. Our average arrival time is under 20 minutes."),
            ("Is same-day tyre fitting available in Southwark?",
             "Yes. Same-day slots are available every day of the week throughout "
             "Southwark. Emergency cover operates 24 hours a day."),
            ("Can you fit tyres near London Bridge or Borough Market?",
             "Yes. We cover SE1 including the Borough Market and London Bridge areas, "
             "working within the constraints of central London parking."),
            ("Do you offer puncture repair in Southwark?",
             "Yes. Puncture repair is available from 25 pounds. Our fitter will "
             "assess the damage and advise whether repair or replacement is the best option."),
        ],
    },
    'sutton': {
        'name': 'Sutton',
        'postcodes': ['SM1', 'SM2', 'SM3', 'SM5', 'SM6'],
        'intro': (
            "Sutton is a South London borough with a pleasant, suburban character, "
            "centred on the busy market town of Sutton with its retail centre and "
            "transport links. Surrounding areas include the leafy streets of Cheam "
            "and North Cheam, the residential avenues of Carshalton and Wallington, "
            "and the quieter village of Beddington. "
            "The A217 Brighton Road and A240 are the main routes through the "
            "borough, carrying commuter traffic southbound towards the M25 "
            "and northbound towards Wimbledon and central London."
        ),
        'coverage': (
            "We cover all of Sutton, including Sutton town centre, Cheam, "
            "North Cheam, Carshalton, Wallington, Beddington, Belmont, "
            "and Woodmansterne. Postcodes served include SM1, SM2, SM3, SM5, and SM6. "
            "Our mobile fitters reach every part of the borough within approximately "
            "20 minutes from your call."
        ),
        'why_us': (
            "Sutton's family-friendly, car-dependent communities rely on "
            "FixMyTyreNow for fast, convenient tyre fitting that comes to them. "
            "Whether you are parked outside your home in Cheam or in a car park "
            "in Sutton town centre, our fitters arrive quickly with the right "
            "tyre in stock. We offer same-day service and 24-hour emergency "
            "cover throughout Sutton every day of the week."
        ),
        'faq': [
            ("Do you cover Cheam, Carshalton, and Wallington?",
             "Yes. We cover all of Sutton including Sutton town, Cheam, North Cheam, "
             "Carshalton, Wallington, Beddington, Belmont, and all surrounding areas."),
            ("Can you help with a tyre issue on the A217?",
             "Yes. The A217 is a key route through Sutton and we respond to "
             "roadside callouts along it regularly. Our average arrival is under 20 minutes."),
            ("Is same-day mobile tyre fitting available in Sutton?",
             "Yes. Same-day appointments are available seven days a week. "
             "Emergency cover operates 24 hours a day throughout Sutton."),
            ("How long does a mobile tyre fitting take?",
             "Most fittings take between 30 and 45 minutes from when our fitter "
             "arrives. We include wheel balancing and pressure checks as standard."),
            ("Do you need access to a garage or special equipment in Sutton?",
             "No. Our mobile vans carry all equipment needed to fit and balance "
             "tyres at any outdoor location throughout Sutton."),
        ],
    },
    'tower-hamlets': {
        'name': 'Tower Hamlets',
        'postcodes': ['E1', 'E2', 'E3', 'E14'],
        'intro': (
            "Tower Hamlets is a dynamic East London borough encompassing the "
            "financial powerhouse of Canary Wharf, the historic streets of "
            "Whitechapel and Stepney, the vibrant Brick Lane area of Bethnal Green, "
            "and the waterfront regeneration of Wapping and Limehouse. "
            "It is one of London's most densely populated boroughs, with significant "
            "traffic on the A13 and A11, and a large professional workforce "
            "that relies on both public transport and private vehicles."
        ),
        'coverage': (
            "We cover all of Tower Hamlets, including Canary Wharf, Whitechapel, "
            "Bethnal Green, Stepney, Mile End, Bow, Poplar, Limehouse, Wapping, "
            "and the Isle of Dogs. Postcodes served include E1, E2, E3, and E14. "
            "Our mobile fitters reach every part of the borough within approximately "
            "20 minutes, navigating the dense urban road network efficiently."
        ),
        'why_us': (
            "Tower Hamlets residents and workers benefit from a mobile tyre service "
            "that removes the need to find and travel to a garage in one of London's "
            "busiest boroughs. FixMyTyreNow dispatches a fitter directly to your "
            "location, whether that is a car park in Canary Wharf or a residential "
            "street in Bethnal Green. Same-day and 24-hour emergency cover "
            "is available throughout the borough every day."
        ),
        'faq': [
            ("Do you serve Canary Wharf, Whitechapel, and Bethnal Green?",
             "Yes. We cover all of Tower Hamlets including Canary Wharf, Whitechapel, "
             "Bethnal Green, Stepney, Mile End, Bow, Poplar, Limehouse, and Wapping."),
            ("Can you come to a car park in Canary Wharf?",
             "Yes. We serve E14 and the Canary Wharf area, including car parks and "
             "street locations throughout the Isle of Dogs."),
            ("How quickly can a fitter reach me in Tower Hamlets?",
             "Our average arrival time across Tower Hamlets is under 20 minutes. "
             "We dispatch the nearest available fitter to your exact location."),
            ("Is 24-hour emergency tyre service available in Tower Hamlets?",
             "Yes. Emergency tyre fitting operates around the clock throughout "
             "Tower Hamlets. Call us any time for immediate dispatch."),
            ("Do you work within the Congestion Charge Zone in Tower Hamlets?",
             "Yes. Our fitters are fully operational within the CCZ and ULEZ. "
             "We come to your location regardless of which zone applies."),
        ],
    },
    'waltham-forest': {
        'name': 'Waltham Forest',
        'postcodes': ['E4', 'E10', 'E11', 'E17'],
        'intro': (
            "Waltham Forest is a North-East London borough stretching from the "
            "lively streets of Walthamstow in the south to the green spaces of "
            "Chingford and Epping Forest in the north. Walthamstow Village and "
            "the famous Walthamstow Market give the borough a distinctive local "
            "character, while Leytonstone and Leyton are popular residential areas "
            "for young families and commuters. The A104 Epping New Road and "
            "A112 connect the borough to the M25 and central London, "
            "and the area sees a high volume of daily commuter traffic."
        ),
        'coverage': (
            "We cover all of Waltham Forest, including Walthamstow, Leyton, "
            "Leytonstone, Chingford, High Maynard, Higham Hill, Wood Street, "
            "and Hale End. Postcodes served include E4, E10, E11, and E17. "
            "Our mobile fitters reach every part of the borough within approximately "
            "20 minutes, from Chingford in the north to Leyton in the south."
        ),
        'why_us': (
            "Waltham Forest drivers trust FixMyTyreNow for a fast and professional "
            "service that fits around their busy lives. Whether you need an emergency "
            "callout on the A104 or a planned tyre change at home in Walthamstow, "
            "our fitters arrive quickly with the right tyre in stock. We offer "
            "same-day service and 24-hour emergency cover throughout the borough "
            "every day of the week."
        ),
        'faq': [
            ("Do you cover Walthamstow, Chingford, and Leyton?",
             "Yes. We cover all of Waltham Forest including Walthamstow, Chingford, "
             "Leyton, Leytonstone, Higham Hill, Wood Street, and all surrounding areas."),
            ("Can you help with a tyre problem on the A104?",
             "Yes. The A104 is a key route through Waltham Forest and we respond "
             "to roadside callouts along it regularly. Our average arrival is under 20 minutes."),
            ("Is same-day tyre fitting available in Waltham Forest?",
             "Yes. Same-day fitting is available every day of the week. "
             "Emergency cover operates 24 hours a day throughout the borough."),
            ("How do I book a mobile tyre fitter in Waltham Forest?",
             "Book online with a 10 pound deposit or call us directly. We confirm "
             "your appointment and dispatch the nearest available fitter."),
            ("What services do you offer in Waltham Forest?",
             "We offer emergency tyre replacement, standard tyre fitting, puncture "
             "repair, wheel balancing, and run-flat replacement across all of Waltham Forest."),
        ],
    },
    'wandsworth': {
        'name': 'Wandsworth',
        'postcodes': ['SW11', 'SW12', 'SW17', 'SW18'],
        'intro': (
            "Wandsworth is a South London borough with a riverside location along "
            "the Thames, encompassing the popular areas of Battersea, Clapham, "
            "Tooting, and Balham. The borough has undergone significant regeneration, "
            "particularly in Battersea with the development around the iconic "
            "Battersea Power Station, and it attracts a young professional "
            "population that values convenience and speed. "
            "The A3 runs through the eastern part of the borough and is one "
            "of the main routes out of central London towards the M25."
        ),
        'coverage': (
            "We cover all of Wandsworth, including Battersea, Clapham, Balham, "
            "Tooting, Wandsworth town, Earlsfield, Southfields, and Furzedown. "
            "Postcodes served include SW11, SW12, SW17, and SW18. Our mobile "
            "fitters reach every part of the borough within approximately 20 "
            "minutes, from the riverside in Battersea to the residential streets of Tooting."
        ),
        'why_us': (
            "Wandsworth's young, active population demands a mobile service that "
            "works around their schedule, and FixMyTyreNow delivers exactly that. "
            "We fit tyres at your home, workplace, or any roadside location "
            "across the borough. Our fitters carry a wide range of popular tyre "
            "sizes and offer same-day service and 24-hour emergency cover "
            "throughout Wandsworth every day of the year."
        ),
        'faq': [
            ("Do you cover Battersea, Balham, and Tooting?",
             "Yes. We cover all of Wandsworth including Battersea, Clapham, Balham, "
             "Tooting, Earlsfield, Southfields, Wandsworth town, and all surrounding areas."),
            ("Can you reach me near Battersea Power Station?",
             "Yes. We cover the SW11 area including the Battersea Power Station "
             "development and surrounding streets."),
            ("Can you help with a breakdown on the A3?",
             "Yes. The A3 runs through Wandsworth and we attend roadside callouts "
             "along it regularly. Our average arrival time is under 20 minutes."),
            ("Is same-day tyre fitting available in Wandsworth?",
             "Yes. Same-day appointments are available every day of the week. "
             "Emergency cover operates 24 hours a day across the whole borough."),
            ("How do I book mobile tyre fitting in Wandsworth?",
             "Book online in under 60 seconds with a 10 pound deposit, or call us "
             "directly. We confirm your slot and send the nearest available fitter."),
        ],
    },
}

# ---------------------------------------------------------------------------
# Service data for combo pages
# ---------------------------------------------------------------------------
SERVICES = {
    'emergency-tyre-replacement': {
        'name': 'Emergency Tyre Replacement',
        'slug': 'emergency-tyre-replacement',
        'price': 'From £69',
        'short_desc': 'our fastest response service',
    },
    'standard-tyre-fitting': {
        'name': 'Standard Tyre Fitting',
        'slug': 'standard-tyre-fitting',
        'price': 'From £65',
        'short_desc': 'professional mobile tyre fitting',
    },
    'puncture-repair': {
        'name': 'Puncture Repair',
        'slug': 'puncture-repair',
        'price': 'From £25',
        'short_desc': 'fast on-the-spot puncture repair',
    },
    'wheel-balancing': {
        'name': 'Wheel Balancing',
        'slug': 'wheel-balancing',
        'price': 'From £15',
        'short_desc': 'precision mobile wheel balancing',
    },
    'run-flat-replacement': {
        'name': 'Run-Flat Replacement',
        'slug': 'run-flat-replacement',
        'price': 'From £110',
        'short_desc': 'specialist run-flat tyre replacement',
    },
}


def build_borough_intro_html(slug, data):
    """Build rich HTML for the location-intro section of a borough page."""
    name = data['name']
    postcodes_str = ', '.join(data['postcodes'])

    lines = [
        '<section class="location-intro">',
        f'<h2>Mobile Tyre Fitting in {name}</h2>',
        f'<p>{data["intro"]}</p>',
        f'<p>{data["coverage"]}</p>',
        f'<p>{data["why_us"]}</p>',
        '</section>',
        '',
        '<section class="location-faq">',
        f'<h2>Mobile Tyre Fitting {name}: Frequently Asked Questions</h2>',
    ]
    for q, a in data['faq']:
        lines.append('<details class="faq-item">')
        lines.append(f'<summary>{q}</summary>')
        lines.append(f'<p>{a}</p>')
        lines.append('</details>')
    lines.append('</section>')

    return '\n'.join(lines)


def fix_em_dashes(content):
    """Replace em-dashes (U+2014) with a comma+space, handling surrounding spaces."""
    # Replace optional-space + em-dash + optional-space with a comma
    content = re.sub(r'\s*\u2014\s*', ', ', content)
    # Also fix unicode escape in JSON-LD
    content = re.sub(r'\s*\\u2014\s*', ', ', content)
    return content


def update_borough_page(filepath, slug, data):
    """Update a borough index.html with rich content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix em-dashes first
    content = fix_em_dashes(content)

    # Replace the existing location-intro section
    # Pattern: <section class="location-intro">...</section>
    old_intro_pattern = re.compile(
        r'<section class="location-intro">.*?</section>',
        re.DOTALL
    )
    new_intro = build_borough_intro_html(slug, data)

    if old_intro_pattern.search(content):
        content = old_intro_pattern.sub(new_intro, content)
    else:
        # Fallback: insert before </main>
        content = content.replace('</main>', new_intro + '\n\n</main>', 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


def fix_em_dashes_in_file(filepath):
    """Fix em-dashes in any file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = fix_em_dashes(content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def process_all_areas():
    changed = 0
    errors = 0

    # 1. Process all borough index pages
    print("=== Updating borough pages with rich content ===")
    for slug, data in BOROUGHS.items():
        borough_dir = os.path.join(AREAS_DIR, slug)
        filepath = os.path.join(borough_dir, 'index.html')
        if not os.path.exists(filepath):
            print(f"  SKIP (not found): {slug}/index.html")
            continue
        try:
            update_borough_page(filepath, slug, data)
            print(f"  OK: {slug}/index.html")
            changed += 1
        except Exception as e:
            print(f"  ERROR: {slug}/index.html - {e}")
            errors += 1

    # 2. Fix em-dashes in all remaining areas files
    print("\n=== Fixing em-dashes across all areas pages ===")
    for root, dirs, files in os.walk(AREAS_DIR):
        for filename in files:
            if filename == 'index.html':
                filepath = os.path.join(root, filename)
                try:
                    if fix_em_dashes_in_file(filepath):
                        rel = os.path.relpath(filepath, AREAS_DIR)
                        print(f"  Fixed em-dashes: {rel}")
                        changed += 1
                except Exception as e:
                    print(f"  ERROR: {filepath} - {e}")
                    errors += 1

    # 3. Also fix em-dashes in areas/index.html
    areas_index = os.path.join(AREAS_DIR, 'index.html')
    if os.path.exists(areas_index):
        if fix_em_dashes_in_file(areas_index):
            print("  Fixed em-dashes: areas/index.html")

    print(f"\nDone. Files changed: {changed}, Errors: {errors}")


if __name__ == '__main__':
    process_all_areas()
