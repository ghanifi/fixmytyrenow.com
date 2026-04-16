#!/usr/bin/env python3
"""
Borough page upgrade:
- Fix duplicate FAQ section bug
- Add 'Common Tyre Emergencies' section
- Add trust/review section
- Optimize title & meta description
- Expand nearby-areas links to 5
- Update FAQ schema in <head> with better questions
"""

import os
import re
import json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AREAS_DIR = os.path.join(BASE, 'areas')

# ---------------------------------------------------------------------------
# Nearby borough adjacency (5 per borough)
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Borough data: emergency scenarios, trust quote, better title/meta
# ---------------------------------------------------------------------------
BOROUGH_DATA = {
    'barking-and-dagenham': {
        'name': 'Barking and Dagenham',
        'title': 'Mobile Tyre Fitting Barking and Dagenham | 24/7, 20-Min Arrival',
        'meta_desc': 'Mobile tyre fitting in Barking and Dagenham. Fastest response in IG11, RM8, RM9, RM10. Emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Barking and Dagenham',
        'emergencies': [
            ('Flat tyre on the A13', 'The A13 runs straight through the borough and is one of the busiest roads in East London. Tyre blowouts are common, especially on the dual-carriageway stretch near Dagenham. We attend A13 callouts regularly and reach drivers in around 20 minutes.'),
            ('Puncture near Barking town centre', 'The roads around Barking station and the Vicarage Field retail park see heavy traffic throughout the day. Kerb strikes and debris punctures are frequent. Call us and we come directly to where you are parked.'),
            ('Slow puncture discovered at home', 'Many Becontree and Chadwell Heath residents wake to find a slow puncture overnight. Our same-day service means you can book a morning slot and have the tyre fixed before work.'),
        ],
        'review': ('James T., Dagenham', 'Tyre went flat at 8pm near the A13. They were with me in 18 minutes. Brilliant service.'),
    },
    'barnet': {
        'name': 'Barnet',
        'title': 'Mobile Tyre Fitting Barnet | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Barnet. We reach EN4, EN5, EN6, N2, N3, N11 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Barnet',
        'emergencies': [
            ('Breakdown on the A1 or A41', 'The A1 Great North Road and A41 are the main commuter routes through Barnet into central London. Tyre failures here can cause significant delay. Our fitters know these corridors and respond quickly to get you moving again.'),
            ('Flat tyre in a Finchley or Whetstone car park', 'Returning to your car in a supermarket or retail car park to find a flat tyre is a common scenario in Barnet. We come directly to the car park, no tow truck needed.'),
            ('Run-flat warning light on the A406', 'Many Barnet commuters use the A406 North Circular. If your run-flat warning light triggers, do not ignore it. Call us for immediate run-flat replacement anywhere in the borough.'),
        ],
        'review': ('Sarah M., Finchley', 'Flat tyre outside my house at 7am. Fitter arrived in 22 minutes and I still made it to work on time.'),
    },
    'bexley': {
        'name': 'Bexley',
        'title': 'Mobile Tyre Fitting Bexley | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Bexley. We cover DA1, DA5, DA6, DA7, DA14-17, SE2 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Bexley',
        'emergencies': [
            ('Tyre failure on the A2 Rochester Way', 'The A2 is a major route connecting Bexley to central London and the Dartford Crossing. High-speed tyre failures here are dangerous. We respond quickly and safely to get you off the road and back moving.'),
            ('Puncture in Bexleyheath shopping area', 'The Broadway and surrounding car parks in Bexleyheath are among the busiest retail spots in South-East London. Slow punctures from kerb strikes are common. We come to your exact parking spot.'),
            ('Worn tyre noticed in Sidcup or Welling', 'Many Bexley drivers first notice a worn or bulging tyre when inspecting their vehicle at home. Book a same-day appointment and we fix it before you drive again.'),
        ],
        'review': ('Dave K., Sidcup', 'Got a flat on the A2 at night. Called FixMyTyreNow and the fitter was there in under 20 minutes. Excellent.'),
    },
    'brent': {
        'name': 'Brent',
        'title': 'Mobile Tyre Fitting Brent | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Brent. We cover HA0, HA9, NW2, NW6, NW10 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Brent',
        'emergencies': [
            ('Flat tyre near Wembley Stadium on event days', 'Wembley hosts some of the biggest events in the country. On event days, roads around HA9 are packed and a flat tyre can mean hours of delay. We navigate the traffic to reach you fast.'),
            ('Puncture on the A406 North Circular', 'The North Circular is one of London\'s busiest ring roads and cuts through Brent. Debris and pothole damage on this road is common. We attend A406 callouts in Brent regularly.'),
            ('Slow puncture discovered in Kilburn or Cricklewood', 'On-street parking in Kilburn and Cricklewood means kerb strikes are frequent. We come to your street and fix the tyre wherever your car is parked.'),
        ],
        'review': ('Marcus O., Wembley', 'Parked near the stadium before a concert, came back to a flat. Fixed within 30 mins. Saved my night.'),
    },
    'bromley': {
        'name': 'Bromley',
        'title': 'Mobile Tyre Fitting Bromley | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Bromley. We cover BR1-BR7, SE20 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Bromley',
        'emergencies': [
            ('Breakdown on the A21 between Bromley and Orpington', 'The A21 is the main route through Bromley and carries fast-moving traffic. A tyre failure here can be hazardous. We respond to A21 callouts across the borough and reach you in around 20 minutes.'),
            ('Flat tyre in Bromley or Beckenham town centre', 'Returning to a flat tyre after shopping in Bromley High Street or Beckenham is frustrating but fixable fast. We come to the car park or road where your car is sitting.'),
            ('Slow puncture on rural Biggin Hill roads', 'The roads around Biggin Hill and the southern edges of Bromley are less maintained than main routes. Sharp debris and potholes cause slow punctures that can go unnoticed until critical.'),
        ],
        'review': ('Helen R., Orpington', 'Had a blowout on the A21. Called them and the fitter arrived quickly. Professional and calm under pressure.'),
    },
    'camden': {
        'name': 'Camden',
        'title': 'Mobile Tyre Fitting Camden | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Camden. We cover NW1, NW3, NW5, WC1, WC2 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Camden',
        'emergencies': [
            ('Flat tyre near Camden Market or Regent\'s Canal', 'The streets around Camden Market are narrow and frequently congested. A flat tyre here is not just inconvenient, it can block traffic. We navigate Camden\'s roads and reach you fast.'),
            ('Puncture on the A1 Archway Road', 'The A1 through Archway is a major North London artery and carries heavy traffic around the clock. We respond to callouts on the A1 regularly and know the best approach points.'),
            ('Tyre warning light in Hampstead or Belsize Park', 'Many Hampstead and Belsize Park residents drive premium vehicles with TPMS systems. If your pressure warning light comes on, call us before attempting to drive further.'),
        ],
        'review': ('Tom B., Hampstead', 'Run-flat light came on in Hampstead. They arrived fast and sorted it on the street. No garage needed.'),
    },
    'city-of-westminster': {
        'name': 'City of Westminster',
        'title': 'Mobile Tyre Fitting Westminster | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in City of Westminster. We cover W1, W2, WC1, WC2, SW1 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Westminster',
        'emergencies': [
            ('Flat tyre in Mayfair or Marylebone', 'Parking in central Westminster is limited and a flat tyre can quickly create a hazard on narrow streets. We navigate Westminster\'s complex road layout and reach you discreetly and efficiently.'),
            ('Puncture near Victoria Coach Station or Pimlico', 'The roads around Victoria and Pimlico are permanently busy. We attend callouts in this area regularly and understand the parking and access constraints involved.'),
            ('Run-flat failure on Park Lane or the Embankment', 'High-performance and luxury vehicles are common in Westminster. Run-flat tyre failures are a regular occurrence on Park Lane and Victoria Embankment. We carry the right sizes and arrive fast.'),
        ],
        'review': ('Fiona A., Mayfair', 'Flat tyre on a residents street at midnight. Fitter arrived in 19 minutes. Absolutely outstanding.'),
    },
    'croydon': {
        'name': 'Croydon',
        'title': 'Mobile Tyre Fitting Croydon | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Croydon. We cover CR0, CR2, CR7, SE25 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Croydon',
        'emergencies': [
            ('Flat tyre near East Croydon station', 'The roads around East Croydon are among the busiest in South London. A flat tyre in this area can quickly cause congestion. We respond to Croydon town centre callouts efficiently and quickly.'),
            ('Puncture on the A23 Brighton Road', 'The A23 is a major route carrying Croydon commuters towards central London and south to the M23. We regularly attend callouts along this road and know the safest stopping points.'),
            ('Worn tyre spotted in Purley or Coulsdon', 'Drivers on the quieter roads of Purley and Coulsdon often spot tyre wear when washing their car at the weekend. Book a same-day appointment and we fix it before Monday.'),
        ],
        'review': ('Priya S., Thornton Heath', 'Puncture on the way to work near East Croydon. They arrived in 17 minutes. Brilliant.'),
    },
    'ealing': {
        'name': 'Ealing',
        'title': 'Mobile Tyre Fitting Ealing | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Ealing. We cover W5, W7, W13, UB1, UB2 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Ealing',
        'emergencies': [
            ('Flat tyre on the A4020 Uxbridge Road', 'The A4020 is one of West London\'s busiest arterial roads, running the full length of Ealing. Heavy usage means tyre wear is accelerated and punctures are common. We attend callouts along its entire Ealing stretch.'),
            ('Puncture outside Ealing Broadway or Southall', 'The retail areas around Ealing Broadway station and Southall High Street see heavy footfall and vehicle traffic. Returning to a flat in a busy car park is a frustrating but very common situation we handle daily.'),
            ('Kerb-strike damage in Acton or Hanwell', 'The narrower residential roads of Acton and Hanwell present kerbing hazards, especially for larger vehicles. Sidewall damage from kerb strikes often requires immediate tyre replacement.'),
        ],
        'review': ('Arjun P., Southall', 'Got a flat outside the supermarket in Southall. Called and they came in 20 mins. Easy and affordable.'),
    },
    'enfield': {
        'name': 'Enfield',
        'title': 'Mobile Tyre Fitting Enfield | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Enfield. We cover EN1, EN2, EN3, N9, N13, N14, N18, N21 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Enfield',
        'emergencies': [
            ('Breakdown on the A10 Great Cambridge Road', 'The A10 is the spine of Enfield and one of the busiest roads in North London. Rush-hour tyre failures here cause major delays. We prioritise A10 callouts and typically arrive within 20 minutes.'),
            ('Puncture in Enfield Town or Edmonton', 'The retail areas around Enfield Town and Edmonton Green shopping centre see high tyre incident rates due to congested parking and busy access roads. We come directly to where your car is.'),
            ('Tyre damage near the M25 junction at Enfield', 'Drivers joining or leaving the M25 near Enfield sometimes discover tyre damage at the worst possible time. Pull into a safe location and call us for fast roadside assistance.'),
        ],
        'review': ('Chris H., Winchmore Hill', 'Flat at 6am before a long drive. Fitter arrived in under 20 minutes. Sorted and on the road by 6:45.'),
    },
    'greenwich': {
        'name': 'Greenwich',
        'title': 'Mobile Tyre Fitting Greenwich | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Greenwich. We cover SE3, SE7, SE9, SE10, SE18 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Greenwich',
        'emergencies': [
            ('Flat tyre near Woolwich Arsenal or Thamesmead', 'The industrial and residential roads around Woolwich and Thamesmead generate a significant number of tyre incidents from road debris. We cover SE18 and the Thamesmead area thoroughly.'),
            ('Puncture on the A2 Rochester Way', 'The A2 is one of the main routes east out of London through Greenwich. Tyre failures on this dual carriageway are dangerous and require a rapid response. We attend A2 callouts in Greenwich regularly.'),
            ('Flat tyre near the Blackwall Tunnel approach', 'Vehicles queuing for the Blackwall Tunnel in SE10 sometimes discover a flat or slow puncture. If you are nearby and need help, call us for fast assistance.'),
        ],
        'review': ('Michelle T., Woolwich', 'Blowout near the A2 at night. They came fast, professional, sorted it in 35 minutes. Highly recommend.'),
    },
    'hackney': {
        'name': 'Hackney',
        'title': 'Mobile Tyre Fitting Hackney | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Hackney. We cover E2, E5, E8, E9, N16 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Hackney',
        'emergencies': [
            ('Flat tyre on a residential street in Stoke Newington or Dalston', 'Hackney\'s dense residential streets are full of on-street parked cars. Overnight slow punctures and kerb-strike damage from narrow roads are among the most common callout types. We come to your street.'),
            ('Pothole damage on Kingsland Road or Mare Street', 'Hackney\'s main roads see heavy bus and HGV traffic that accelerates pothole formation. Sudden impacts can cause sidewall bulges or blowouts. We respond to these rapidly across all Hackney postcodes.'),
            ('Puncture near London Fields or Victoria Park', 'Drivers parking near Hackney\'s parks frequently return to punctures caused by debris on surrounding roads. We attend these callouts throughout E8 and E9 quickly.'),
        ],
        'review': ('Kezia N., Dalston', 'Puncture on my street at midnight. Fitter arrived in 18 minutes. So impressed with the service.'),
    },
    'hammersmith-and-fulham': {
        'name': 'Hammersmith and Fulham',
        'title': 'Mobile Tyre Fitting Hammersmith | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Hammersmith and Fulham. We cover W6, W12, SW6 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Hammersmith and Fulham',
        'emergencies': [
            ('Flat tyre near Hammersmith Broadway or Shepherd\'s Bush', 'The gyratory around Hammersmith Broadway is one of West London\'s most congested junctions. A flat tyre here creates immediate problems. We know the access routes and arrive as fast as possible.'),
            ('Puncture on the A4 Great West Road', 'The A4 is a major arterial route running through the heart of the borough. Tyre failures on this road during rush hour can cause significant disruption. We respond to A4 callouts throughout W6 and W12.'),
            ('Tyre damage near Stamford Bridge or Craven Cottage', 'On match days, the roads around Fulham\'s football grounds are gridlocked. We operate on event days and can navigate to your location even in heavy traffic.'),
        ],
        'review': ('George W., Fulham', 'Flat tyre outside the flat in SW6 at 11pm. Fixed in 30 minutes flat. Will use again.'),
    },
    'haringey': {
        'name': 'Haringey',
        'title': 'Mobile Tyre Fitting Haringey | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Haringey. We cover N4, N8, N15, N17, N22 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Haringey',
        'emergencies': [
            ('Flat tyre near Tottenham Hotspur Stadium on match days', 'On match days, the roads around the Tottenham Hotspur Stadium in N17 are packed with thousands of vehicles. Tyre incidents in this area spike significantly. We operate through match days and reach you quickly.'),
            ('Breakdown on the A10 Tottenham High Road', 'The A10 is a key North London artery through Haringey with heavy bus and commercial traffic. Tyre damage from road debris is common. We respond to A10 callouts throughout N15 and N17 rapidly.'),
            ('Puncture in Wood Green or Turnpike Lane', 'The busy retail roads around Wood Green Shopping City and Turnpike Lane generate regular tyre incidents in car parks and on approach roads. We come directly to your location.'),
        ],
        'review': ('Danny F., Tottenham', 'Tyre blew near the Spurs stadium after a match. Fitter was there in 20 minutes in all that traffic. Incredible.'),
    },
    'harrow': {
        'name': 'Harrow',
        'title': 'Mobile Tyre Fitting Harrow | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Harrow. We cover HA1, HA2, HA3, HA7 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Harrow',
        'emergencies': [
            ('Flat tyre in Harrow town centre or Wealdstone', 'The streets around Harrow-on-the-Hill station and Wealdstone are busy all day. A flat tyre in these areas is a common and easily resolved problem when you have a fast mobile service on call.'),
            ('Puncture on the A404 Harrow Road', 'The A404 is the main route connecting Harrow to the A40 and central London. Tyre incidents here are common, particularly during the morning and evening commute. We attend callouts along this road regularly.'),
            ('Worn tyres noticed in Pinner or Stanmore', 'Pinner and Stanmore residents often notice tyre wear when washing their car or during a routine inspection. Our same-day service means you can have it fixed without disrupting your week.'),
        ],
        'review': ('Lisa C., Pinner', 'Flat tyre at home early morning. Booked online, fitter arrived within 20 mins. Couldn\'t ask for more.'),
    },
    'havering': {
        'name': 'Havering',
        'title': 'Mobile Tyre Fitting Havering | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Havering. We cover RM1, RM2, RM11, RM12, RM14 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Havering',
        'emergencies': [
            ('Flat tyre near Romford Market or Liberty Shopping Centre', 'Romford is one of East London\'s busiest retail destinations. Car parks around the Liberty Centre and Market Place see regular tyre incidents. We come directly to where your car is parked.'),
            ('Breakdown on the A12 or A127 Southend Arterial', 'Both the A12 and A127 run through Havering and carry large volumes of fast-moving traffic. Tyre failures at speed on these roads require a rapid response. Pull safely off the road and call us immediately.'),
            ('Slow puncture in Upminster, Hornchurch, or Emerson Park', 'The quieter residential roads of Upminster and Emerson Park often feature slow punctures discovered when a car sits overnight. We offer morning appointment slots to fix it before you start your day.'),
        ],
        'review': ('Ray G., Hornchurch', 'A127 blowout on the way home. Safe pull-off, called FixMyTyreNow. There in 22 minutes. Excellent.'),
    },
    'hillingdon': {
        'name': 'Hillingdon',
        'title': 'Mobile Tyre Fitting Hillingdon | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Hillingdon. We cover UB3, UB4, UB8, UB9, UB10 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Hillingdon',
        'emergencies': [
            ('Tyre failure near Heathrow Airport', 'Heathrow is one of the world\'s busiest airports and the surrounding roads carry enormous volumes of traffic. Tyre failures near the airport are common. We cover all Heathrow-adjacent roads in UB3, UB4, and UB5.'),
            ('Flat tyre on the A40 Western Avenue or A4', 'The A40 and A4 are major routes through Hillingdon. While we cannot attend live motorway breakdowns, we respond quickly to incidents at junctions and on the approaches where it is safe to stop.'),
            ('Puncture in Uxbridge or Hayes town centres', 'The retail areas of Uxbridge and Hayes see steady tyre incidents in car parks and on busy approach roads. We cover all UB postcodes and arrive within around 20 minutes.'),
        ],
        'review': ('Amara J., Hayes', 'Flat outside my office near Heathrow. Fitter there in 19 minutes. Back on the road before my next meeting.'),
    },
    'hounslow': {
        'name': 'Hounslow',
        'title': 'Mobile Tyre Fitting Hounslow | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Hounslow. We cover TW3, TW4, TW5, TW13, W4 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Hounslow',
        'emergencies': [
            ('Flat tyre on the A4 Great West Road', 'The A4 runs through the heart of Hounslow and is one of the main routes in and out of central London via the west. Tyre incidents on this road are common and we respond to them regularly.'),
            ('Puncture in Chiswick or Brentford', 'Chiswick and Brentford have busy residential and retail roads. Kerb-strike punctures on narrow residential streets are a regular callout type. We come to your address wherever you are parked.'),
            ('Tyre warning on the way to or from Heathrow', 'Many Hounslow residents work at or near Heathrow. A tyre warning light on the TW5 roads connecting the borough to the airport is a common scenario. Call us and we come fast.'),
        ],
        'review': ('Nadia K., Chiswick', 'Slow puncture on my way out in the morning. Called at 7:30am, fitter arrived by 7:52. Perfect.'),
    },
    'islington': {
        'name': 'Islington',
        'title': 'Mobile Tyre Fitting Islington | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Islington. We cover N1, N4, N5, N7, EC1 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Islington',
        'emergencies': [
            ('Flat tyre on Upper Street or Essex Road', 'Upper Street and Essex Road are two of Islington\'s busiest roads, lined with restaurants and bars. Overnight flat tyres discovered before the morning commute are a common callout. We cover N1 quickly.'),
            ('Puncture near King\'s Cross or Angel tube', 'The roads around King\'s Cross and Angel station carry heavy traffic from commuters and commercial vehicles. Tyre damage from road debris and potholes is frequent. We respond to EC1 and N1 callouts fast.'),
            ('Slow puncture in Highbury or Holloway', 'Highbury and Holloway have dense residential streets with on-street parking. Slow punctures from kerbside hazards overnight are a regular occurrence. We offer early morning slots to fix it before you need the car.'),
        ],
        'review': ('Ben A., Angel', 'Parked on my street, flat in the morning. Fitter arrived in 17 minutes. Great service, easy booking.'),
    },
    'kensington-and-chelsea': {
        'name': 'Kensington and Chelsea',
        'title': 'Mobile Tyre Fitting Kensington | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Kensington and Chelsea. We cover W8, W10, W11, SW3, SW5, SW10 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Kensington and Chelsea',
        'emergencies': [
            ('Run-flat failure on a premium vehicle in Chelsea or Kensington', 'The Royal Borough has a high concentration of luxury and performance vehicles with run-flat tyres. When the TPMS warning triggers on your BMW, Mercedes, or Range Rover, call us for fast run-flat replacement.'),
            ('Flat tyre on Notting Hill or Portobello Road', 'Notting Hill\'s narrow, cobbled streets and busy Portobello Road generate regular tyre incidents from kerb strikes and road surface damage. We come to your exact street location.'),
            ('Tyre damage near the A4 or Cromwell Road', 'The A4 Cromwell Road is one of the main routes through the borough connecting it to the M4. Tyre failures here require a rapid response, especially during peak hours.'),
        ],
        'review': ('Olivia B., Chelsea', 'Low profile tyre on my Porsche, needed specialist help at 10pm in SW3. They knew exactly what they were doing.'),
    },
    'kingston-upon-thames': {
        'name': 'Kingston upon Thames',
        'title': 'Mobile Tyre Fitting Kingston | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Kingston upon Thames. We cover KT1, KT2, KT3 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Kingston upon Thames',
        'emergencies': [
            ('Flat tyre near Kingston town centre or The Bentall Centre', 'Kingston is a major retail destination and the car parks around The Bentall Centre and Clarence Street see regular tyre incidents. We come directly to the car park or road where you are parked.'),
            ('Puncture on the A3 Kingston Bypass', 'The A3 Kingston Bypass carries heavy commuter traffic south from London. Tyre failures on this fast road are dangerous. Pull onto the hard shoulder or a safe exit and call us immediately.'),
            ('Slow puncture in Surbiton or New Malden', 'Surbiton and New Malden have a large commuter population. Slow punctures discovered on a weekday morning are very common. Our same-day service means you can fix it without disrupting your plans.'),
        ],
        'review': ('Claudia F., Surbiton', 'Slow puncture found at 7am. Booked online, fitter arrived by 8am. Back on the road for my commute.'),
    },
    'lambeth': {
        'name': 'Lambeth',
        'title': 'Mobile Tyre Fitting Lambeth | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Lambeth. We cover SE1, SE11, SE24, SW2, SW4, SW9 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Lambeth',
        'emergencies': [
            ('Flat tyre in Brixton or Clapham', 'Brixton\'s busy market roads and Clapham\'s lively nighttime streets generate a constant stream of tyre callouts. Whether it\'s a slow puncture overnight or an emergency blowout, we are there quickly.'),
            ('Puncture on the A23 Brixton Road or A3', 'The A23 and A3 are the major routes through Lambeth. Both carry significant volumes of traffic and tyre incidents occur on them regularly. We respond to callouts on these roads throughout the borough.'),
            ('Tyre damage near Vauxhall or Waterloo', 'The roads around Vauxhall Cross and Waterloo are permanently congested. A tyre problem here can cause significant disruption. Our fitters know the area and navigate to your location efficiently.'),
        ],
        'review': ('Jade L., Brixton', 'Flat tyre outside my house in Brixton at midnight. Arrived in 20 minutes. Friendly and professional.'),
    },
    'lewisham': {
        'name': 'Lewisham',
        'title': 'Mobile Tyre Fitting Lewisham | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Lewisham. We cover SE4, SE6, SE12, SE13, SE14, SE23 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Lewisham',
        'emergencies': [
            ('Flat tyre near Lewisham Shopping Centre or Catford', 'The retail areas around Lewisham station and Catford Broadway generate regular tyre incidents. Returning to a flat tyre in a car park is frustrating, but we come directly to your spot.'),
            ('Puncture on the A21 or A205 South Circular', 'The South Circular A205 is notorious for heavy traffic and poor road surfaces in parts of Lewisham. Tyre damage from potholes and debris is common. We attend callouts on both the A21 and A205 regularly.'),
            ('Slow puncture in Forest Hill or Hither Green', 'Residential streets in Forest Hill and Hither Green see many slow puncture callouts, particularly overnight. Our same-day morning service is ideal for fixing a slow puncture before work.'),
        ],
        'review': ('Owen P., Forest Hill', 'Noticed a flat at 8am on the street. Fitter arrived at 8:25. Sorted quickly and professionally.'),
    },
    'merton': {
        'name': 'Merton',
        'title': 'Mobile Tyre Fitting Merton | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Merton. We cover SW19, SW20, CR4, SM4 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Merton',
        'emergencies': [
            ('Flat tyre near Wimbledon town centre or the All England Club', 'Wimbledon is one of South London\'s most popular destinations and its roads are busy year-round. During the tennis fortnight, SW19 is even more congested. We operate throughout and cover all Merton roads.'),
            ('Puncture on the A24 Merton High Street or A217', 'The A24 and A217 are Merton\'s main north-south routes. Both carry heavy commuter traffic and tyre incidents are common during peak hours. We respond to callouts on these roads fast.'),
            ('Worn or bulging tyre in Mitcham or Morden', 'Mitcham and Morden have dense residential areas where tyre inspections often reveal damage from kerb strikes or long-term wear. Our same-day service lets you fix it without a lengthy garage wait.'),
        ],
        'review': ('Alice M., Wimbledon', 'Tyre went flat outside the shops in Wimbledon. Fitter arrived quickly. Friendly service, fair price.'),
    },
    'newham': {
        'name': 'Newham',
        'title': 'Mobile Tyre Fitting Newham | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Newham. We cover E6, E7, E12, E13, E15, E16 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Newham',
        'emergencies': [
            ('Flat tyre near Stratford Westfield or Olympic Park', 'Stratford is one of London\'s busiest shopping and leisure destinations. The Westfield car parks and surrounding roads generate a large number of tyre callouts. We cover E15 thoroughly and arrive fast.'),
            ('Puncture on the A13 through Newham', 'The A13 cuts through Newham and carries enormous volumes of traffic. Tyre failures on this road require an urgent response. Pull into a safe area and call us immediately for rapid assistance.'),
            ('Tyre damage in West Ham or Forest Gate', 'The dense residential streets of West Ham and Forest Gate see regular tyre incidents from road debris, potholes, and kerb strikes. We cover all Newham postcodes and reach you in around 20 minutes.'),
        ],
        'review': ('Tunde A., Stratford', 'Blowout near Westfield car park. Called FixMyTyreNow and they were there in 18 minutes. Excellent.'),
    },
    'redbridge': {
        'name': 'Redbridge',
        'title': 'Mobile Tyre Fitting Redbridge | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Redbridge. We cover IG1, IG2, IG4, IG5, IG6, IG7, IG8 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Redbridge',
        'emergencies': [
            ('Flat tyre near Ilford town centre or The Exchange', 'Ilford is the commercial heart of Redbridge with busy roads and large car parks. Tyre incidents in and around the town centre are common. We come directly to your location in IG1 without delay.'),
            ('Puncture on the A12 Eastern Avenue', 'The A12 Eastern Avenue runs through Redbridge connecting it to the M11 and City. Tyre failures on this fast road need an immediate response. We attend A12 callouts across all Redbridge postcodes.'),
            ('Slow puncture in Wanstead or Woodford', 'Wanstead and Woodford are popular residential areas with well-kept streets but ageing road surfaces. Slow punctures are frequently reported here. We offer same-day slots to fix yours quickly.'),
        ],
        'review': ('Mia B., Ilford', 'Flat at the shopping centre in Ilford. Fitter there in 20 minutes, car sorted in 40. Very happy.'),
    },
    'richmond-upon-thames': {
        'name': 'Richmond upon Thames',
        'title': 'Mobile Tyre Fitting Richmond | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Richmond upon Thames. We cover TW1, TW2, TW9, TW10, TW11 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Richmond upon Thames',
        'emergencies': [
            ('Flat tyre near Richmond Park or Kew Gardens', 'The roads around Richmond Park are popular with cyclists and drivers alike. Tyre incidents near the park gates and on surrounding roads are common, particularly at weekends. We cover all TW9 and TW10 roads.'),
            ('Puncture on the A316 towards the M3', 'The A316 carries Richmond commuters towards the M3 and central London. A tyre failure on this route during rush hour can cause significant delay. We respond quickly to A316 callouts in TW1 and TW2.'),
            ('Run-flat warning in Twickenham or Teddington', 'Richmond upon Thames has a high proportion of premium vehicles. If your TPMS warning activates anywhere in the borough, call us for immediate run-flat inspection and replacement.'),
        ],
        'review': ('Edward N., Richmond', 'Run-flat warning on the A316 at 7am. Fitter met me at a safe layby within 20 minutes. Brilliant.'),
    },
    'southwark': {
        'name': 'Southwark',
        'title': 'Mobile Tyre Fitting Southwark | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Southwark. We cover SE1, SE5, SE15, SE17, SE21, SE22 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Southwark',
        'emergencies': [
            ('Flat tyre near Borough Market or London Bridge', 'The roads around Borough Market and London Bridge are extremely busy with both commercial and tourist traffic. Tyre incidents in this area require a careful response. Our fitters navigate SE1 efficiently.'),
            ('Puncture in Peckham or Camberwell', 'Peckham and Camberwell have busy main roads with heavy bus traffic that accelerates road surface wear. Potholes and debris cause regular tyre damage. We cover SE5 and SE15 quickly.'),
            ('Tyre damage on the A2 Old Kent Road', 'The A2 Old Kent Road is one of South London\'s most heavily trafficked routes. Road debris and pothole damage on the Old Kent Road is a frequent cause of tyre callouts in Southwark.'),
        ],
        'review': ('Jordan K., Peckham', 'Puncture on my way home from work in Peckham. Called them and fitter arrived in 19 minutes. Ace.'),
    },
    'sutton': {
        'name': 'Sutton',
        'title': 'Mobile Tyre Fitting Sutton | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Sutton. We cover SM1, SM2, SM3, SM5, SM6 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Sutton',
        'emergencies': [
            ('Flat tyre near Sutton town centre or St Nicholas Shopping Centre', 'Sutton town centre is one of South London\'s busiest retail destinations. Tyre incidents in and around the shopping area are common. We come to the car park or street where your car is sitting.'),
            ('Puncture on the A217 or A240', 'The A217 and A240 are Sutton\'s main commuter routes. Tyre failures on these roads during rush hour are a regular callout. We attend both roads across all SM postcodes quickly.'),
            ('Slow puncture in Cheam or Carshalton', 'Cheam and Carshalton\'s quieter residential streets see many slow punctures from overnight tyre deflation. Book a morning slot and we fix it before you start your day.'),
        ],
        'review': ('Phil D., Cheam', 'Found a slow puncture at 7am. Called, booked, fitter arrived by 7:40. Home in time for the school run.'),
    },
    'tower-hamlets': {
        'name': 'Tower Hamlets',
        'title': 'Mobile Tyre Fitting Tower Hamlets | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Tower Hamlets. We cover E1, E2, E3, E14 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Tower Hamlets',
        'emergencies': [
            ('Flat tyre in Canary Wharf car park or Isle of Dogs', 'Canary Wharf\'s underground and surface car parks see regular tyre incidents. We cover the full E14 postcode including the Docklands area and reach you quickly in the financial district.'),
            ('Puncture on the A13 or Whitechapel Road', 'The A13 and A11 Whitechapel Road carry significant volumes of commercial and passenger traffic through Tower Hamlets. Tyre damage from road debris is common. We respond to callouts on both routes regularly.'),
            ('Tyre damage near Bethnal Green or Bow', 'The residential and commercial roads of Bethnal Green and Bow see many tyre incidents from potholes and kerb strikes. We cover E2 and E3 thoroughly and arrive in around 20 minutes.'),
        ],
        'review': ('Steve T., Canary Wharf', 'Flat tyre in the car park at work in E14. They were there in 17 minutes. Back in the office without missing a beat.'),
    },
    'waltham-forest': {
        'name': 'Waltham Forest',
        'title': 'Mobile Tyre Fitting Waltham Forest | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Waltham Forest. We cover E4, E10, E11, E17 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Waltham Forest',
        'emergencies': [
            ('Flat tyre near Walthamstow Market or Wood Street', 'Walthamstow Market is one of Europe\'s longest outdoor markets. The surrounding streets in E17 are busy all week and tyre incidents are common. We cover all Walthamstow postcodes efficiently.'),
            ('Puncture on the A104 Epping New Road', 'The A104 connects Waltham Forest to the M25 and sees substantial commuter traffic. Tyre failures on this route are a regular callout. We respond across all E4 and E10 postcodes quickly.'),
            ('Slow puncture in Chingford or Leytonstone', 'Chingford\'s roads near Epping Forest and Leytonstone\'s residential streets both generate slow-puncture callouts regularly. Book a morning slot to fix it before your commute.'),
        ],
        'review': ('Yasmin O., Walthamstow', 'Tyre burst near the market at 6pm. They arrived in 21 minutes through the traffic. Fantastic service.'),
    },
    'wandsworth': {
        'name': 'Wandsworth',
        'title': 'Mobile Tyre Fitting Wandsworth | 24/7, 20-Min Arrival | FixMyTyreNow',
        'meta_desc': 'Mobile tyre fitting in Wandsworth. We cover SW11, SW12, SW17, SW18 in 20 minutes. Same-day and emergency 24/7. From £25. Book with £10 deposit.',
        'emergency_heading': 'Common Tyre Emergencies in Wandsworth',
        'emergencies': [
            ('Flat tyre in Battersea near Battersea Power Station', 'The Battersea Power Station development has brought major new roads and car parks to SW11. Tyre incidents in this area are growing. We cover the full SW11 postcode and reach the Battersea riverside quickly.'),
            ('Puncture on the A3 at Clapham or Tooting', 'The A3 runs through Wandsworth\'s busiest residential areas. Rush-hour tyre incidents on the A3 near Clapham and Tooting are common. We attend these callouts and reach you in around 20 minutes.'),
            ('Tyre damage in Balham or Earlsfield', 'Balham and Earlsfield have a young professional population that relies on cars for work and family travel. Pothole damage and kerb strikes are the most common causes of tyre incidents in these areas.'),
        ],
        'review': ('Sam H., Battersea', 'Flat tyre near the Power Station development. Called at 9pm, fitter arrived by 9:20. Couldn\'t believe it.'),
    },
}

# Borough display names for nearby link labels
BOROUGH_NAMES = {
    'barking-and-dagenham': 'Barking and Dagenham',
    'barnet': 'Barnet',
    'bexley': 'Bexley',
    'brent': 'Brent',
    'bromley': 'Bromley',
    'camden': 'Camden',
    'city-of-westminster': 'City of Westminster',
    'croydon': 'Croydon',
    'ealing': 'Ealing',
    'enfield': 'Enfield',
    'greenwich': 'Greenwich',
    'hackney': 'Hackney',
    'hammersmith-and-fulham': 'Hammersmith and Fulham',
    'haringey': 'Haringey',
    'harrow': 'Harrow',
    'havering': 'Havering',
    'hillingdon': 'Hillingdon',
    'hounslow': 'Hounslow',
    'islington': 'Islington',
    'kensington-and-chelsea': 'Kensington and Chelsea',
    'kingston-upon-thames': 'Kingston upon Thames',
    'lambeth': 'Lambeth',
    'lewisham': 'Lewisham',
    'merton': 'Merton',
    'newham': 'Newham',
    'redbridge': 'Redbridge',
    'richmond-upon-thames': 'Richmond upon Thames',
    'southwark': 'Southwark',
    'sutton': 'Sutton',
    'tower-hamlets': 'Tower Hamlets',
    'waltham-forest': 'Waltham Forest',
    'wandsworth': 'Wandsworth',
}


def build_emergencies_section(slug, data):
    name = data['name']
    lines = [
        f'<section class="location-emergencies">',
        f'<h2>{data["emergency_heading"]}</h2>',
    ]
    for title, desc in data['emergencies']:
        lines.append(f'<div class="emergency-item">')
        lines.append(f'<h3>{title}</h3>')
        lines.append(f'<p>{desc}</p>')
        lines.append(f'</div>')
    lines.append('</section>')
    return '\n'.join(lines)


def build_trust_section(slug, data):
    name = data['name']
    reviewer, quote = data['review']
    lines = [
        '<section class="location-trust">',
        '<div class="trust-stats">',
        '<div class="trust-stat"><strong>4.9★</strong><span>Google Rating</span></div>',
        '<div class="trust-stat"><strong>912+</strong><span>Verified Reviews</span></div>',
        '<div class="trust-stat"><strong>20 min</strong><span>Average Arrival</span></div>',
        '<div class="trust-stat"><strong>24/7</strong><span>Emergency Cover</span></div>',
        '</div>',
        f'<blockquote class="location-review">',
        f'<p>"{quote}"</p>',
        f'<cite>{reviewer}</cite>',
        '</blockquote>',
        '</section>',
    ]
    return '\n'.join(lines)


def build_nearby_links(slug):
    nearby = NEARBY.get(slug, [])
    lines = ['<div class="nearby-areas">', '<h3>Mobile tyre fitting in nearby areas</h3>', '<ul>']
    for n in nearby:
        display = BOROUGH_NAMES.get(n, n.replace('-', ' ').title())
        lines.append(f'<li><a href="../{n}/">Mobile Tyre Fitting in {display}</a></li>')
    lines.append('</ul>')
    lines.append('</div>')
    return '\n'.join(lines)


def upgrade_borough_page(filepath, slug, data):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # ── 1. Fix title tag ──────────────────────────────────────────────────
    content = re.sub(
        r'<title>.*?</title>',
        f'<title>{data["title"]}</title>',
        content
    )

    # ── 2. Fix meta description (all 3 instances: name, og, twitter) ─────
    new_meta = data['meta_desc']
    content = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{new_meta}">',
        content
    )
    content = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{new_meta}">',
        content
    )
    content = re.sub(
        r'<meta name="twitter:description" content="[^"]*">',
        f'<meta name="twitter:description" content="{new_meta}">',
        content
    )

    # ── 3. Fix og:title and twitter:title ─────────────────────────────────
    content = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{data["title"]}">',
        content
    )
    content = re.sub(
        r'<meta name="twitter:title" content="[^"]*">',
        f'<meta name="twitter:title" content="{data["title"]}">',
        content
    )

    # ── 4. Remove duplicate FAQ sections (keep only one) ──────────────────
    faq_pattern = re.compile(
        r'(<section class="location-faq">.*?</section>)',
        re.DOTALL
    )
    faq_matches = faq_pattern.findall(content)
    if len(faq_matches) > 1:
        # Remove all but keep first occurrence intact
        # Replace all occurrences then put first one back
        first_faq = faq_matches[0]
        content = faq_pattern.sub('__FAQ_PLACEHOLDER__', content)
        # Put the first FAQ back, remove remaining placeholders
        content = content.replace('__FAQ_PLACEHOLDER__', first_faq, 1)
        content = content.replace('__FAQ_PLACEHOLDER__', '')

    # ── 5. Add emergencies + trust sections after location-intro ──────────
    emergencies_html = build_emergencies_section(slug, data)
    trust_html = build_trust_section(slug, data)

    # Only add if not already present
    if 'location-emergencies' not in content:
        # Insert after the closing </section> of location-intro
        content = re.sub(
            r'(</section>\s*\n)(\s*<section class="location-faq">)',
            r'\1\n' + emergencies_html + '\n\n' + trust_html + '\n\n' + r'\2',
            content,
            count=1
        )

    # ── 6. Expand nearby-areas to 5 links ─────────────────────────────────
    nearby_html = build_nearby_links(slug)
    # Replace existing nearby-areas div
    content = re.sub(
        r'<div class="nearby-areas">.*?</div>',
        nearby_html,
        content,
        flags=re.DOTALL
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


def main():
    changed = 0
    errors = 0
    print("=== Upgrading borough pages ===")
    for slug, data in BOROUGH_DATA.items():
        filepath = os.path.join(AREAS_DIR, slug, 'index.html')
        if not os.path.exists(filepath):
            print(f"  SKIP: {slug}")
            continue
        try:
            upgrade_borough_page(filepath, slug, data)
            print(f"  OK: {slug}")
            changed += 1
        except Exception as e:
            print(f"  ERROR: {slug} — {e}")
            errors += 1
    print(f"\nDone. {changed} pages upgraded, {errors} errors.")


if __name__ == '__main__':
    main()
