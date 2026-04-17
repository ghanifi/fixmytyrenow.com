"""
Remaining schema and content fixes:
1. streetAddress: remove redundant ", London, England" → "86-90 Paul Street"
2. Service pages: add aggregateRating to Service schema
3. About page: fix vague arrival time claim
4. Nav: remove aria-current from hash-fragment links
"""
import glob, re, sys, json
sys.stdout.reconfigure(encoding='utf-8')
import os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

html_files = glob.glob('**/*.html', recursive=True)
stats = {'street': 0, 'aria': 0, 'about': 0, 'service_rating': 0, 'files': 0}

# ── 1. Fix streetAddress ──────────────────────────────────────────────────────
STREET_OLD = '"streetAddress":"86-90 Paul Street, London, England"'
STREET_NEW = '"streetAddress":"86-90 Paul Street"'

# ── 2. Service aggregateRating (inject into Service schema) ───────────────────
AGGREGATE_RATING = '"aggregateRating":{"@type":"AggregateRating","ratingValue":"4.9","reviewCount":"912","bestRating":"5","worstRating":"1"},'

# Pattern: full Service schema JSON-LD block
SERVICE_SCHEMA_PAT = re.compile(
    r'(<script type="application/ld\+json">)(\{"@context":"https://schema\.org","@type":"Service".*?</script>)',
    re.DOTALL
)

# ── 3. About page arrival time ────────────────────────────────────────────────
ABOUT_OLD = 'but we aim to reach most customers as quickly as possible within London.'
ABOUT_NEW = 'with an average arrival time of 20 minutes across all 32 London boroughs.'

# ── 4. aria-current on hash-fragment nav links ────────────────────────────────
ARIA_PAT = re.compile(r'(<a href="[^"]*#[^"]*") aria-current="page"')

for f in html_files:
    content = open(f, encoding='utf-8').read()
    original = content

    # 1. Fix streetAddress
    if STREET_OLD in content:
        content = content.replace(STREET_OLD, STREET_NEW)
        stats['street'] += 1

    # 2. Add aggregateRating to Service schema
    if '"@type":"Service"' in content and 'aggregateRating' not in content:
        def inject_rating(m):
            tag_open = m.group(1)
            rest = m.group(2)
            if '"offers"' in rest and 'aggregateRating' not in rest:
                rest = rest.replace('"offers":', AGGREGATE_RATING + '"offers":', 1)
                stats['service_rating'] += 1
            return tag_open + rest
        content = SERVICE_SCHEMA_PAT.sub(inject_rating, content)

    # 3. Fix About page vague arrival claim
    if ABOUT_OLD in content:
        content = content.replace(ABOUT_OLD, ABOUT_NEW)
        stats['about'] += 1

    # 4. Remove aria-current from hash-fragment nav links
    new_content = ARIA_PAT.sub(r'\1', content)
    if new_content != content:
        content = new_content
        stats['aria'] += 1

    if content != original:
        stats['files'] += 1
        open(f, 'w', encoding='utf-8').write(content)

print('=== Results ===')
for k, v in stats.items():
    print(f'  {k}: {v}')
