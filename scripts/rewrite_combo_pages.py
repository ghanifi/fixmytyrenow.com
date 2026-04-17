"""
Comprehensive combo page content rewriter.
Replaces generic boilerplate with unique, informative, locally-relevant content.
32 boroughs x 5 services = 160 pages.

Rules:
- No emdash (-- or special char). Use colon, comma, or period instead.
- Arrival time always 20 minutes.
- Accurate service info and pricing.
- Real local context per borough.
- FAQs answer genuine questions people search for.
"""
import glob, re, os, sys, random
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── BOROUGH DATA ──────────────────────────────────────────────────────────────
BOROUGHS = [
    ('barking-and-dagenham', {
        'name': 'Barking and Dagenham',
        'road1': 'A13', 'road2': 'A406 North Circular', 'road3': 'A124',
        'area1': 'Barking town centre', 'area2': 'Becontree',
        'area3': 'Dagenham', 'area4': 'Chadwell Heath',
        'vehicle': 'vans and commercial vehicles', 'tmpl': 0,
        'pc': ['RM6', 'RM8', 'RM9', 'RM10'],
        'lid': 57,
    }),
    ('barnet', {
        'name': 'Barnet',
        'road1': 'A1 Great North Road', 'road2': 'A41', 'road3': 'A406 North Circular',
        'area1': 'High Barnet', 'area2': 'Finchley',
        'area3': 'Whetstone', 'area4': 'New Barnet',
        'vehicle': 'family saloons and SUVs', 'tmpl': 5,
        'pc': ['EN4', 'EN5', 'N2', 'N3', 'N11'],
        'lid': 63,
    }),
    ('bexley', {
        'name': 'Bexley',
        'road1': 'A2', 'road2': 'A2000 Rochester Way', 'road3': 'A207',
        'area1': 'Bexleyheath', 'area2': 'Sidcup',
        'area3': 'Erith', 'area4': 'Welling',
        'vehicle': 'family cars and MPVs', 'tmpl': 4,
        'pc': ['DA5', 'DA6', 'DA7', 'DA15', 'DA16'],
        'lid': 55,
    }),
    ('brent', {
        'name': 'Brent',
        'road1': 'A406 North Circular', 'road2': 'A40 Western Avenue', 'road3': 'A404',
        'area1': 'Wembley', 'area2': 'Harlesden',
        'area3': 'Kilburn', 'area4': 'Neasden',
        'vehicle': 'cars and vans', 'tmpl': 2,
        'pc': ['NW2', 'NW9', 'NW10'],
        'lid': 44,
    }),
    ('bromley', {
        'name': 'Bromley',
        'road1': 'A21', 'road2': 'A232', 'road3': 'A20',
        'area1': 'Bromley town centre', 'area2': 'Beckenham',
        'area3': 'Orpington', 'area4': 'Penge',
        'vehicle': 'family cars and SUVs', 'tmpl': 4,
        'pc': ['BR1', 'BR2', 'BR3', 'BR5', 'BR6'],
        'lid': 52,
    }),
    ('camden', {
        'name': 'Camden',
        'road1': 'A1 Archway Road', 'road2': 'A501 Euston Road', 'road3': 'A5',
        'area1': 'Camden Town', 'area2': 'Kentish Town',
        'area3': 'Hampstead', 'area4': 'Belsize Park',
        'vehicle': 'cars and private hire vehicles', 'tmpl': 6,
        'pc': ['NW1', 'NW3', 'NW5', 'NW6'],
        'lid': 43,
    }),
    ('city-of-westminster', {
        'name': 'City of Westminster',
        'road1': 'A4 Park Lane', 'road2': 'A40 Marylebone Road', 'road3': 'A302',
        'area1': 'Mayfair', 'area2': 'Pimlico',
        'area3': 'Paddington', 'area4': 'Soho',
        'vehicle': 'premium and prestige cars', 'tmpl': 7,
        'pc': ['W1', 'W2', 'SW1', 'WC2'],
        'lid': 21,
    }),
    ('croydon', {
        'name': 'Croydon',
        'road1': 'A23 Brighton Road', 'road2': 'A232', 'road3': 'A236',
        'area1': 'Croydon town centre', 'area2': 'Thornton Heath',
        'area3': 'Purley', 'area4': 'Norbury',
        'vehicle': 'family cars and hatchbacks', 'tmpl': 5,
        'pc': ['CR0', 'CR2', 'CR5', 'CR8'],
        'lid': 51,
    }),
    ('ealing', {
        'name': 'Ealing',
        'road1': 'A40 Western Avenue', 'road2': 'A4020 Uxbridge Road', 'road3': 'A406',
        'area1': 'Ealing Broadway', 'area2': 'Acton',
        'area3': 'Southall', 'area4': 'Hanwell',
        'vehicle': 'family cars and SUVs', 'tmpl': 2,
        'pc': ['W3', 'W5', 'W7', 'W13'],
        'lid': 45,
    }),
    ('enfield', {
        'name': 'Enfield',
        'road1': 'A10 Great Cambridge Road', 'road2': 'A110', 'road3': 'A1010',
        'area1': 'Enfield town', 'area2': 'Edmonton',
        'area3': 'Southgate', 'area4': 'Palmers Green',
        'vehicle': 'family cars and vans', 'tmpl': 0,
        'pc': ['EN1', 'EN2', 'EN3', 'EN4'],
        'lid': 62,
    }),
    ('greenwich', {
        'name': 'Greenwich',
        'road1': 'A2', 'road2': 'A102 Blackwall Tunnel approach', 'road3': 'A206',
        'area1': 'Greenwich town', 'area2': 'Woolwich',
        'area3': 'Charlton', 'area4': 'Blackheath',
        'vehicle': 'cars and light vans', 'tmpl': 4,
        'pc': ['SE7', 'SE8', 'SE9', 'SE10'],
        'lid': 54,
    }),
    ('hackney', {
        'name': 'Hackney',
        'road1': 'A10 Stoke Newington High Street', 'road2': 'A107', 'road3': 'A102',
        'area1': 'Hackney Central', 'area2': 'Stoke Newington',
        'area3': 'Dalston', 'area4': 'Shoreditch',
        'vehicle': 'cars and private hire vehicles', 'tmpl': 6,
        'pc': ['E2', 'E5', 'E8', 'N16'],
        'lid': 41,
    }),
    ('hammersmith-and-fulham', {
        'name': 'Hammersmith and Fulham',
        'road1': 'A4 Great West Road', 'road2': 'A316', 'road3': 'A219',
        'area1': 'Hammersmith', 'area2': 'Fulham',
        'area3': "Shepherd's Bush", 'area4': 'Parsons Green',
        'vehicle': 'cars and prestige vehicles', 'tmpl': 7,
        'pc': ['W6', 'W12', 'SW6', 'SW10'],
        'lid': 33,
    }),
    ('haringey', {
        'name': 'Haringey',
        'road1': 'A10 Green Lanes', 'road2': 'A109 Wood Green High Road', 'road3': 'A1080',
        'area1': 'Wood Green', 'area2': 'Tottenham',
        'area3': 'Hornsey', 'area4': 'Crouch End',
        'vehicle': 'family cars', 'tmpl': 5,
        'pc': ['N4', 'N8', 'N15', 'N17'],
        'lid': 61,
    }),
    ('harrow', {
        'name': 'Harrow',
        'road1': 'A40 Western Avenue', 'road2': 'A312 Harrow Road', 'road3': 'A404',
        'area1': 'Harrow town centre', 'area2': 'Stanmore',
        'area3': 'Pinner', 'area4': 'Kenton',
        'vehicle': 'family cars and SUVs', 'tmpl': 3,
        'pc': ['HA1', 'HA2', 'HA3', 'HA5'],
        'lid': 64,
    }),
    ('havering', {
        'name': 'Havering',
        'road1': 'A127 Southend Arterial Road', 'road2': 'A12', 'road3': 'A1306',
        'area1': 'Romford', 'area2': 'Hornchurch',
        'area3': 'Upminster', 'area4': 'Harold Wood',
        'vehicle': 'family cars and commercial vehicles', 'tmpl': 0,
        'pc': ['RM1', 'RM3', 'RM5', 'RM7', 'RM11'],
        'lid': 56,
    }),
    ('hillingdon', {
        'name': 'Hillingdon',
        'road1': 'A40 Western Avenue', 'road2': 'A4 Great West Road', 'road3': 'A408',
        'area1': 'Uxbridge', 'area2': 'Hayes',
        'area3': 'Ruislip', 'area4': 'Yiewsley',
        'vehicle': 'cars and airport-hire vehicles', 'tmpl': 1,
        'pc': ['UB3', 'UB4', 'UB7', 'UB8', 'UB10'],
        'lid': 65,
    }),
    ('hounslow', {
        'name': 'Hounslow',
        'road1': 'M4 motorway', 'road2': 'A316 Great Chertsey Road', 'road3': 'A315',
        'area1': 'Hounslow town centre', 'area2': 'Brentford',
        'area3': 'Chiswick', 'area4': 'Feltham',
        'vehicle': 'cars and airport-related vehicles', 'tmpl': 1,
        'pc': ['TW3', 'TW4', 'TW5', 'TW6'],
        'lid': 46,
    }),
    ('islington', {
        'name': 'Islington',
        'road1': 'A1 Upper Street', 'road2': 'A502 Holloway Road', 'road3': 'A503',
        'area1': 'Islington', 'area2': 'Holloway',
        'area3': 'Highbury', 'area4': 'Archway',
        'vehicle': 'cars and private hire vehicles', 'tmpl': 6,
        'pc': ['N1', 'N5', 'N7', 'N19'],
        'lid': 42,
    }),
    ('kensington-and-chelsea', {
        'name': 'Kensington and Chelsea',
        'road1': 'A4 Cromwell Road', 'road2': 'A3220 Holland Park Avenue', 'road3': 'A315',
        'area1': 'Kensington', 'area2': 'Chelsea',
        'area3': 'Notting Hill', 'area4': 'South Kensington',
        'vehicle': 'premium and prestige vehicles', 'tmpl': 7,
        'pc': ['W8', 'W11', 'SW3', 'SW7'],
        'lid': 32,
    }),
    ('kingston-upon-thames', {
        'name': 'Kingston upon Thames',
        'road1': 'A308 Kingston By-Pass', 'road2': 'A240', 'road3': 'A3',
        'area1': 'Kingston town centre', 'area2': 'Surbiton',
        'area3': 'New Malden', 'area4': 'Tolworth',
        'vehicle': 'family cars and SUVs', 'tmpl': 4,
        'pc': ['KT1', 'KT2', 'KT3', 'KT5', 'KT6'],
        'lid': 48,
    }),
    ('lambeth', {
        'name': 'Lambeth',
        'road1': 'A23 Brixton Road', 'road2': 'A3 Clapham Road', 'road3': 'A202',
        'area1': 'Brixton', 'area2': 'Clapham',
        'area3': 'Vauxhall', 'area4': 'Streatham',
        'vehicle': 'cars and private hire vehicles', 'tmpl': 6,
        'pc': ['SW2', 'SW4', 'SW9', 'SW16'],
        'lid': 35,
    }),
    ('lewisham', {
        'name': 'Lewisham',
        'road1': 'A20 Lee High Road', 'road2': 'A21 Lewisham High Street', 'road3': 'A205',
        'area1': 'Lewisham town centre', 'area2': 'Catford',
        'area3': 'Forest Hill', 'area4': 'Sydenham',
        'vehicle': 'family cars', 'tmpl': 3,
        'pc': ['SE4', 'SE6', 'SE13', 'SE23'],
        'lid': 53,
    }),
    ('merton', {
        'name': 'Merton',
        'road1': 'A24 Wimbledon High Street', 'road2': 'A236', 'road3': 'A297',
        'area1': 'Wimbledon', 'area2': 'Morden',
        'area3': 'Mitcham', 'area4': 'Colliers Wood',
        'vehicle': 'family cars and SUVs', 'tmpl': 4,
        'pc': ['SW19', 'SW20', 'CR4'],
        'lid': 49,
    }),
    ('newham', {
        'name': 'Newham',
        'road1': 'A13 East India Dock Road', 'road2': 'A118', 'road3': 'A112',
        'area1': 'Stratford', 'area2': 'East Ham',
        'area3': 'Forest Gate', 'area4': 'West Ham',
        'vehicle': 'cars and light vans', 'tmpl': 0,
        'pc': ['E6', 'E7', 'E12', 'E13'],
        'lid': 59,
    }),
    ('redbridge', {
        'name': 'Redbridge',
        'road1': 'A12 Eastern Avenue', 'road2': 'A123', 'road3': 'A113',
        'area1': 'Ilford', 'area2': 'Woodford',
        'area3': 'Wanstead', 'area4': 'Gants Hill',
        'vehicle': 'family cars and SUVs', 'tmpl': 2,
        'pc': ['IG1', 'IG2', 'IG4', 'IG5', 'IG6'],
        'lid': 58,
    }),
    ('richmond-upon-thames', {
        'name': 'Richmond upon Thames',
        'road1': 'A316 Upper Richmond Road', 'road2': 'A205 South Circular', 'road3': 'A307',
        'area1': 'Richmond', 'area2': 'Twickenham',
        'area3': 'Kew', 'area4': 'Teddington',
        'vehicle': 'premium cars and SUVs', 'tmpl': 7,
        'pc': ['TW1', 'TW2', 'TW9', 'TW10'],
        'lid': 47,
    }),
    ('southwark', {
        'name': 'Southwark',
        'road1': 'A2 Old Kent Road', 'road2': 'A200 Jamaica Road', 'road3': 'A215',
        'area1': 'Peckham', 'area2': 'Bermondsey',
        'area3': 'Camberwell', 'area4': 'Dulwich',
        'vehicle': 'cars and private hire vehicles', 'tmpl': 6,
        'pc': ['SE1', 'SE5', 'SE15', 'SE16'],
        'lid': 37,
    }),
    ('sutton', {
        'name': 'Sutton',
        'road1': 'A24 Sutton High Street', 'road2': 'A232', 'road3': 'A217',
        'area1': 'Sutton town', 'area2': 'Carshalton',
        'area3': 'Cheam', 'area4': 'Wallington',
        'vehicle': 'family cars and SUVs', 'tmpl': 3,
        'pc': ['SM1', 'SM2', 'SM4', 'SM5'],
        'lid': 50,
    }),
    ('tower-hamlets', {
        'name': 'Tower Hamlets',
        'road1': 'A11 Mile End Road', 'road2': 'A13', 'road3': 'A1203',
        'area1': 'Canary Wharf', 'area2': 'Whitechapel',
        'area3': 'Stepney', 'area4': 'Poplar',
        'vehicle': 'cars and private hire vehicles', 'tmpl': 6,
        'pc': ['E1', 'E2', 'E3', 'E14'],
        'lid': 40,
    }),
    ('waltham-forest', {
        'name': 'Waltham Forest',
        'road1': 'A104 Woodford New Road', 'road2': 'A112', 'road3': 'A503',
        'area1': 'Walthamstow', 'area2': 'Leyton',
        'area3': 'Chingford', 'area4': 'Leytonstone',
        'vehicle': 'family cars and vans', 'tmpl': 2,
        'pc': ['E4', 'E10', 'E11', 'E17'],
        'lid': 60,
    }),
    ('wandsworth', {
        'name': 'Wandsworth',
        'road1': 'A3 Trinity Road', 'road2': 'A205 South Circular', 'road3': 'A214',
        'area1': 'Tooting', 'area2': 'Battersea',
        'area3': 'Putney', 'area4': 'Balham',
        'vehicle': 'family cars and prestige vehicles', 'tmpl': 5,
        'pc': ['SW11', 'SW12', 'SW15', 'SW17', 'SW18'],
        'lid': 34,
    }),
]
BOROUGHS_DICT = dict(BOROUGHS)
BOROUGH_LIST = [slug for slug, _ in BOROUGHS]

# ── SERVICE DATA ──────────────────────────────────────────────────────────────
SERVICES = {
    'emergency-tyre-replacement': {
        'name': 'Emergency Tyre Replacement',
        'sid': 16, 'price': '£69', 'price_num': '69.00',
        'duration': '30 mins',
    },
    'standard-tyre-fitting': {
        'name': 'Standard Tyre Fitting',
        'sid': 17, 'price': '£65', 'price_num': '65.00',
        'duration': '45 mins',
    },
    'puncture-repair': {
        'name': 'Puncture Repair',
        'sid': 18, 'price': '£25', 'price_num': '25.00',
        'duration': '30 mins',
    },
    'wheel-balancing': {
        'name': 'Wheel Balancing',
        'sid': 19, 'price': '£15', 'price_num': '15.00',
        'duration': '30 mins',
    },
    'run-flat-replacement': {
        'name': 'Run-Flat Tyre Replacement',
        'sid': 20, 'price': '£110', 'price_num': '110.00',
        'duration': '45 mins',
    },
}
SERVICE_LIST = list(SERVICES.keys())

# ── INTRO TEMPLATES ────────────────────────────────────────────────────────────
# 8 templates (0-7) per service. Borough 'tmpl' field selects which one.

INTROS = {

'emergency-tyre-replacement': [
# 0: arterial/industrial
'<p>{road1} and the surrounding network carry some of the highest freight and commuter volumes in this part of London. Tyre failures on these roads range from slow punctures caused by road debris to sudden blowouts under motorway-speed conditions. When a tyre fails on a live carriageway, the priority is to get the vehicle off the road safely and call for mobile help rather than attempting to drive to a garage.</p><p>FixMyTyreNow dispatches the nearest available technician to your exact location across all of {borough}, with an average arrival time of 20 minutes. We carry a comprehensive range of tyre sizes for cars, SUVs, and light commercial vehicles. The from {price} price covers the replacement tyre, fitting, computerised wheel balancing, and inflation to your vehicle manufacturer\'s specification. No callout fee is added.</p>',
# 1: transport hub (Heathrow, M4)
'<p>{borough} sits on one of the busiest transport corridors in the country, with the {road1} and {road2} carrying high volumes of early-morning departures and late-night arrivals. Drivers here often experience tyre problems at the most inconvenient times: preparing for an early flight, returning from a long journey, or mid-shift in a hire vehicle. When a tyre gives way in these circumstances, you need a fast, professional mobile response.</p><p>Our emergency technicians cover every part of {borough} around the clock, typically arriving within 20 minutes of your call. Whether you are in {area1}, {area2}, or parked near {area3}, we come to your location carrying replacement tyres for most car and van specifications. Pricing starts from {price} for a standard fitment, confirmed before any work begins.</p>',
# 2: suburban commuter
'<p>Suburban driving in {borough} involves a mix of residential street manoeuvres, busy retail junctions, and longer runs on arterial roads like {road1} and {road2}. This combination accelerates tyre wear and increases the chance of kerb damage and punctures. Many drivers in the borough discover a tyre problem at home in the morning, in a car park, or on the way to or from work. In each case, calling for mobile help is faster than any alternative.</p><p>We cover all of {borough}: {area1}, {area2}, {area3}, and {area4}. Emergency callouts are attended 24 hours a day with an average arrival time of 20 minutes. Each technician carries tyres for most standard and common vehicle specifications. The from {price} fee includes supply, fitting, balancing, and pressure setting with no hidden callout charge.</p>',
# 3: residential discovery
'<p>A significant proportion of emergency callouts in {borough} are not roadside blowouts. They are flat tyres discovered at home, in a residential bay, or in a car park. A tyre losing air slowly over several days may look borderline one evening and be completely flat by morning. Discovering this when you need to leave for work, school, or an appointment is when fast mobile help matters most.</p><p>FixMyTyreNow covers the whole of {borough}, from {area1} to {area4}, responding to callouts at homes, workplaces, car parks, and roadsides alike. Our 24-hour service dispatches the closest technician immediately, with a typical arrival time of 20 minutes. We carry a wide range of tyre sizes and complete fitting including balancing for a from {price} all-in price, confirmed before we start.</p>',
# 4: outer suburban with specific road context
'<p>The {road1} connects {borough} to central London and the wider motorway network, making it the most used road in the borough by a significant margin. Tyre failures on this route are among the most frequent callouts we attend here. Whether the cause is a pothole, road debris, an aged tyre that finally fails, or a blowout from overloading, the outcome is the same: you cannot drive safely to a garage and you need professional help at your location.</p><p>Our mobile technicians serve all areas of {borough} including {area1}, {area2}, {area3}, and {area4}. We operate around the clock and typically reach drivers within 20 minutes of a call. Replacement tyres, fitting, balancing, and inflation are included in the from {price} price. We cover all of the borough\'s postcodes.</p>',
# 5: commuter/high-mileage
'<p>High commuter mileage is a defining feature of driving in {borough}. The daily run along {road1} and the junction-heavy sections of {road2} put tyres through more stress per year than in many other parts of London. Wear happens faster than drivers realise, and a tyre that looked fine on a visual check can give way under the combined pressures of motorway driving and emergency braking. When that happens, mobile emergency replacement is the only practical option.</p><p>We cover all of {borough}, including {area1}, {area2}, {area3}, and {area4}, with a 24-hour emergency service and an average technician arrival time of 20 minutes. All tyres are sourced from authorised UK distributors. Pricing starts from {price} and covers the tyre, fitting, balancing, and all incidental hardware. No callout fee applies.</p>',
# 6: inner-city dense
'<p>Urban driving in {borough} produces a distinct set of tyre problems. Slow punctures from road debris and valve damage are common on heavily trafficked routes like {road1}. Kerb strikes during tight parking manoeuvres on residential streets in {area2} and {area3} cause sudden pressure loss or sidewall bulges. Unlike outer-borough blowouts on fast roads, inner-city tyre failures tend to be discovered rather than felt. But the result is the same: you need a technician to come to you.</p><p>FixMyTyreNow responds to emergency callouts across {borough} 24 hours a day. Our average arrival time is 20 minutes from your call. We attend at residential bays, car parks, workplaces, and on the roadside equally. All emergency replacements include the tyre, fitting, computerised balancing, and pressure correction. The from {price} price has no callout surcharge added.</p>',
# 7: premium/prestige
'<p>Vehicles in {borough} include a high proportion of premium and prestige models from BMW, Mercedes-Benz, Audi, Porsche, and Land Rover. These vehicles frequently run on larger rim diameters with low-profile tyres that are more vulnerable to pothole and kerb damage, and more expensive to replace. Many also feature run-flat specifications or tyre pressure monitoring systems that require a reset after any change. Emergency tyre replacement on these vehicles requires stocking the right brands and having the technical knowledge to handle modern vehicle systems.</p><p>FixMyTyreNow carries Michelin, Continental, Pirelli, and Bridgestone on all emergency vans, alongside mid-range alternatives. We cover {area1}, {area2}, {area3}, and {area4}, responding within 20 minutes on average. Prices start from {price} for standard fitments. Premium brands and low-profile specifications are priced by size and confirmed before work begins.</p>',
],

'standard-tyre-fitting': [
# 0: arterial
'<p>Tyres on vehicles regularly driven on {road1} and {road2} wear at a faster rate than average. High-speed motorway running, regular heavy braking at junctions, and the kerb strikes that come with frequent lane changes and manoeuvres all contribute to earlier-than-expected wear. Most drivers in {borough} underestimate how quickly tread depth drops from acceptable to illegal, particularly on the front axle where steering and braking loads are greatest.</p><p>Standard tyre fitting from FixMyTyreNow is available same-day across all of {borough}. A mobile technician comes to your home, workplace, or any accessible car park with replacement tyres ready to fit. The from {price} price includes removal of the old tyre, mounting and seating of the new one, computerised wheel balancing, inflation to manufacturer specification, and a torque check on all wheel bolts. Old tyres are taken away and recycled.</p>',
# 1: transport hub
'<p>Vehicles in {borough} often cover unusually high annual mileages due to airport-related travel, long-distance motorway commutes, and rental or private hire use. High mileage means tyre replacement intervals arrive sooner than the average calendar-based expectation. On the {road1} and {road2} corridors, it is not uncommon for front tyres on high-mileage vehicles to reach the legal minimum tread depth in under 18 months. Planning a scheduled replacement before failure is always preferable to an emergency callout.</p><p>We provide same-day and advance-booked standard tyre fitting across all of {borough}. A technician comes to your exact location with your chosen tyres already loaded on the van. Fitting includes balancing, pressure setting, and torque verification. Prices start from {price} and are confirmed by tyre size and brand before booking is confirmed. Old tyres are removed at no extra charge.</p>',
# 2: suburban
'<p>Planned tyre replacement in {borough} makes practical sense for most drivers. Identifying the right time to replace: approaching the 3mm advisory threshold rather than waiting for the legal 1.6mm minimum, means safer braking distances in wet conditions and no risk of being stopped by police or failing an MOT on tyre condition. Our mobile fitting service removes the need to take a vehicle to a garage and wait. We come to you at a time that suits your schedule.</p><p>Standard tyre fitting is available across all of {borough}, including {area1}, {area2}, {area3}, and {area4}. Bookings are accepted daily from 06:00 to 22:00. A £10 deposit secures the slot and is deducted from the final invoice. Fitting includes balancing and pressure setting. Tyre brands available range from Michelin and Continental at the premium end through to budget-conscious alternatives. All carry the manufacturer\'s warranty.</p>',
# 3: residential
'<p>Most drivers in {borough} replace tyres reactively, after a puncture or a failed MOT, rather than proactively. Scheduling a replacement when tread depth approaches 3mm is consistently better: stopping distances in wet conditions improve significantly above the 1.6mm legal minimum, and the risk of a sudden failure on a busy road is substantially reduced. Mobile fitting means there is no need to drive on a borderline tyre to reach a garage.</p><p>FixMyTyreNow offers same-day standard tyre fitting across all of {borough}. The service comes directly to your driveway, car parking space, or workplace. Slots are available from 06:00 to 22:00. The from {price} price per tyre covers removal of the old tyre, mounting, balancing, inflation, and torque checking. We stock premium, mid-range, and budget-conscious tyre brands to suit different budgets.</p>',
# 4: outer suburban
'<p>For drivers in {borough} who cover regular miles on the {road1} and {road2}, tyre wear is a practical issue that needs regular monitoring. A tyre depth gauge costs a few pounds and takes seconds to use. The UK legal minimum is 1.6mm across the central three-quarters of the tyre. Most tyre manufacturers recommend replacement at 3mm because wet-weather braking performance deteriorates from that point. Waiting until the last millimetre carries real risk and no cost benefit.</p><p>We offer scheduled standard tyre fitting across all postcodes in {borough}, including {area1}, {area2}, and {area3}. A mobile technician arrives at your chosen location at the agreed time, carrying the tyres you have selected. All fittings include computerised balancing, inflation to spec, and TPMS reset where required. Fitting times are typically 45 minutes per tyre. Old tyres are collected and disposed of responsibly.</p>',
# 5: commuter
'<p>Commuter vehicles in {borough} often run on the same tyres for longer than they should. The daily run along {road1} and {road2} is familiar enough that gradual wear goes unnoticed until it is pointed out at a service or an MOT. Front tyres wear fastest on front-wheel-drive cars, and the difference in wear between front and rear axle can be significant within 12 to 18 months on a commuter vehicle. Regular rotation and timely replacement keep all four tyres working within their designed performance range.</p><p>Standard tyre fitting is available across all of {borough} including {area1}, {area2}, {area3}, and {area4}. Book a time slot from 06:00 to 22:00 and a mobile technician will come to your home, work address, or any accessible location. The from {price} per tyre price includes supply, fitting, balancing, and disposal of the old tyre.</p>',
# 6: inner-city
'<p>Inner-city driving in {borough} is hard on tyres in specific ways. Tight parking manoeuvres on residential streets cause frequent kerb contact that damages sidewalls and distorts rim profiles. Speed bumps, poorly maintained road surfaces, and frequent emergency braking at junctions contribute to uneven wear patterns. Tyres on vehicles in {area2} and {area3} typically show more localised wear damage than equivalent mileage on outer-city roads.</p><p>FixMyTyreNow provides standard tyre fitting across all of {borough}, coming to your location at a time that suits you. Slots run daily from 06:00 to 22:00. The technician carries your chosen tyre brand ready to fit, completes balancing and pressure setting, and takes the old tyre away. Starting from {price} per tyre with a £10 booking deposit deducted from the final bill.</p>',
# 7: premium
'<p>Premium vehicles in {borough} require tyre choices that match the vehicle\'s performance envelope. Fitting a budget-range tyre on a BMW 5 Series or a Porsche Cayenne saves money upfront but compromises the handling and braking characteristics those vehicles are designed to deliver. It may also void aspects of the manufacturer\'s warranty on drivetrain components. Our technicians can advise on the correct specification for your vehicle and carry the appropriate brands.</p><p>We offer standard tyre fitting across all of {borough}, including {area1}, {area2}, and {area3}. Bookings are available from 06:00 to 22:00 daily. Michelin, Continental, Pirelli, and Bridgestone are held in stock for most common premium vehicle fitments. Fitting includes balancing, inflation to manufacturer spec, TPMS reset, and a torque check. Prices start from {price} and are confirmed by specification before booking.</p>',
],

'puncture-repair': [
# 0: arterial
'<p>Punctures on vehicles driven regularly on {road1} and {road2} are often caused by road debris: nails, screws, and metal fragments are common on urban arterial roads and on approach roads to industrial areas. A nail puncture in the tread is not always immediately obvious. The tyre may lose pressure slowly over hours rather than going flat at once. Monitoring tyre pressure regularly is the best early warning, but once a slow puncture is confirmed, getting it professionally assessed is the next step.</p><p>FixMyTyreNow provides mobile puncture repair across all of {borough}. When we arrive, we remove the tyre from the wheel and carry out a full internal inspection. If the damage falls within the repairable zone and size limits set by the BSAU 144e industry standard, we carry out a two-stage plug-and-patch repair at the from {price} rate. Sidewall damage, large holes, or damage from running flat always requires tyre replacement rather than repair.</p>',
# 1: transport/Heathrow
'<p>Vehicles in {borough} driven on airport roads, approach carriageways, and the {road1} corridor encounter construction debris and the kind of surface damage that leads to regular nail and screw punctures. These are often slow punctures that develop gradually. Tyre pressure monitoring systems alert the driver when pressure drops by around 25%, which may not happen until the tyre is already significantly underinflated. Having a puncture assessed and repaired at your location is faster than finding a fitting centre near a busy airport corridor.</p><p>We cover all of {borough} for mobile puncture repair, attending your home, workplace, or car park within an average of 20 minutes. A complete internal inspection determines whether the damage is repairable under BSAU 144e guidelines. Confirmed repairs cost from {price} and are road-legal for the full life of the tyre. Where repair is not possible, we can complete an immediate tyre replacement.</p>',
# 2: suburban
'<p>Most tyre punctures in {borough} are repairable under the UK\'s BSAU 144e standard, provided the damage is within the central tread area and the hole is no larger than 6mm in diameter. Nail and screw punctures that fit these criteria can be repaired with a two-stage internal plug-and-patch that is road-legal and covered by the tyre manufacturer\'s ongoing warranty. Repair costs significantly less than replacement and is the right choice when the tyre has useful life remaining.</p><p>FixMyTyreNow carries out mobile puncture assessments and repairs across all of {borough}, from {area1} to {area4}. We come to your home, workplace, or any accessible location. If the puncture is repairable, the work takes around 30 minutes and costs from {price}. If repair is not possible, we carry a range of replacement tyres and can fit one at the same visit.</p>',
# 3: residential
'<p>Slow punctures are the most common tyre problem we attend in {borough}\'s residential areas. A nail or screw picked up on a local road works its way into the tread and creates a gradual leak that may take hours or days to become noticeable. Many drivers first notice it when they return to their car after parking overnight or come out to a noticeably softer tyre in the morning. At that point, the tyre may still be repairable if it has not been driven flat.</p><p>We provide mobile puncture repair across all of {borough}. The visit includes a full internal inspection and removal of the tyre from the wheel. If the damage meets BSAU 144e repair criteria, the work is completed on the spot for from {price}. If the tyre has been driven on while flat or the damage is in the sidewall, we assess whether replacement is needed and can carry that out immediately if you have a tyre available or from our van stock.</p>',
# 4: outer suburban road
'<p>The {road1} and surrounding residential roads in {borough} produce a consistent pattern of tyre punctures. Road debris from construction sites, kerb debris from verge maintenance, and general surface damage create the conditions for nail, screw, and glass punctures on a regular basis. Whether the puncture causes an immediate pressure loss or a slow leak over several hours, the first step is always to get the tyre professionally assessed before deciding whether repair or replacement is the correct outcome.</p><p>FixMyTyreNow\'s mobile puncture repair service covers all areas of {borough}. We arrive within an average of 20 minutes, remove the tyre from the rim, and carry out a full internal and external inspection. Repairable damage is fixed to BSAU 144e standard for from {price}. Where repair is not safe or not possible, we can complete tyre replacement at the same call.</p>',
# 5: commuter
'<p>Commuter vehicles in {borough} rack up high annual mileages on {road1} and {road2}, increasing the probability of picking up a nail or screw. When a puncture does occur, the decision between repair and replacement comes down to where the damage is and the condition of the tyre. A recent tyre with good remaining tread and a repairable puncture in the central zone is always worth repairing. A tyre with less than 3mm tread remaining or damage outside the repair zone needs replacement. We assess and advise when we arrive.</p><p>Mobile puncture repair is available across all of {borough}, including {area1}, {area2}, {area3}, and {area4}, with a 20-minute average arrival time. Confirmed repairs cost from {price} and are carried out to BSAU 144e industry standard. All repairs are guaranteed for the life of the tyre.</p>',
# 6: inner-city
'<p>Urban roads in {borough} carry a higher-than-average density of the debris that causes punctures: screws and nails from construction work, glass fragments, and metal pieces from road maintenance are regular findings when we carry out internal tyre inspections here. Slow punctures are more common in inner-city driving than sudden blowouts, partly because vehicle speeds are lower but also because road surfaces are more frequently disturbed by utility works and building activity in areas like {area2} and {area3}.</p><p>We provide mobile puncture repair across all of {borough}. When we attend, we remove the tyre and inspect it internally and externally. If the damage is repairable under BSAU 144e guidelines, we complete the plug-and-patch repair on the spot for from {price}. If not, we explain the finding and can complete a tyre replacement at the same visit. Our average response time is 20 minutes.</p>',
# 7: premium
'<p>Run-flat tyres, a common fitment on BMW, Mini, and Mercedes-Benz vehicles in {borough}, cannot be repaired once they have been driven in run-flat mode. The reinforced sidewall breaks down internally under deflated load and the damage is not visible from outside. A tyre pressure monitoring system alert that is acknowledged and driven on for any distance typically rules out repair. For non-run-flat vehicles with a standard puncture, the same BSAU 144e repair criteria apply regardless of tyre brand or price point.</p><p>FixMyTyreNow provides mobile puncture assessment and repair across all of {borough}, including {area1}, {area2}, and {area3}. We arrive within 20 minutes on average, carry out a full internal inspection, and either complete the repair for from {price} or advise on replacement if the tyre cannot be safely repaired. We stock premium brands for same-visit replacement if needed.</p>',
],

'wheel-balancing': [
# 0: arterial
'<p>Wheels on vehicles regularly driven on {road1} frequently go out of balance from the potholes and surface irregularities that are unavoidable on high-traffic arterial roads. A small imbalance in the wheel-and-tyre assembly, even just 5 to 10 grams out of true, is enough to cause a noticeable vibration through the steering wheel at motorway speeds. Left unchecked, that vibration transfers load through the suspension and causes localised tyre wear that shortens tyre life.</p><p>FixMyTyreNow provides mobile wheel balancing across all of {borough}, coming to your home, work, or any accessible location. Our technicians use computerised on-van balancing equipment calibrated to manufacturer tolerance. Each wheel is balanced to within 1 gram. The from {price} per wheel price covers assessment, weight application, and re-check. Work is typically complete within 30 minutes for a full axle.</p>',
# 1: motorway/transport
'<p>High-speed motorway driving on the {road1} and airport approach roads amplifies the effect of wheel imbalance. A wheel that runs smoothly at 40 mph may produce significant vibration at 70 mph. This vibration wears tyres unevenly, particularly on the outer tread edges, and reduces ride comfort over long distances. Drivers who regularly use the motorway sections of {road1} often notice the symptom most clearly on long drives, when the vibration has been continuous for an extended period.</p><p>Our mobile balancing service covers all areas of {borough}, attending at your home, workplace, or any suitable location. We use on-van computerised balancing equipment and work to a tolerance of 1 gram per wheel. All four wheels can be balanced in a single visit. The service costs from {price} per wheel with no callout fee. Average arrival time is 20 minutes from your call.</p>',
# 2: suburban
'<p>Wheel balance is commonly overlooked in routine vehicle maintenance in {borough}, partly because the symptoms develop gradually. Vibration through the steering wheel at around 60 to 70 mph, uneven tyre wear visible on the outer or inner tread blocks, and a steering wheel that pulls slightly to one side are all signs that one or more wheels may be out of balance. These symptoms tend to worsen over time if untreated, leading to faster tyre wear and higher fuel consumption.</p><p>Mobile wheel balancing from FixMyTyreNow covers all of {borough}, including {area1}, {area2}, {area3}, and {area4}. A technician comes to your location and completes the balancing using precision on-van equipment, applying or adjusting weights to bring each wheel within tolerance. Work takes around 30 minutes for a full set. Pricing is from {price} per wheel, with no callout fee.</p>',
# 3: residential
'<p>New tyre fitments should always be followed by wheel balancing, but it is also worth checking balance when you notice a new vibration, after a significant kerb impact, or any time a balancing weight falls off. Balancing weights can be dislodged by car washes, kerb strikes, and even road debris. When a weight is lost, the wheel immediately goes out of balance. The resulting vibration at speed is the first sign that something has changed.</p><p>FixMyTyreNow carries out mobile wheel balancing across all of {borough}. We come to your location and balance each wheel to within 1 gram of tolerance using computerised equipment. The full process for four wheels takes approximately 30 minutes. Pricing starts from {price} per wheel. Average arrival time after calling is 20 minutes. There is no callout fee.</p>',
# 4: outer suburban
'<p>Wheels on vehicles driven in {borough} are knocked out of balance by the road surfaces on routes like the {road1} more quickly than most drivers expect. A significant pothole impact can shift a wheel\'s balance point immediately, and the effect is felt before the next motorway drive. Tyre manufacturers recommend re-balancing every 10,000 miles or whenever a new tyre is fitted, but a notable vibration at speed is always a good enough reason to book sooner.</p><p>Mobile wheel balancing is available across all areas of {borough}, covering {area1}, {area2}, {area3}, and {area4}. A technician arrives at your location within an average of 20 minutes, completes the balancing using on-van computerised equipment, and adjusts weights to bring each wheel within specification. The from {price} per wheel price is all-inclusive, with no callout fee added.</p>',
# 5: commuter
'<p>Commuter vehicles in {borough} cover enough annual mileage that wheel balance becomes a meaningful maintenance item rather than an afterthought. Every 10,000 to 12,000 miles is a reasonable interval for re-balancing, coinciding roughly with the rotation interval most manufacturers recommend. Keeping wheels balanced reduces the uneven wear that cuts tyre life short and eliminates the low-frequency vibration that contributes to driver fatigue on the daily {road1} commute.</p><p>We provide mobile wheel balancing across all of {borough}, including {area1}, {area2}, {area3}, and {area4}. Slots are available from 06:00 to 22:00 daily. A technician comes to your home or workplace and completes the work on-site using precision balancing equipment. Four wheels typically take 30 minutes. Pricing starts from {price} per wheel with no callout fee.</p>',
# 6: inner-city
'<p>In inner-city {borough}, the road surfaces on routes like {road1} and the side streets of {area2} and {area3} are among the most pothole-affected in London. Each significant impact can shift wheel balance. Drivers often attribute steering vibration to road surface quality rather than wheel balance because the roads are genuinely rough. The distinction matters: road roughness cannot be fixed but a wheel balance issue can be resolved in under an hour, eliminating the vibration regardless of the surface.</p><p>Mobile wheel balancing is available across {borough}. We come to your location, assess all four wheels, and bring each one within tolerance using computerised equipment. The process takes around 30 minutes for a full set. From {price} per wheel, no callout fee. Average arrival time is 20 minutes after you call.</p>',
# 7: premium
'<p>Large-diameter alloy wheels on premium vehicles in {borough} are more sensitive to balance issues than standard 15 or 16-inch fitments. A 20-inch wheel on a Range Rover or BMW 7 Series amplifies any imbalance at the tyre\'s outer diameter, making the vibration felt at lower speeds and more acutely through the steering. Run-flat tyres, common on many premium vehicles, also require careful balancing due to their reinforced sidewall affecting the wheel\'s natural resonance frequency.</p><p>FixMyTyreNow provides mobile wheel balancing across all of {borough}, including {area1}, {area2}, {area3}, and {area4}. Our precision computerised equipment handles large-diameter wheels correctly. Each wheel is balanced to within 1 gram of tolerance. Four wheels are typically completed in 30 minutes. Pricing starts from {price} per wheel, with no callout fee. Average arrival time is 20 minutes.</p>',
],

'run-flat-replacement': [
# 0: arterial
'<p>Run-flat tyres are increasingly common on vehicles driven on {road1} and {road2} in {borough}. Originally developed as a safety feature to allow drivers to continue to a service point after a puncture, run-flat technology has been standard equipment on BMW, Mini, and a growing range of Mercedes-Benz models for many years. The critical point is that a run-flat tyre driven in run-flat mode must be replaced, not repaired. The reinforced sidewall breaks down internally once the tyre has carried load without adequate inflation pressure, and this damage cannot be detected from the outside.</p><p>FixMyTyreNow provides specialist run-flat replacement across all of {borough}, with technicians carrying stock for common BMW, Mini, and Mercedes-Benz fitments. Average response time is 20 minutes. Prices start from {price} per tyre, inclusive of fitting, balancing, and TPMS reset. Where we hold the correct tyre in stock, replacement can be completed in a single visit. For less common specifications, we can source and deliver within 30 to 60 minutes.</p>',
# 1: transport hub
'<p>Vehicles in {borough} used for airport transfers, long-distance private hire, and regular motorway journeys frequently run on run-flat tyres. The high-speed sustained loading of motorway driving increases the thermal and mechanical stress on run-flat sidewalls more than urban use. A run-flat that develops a pressure fault on the {road1} corridor may complete the journey without visible deflation, but if the TPMS has triggered a warning and the tyre has been driven in underinflated condition for any distance, replacement is required regardless of outward appearance.</p><p>We carry out run-flat replacement across all of {borough}, covering {area1}, {area2}, {area3}, and {area4}. Our technicians have the specialist equipment required to mount and demount reinforced run-flat sidewalls correctly without damaging the alloy rim. The from {price} price covers supply of the replacement tyre, fitting, computerised balancing, and TPMS reset. Average arrival time is 20 minutes.</p>',
# 2: suburban
'<p>Run-flat tyres fitted as original equipment on vehicles sold in {borough} are typically from BMW, Mini, Mercedes-Benz, or Audi. These tyres cannot be repaired after use in run-flat mode and require specific handling equipment that differs from standard tyre fitting machinery. The reinforced sidewall requires higher break-off forces that can damage an alloy wheel if the wrong equipment is used. Using a specialist mobile service for run-flat replacement protects the wheel as well as ensuring the correct specification is fitted.</p><p>FixMyTyreNow provides mobile run-flat replacement across all of {borough}: {area1}, {area2}, {area3}, and {area4}. We stock BMW-approved, Mini-approved, and Mercedes-Benz-approved run-flat tyres from brands including Michelin, Continental, and Bridgestone. The from {price} per tyre price includes fitting, balancing, and TPMS sensor reset. Average arrival time after calling is 20 minutes.</p>',
# 3: residential
'<p>Run-flat equipped vehicles in {borough} often alert their drivers to a tyre pressure issue via the TPMS warning light in circumstances where there is no visible deflation: parked on a driveway, leaving home in the morning, or after a brief stop. The absence of a visible flat tyre leads some drivers to attempt to continue driving, believing the alert is minor. Any continued driving on a run-flat tyre once the TPMS has warned of pressure loss risks permanent sidewall damage. The correct response is to call for mobile replacement.</p><p>We cover all of {borough} for run-flat replacement, responding within an average of 20 minutes. Our technicians carry specialist demounting equipment and a range of run-flat tyres for common vehicles. The from {price} per tyre price covers supply, fitting, balancing, and TPMS reset. We confirm tyre availability and price before dispatch. There is no callout fee.</p>',
# 4: outer suburban
'<p>The {road1} is a regular route for BMW and Mercedes drivers in {borough}, and it is where run-flat pressure alerts are most commonly triggered. A slow puncture on a run-flat tyre may allow the vehicle to continue for a short distance after the alert, but the cumulative damage to the sidewall increases with every mile driven. Most manufacturers specify that run-flat tyres must not be driven more than 50 miles at speeds no greater than 50 mph after a pressure loss, and replacement should happen at the first opportunity.</p><p>FixMyTyreNow covers all areas of {borough} for specialist run-flat replacement. Our technicians carry the correct equipment for reinforced tyre demounting and have stock of run-flat approved tyres for BMW, Mini, and other common vehicles in the borough. The from {price} price includes the tyre, fitting, balancing, and TPMS reset. Average arrival time is 20 minutes.</p>',
# 5: commuter
'<p>Commuter drivers in {borough} with run-flat equipped vehicles often encounter pressure alerts on early morning or late evening runs on {road1} and {road2}. Because run-flat tyres visually maintain their shape even when pressure is critically low, the tendency is to underestimate the urgency. However, manufacturers are clear: a run-flat tyre that has been operated at low pressure, even briefly, must be replaced before the vehicle returns to normal use. The internal structure cannot be inspected without removal and specialist equipment.</p><p>Mobile run-flat replacement covers all of {borough}, including {area1}, {area2}, {area3}, and {area4}. We carry BMW-original-equipment run-flat tyre stock and can source other common specifications within 30 to 60 minutes where not immediately available. Prices start from {price} per tyre, covering supply, fitting, balancing, and TPMS reset. Response time averages 20 minutes from your call.</p>',
# 6: inner-city
'<p>Run-flat equipped vehicles in {borough}\'s inner-city streets encounter the kerb damage and debris punctures that affect any tyre, but with a key difference. The reinforced sidewall of a run-flat tyre is more susceptible to irreparable damage from sidewall impacts than a conventional tyre, and once damage has occurred in that zone, no repair is possible under any circumstances. The same applies if the tyre has been driven on when flat. In both cases, replacement is the only safe outcome.</p><p>FixMyTyreNow provides mobile run-flat replacement across all of {borough}. We attend at residential streets, underground car parks, business addresses, and on roadsides. Our technicians carry specialist equipment for safe alloy-preserving demounting. The from {price} per tyre price covers the replacement run-flat tyre, fitting, balancing, and TPMS reset. Average arrival time is 20 minutes.</p>',
# 7: premium
'<p>In {borough}, where a high proportion of vehicles are premium-branded models, run-flat tyre replacement is one of the more frequent call types we handle. BMW, Mercedes-Benz, Mini, and Porsche all use run-flat specifications as standard on many of their models, and tyre pressure events are accordingly more common. The cost of run-flat replacement is higher than standard tyres, partly because the reinforced construction requires more raw material and partly because the fitting process requires specialist equipment. We are transparent about pricing before we arrive.</p><p>We cover {area1}, {area2}, {area3}, and {area4} for mobile run-flat replacement. Stock includes Michelin Pilot Sport A/S run-flat, Continental ContiSportContact SSR, Pirelli Cinturato run-flat, and Bridgestone DriveGuard for common fitment sizes. Prices start from {price} per tyre and are confirmed by size and brand before dispatch. Fitting, balancing, and TPMS reset are included. Response time averages 20 minutes.</p>',
],

}

# ── SERVICE WHAT SECTION ─────────────────────────────────────────────────────
SERVICE_WHAT = {

'emergency-tyre-replacement': '''<h2>What Emergency Tyre Replacement Includes</h2>
<p>Every emergency callout covers the following as standard:</p>
<ul>
<li><strong>Tyre and wheel assessment on arrival:</strong> the technician inspects the condition of the tyre, the wheel rim, the valve, and the surrounding area before starting work.</li>
<li><strong>Tyre supply:</strong> a replacement tyre matching or exceeding your existing specification is taken from van stock. The brand and price are confirmed with you before fitting begins.</li>
<li><strong>Tyre fitting:</strong> the old tyre is removed and the new tyre is mounted and seated correctly on the rim.</li>
<li><strong>Computerised wheel balancing:</strong> the wheel and tyre assembly is balanced using on-van equipment to within 1 gram of tolerance.</li>
<li><strong>Inflation to specification:</strong> the tyre is inflated to the pressure shown on your vehicle\'s door sill or handbook.</li>
<li><strong>TPMS reset:</strong> where your vehicle has a tyre pressure monitoring system, we reset the sensor after fitting.</li>
<li><strong>Torque check:</strong> all wheel bolts are tightened to the correct torque for your vehicle.</li>
<li><strong>Old tyre removal:</strong> the removed tyre is taken away and sent for recycling at no extra charge.</li>
</ul>
<p>The from £69 price is all-inclusive. There is no callout fee and no charge for balancing or disposal on top of the tyre and fitting cost.</p>''',

'standard-tyre-fitting': '''<h2>What Standard Tyre Fitting Includes</h2>
<p>A standard tyre fitting appointment covers the following in a single visit:</p>
<ul>
<li><strong>Tyre selection advice:</strong> if you are unsure which tyre to choose, the technician can discuss the options for your vehicle and typical usage. All brands and prices are confirmed before any work starts.</li>
<li><strong>Old tyre removal:</strong> the existing tyre is safely broken from the rim and removed.</li>
<li><strong>New tyre mounting:</strong> the replacement tyre is fitted to the rim and the bead is seated correctly.</li>
<li><strong>Computerised wheel balancing:</strong> each fitted wheel is balanced using on-van equipment to ensure smooth running at all speeds.</li>
<li><strong>Inflation to manufacturer specification:</strong> pressures are set according to the figure on your vehicle\'s door sill or in the handbook.</li>
<li><strong>TPMS reset:</strong> where fitted, the tyre pressure monitoring system sensor is reset or re-synced after the new tyre is installed.</li>
<li><strong>Torque check:</strong> all wheel bolts are tightened to the correct specification.</li>
<li><strong>Old tyre disposal:</strong> the removed tyre is taken away and recycled responsibly.</li>
</ul>
<p>Fitting times are approximately 45 minutes per tyre. Two tyres on the same axle are completed in around 75 minutes. Slots are available daily from 06:00 to 22:00. A £10 deposit is taken at booking and deducted from the final invoice.</p>''',

'puncture-repair': '''<h2>How Puncture Repair Works</h2>
<p>A professional puncture repair involves more than inserting a plug from the outside. The industry standard is the two-stage internal plug-and-patch method, as defined by BSAU 144e. Here is what a repair visit involves:</p>
<ul>
<li><strong>Wheel removal:</strong> the wheel is taken off the vehicle so the tyre can be fully inspected from both inside and out.</li>
<li><strong>Tyre demounting:</strong> the tyre is broken from the rim and the inside of the casing is inspected for any damage not visible from outside.</li>
<li><strong>Damage assessment:</strong> the puncture is assessed against the repair criteria. The damage must be in the central tread zone, no larger than 6mm, and the tyre must not have been driven flat. If any of these conditions are not met, repair is not permitted under BSAU 144e.</li>
<li><strong>Internal patch application:</strong> a chemical vulcanising patch is applied to the interior of the tyre casing over the puncture site. This is the primary seal.</li>
<li><strong>External plug insertion:</strong> a rubber plug is inserted through the puncture from inside out to fill the hole in the casing. This is the secondary seal.</li>
<li><strong>Curing:</strong> the repair is allowed to cure before the tyre is remounted.</li>
<li><strong>Remounting and balancing:</strong> the tyre is remounted on the rim, inflated to specification, and balanced.</li>
</ul>
<p>A correctly completed plug-and-patch repair is road-legal for the remaining life of the tyre and does not need to be disclosed when selling the vehicle. Foam sealant products used as a temporary measure can contaminate the inside of the tyre and make professional repair impossible. If you have used sealant, please tell us when you call.</p>''',

'wheel-balancing': '''<h2>How Mobile Wheel Balancing Works</h2>
<p>Wheel balancing corrects the uneven weight distribution around a wheel-and-tyre assembly. Here is what the service involves:</p>
<ul>
<li><strong>Wheel removal:</strong> each wheel is removed from the vehicle and mounted on the on-van balancing machine.</li>
<li><strong>Spin test:</strong> the machine spins the wheel at speed and measures the precise weight distribution across the full circumference of the assembly.</li>
<li><strong>Weight placement calculation:</strong> the machine calculates the exact location and weight of the balancing weights needed to bring the assembly into balance.</li>
<li><strong>Weight application:</strong> clip-on weights are applied to the rim at the calculated positions. Alloy wheels typically use adhesive weights applied to the inner face of the rim to preserve appearance.</li>
<li><strong>Re-check spin:</strong> the wheel is spun again to confirm the balance is within tolerance, typically within 1 gram.</li>
<li><strong>Reinstallation:</strong> the wheel is refitted to the vehicle and torqued to specification.</li>
</ul>
<p>Wheel balancing is different from wheel alignment. Balancing addresses weight distribution around the wheel axis. Alignment addresses the geometry of the wheel relative to the road and the vehicle\'s other wheels. If your vehicle pulls to one side when driving straight, the issue is more likely alignment than balance. Vibration through the steering wheel at speed points to a balance issue. Both can be present at the same time.</p>''',

'run-flat-replacement': '''<h2>Why Run-Flat Replacement Requires Specialist Equipment</h2>
<p>Run-flat tyres have a reinforced sidewall that allows the tyre to support the vehicle\'s weight without air pressure for a limited distance. This reinforcement makes them significantly more resistant to the standard tyre-changing machinery used at most garages and kerbside fitting services. Attempting to demount a run-flat tyre without the correct equipment can crack or permanently deform the bead of the tyre and, more critically, scratch or break the alloy wheel rim.</p>
<p>Our run-flat replacement technicians carry dedicated run-flat capable tools and work to the procedures specified for each vehicle type. Here is what a run-flat replacement involves:</p>
<ul>
<li><strong>TPMS sensor check:</strong> before any work begins, we confirm the pressure sensor is functional and record the current fault code if one is stored.</li>
<li><strong>Specialist demounting:</strong> the run-flat tyre is removed using low-force tooling that preserves the rim finish and does not damage the bead seat.</li>
<li><strong>Rim inspection:</strong> the rim is inspected for any damage caused by operation in run-flat mode. Cosmetic marks are noted and structural damage is flagged.</li>
<li><strong>New tyre mounting:</strong> the replacement run-flat tyre is mounted using the same specialist low-force equipment.</li>
<li><strong>Balancing:</strong> the assembly is balanced using on-van computerised equipment.</li>
<li><strong>TPMS reset:</strong> the pressure sensor is reset to clear the low-pressure warning. Where a relearn procedure is required, this is completed at the same visit.</li>
<li><strong>Torque check:</strong> wheel bolts are tightened to the specification for your vehicle.</li>
</ul>
<p>Run-flat tyres that have been driven in run-flat mode cannot be repaired. The internal structure breaks down under load without adequate pressure and the damage is not visible externally. All run-flat tyres presenting after a pressure event require replacement, regardless of outward appearance.</p>''',

}

# ── FAQ POOLS (15 per service) ─────────────────────────────────────────────────
FAQS = {

'emergency-tyre-replacement': [
{'q': 'How quickly can you reach me in {borough}?',
 'a': 'Our average arrival time across {borough} is 20 minutes from the moment you call. We track the location of all available technicians in real time and dispatch the one closest to you. On the {road1} or in residential areas like {area2}, we typically arrive faster during off-peak hours.'},
{'q': 'My tyre blew out on the {road1}. Can you come to that road?',
 'a': 'Yes. We attend roadside callouts on the {road1} regularly and can reach most points within 20 minutes. If you have broken down on a live carriageway, pull as far left as safely possible, switch on your hazard lights, and stay behind the barrier or in the vehicle with your seatbelt on. Call us with your exact location and the direction you are travelling.'},
{'q': 'I found my tyre flat at home in {area1}. Can you come to a residential address?',
 'a': 'Residential callouts make up a large part of our work in {borough}. We come to your driveway, your residents parking bay, your garage forecourt, or wherever the vehicle is located. You do not need to be on the road for us to help. Just give us your postcode and we will find you.'},
{'q': 'Do you offer emergency tyre replacement at night in {borough}?',
 'a': 'Yes. Our emergency service operates 24 hours a day, 365 days a year. Whether it is 2am in {area2} or 4am near {area3}, we will dispatch a technician to you. There is no premium rate for night-time callouts. The from £69 price applies at any hour.'},
{'q': 'What tyre brands do you carry?',
 'a': 'Our vans carry Michelin, Continental, Pirelli, Bridgestone, and Goodyear for premium fitments, and Hankook, Yokohama, and Falken for mid-range. Budget options from Nexen and Landsail are also available. For less common sizes or specific brand requests, we can source from a local distributor, which typically adds 30 to 60 minutes. All brands are genuine, sourced from authorised UK distributors, and carry the manufacturer\'s warranty.'},
{'q': 'Can I get a tyre replaced in a car park in {area2}?',
 'a': 'Yes. Multi-storey and surface-level car parks are some of our most common callout locations. We attend in {area2}, {area3}, and any other location in {borough} where a car park is accessible to a van. Let us know the car park name or address and the floor level when you call so we can find you quickly.'},
{'q': 'What if I drove on a flat and my wheel might be damaged?',
 'a': 'We assess the wheel rim before fitting a new tyre. Minor kerb damage or light scuffing from driving briefly on a deflated tyre does not usually prevent fitting. If the rim is cracked or severely bent, we will tell you clearly and explain your options. Fitting a tyre on a structurally compromised rim is unsafe, and we do not do it.'},
{'q': 'My car has a locking wheel nut and I cannot find the key. Can you still help?',
 'a': 'If you cannot find your locking wheel nut key, call us and describe the vehicle. In many cases we can identify the key type and may carry a matching removal tool. If the key is completely lost, a specialist lock removal may be needed first, but this is uncommon. Most keys are stored in the glovebox or boot alongside the vehicle documents.'},
{'q': 'What is included in the from £69 price?',
 'a': 'The from £69 price covers the replacement tyre, fitting, computerised wheel balancing, inflation to manufacturer specification, and a torque check on the wheel bolts. Old tyre disposal is included. There is no separate callout fee. The only variable is the tyre brand and specification you choose, which we confirm with you before starting work.'},
{'q': 'How do I pay when the technician arrives?',
 'a': 'A £10 deposit is taken at the time of booking via Revolut, which is deducted from the final invoice. The remaining balance is paid directly to the technician on completion using card, Apple Pay, Google Pay, or bank transfer. Cash is not accepted. You will receive a written receipt for the full amount.'},
{'q': 'Do you fit run-flat tyres as part of the emergency service in {borough}?',
 'a': 'Run-flat tyres require specialist demounting equipment not carried on standard emergency vans. If you call with a run-flat fitment, we will confirm whether a run-flat capable technician is available in your area of {borough}. In most cases we can assist, though lead time may be slightly longer. The run-flat replacement service starts from £110.'},
{'q': 'What should I do while waiting for the technician?',
 'a': 'If you are on a public road, stay in the vehicle with your seatbelt fastened and hazard lights on. If you are in a car park or on your driveway, you can go indoors if preferred. The technician will call you when they are around five minutes away. Keep your phone close and have the vehicle registration ready if you know it.'},
{'q': 'Can you replace van or commercial vehicle tyres in {borough}?',
 'a': 'Yes. We carry tyres for most light commercial vans including Ford Transit, Mercedes Sprinter, Volkswagen Transporter, and similar models. Load-rated van tyres are stocked across common sizes. Larger commercial vehicles may need a specialist booking; call us with the vehicle type and axle configuration and we will advise on availability.'},
{'q': 'Do you provide a receipt for insurance or business claims?',
 'a': 'Yes. A full receipt specifying the tyre brand, size, price, fitting cost, and date of work is provided for every job. This can be sent by email at the time of completion or issued as a printed receipt. For business use, we can address the invoice to a company name and VAT number if required.'},
{'q': 'What if you do not have my tyre size in stock?',
 'a': 'We hold the most common tyre sizes for most vehicles across all vans. If your size is unusual or you require a specific brand not in stock, we can typically source it from a nearby distributor depot within 30 to 60 minutes. We confirm availability before dispatch so there are no surprises on arrival.'},
],

'standard-tyre-fitting': [
{'q': 'How do I know when my tyres need replacing in {borough}?',
 'a': 'UK law requires a minimum tread depth of 1.6mm across the central three-quarters of the tyre width. However, tyre performance, particularly wet weather braking, drops noticeably below 3mm. Most manufacturers and road safety organisations recommend replacement at 3mm. Use a tread depth gauge, available from any motorist supplier for a few pounds, or ask your technician to measure during any service visit.'},
{'q': 'Can you fit new tyres at my home in {area1}?',
 'a': 'Yes. Standard tyre fitting is available at any accessible location in {borough}, including driveways, residential parking bays, garages, and workplace car parks. The van carries the tools and equipment to complete the full fitting, balancing, and disposal process on-site. You do not need a flat or level surface, just enough clearance for the technician to work safely around each wheel.'},
{'q': 'How long does standard tyre fitting take?',
 'a': 'A single tyre takes approximately 45 minutes including removal of the old tyre, mounting, seating, balancing, inflation, and torque checking. Two tyres on the same axle take around 75 to 90 minutes. A full set of four takes approximately 2 to 2.5 hours. We will give you an estimated completion time when you book.'},
{'q': 'What tyre brands do you offer and how do they differ?',
 'a': 'We stock premium brands including Michelin, Continental, Pirelli, and Bridgestone, which offer the best wet and dry performance and the longest tread life. Mid-range brands such as Hankook, Yokohama, and Falken provide good performance at a lower price point. Budget brands including Nexen and Landsail meet the legal requirements and are suitable for lower-mileage vehicles. All brands are genuine and carry the manufacturer\'s warranty.'},
{'q': 'Do you book same-day tyre fitting in {borough}?',
 'a': 'Yes. Same-day slots are available across {borough} subject to technician availability. Booking in the morning generally secures a same-day visit. The booking process requires a £10 deposit to confirm the slot. For next-day and advance bookings, slots run from 06:00 to 22:00.'},
{'q': 'What is included in the from £65 fitting price?',
 'a': 'The from £65 price covers the tyre itself, removal of the old tyre, mounting and seating of the new one, computerised wheel balancing, inflation to manufacturer specification, TPMS reset where required, and a torque check on the wheel bolts. The old tyre is taken away and recycled. There are no extra charges for balancing or disposal on top of the tyre price.'},
{'q': 'Can you rotate my tyres when you fit new ones?',
 'a': 'Yes. If you are fitting new tyres to one axle and want to move the existing tyres to the other axle at the same time, we can do this in the same visit. The cost is the fitting charge for the new tyres plus a balancing charge for the moved tyres. Let us know when booking so the technician allows the correct time.'},
{'q': 'What happens to my old tyres?',
 'a': 'All tyres removed during a standard fitting are taken away by the technician at no extra charge and disposed of through a licensed tyre recycling facility. You do not need to arrange disposal yourself.'},
{'q': 'Do you do seasonal tyre changes in {borough}?',
 'a': 'Yes. If you run a second set of seasonal tyres on a separate set of wheels, we can swap them over at your location. The visit covers removal of the current set, fitting of the seasonal set, balancing, and inflation. Pricing is the fitting charge per tyre. If the tyres are already mounted on rims, the visit is faster and costs less than a full swap from loose tyres.'},
{'q': 'Is the same tyre fitting service available for electric vehicles?',
 'a': 'Yes. Electric vehicles use standard tyre sizes and the fitting process is the same as for conventional vehicles. Some EVs require load-rated tyres to handle the additional weight of the battery pack, and some use noise-reducing foam-lined tyres. We check the specification for your vehicle before fitting to ensure the replacement meets the manufacturer\'s requirements.'},
{'q': 'Can you fit tyres for a vehicle with a TPMS system?',
 'a': 'Yes. All tyre fittings include a TPMS sensor check and reset where the system requires it. On most vehicles, the TPMS relearns the new tyre pressure automatically after a short drive. On some BMW, Mercedes, and VAG group vehicles, a manual reset procedure is needed. Our technicians carry the tools to complete this on-site.'},
{'q': 'What if my vehicle has different size tyres on front and rear?',
 'a': 'Staggered fitments, where the front and rear tyres are different sizes, are common on performance cars including BMW M-series and Porsche 911. We handle staggered fitments routinely. Let us know the front and rear sizes when you book so we carry the correct stock. Tyre rotation is not recommended on staggered fitments due to the size difference.'},
{'q': 'How soon can I drive after new tyres are fitted?',
 'a': 'You can drive immediately after fitting. There is no curing time required for new tyres. We recommend a steady first 100 miles while the new tyre beds into the rim and the tread compounds reach their optimal operating characteristics. This means avoiding hard cornering and heavy braking during that initial period where possible.'},
{'q': 'Can I book tyre fitting for early morning in {borough}?',
 'a': 'Yes. Slots are available from 06:00 daily across {borough}. Early morning bookings are popular with drivers who want their tyres changed before starting a commute or a long journey. Book the previous day to secure the specific time you need. The £10 deposit confirms the slot.'},
{'q': 'What if the tyre I want is not in stock on the day?',
 'a': 'If a specific brand or size is not immediately available on the van, we can source it from a distribution depot, typically within 30 to 60 minutes in {borough}. We confirm availability when you book so you know before the technician arrives whether the tyre will be on the van or needs sourcing.'},
],

'puncture-repair': [
{'q': 'Can you repair a nail puncture in the tread of my tyre?',
 'a': 'Yes, provided the nail has penetrated the central tread area and the hole is no larger than 6mm. These are the most common repair cases. We remove the nail, carry out a full internal inspection, and apply a two-stage plug-and-patch repair to BSAU 144e standard. If the nail has caused any delamination or internal damage visible inside the tyre, repair is not safe and we will tell you so.'},
{'q': 'My tyre has a slow puncture. How do I know if it can be repaired?',
 'a': 'A slow puncture that can be repaired typically involves a small object like a nail or screw in the central tread area. The tyre has been losing pressure but has not been driven completely flat. If you have kept the vehicle still and not driven on the flat, the casing is more likely to be in good condition and repair is more likely to be possible. Call us and we will assess when we arrive.'},
{'q': 'I drove on a flat. Can the tyre still be repaired?',
 'a': 'Driving on a flat tyre almost always rules out repair. Once a tyre has carried the vehicle\'s weight without air pressure, the sidewall and casing typically sustain internal damage that cannot be patched. The damage is not always visible from the outside. When we inspect the inside of the tyre, we can confirm whether repair is possible. In most cases where a vehicle has been driven on a flat, replacement is the only safe option.'},
{'q': 'Can you repair a tyre with sidewall damage?',
 'a': 'No. Sidewall damage is not repairable under BSAU 144e guidelines. The sidewall flexes continuously as the tyre rolls, and a repair patch in that zone would be subject to constant movement that would break down the repair. Any tyre with a cut, bulge, or crack in the sidewall needs to be replaced. Attempting to repair sidewall damage is specifically prohibited by the standard.'},
{'q': 'Is a repaired tyre as safe as a new one?',
 'a': 'A correctly completed plug-and-patch repair to BSAU 144e standard restores the tyre\'s full structural integrity within the repaired zone. The tyre can be used at normal speeds and loads for its remaining tread life without restriction. The repair does not need to be disclosed when selling the vehicle. Only one repair per tyre is permitted in the central zone under the standard.'},
{'q': 'I used foam tyre sealant from a can. Can the tyre still be professionally repaired?',
 'a': 'Foam sealant contaminates the inside of the tyre casing and the wheel rim, making professional inspection and repair very difficult. In most cases, a tyre that has had sealant applied cannot be repaired because the interior cannot be properly assessed or the patch will not bond to a contaminated surface. If you have used sealant, tell us when you call. We will advise whether assessment is possible or whether replacement is the more practical route.'},
{'q': 'How much does puncture repair cost in {borough}?',
 'a': 'Puncture repair costs from £25 per tyre. This covers the full assessment, removal of the object causing the puncture, internal and external inspection, two-stage plug-and-patch repair, remounting, balancing, and inflation to specification. There is no callout fee on top of this price. If the tyre cannot be repaired and you want a replacement, the fitting price starts from £65 and the repair assessment charge is not added to the replacement cost.'},
{'q': 'How long does a puncture repair take?',
 'a': 'A single tyre repair takes approximately 30 minutes from arrival. This covers wheel removal, tyre demounting, internal inspection, repair application, curing, remounting, balancing, and refitting. If the assessment shows the tyre is not repairable and you want a replacement tyre fitted in the same visit, the total time will be around 45 minutes.'},
{'q': 'Can you repair a run-flat tyre?',
 'a': 'Run-flat tyres cannot be repaired once they have been used in run-flat mode. The reinforced sidewall sustains internal damage that is not visible externally but makes repair unsafe. If a run-flat tyre has received a puncture but has not been driven while flat, and the TPMS alert has not triggered, there is a small possibility of repair, but this needs assessment on a case-by-case basis. Most run-flat punctures result in replacement.'},
{'q': 'Do you come to me for a puncture repair or do I need to bring the wheel to you?',
 'a': 'We come to you. Whether your car is in {area1}, outside your home in {area3}, or in a car park, we attend with the full repair equipment on the van. You do not need to remove the wheel yourself or transport anything. Average arrival time in {borough} is 20 minutes.'},
{'q': 'Can you repair a puncture on a {vehicle} tyre?',
 'a': 'Yes. The BSAU 144e repair standard applies to all passenger car and light commercial vehicle tyres. We repair punctures on car tyres, SUV and 4x4 tyres, and most van tyre sizes. For larger or specialist tyres, call us with the tyre details and we will confirm whether we can assist.'},
{'q': 'What is the BSAU 144e standard?',
 'a': 'BSAU 144e is the British Standard that defines the criteria and method for safe tyre repair in the UK. It specifies that repairs are only permitted in the central tread area, for damage no larger than 6mm, using a two-stage internal plug-and-patch method. Repairs outside these criteria are not permitted under the standard. Any repair we complete meets this standard as a minimum.'},
{'q': 'Will a repaired tyre affect my MOT?',
 'a': 'A correctly completed puncture repair does not affect an MOT result, provided the tyre meets all other requirements including minimum tread depth, no cracking, no bulging, and no visible structural damage. The repair itself is not a fail condition. An MOT examiner checking the tyre will not necessarily know it has been repaired unless they look specifically for it.'},
{'q': 'Can you repair the spare tyre from my boot?',
 'a': 'Yes. If you have a spare tyre that has been punctured and you would like it repaired for future use, we can carry out the assessment and repair in the same way as any other tyre. Bring the wheel out for the technician when they arrive and we will include it in the same visit at the standard price.'},
{'q': 'My tyre keeps losing pressure but I cannot find a nail. What is causing it?',
 'a': 'Slow pressure loss without an obvious cause can have several explanations: a very small nail or wire that is hard to see, a faulty or corroded valve core, a slow rim leak where the tyre bead no longer seals perfectly against the wheel, or in rare cases, a crack in the wheel itself. We can identify the cause when we remove and inspect the tyre. Valve replacements and bead seals are included in the repair or fitting visit at no extra charge where needed.'},
],

'wheel-balancing': [
{'q': 'How do I know if my wheels need balancing?',
 'a': 'The most common symptom is a vibration felt through the steering wheel at speeds between 60 and 70 mph that was not present before. Uneven tyre wear, particularly on the outer or inner tread blocks, is another indicator. If you have recently had a new tyre fitted without balancing, or if a balancing weight has fallen off, the imbalance can develop suddenly. Any of these signs are a good reason to book a mobile balancing check.'},
{'q': 'Can unbalanced wheels damage my tyres?',
 'a': 'Yes. An out-of-balance wheel causes the tyre to vibrate as it rolls, creating a cyclical loading pattern that wears down specific tread blocks faster than others. This produces the cupping or scalloping pattern sometimes seen on tyres with chronic balance issues. In addition to shortening tyre life, the vibration transfers load through the wheel bearings and steering components, increasing wear on those parts over time.'},
{'q': 'Do new tyres need to be balanced when fitted?',
 'a': 'Yes. Every new tyre should be balanced as part of the fitting process. The weight distribution of any tyre, even a new one, is not perfectly even from the factory. The machine-applied balancing weights correct for the variation in both the tyre and the wheel. Any fitting that does not include balancing leaves the assembly potentially out of balance from the start.'},
{'q': 'How often should wheel balancing be checked?',
 'a': 'After every new tyre fitting, after any significant impact such as a kerb strike or pothole, and every 10,000 to 12,000 miles as a maintenance item. If you drive on the {road1} or {road2} regularly, the higher frequency of pothole impacts may mean more frequent checks are justified. The cost is low relative to the tyre wear it prevents.'},
{'q': 'Is wheel balancing the same as wheel alignment?',
 'a': 'No. Wheel balancing corrects the weight distribution of the wheel-and-tyre assembly around its rotation axis. Wheel alignment, also called tracking, adjusts the angle at which each wheel makes contact with the road surface relative to the vehicle\'s geometry. Symptoms overlap: both can cause uneven tyre wear and pulling to one side. But the solutions are different. We offer balancing as a mobile service. Alignment requires a four-wheel alignment rig and a fixed workshop.'},
{'q': 'Can you balance all four wheels in one visit?',
 'a': 'Yes. Our standard mobile balancing visit covers all four wheels. We remove each wheel, spin it on the balancing machine, apply or adjust weights, and refit in sequence. Four wheels typically take around 30 minutes to complete. If you want to include just the front or just the rear axle, that is also possible and priced per wheel from £15.'},
{'q': 'My car vibrates at high speed on the {road1}. Is it definitely a balance issue?',
 'a': 'High-speed vibration is the most common symptom of wheel imbalance, but it can also be caused by wheel alignment issues, worn tyres with flat spots, worn suspension components, or wheel bearing wear. Balancing is the first and least expensive check to make. If balancing resolves the vibration, the problem is confirmed. If it does not, we can advise on what to investigate next.'},
{'q': 'Can balancing weights fall off?',
 'a': 'Yes. Clip-on weights applied to the inner edge of standard steel and alloy wheels can be dislodged by kerb contact, car wash equipment, or road debris. Adhesive weights on alloy wheels are more resilient to kerb contact but can be affected by high-pressure washes. When a weight is lost, the wheel immediately goes out of balance. A new vibration that appeared after a car wash or a kerb strike is a strong indicator that a weight has been dislodged.'},
{'q': 'Do you use the correct weights for alloy wheels?',
 'a': 'Yes. Alloy wheels are typically balanced using adhesive weights applied to the inner face of the rim. This avoids the clip damage that standard lead weights can cause to alloy finishes. Our technicians carry both clip-on weights and adhesive weights and apply the correct type for your wheel style. We do not use clip-on weights on alloy rims where adhesive placement is possible.'},
{'q': 'How much does wheel balancing cost in {borough}?',
 'a': 'Wheel balancing is priced from £15 per wheel. All four wheels cost from £60 in total. There is no callout fee on top of this price. The full visit typically takes 30 to 40 minutes. A £10 booking deposit is taken when you schedule the appointment and is deducted from the final invoice.'},
{'q': 'Can wheel imbalance affect fuel consumption?',
 'a': 'Yes, though the effect is modest. An out-of-balance wheel creates a cyclical oscillation that requires the engine to work slightly harder to maintain speed, particularly at motorway speeds. The resistance is small but measurable over the course of a high-mileage year. Correcting balance is not a meaningful fuel-saving exercise on its own, but it contributes to overall vehicle efficiency alongside correct tyre pressure and alignment.'},
{'q': 'Do electric vehicles need wheel balancing?',
 'a': 'Yes. Electric vehicles require wheel balancing in exactly the same way as conventional vehicles. In fact, because EVs are heavier due to battery weight, tyre and wheel balance is arguably more important because the higher loads amplify vibration effects. Many EV manufacturers also specify noise-reducing foam-lined tyres that need careful balancing. We handle EV tyres and wheels in the same way as conventional vehicles.'},
{'q': 'Can you balance a spare wheel?',
 'a': 'Yes. If you have a full-size spare wheel and tyre and you want it balanced, we can include it in the same visit. This is worth doing if you rotate tyres or if the spare has not been balanced since it was last used. Space-saver spares should not be balanced for regular use but we can check the assembly condition.'},
{'q': 'What is the tolerance for a correctly balanced wheel?',
 'a': 'The industry standard for wheel balance is within 1 gram of the target weight distribution across the full circumference. Our computerised balancing machines measure and correct to within this tolerance. A wheel balanced to 1 gram will produce no measurable vibration at any road speed within the vehicle\'s legal operating range.'},
{'q': 'Can you balance my wheels at my workplace in {area1}?',
 'a': 'Yes. We attend workplaces, office car parks, and industrial estates across {borough} including in {area1}. The balancing equipment is fully mobile and van-mounted. You do not need a garage or workshop. A level surface with enough clearance to work around the vehicle is sufficient.'},
],

'run-flat-replacement': [
{'q': 'How do I know if my car has run-flat tyres?',
 'a': 'Run-flat tyres are marked on the sidewall with a manufacturer-specific code. BMW approved run-flats carry an asterisk (*) marking. Continental run-flats are labelled SSR (Self Supporting Runflat). Bridgestone run-flats use RFT. Michelin uses ZP (Zero Pressure). Goodyear uses ROF (Run On Flat). Most vehicles with run-flat tyres also lack a spare wheel. If your car has no spare and the TPMS light is on, the tyre is almost certainly a run-flat fitment.'},
{'q': 'Can run-flat tyres be repaired after a puncture?',
 'a': 'In most cases, no. A run-flat tyre that has been driven in run-flat mode, even briefly, has sustained internal sidewall damage that cannot be repaired. The damage is not visible externally. Tyres from vehicles where the TPMS has triggered a low-pressure warning must be treated as potentially damaged internally, regardless of whether the vehicle was driven on after the alert. A small number of run-flat tyres with a puncture that was caught immediately before any run-flat use may be assessable for repair, but this needs case-by-case evaluation.'},
{'q': 'Why does run-flat tyre replacement cost more than standard fitting?',
 'a': 'Run-flat tyres cost more than equivalent standard tyres because the reinforced sidewall requires additional materials and manufacturing precision. The fitting process also takes longer because specialist low-force demounting equipment is needed to safely remove the reinforced bead without damaging the alloy wheel rim. The from £110 price reflects the combined tyre cost and the specialist fitting charge.'},
{'q': 'Which vehicles in {borough} commonly have run-flat tyres?',
 'a': 'BMW has been the most widespread user of run-flat tyres since around 2003 and supplies most models with run-flat equipment as standard. Mini, which shares platforms with BMW, also uses run-flats broadly. Mercedes-Benz A-Class, C-Class, and E-Class models frequently carry run-flat fitments on larger wheel options. Audi A4 and A6 variants, Porsche Cayenne and Macan, and some Land Rover Evoque and Velar models also use run-flat specifications. If you drive any of these vehicles in {borough} and do not have a spare wheel in the boot, you almost certainly have run-flats.'},
{'q': 'What should I do if my TPMS light comes on in {borough}?',
 'a': 'Do not ignore it and do not continue driving at normal speed or for a long distance. Pull over safely as soon as possible and call us. If the tyre is visibly flat, the run-flat may already be at or past the end of its usable deflated range. If the tyre looks normal and you have just noticed the warning, you may have a short window before the casing sustains irreparable damage. In either case, calling for immediate mobile replacement in {borough} is the safest response.'},
{'q': 'How far can I drive on a run-flat tyre with the TPMS warning on?',
 'a': 'The standard manufacturer guideline is a maximum of 50 miles at no more than 50 mph after a pressure loss is detected. This is a conservative maximum under ideal conditions, not a reliable safe range for all scenarios. The actual limit depends on the severity of the pressure loss, the ambient temperature, the load in the vehicle, and the road surface. Treating the 50-mile figure as an absolute limit rather than a target is the safer approach.'},
{'q': 'Can you come to me in {area2} for a run-flat replacement?',
 'a': 'Yes. We cover all of {borough} including {area1}, {area2}, {area3}, and {area4} for run-flat replacement. Our average arrival time is 20 minutes. When you call, give us your location, vehicle make and model, and any tyre size information you have. We will confirm which run-flat tyre we have in stock for your fitment before dispatch.'},
{'q': 'Do you need to reset the TPMS after replacing a run-flat tyre?',
 'a': 'Yes. The TPMS sensor must be reset after any tyre change on a vehicle equipped with the system. On most vehicles, the reset is done via a button sequence or a menu option on the dashboard. On BMW, some Mercedes-Benz, and some Porsche models, a tyre-specific relearn procedure is required that the technician completes using a dedicated TPMS reset tool. We carry this equipment and include the reset as part of every run-flat replacement.'},
{'q': 'What brands of run-flat tyres do you stock?',
 'a': 'Our technicians carry Michelin Pilot Sport A/S, Continental ContiSportContact SSR, Pirelli P Zero runflat, and Bridgestone DriveGuard across the most common sizes. For less common fitments, such as very large diameter or unusual aspect ratios, we may need to source from a distributor, which typically takes 30 to 60 minutes in {borough}. All tyres are genuine, sourced from authorised UK distributors.'},
{'q': 'Is it safe to fit a non-run-flat tyre in place of a run-flat on my BMW?',
 'a': 'Technically possible but not recommended by BMW. Fitting a conventional tyre in place of a run-flat means the TPMS will still alert for pressure loss, but if a puncture occurs at speed, there is no run-flat capability. BMW specifically advises against mixing run-flat and non-run-flat tyres on the same vehicle. If budget is a concern, there are own-brand run-flat options available at lower price points than OEM-approved brands that still carry the required specification.'},
{'q': 'Can my alloy wheels be damaged when removing a run-flat tyre?',
 'a': 'Incorrect removal technique can scratch or crack alloy wheel rims. Run-flat tyres require more force to break the bead than standard tyres, and using standard tyre irons on an alloy rim can cause permanent cosmetic or structural damage. Our technicians use low-force run-flat specific demounting tools and follow procedures that prioritise rim protection. We inspect the rim before and after removal and advise if any damage is present.'},
{'q': 'I only need one run-flat tyre replaced. Do you match the brand on the other tyres?',
 'a': 'We recommend matching the same tyre brand and model on the same axle where possible, as mixing different compounds can affect handling balance, particularly during emergency manoeuvres. If an exact match is not available immediately, we will fit the nearest equivalent specification in the same performance category and advise on sourcing an exact match if you prefer. We never fit a standard tyre to replace a run-flat without your explicit consent and a clear explanation of the implications.'},
{'q': 'How long does run-flat replacement take?',
 'a': 'A single run-flat tyre typically takes 45 to 55 minutes to replace, slightly longer than a standard tyre due to the specialist demounting process and the TPMS reset procedure. Two tyres on the same axle take approximately 80 to 90 minutes. We will give you a realistic time estimate when you call.'},
{'q': 'Can you replace run-flat tyres on a BMW in {area1}?',
 'a': 'Yes. We carry BMW-fitment run-flat tyres as a standard stock item and attend callouts across {borough}, including {area1}, {area2}, and {area3}. For the most common BMW sizes such as 225/45 R18, 245/40 R18, and 225/40 R19, we typically hold stock on the van. For larger or less common fitments, we source from a nearby depot within 30 to 60 minutes.'},
{'q': 'Does run-flat replacement affect my BMW or Mini warranty?',
 'a': 'Fitting a non-OEM-approved run-flat tyre that meets the required specification does not void your vehicle warranty for unrelated items. However, if tyre-related damage occurs to suspension components or wheel bearings and a non-approved tyre was fitted, the manufacturer may decline a warranty claim on those items. Fitting a BMW-approved star-marked run-flat from any brand protects your position. We stock approved-specification run-flat tyres and confirm the approval status before fitting.'},
],

}

# ── POSTCODE DATA ──────────────────────────────────────────────────────────────
POSTCODES = {b: d['pc'] for b, d in BOROUGHS_DICT.items()}

# ── HELPERS ───────────────────────────────────────────────────────────────────
def fill(text, b, svc):
    """Substitute placeholders. No emdash anywhere."""
    pc = b.get('pc', [])
    return (text
        .replace('{borough}', b['name'])
        .replace('{road1}',   b['road1'])
        .replace('{road2}',   b['road2'])
        .replace('{road3}',   b.get('road3', b['road2']))
        .replace('{area1}',   b['area1'])
        .replace('{area2}',   b['area2'])
        .replace('{area3}',   b['area3'])
        .replace('{area4}',   b['area4'])
        .replace('{vehicle}', b.get('vehicle', 'cars and vans'))
        .replace('{pc1}',     pc[0] if len(pc) > 0 else '')
        .replace('{pc2}',     pc[1] if len(pc) > 1 else '')
        .replace('{pc3}',     pc[2] if len(pc) > 2 else '')
        .replace('{price}',   svc['price'])
        .replace('\u2014', '-')   # em dash
        .replace('\u2013', '-')   # en dash
        .replace('--', '-')
    )


def get_faqs(service_slug, borough_idx):
    pool = FAQS[service_slug]
    rng = random.Random(borough_idx * 31 + SERVICE_LIST.index(service_slug) * 97)
    shuffled = pool[:]
    rng.shuffle(shuffled)
    return shuffled[:5]


def generate_main_content(borough_slug, service_slug, b_idx):
    b   = BOROUGHS_DICT[borough_slug]
    svc = SERVICES[service_slug]

    intro_templates = INTROS[service_slug]
    tmpl_idx = b.get('tmpl', 0) % len(intro_templates)
    intro_html = fill(intro_templates[tmpl_idx], b, svc)

    what_html = fill(SERVICE_WHAT[service_slug], b, svc)

    faqs = get_faqs(service_slug, b_idx)
    faq_items = []
    for fq in faqs:
        q = fill(fq['q'], b, svc)
        a = fill(fq['a'], b, svc)
        faq_items.append(
            f'<details class="faq-item">\n'
            f'<summary>{q}</summary>\n'
            f'<p>{a}</p>\n'
            f'</details>'
        )

    pc_chips = ''.join(
        f'<span class="postcode-chip">{pc}</span>'
        for pc in b.get('pc', [])
    )

    content = (
        f'<section class="borough-intro">\n'
        f'<h2>{svc["name"]} in {b["name"]}</h2>\n'
        f'{intro_html}\n'
        f'</section>\n\n'

        f'<section class="service-what">\n'
        f'{what_html}\n'
        f'</section>\n\n'

        f'<section class="borough-local">\n'
        f'<h2>Areas and Postcodes We Cover in {b["name"]}</h2>\n'
        f'<p>Our mobile technicians serve every part of {b["name"]}, including '
        f'{b["area1"]}, {b["area2"]}, {b["area3"]}, and {b["area4"]}. '
        f'We know the local roads, including the {b["road1"]} and {b["road2"]}, '
        f'and can reach you at any accessible location within the borough. '
        f'Average arrival time after your call is 20 minutes.</p>\n'
        f'<div class="postcode-chips">{pc_chips}</div>\n'
        f'</section>\n\n'

        f'<section class="borough-faq">\n'
        f'<h2>Questions about {svc["name"]} in {b["name"]}</h2>\n'
        + '\n'.join(faq_items) +
        f'\n</section>'
    )

    # Final emdash sweep
    content = content.replace('\u2014', '-').replace('\u2013', '-')
    return content


# ── PAGE UPDATE ───────────────────────────────────────────────────────────────
# Pattern: replace from <section class="borough-intro"> to end of </section>
# before <section class="borough-cta">
REPLACE_PAT = re.compile(
    r'<section class="borough-intro">.*?</section>\s*\n\s*(?=<section class="borough-cta">)',
    re.DOTALL
)

# Fallback: find sections individually and replace up to borough-faq closing
REPLACE_PAT2 = re.compile(
    r'<section class="borough-intro">.*?</section>\s*\n',
    re.DOTALL
)


def update_file(filepath, borough_slug, service_slug, b_idx):
    content = open(filepath, encoding='utf-8').read()

    new_sections = generate_main_content(borough_slug, service_slug, b_idx) + '\n\n'

    # Try primary pattern first (everything between borough-intro and borough-cta)
    replaced = REPLACE_PAT.sub(new_sections, content, count=1)
    if replaced != content:
        open(filepath, 'w', encoding='utf-8').write(replaced)
        return 'ok'

    # Fallback: replace sections one by one
    # Find the span from first <section class="borough-intro"> to last </section> before borough-cta
    cta_pos = content.find('<section class="borough-cta">')
    intro_pos = content.find('<section class="borough-intro">')
    if cta_pos > 0 and intro_pos > 0 and intro_pos < cta_pos:
        # Find the last </section> before the CTA
        region = content[intro_pos:cta_pos]
        # Remove all the old sections
        new_content = content[:intro_pos] + new_sections + content[cta_pos:]
        open(filepath, 'w', encoding='utf-8').write(new_content)
        return 'ok-fallback'

    return 'failed'


# ── MAIN ──────────────────────────────────────────────────────────────────────
stats = {'ok': 0, 'ok-fallback': 0, 'failed': 0, 'missing': 0}

for b_idx, (borough_slug, _) in enumerate(BOROUGHS):
    for service_slug in SERVICE_LIST:
        filepath = f'areas/{borough_slug}/{service_slug}/index.html'
        if not os.path.exists(filepath):
            print(f'  [missing] {filepath}')
            stats['missing'] += 1
            continue

        result = update_file(filepath, borough_slug, service_slug, b_idx)
        stats[result] = stats.get(result, 0) + 1
        if result == 'failed':
            print(f'  [FAILED] {filepath}')

total = sum(stats.values())
print(f'\nTotal pages: {total}')
for k, v in stats.items():
    if v: print(f'  {k}: {v}')
