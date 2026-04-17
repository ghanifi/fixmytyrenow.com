"""
Bulk schema fixes based on SEO audit 2026-04-17:
M-1: reviewCount string -> integer (912 not "912")
M-2: telephone -> E.164 format (+447340645595)
L-1: Add logo property to AutomotiveBusiness schema
L-3: Add worstRating to Review blocks on combo pages
"""
import glob, re, sys, json
sys.stdout.reconfigure(encoding='utf-8')
import os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

html_files = sorted(glob.glob('**/*.html', recursive=True))
stats = {
    'review_count': 0,
    'telephone': 0,
    'logo': 0,
    'worst_rating': 0,
    'files': 0,
}

LOGO_PROP = '"logo":{"@type":"ImageObject","url":"https://fixmytyrenow.com/wp-content/themes/FixMyTyreNow_edit/assets/img/logo.png"},'

for filepath in html_files:
    content = open(filepath, encoding='utf-8').read()
    original = content

    # M-1: reviewCount string -> integer
    content = content.replace('"reviewCount":"912"', '"reviewCount":912')
    if content != original:
        stats['review_count'] += content.count('"reviewCount":912') - original.count('"reviewCount":912')

    # M-2: telephone to E.164
    if '"telephone":"07340645595"' in content:
        content = content.replace('"telephone":"07340645595"', '"telephone":"+447340645595"')
        stats['telephone'] += 1

    # L-1: Add logo to AutomotiveBusiness schema (only if not already present)
    if '"@type":"AutomotiveBusiness"' in content and '"logo"' not in content:
        content = content.replace(
            '"@type":"AutomotiveBusiness"',
            '"@type":"AutomotiveBusiness",' + LOGO_PROP[:-1],  # strip trailing comma, add after @type
        )
        # Actually insert properly: logo goes after @type
        # Re-do: replace the pattern with comma-correct version
        content = content.replace(
            '"@type":"AutomotiveBusiness",' + LOGO_PROP[:-1],
            '"@type":"AutomotiveBusiness"',
        )
        # Insert logo before "name": (after @type of AutomotiveBusiness)
        content = content.replace(
            '"@type":"AutomotiveBusiness","name":"FixMyTyreNow"',
            '"@type":"AutomotiveBusiness",' + LOGO_PROP + '"name":"FixMyTyreNow"',
        )
        if '"logo"' in content:
            stats['logo'] += 1

    # L-3: Add worstRating to Review blocks (combo pages only)
    if '"@type":"Review"' in content and '"worstRating"' not in content:
        content = content.replace(
            '"bestRating":"5"}',
            '"bestRating":"5","worstRating":"1"}',
        )
        if '"worstRating"' in content:
            stats['worst_rating'] += 1

    if content != original:
        stats['files'] += 1
        open(filepath, 'w', encoding='utf-8').write(content)

print('=== Schema bulk fix results ===')
for k, v in stats.items():
    print(f'  {k}: {v}')
