"""
Expand all 5 service pages with substantive, expert content (800+ words).
Replaces the thin 3-paragraph body content with full service guides.
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SERVICE_CONTENT = {

'standard-tyre-fitting': """
<div class="service-content">
<h2>What Is Standard Tyre Fitting?</h2>
<p>Standard tyre fitting is the process of removing your existing tyres and mounting new ones on your vehicle's wheels. At FixMyTyreNow, we bring a fully equipped mobile fitting van directly to your location across all 32 London boroughs — no garage visit required. A full standard tyre fitting takes approximately 45 minutes per tyre and includes removal of the old tyre, mounting of the new tyre, computerised wheel balancing, inflation to the manufacturer's recommended pressure, and a torque check on all wheel bolts.</p>

<h2>What's Included in Every Standard Tyre Fit</h2>
<ul>
<li><strong>Old tyre removal</strong> — the wheel is removed from your vehicle and the existing tyre broken off the rim safely</li>
<li><strong>New tyre mounting</strong> — the replacement tyre is seated on the rim and bead sealed</li>
<li><strong>Computerised wheel balancing</strong> — weights are applied to eliminate vibration at speed</li>
<li><strong>Inflation to spec</strong> — pressures set to your vehicle manufacturer's recommendation (found on the door sill sticker)</li>
<li><strong>Torque check</strong> — all wheel bolts tightened to the correct torque specification using a calibrated wrench</li>
<li><strong>TPMS reset</strong> — where applicable, we reset your tyre pressure monitoring system warning light</li>
</ul>

<h2>Tyre Brands We Stock</h2>
<p>Our vans carry a curated stock of the most common tyre sizes across all major brand tiers. Premium brands include <strong>Michelin</strong>, <strong>Continental</strong>, <strong>Pirelli</strong>, <strong>Bridgestone</strong>, and <strong>Goodyear</strong>. Mid-range options include <strong>Hankook</strong>, <strong>Yokohama</strong>, and <strong>Falken</strong>. Budget alternatives from <strong>Nexen</strong>, <strong>Landsail</strong>, and <strong>Radar</strong> are also available. All tyres are sourced from authorised UK distributors and carry the full manufacturer's warranty.</p>
<p>If your vehicle requires a less common size or a specific brand not held in stock, we can usually source it from a nearby distribution depot within 30–60 minutes. We'll confirm availability and price before dispatch so there are no surprises.</p>

<h2>How to Choose the Right Tyres</h2>
<p>Your tyre size is printed on the sidewall of your existing tyres in a format such as <strong>205/55 R16 91V</strong>. The first number is the width in millimetres, the second is the aspect ratio (sidewall height as a percentage of width), R indicates radial construction, the third number is the rim diameter in inches, and the final number and letter indicate load index and speed rating. Always replace tyres with the same size, or consult your vehicle handbook for approved alternatives.</p>
<p>As a general rule: if you drive mostly in the city at lower speeds, a mid-range tyre will perform comparably to a premium brand in those conditions. If you regularly use motorways or drive a performance vehicle, the handling differences between budget and premium tyres become more significant, particularly in wet conditions. Our technicians can advise you on the best option for your driving pattern and vehicle when they arrive.</p>

<h2>When to Replace Your Tyres</h2>
<p>UK law requires a minimum tread depth of <strong>1.6mm</strong> across the central three-quarters of the tyre's width. Driving on tyres below this limit carries a fine of up to £2,500 per tyre and three penalty points on your licence. In practice, tyre performance — particularly braking distances in wet conditions — begins to deteriorate significantly below 3mm. Most tyre manufacturers recommend replacement at 3mm rather than waiting until the legal minimum.</p>
<p>Beyond tread depth, replace tyres if you observe any of the following: cracks or bulges in the sidewall, damage from kerb impacts, a tyre that repeatedly loses pressure, vibration that persists after balancing, or any tyre over 10 years old regardless of apparent condition. Age degrades the rubber compounds even when tread depth appears adequate.</p>

<h2>Same-Day and Emergency Standard Fitting</h2>
<p>Standard tyre fitting is available same-day across all London boroughs. For non-urgent replacements — worn tyres, seasonal changeovers, or scheduled replacements — book a convenient slot online and our technician will arrive within the agreed window. For situations where a tyre has been driven to failure or is unsafe to drive on, we dispatch in emergency mode with the same 20-minute average arrival time as our emergency replacement service.</p>
<p>All appointments require a £10 deposit at booking, which is deducted from your final invoice. The balance is payable on completion by card, Apple Pay, Google Pay, or bank transfer.</p>

<h2>Frequently Asked Questions</h2>
<details><summary>Do I need to be present while the tyres are fitted?</summary><p>Yes. We require the vehicle owner or an authorised representative to be present to confirm the work before we begin and to make payment on completion. You don't need to stay with the van — you can go back indoors — but we do need someone reachable by phone.</p></details>
<details><summary>Can you fit run-flat tyres as standard fitting?</summary><p>Run-flat tyre replacement is a specialist service due to the additional equipment required to break the reinforced sidewall. It is available from £110 and is listed separately. If you're unsure whether your tyres are run-flats, check for an RFT, ROF, or SSR marking on the sidewall.</p></details>
<details><summary>Will you dispose of my old tyres?</summary><p>Yes. We take old tyres away and dispose of them through a licensed tyre recycling facility at no extra charge. You don't need to arrange disposal yourself.</p></details>
<details><summary>How long does a standard tyre fitting take?</summary><p>Fitting a single tyre takes approximately 30–45 minutes including balancing. Two tyres on the same axle take around 60–75 minutes. We aim to complete the job and be off your driveway or car park within the hour.</p></details>
</div>
""",

'emergency-tyre-replacement': """
<div class="service-content">
<h2>London's Fastest Emergency Tyre Replacement</h2>
<p>A blown tyre, sudden flat, or tyre failure on a London road is a serious safety situation. FixMyTyreNow operates a 24-hour emergency tyre replacement service across all 32 London boroughs with an average arrival time of 20 minutes. We come to you — whether you're stationary on the A406 North Circular, broken down near a junction on the A1, stuck in a car park, or stranded on a residential street. Our fully equipped vans carry a comprehensive stock of replacement tyres in all common sizes so we can complete the replacement on the spot.</p>

<h2>What Happens During an Emergency Callout</h2>
<p>When you call or book online, we immediately identify the closest available technician to your location. You'll receive a confirmation with an estimated arrival time. When the technician arrives, they'll assess the condition of your tyre and wheel, confirm the replacement tyre from stock, complete the fitting including balancing, and have you back on the road. The full process from first call to driving away typically takes 30–50 minutes.</p>
<ul>
<li><strong>Tyre assessment</strong> — the technician confirms whether the tyre is beyond repair and what caused the failure</li>
<li><strong>Rim inspection</strong> — damage to the rim from driving on a flat is checked; minor damage is noted but does not prevent fitting</li>
<li><strong>Emergency replacement</strong> — new tyre mounted, balanced, inflated to spec, wheel bolts torqued</li>
<li><strong>Road safety check</strong> — a brief check of the remaining three tyres is included at no extra charge</li>
</ul>

<h2>Common Emergency Scenarios We Handle Daily</h2>
<p><strong>Blowouts:</strong> A high-speed blowout at motorway speed is the most dangerous scenario. If this happens, do not brake sharply — ease off the accelerator, grip the wheel firmly, and steer to the hard shoulder or a safe stopping point. Once stopped safely, call us immediately. We handle blowout replacements on the M25, A406, A3, A2, and other major London routes daily.</p>
<p><strong>Sudden flats:</strong> More common in city driving, sudden flats are usually caused by kerb impact, pothole damage, or a sharp object penetrating the tread. If the tyre is losing air slowly, drive carefully to a safe stopping location — ideally a car park or wide residential street — before calling. Do not drive on a completely flat tyre; the risk of rim damage increases rapidly.</p>
<p><strong>Slow punctures:</strong> A tyre that needs topping up regularly has a slow puncture. While this is less urgent than a blowout, a slow puncture left unrepaired will eventually fail, sometimes at speed. Book a same-day service rather than waiting.</p>

<h2>Tyre Brands Carried for Emergency Stock</h2>
<p>Emergency stock includes <strong>Continental</strong>, <strong>Michelin</strong>, <strong>Bridgestone</strong>, <strong>Pirelli</strong>, <strong>Goodyear</strong>, <strong>Hankook</strong>, and <strong>Nexen</strong> across the most common London vehicle sizes. Coverage is highest for sizes common on Ford, Volkswagen, Toyota, BMW, Mercedes-Benz, and Vauxhall models. For less common sizes, sourcing from a nearby depot may add 30 minutes to the arrival time — this will be communicated when you call.</p>

<h2>Safety First: While You Wait</h2>
<ul>
<li>Turn on your hazard lights immediately</li>
<li>Move the vehicle as far from live traffic as safely possible</li>
<li>If on a motorway, exit through the passenger door and stand behind the barrier</li>
<li>Do not attempt to change a tyre on a live carriageway yourself</li>
<li>Keep your phone charged — we'll send an ETA update when the technician is 5 minutes away</li>
</ul>

<h2>Pricing and Payment</h2>
<p>Emergency tyre replacement starts from £69 including the replacement tyre and all fitting. The exact price depends on the tyre size and brand selected. A £10 deposit is charged at booking and deducted from the final invoice. Payment on completion by card, Apple Pay, Google Pay, or bank transfer. No callout fee.</p>

<h2>Frequently Asked Questions</h2>
<details><summary>Do you operate on the M25 and motorways?</summary><p>We respond to breakdowns on all major London roads including the M25, M11, A406, A316, A3, and A2. On motorways, you must first reach the hard shoulder and call 999 if the vehicle is blocking a live lane. Once you are in a safe position, call us and we will dispatch immediately.</p></details>
<details><summary>What if you don't have my tyre size in stock?</summary><p>We carry stock for the vast majority of common UK vehicle sizes. If your size is not on the van, we can source it from a nearby depot within 30–60 minutes. We will confirm this before dispatch and will not charge extra for the sourcing time.</p></details>
<details><summary>Can you replace a run-flat in an emergency?</summary><p>Yes. Run-flat emergency replacement is available at a higher price point starting from £110 due to the specialist equipment required. Mention that you have run-flat tyres when you call so we can dispatch the right technician.</p></details>
</div>
""",

'puncture-repair': """
<div class="service-content">
<h2>Professional Mobile Puncture Repair in London</h2>
<p>A repairable puncture is the most cost-effective outcome of a tyre failure. Rather than replacing the tyre entirely, a professional plug-and-patch repair restores the tyre to full roadworthy condition for a fraction of the cost of a new tyre. FixMyTyreNow carries out puncture repairs from £25 to your location anywhere across London's 32 boroughs, with an average arrival time of 20 minutes. Not every puncture is repairable — we'll inspect it on arrival and give you an honest assessment before any work begins.</p>

<h2>When Is a Puncture Repairable?</h2>
<p>Puncture repairability is governed by British Standard BSAU144e and the vehicle manufacturer's guidelines. The key criteria are:</p>
<ul>
<li><strong>Location:</strong> the puncture must be in the central three-quarters of the tread area (the "crown"). Shoulder and sidewall punctures are not repairable.</li>
<li><strong>Size:</strong> the penetrating object must have left a hole no larger than 6mm in diameter</li>
<li><strong>Tread depth:</strong> the tyre must have at least 1.6mm of remaining tread depth after the repair area is buffed</li>
<li><strong>No prior driving on flat:</strong> a tyre driven on while fully deflated typically suffers internal sidewall damage that makes it unsafe to repair even if the tread is intact</li>
<li><strong>No previous repairs nearby:</strong> British Standard prohibits overlapping repairs; if the tyre has already been repaired in the same area, replacement is required</li>
</ul>
<p>Run-flat tyres cannot be repaired under any circumstances — the reinforced sidewalls are compromised by the heat generated when driven deflated, even for short distances.</p>

<h2>The Plug-and-Patch Method</h2>
<p>Our technicians use the industry-standard two-piece plug-and-patch repair method, which is the only repair technique approved by tyre manufacturers and British Standard BSAU144e. The tyre is removed from the wheel, the puncture is cleaned and buffed from the inside, a vulcanising plug is inserted from the inside to seal the channel, and a patch is bonded over the repaired area. The tyre is then remounted, balanced, and inflated to the correct pressure.</p>
<p>We do not use external plug-only repairs (rope plugs or mushroom plugs inserted from outside without removing the tyre). These are temporary roadside solutions only and are not approved as permanent repairs. If a previous repair shop has used this method, we will advise you accordingly.</p>

<h2>Temporary Repair Products — What to Know</h2>
<p>If your vehicle came with a tyre inflation kit (foam sealant) rather than a spare tyre, these kits are designed for single use to get you to a garage, not as a permanent fix. The sealant coats the inside of the tyre and often makes it uncleanable, which means we cannot complete a standard plug-and-patch repair on a tyre that has been treated with sealant. If you have used a foam sealant, the tyre will likely need full replacement rather than repair. Let us know when you call so we can bring a replacement as well.</p>

<h2>Cost and Time</h2>
<p>Puncture repair starts from £25. The repair itself takes approximately 20–30 minutes once the technician is on site. The £10 deposit paid at booking is deducted from the final price. Payment by card, Apple Pay, Google Pay, or bank transfer on completion. No callout fee.</p>

<h2>Frequently Asked Questions</h2>
<details><summary>How do I know if my puncture is repairable?</summary><p>The only way to confirm repairability is a proper internal inspection once the tyre is removed from the wheel. If the nail or object is still embedded in the tread, do not remove it — this keeps air in the tyre until we arrive. If the tyre is completely flat, do not drive on it. Call us and we'll assess on arrival.</p></details>
<details><summary>Is a repaired tyre as safe as a new one?</summary><p>A correctly executed plug-and-patch repair to British Standard BSAU144e produces a tyre that is fully road-legal and safe for normal use. The repaired tyre can be used on any axle position including the driven axle. There is no speed restriction or temporary status on an approved repair.</p></details>
<details><summary>My slow puncture keeps losing air — is that repairable?</summary><p>Usually yes. Slow punctures are typically caused by a small nail or screw in the tread, or occasionally by a faulty valve. Both are repairable or replaceable at low cost. Driving with a persistent slow puncture risks tyre damage and rim damage — book as soon as convenient rather than waiting.</p></details>
<details><summary>Can you repair a tyre if I don't know what caused the puncture?</summary><p>Yes. Our technicians inspect the tyre fully, inside and out, to identify the cause of deflation. Common causes include embedded nails, screws, glass, or kerb damage. If the cause is not immediately visible, the tyre is submerged in water during inspection to locate the air escape point.</p></details>
</div>
""",

'wheel-balancing': """
<div class="service-content">
<h2>Mobile Wheel Balancing in London — From £15 Per Wheel</h2>
<p>Wheel balancing corrects the uneven weight distribution around your tyre and wheel assembly. Every tyre has minor weight variations from the manufacturing process, and every wheel has its own imperfections. When a wheel rotates at speed, any imbalance creates vibration that travels through the suspension into the steering wheel and seat. FixMyTyreNow provides computerised mobile wheel balancing from £15 per wheel, at your location across all 32 London boroughs.</p>

<h2>Signs Your Wheels Need Balancing</h2>
<ul>
<li><strong>Steering wheel vibration</strong> — usually felt from around 50 mph; front wheel imbalance typically causes steering column vibration, rear imbalance is felt through the seat</li>
<li><strong>Uneven tyre wear</strong> — scalloped or cupped wear patterns across the tread, rather than even wear across the width</li>
<li><strong>Vibration in the seat or floor</strong> — particularly at motorway speeds, caused by rear wheel imbalance</li>
<li><strong>Tyre noise</strong> — a rhythmic thumping or humming that changes with speed</li>
</ul>
<p>Wheels should be rebalanced every 6,000–8,000 miles as part of routine maintenance, whenever a new tyre is fitted, after any significant kerb impact or pothole strike, and any time the above symptoms appear.</p>

<h2>How Computerised Wheel Balancing Works</h2>
<p>The wheel is removed from the vehicle and mounted on our balancing machine. The machine spins the wheel and measures the mass distribution using sensors, identifying both the weight and location of any imbalance. Our technician then applies small adhesive or clip-on weights at the precise positions identified by the machine — typically on the inner and outer faces of the rim. The wheel is then re-spun to confirm the imbalance has been corrected to within the acceptable tolerance (typically less than 5 grams). The process takes 10–15 minutes per wheel.</p>
<p>We use dynamic balancing rather than static balancing. Dynamic balancing measures imbalance in two planes simultaneously, which is significantly more accurate than single-plane static methods and is the correct approach for modern tyres at motorway speeds.</p>

<h2>Static vs. Dynamic Imbalance</h2>
<p><strong>Static imbalance</strong> is a single heavy spot on the tyre that causes a vertical bouncing motion at speed. <strong>Dynamic imbalance</strong> is a more complex side-to-side wobble caused by weight being offset at different points around the wheel's width. Most real-world imbalance is a combination of both. Our computerised equipment measures and corrects both simultaneously in a single procedure.</p>

<h2>Wheel Balancing vs. Wheel Alignment</h2>
<p>These are two distinct procedures that are frequently confused. <strong>Wheel balancing</strong> corrects the rotational mass distribution within a single wheel assembly. <strong>Wheel alignment</strong> (also called tracking) sets the angles at which your wheels contact the road — camber, toe, and caster. Misalignment causes the vehicle to pull to one side and produces feathered or one-sided tyre wear, rather than the vibration caused by imbalance. We provide wheel balancing; if you suspect misalignment, this requires a separate alignment service on a four-wheel alignment rig.</p>

<h2>Pricing and Booking</h2>
<p>Wheel balancing is priced at £15 per wheel. A full four-wheel balance costs £60. The £10 booking deposit is deducted from the final invoice. Payment by card, Apple Pay, Google Pay, or bank transfer on completion.</p>

<h2>Frequently Asked Questions</h2>
<details><summary>Do I need to balance all four wheels or just the ones causing vibration?</summary><p>Front wheel imbalance produces steering wheel vibration; rear wheel imbalance produces seat and floor vibration. However, since imbalance can shift as weights come loose, and since rotating tyres will move wheels to different positions, it is best practice to balance all four simultaneously. The cost saving versus doing individual wheels later justifies this approach.</p></details>
<details><summary>Can wheel weights fall off?</summary><p>Adhesive weights applied inside alloy wheel rims can detach if the wheel surface wasn't properly cleaned before application, or after a high-pressure car wash jet is directed at them. Clip-on weights on steel wheels are more secure but can be knocked off by kerb contact. If your steering wheel vibration returns after a recent balance, a lost weight is the most likely cause.</p></details>
<details><summary>My wheels were balanced when I bought the new tyres — why is there vibration again?</summary><p>A few common causes: a balance weight has fallen off; the tyre has developed a flat spot from long-term stationary parking; the tyre has experienced internal belt separation (requires tyre replacement); or a different component — worn shock absorbers, worn wheel bearings, or a bent rim — is causing the vibration. Our technician can help identify the cause on arrival.</p></details>
</div>
""",

'run-flat-replacement': """
<div class="service-content">
<h2>Mobile Run-Flat Tyre Replacement in London</h2>
<p>Run-flat tyres are fitted as original equipment on a growing number of vehicles — most BMW, Mini, and Mercedes-Benz models, as well as many Audi, Volkswagen, and Renault models produced in the last decade. When a run-flat tyre deflates, the reinforced sidewall supports the vehicle's weight, allowing you to continue driving at up to 50 mph for up to 50 miles to reach safety. What they cannot do is be repaired or replaced with standard fitting tools. FixMyTyreNow provides specialist mobile run-flat replacement from £110 across all 32 London boroughs.</p>

<h2>Why Run-Flat Replacement Is a Specialist Service</h2>
<p>The reinforced sidewall that makes run-flat tyres functional in a deflated state also makes them significantly harder to demount from the wheel. Standard tyre fitting machines do not have sufficient force to break the bead on a run-flat sidewall without damaging the tyre or the rim. Our technicians are equipped with run-flat capable tyre machines and use specialised lubricants and techniques developed specifically for run-flat construction. Attempting to fit run-flat tyres with standard equipment risks permanent rim damage.</p>

<h2>Can Run-Flat Tyres Be Repaired?</h2>
<p>No. All major tyre manufacturers — Michelin, Bridgestone, Continental, Pirelli, and Goodyear — prohibit repair of run-flat tyres. The reason is that run-flat sidewalls sustain internal heat damage when driven deflated, even for short distances within the 50-mile limit. This internal damage is not visible from the outside and cannot be reliably detected, making the repaired tyre unsafe at speed. Any puncture to a run-flat tyre requires full replacement.</p>

<h2>Vehicles That Use Run-Flat Tyres</h2>
<p>Common run-flat vehicles include BMW 1 Series, 2 Series, 3 Series, 4 Series, 5 Series, 6 Series, 7 Series, X1, X3, X4, X5, and X6 — the majority of BMW's lineup. Mini Cooper, Clubman, Countryman, and Paceman also use run-flats as standard. Mercedes-Benz C-Class, E-Class, A-Class, and GLC are commonly fitted with run-flat extended mobility tyres (EMT). Audi A3, A4, and Q3 in certain trims, as well as Renault Megane and Kadjar, may also be run-flat equipped.</p>
<p>Run-flat tyres are identifiable by markings on the sidewall. Look for: <strong>RFT</strong> (Bridgestone), <strong>ROF</strong> (Goodyear), <strong>SSR</strong> (Continental), <strong>ZP</strong> (Michelin), <strong>EMT</strong> (various), or <strong>*</strong> (BMW-approved). If you're unsure, our technician can confirm on arrival before any work begins.</p>

<h2>Run-Flat Stock and Compatibility</h2>
<p>We stock run-flat tyres across the most common sizes for BMW, Mini, and Mercedes-Benz. Brands held include <strong>Continental ContiSportContact</strong>, <strong>Pirelli Cinturato</strong>, <strong>Michelin Primacy</strong>, and <strong>Bridgestone Turanza</strong> in run-flat specification. Less common sizes may require sourcing from a depot — we'll confirm at booking. Do not replace run-flat tyres with conventional tyres unless all four tyres are changed simultaneously and your vehicle's TPMS system is reconfigured; mixing run-flat and conventional tyres on the same axle is unsafe and may be illegal on some vehicle configurations.</p>

<h2>TPMS Reset After Run-Flat Replacement</h2>
<p>Vehicles equipped with run-flat tyres rely entirely on the Tyre Pressure Monitoring System (TPMS) to alert the driver to deflation, since there is no visible sag when a run-flat loses pressure. After tyre replacement, the TPMS warning light must be reset. Our technicians carry TPMS reset tools for BMW, Mini, and Mercedes-Benz systems and will reset the system as part of the service.</p>

<h2>Pricing</h2>
<p>Run-flat replacement starts from £110 per tyre including fitting, balancing, and TPMS reset. The price depends on the tyre size and brand selected. A £10 deposit is taken at booking and deducted from the final invoice. Payment on completion by card, Apple Pay, Google Pay, or bank transfer.</p>

<h2>Frequently Asked Questions</h2>
<details><summary>I drove 10 miles on a flat run-flat — is the tyre damaged?</summary><p>Possibly. Run-flat tyres are rated for 50 miles at up to 50 mph from the point of deflation. Driving faster, further, or heavily loaded can cause internal sidewall damage beyond the design limit. In all cases, the tyre must be replaced — it cannot be repaired. The rim should also be inspected for damage.</p></details>
<details><summary>Can I replace just one run-flat or do I need to change all four?</summary><p>You can replace a single run-flat tyre if the replacement matches the specification (brand, size, and speed rating) of the remaining three. BMW recommends matching axle pairs where possible. You should never mix run-flat and non-run-flat tyres on the same vehicle.</p></details>
<details><summary>My BMW has a flat tyre warning but the tyres look fine — what's happening?</summary><p>Run-flat tyres look identical when flat — there is no visible sag. Check your TPMS readout (usually in the iDrive screen or instrument cluster) for which tyre is showing low pressure. Even if the tyre appears visually normal, a TPMS warning requires immediate attention. Call us and we'll bring the correct replacement.</p></details>
<details><summary>My car didn't come with a spare tyre — is that normal?</summary><p>Yes. The majority of vehicles fitted with run-flat tyres from the factory are not supplied with a spare, since the run-flat capability is designed to replace it. If you'd prefer a spare tyre solution, we can advise on space-saver options compatible with your vehicle.</p></details>
</div>
"""

}

# CSS for new sections
FAQ_DETAILS_CSS = """
/* Service page inline FAQ */
.service-content details {
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0;
  margin-bottom: 10px;
}
.service-content details summary {
  padding: 14px 18px;
  font-weight: 600;
  cursor: pointer;
  list-style: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.service-content details summary::-webkit-details-marker { display: none; }
.service-content details summary::after { content: '+'; font-size: 1.2em; color: var(--orange); }
.service-content details[open] summary::after { content: '−'; }
.service-content details p {
  padding: 0 18px 14px;
  margin: 0;
  color: #444;
  font-size: 0.95rem;
  line-height: 1.65;
}
"""

import glob
changed = 0

for service_slug, new_content in SERVICE_CONTENT.items():
    filepath = f'services/{service_slug}/index.html'
    if not os.path.exists(filepath):
        print(f'NOT FOUND: {filepath}')
        continue

    content = open(filepath, encoding='utf-8').read()

    # Find and replace service-content div
    pattern = re.compile(
        r'<div class="service-content">.*?</div>\s*(?=\n\s*</div>\s*\n\s*<section)',
        re.DOTALL
    )

    new_body = new_content.strip()
    replaced = pattern.sub(new_body, content, count=1)

    if replaced == content:
        # Try alternate pattern
        pattern2 = re.compile(
            r'<div class="service-content">.*?</div>(?=\s*\n\s*</div>\s*\n)',
            re.DOTALL
        )
        replaced = pattern2.sub(new_body, content, count=1)

    if replaced == content:
        print(f'Pattern not matched in {filepath} - check manually')
        # Try simple find of service-body
        idx = content.find('<div class="service-content">')
        if idx > -1:
            end = content.find('</div>', idx)
            # Find closing of outer service-body div
            print(f'  service-content starts at {idx}, </div> at {end}')
            print(f'  sample: {content[idx:idx+200]}')
    else:
        open(filepath, 'w', encoding='utf-8').write(replaced)
        changed += 1
        print(f'Updated: {filepath}')

print(f'\nTotal updated: {changed}')
