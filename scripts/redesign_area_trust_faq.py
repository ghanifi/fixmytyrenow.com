"""
Redesign location-trust and location-faq sections on all 32 area pages.

Trust section:
  - Adds Google rating widget (G logo, 4.9 score, stars, count, CTA)
  - Upgrades blockquote to card with avatar initials, stars, source badge

FAQ section:
  - CSS handles numbering/chevron via ::before/::after + counter
  - No HTML changes needed (CSS already applied via stylesheet)
"""
import glob, re, os, sys
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

GOOGLE_G_SVG = (
    '<svg class="tgw-glogo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"'
    ' aria-label="Google" role="img">'
    '<path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92'
    'c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>'
    '<path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77'
    'c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84'
    'C3.99 20.53 7.7 23 12 23z"/>'
    '<path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09'
    'V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>'
    '<path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15'
    'C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84'
    'c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>'
)

GOOGLE_WIDGET = (
    '<div class="trust-google-widget">\n'
    + GOOGLE_G_SVG + '\n'
    '<div class="tgw-center">'
    '<div class="tgw-score-row">'
    '<span class="tgw-score">4.9</span>'
    '<span class="tgw-stars" aria-label="4.9 out of 5 stars">★★★★★</span>'
    '</div>'
    '<div class="tgw-label">912 Google Reviews</div>'
    '</div>'
    '<a href="../../reviews/" class="tgw-cta">See all reviews\u00a0\u2192</a>'
    '\n</div>'
)


def get_initials(cite_text):
    """Extract initials from 'John T., Location' → 'JT'"""
    name_part = cite_text.split(',')[0].strip()
    parts = name_part.split()
    initials = ''
    for p in parts[:2]:
        p_clean = p.strip('.')
        if p_clean:
            initials += p_clean[0].upper()
    return initials or '??'


def update_page(filepath):
    content = open(filepath, encoding='utf-8').read()

    # Skip if already done
    if 'trust-google-widget' in content:
        return 'skip'

    # ── Extract existing blockquote ───────────────────────────────────────
    bq_pat = re.compile(
        r'<blockquote class="location-review">\s*<p>(.*?)</p>\s*<cite>(.*?)</cite>\s*</blockquote>',
        re.DOTALL
    )
    bq_match = bq_pat.search(content)
    if not bq_match:
        return 'no-bq'

    review_text = bq_match.group(1).strip()
    cite_text   = bq_match.group(2).strip()
    initials    = get_initials(cite_text)

    # ── Build enhanced review card ────────────────────────────────────────
    enhanced_bq = (
        '<blockquote class="location-review">\n'
        '<div class="lr-stars" aria-hidden="true">★★★★★</div>\n'
        f'<p>{review_text}</p>\n'
        '<div class="lr-meta">\n'
        f'<div class="lr-avatar" aria-hidden="true">{initials}</div>\n'
        '<div class="lr-info">'
        f'<cite>{cite_text}</cite>'
        '<span class="lr-source">Google Review ✓</span>'
        '</div>\n'
        '</div>\n'
        '</blockquote>'
    )

    # ── Replace blockquote ────────────────────────────────────────────────
    new_content = bq_pat.sub(enhanced_bq, content, count=1)

    # ── Insert Google widget before trust-stats ───────────────────────────
    new_content = new_content.replace(
        '<div class="trust-stats">',
        GOOGLE_WIDGET + '\n<div class="trust-stats">',
        1
    )

    if new_content == content:
        return 'unchanged'

    open(filepath, 'w', encoding='utf-8').write(new_content)
    return 'ok'


stats = {'ok': 0, 'skip': 0, 'no-bq': 0, 'unchanged': 0}
for f in sorted(glob.glob('areas/*/index.html')):
    result = update_page(f)
    stats[result] += 1
    borough = os.path.basename(os.path.dirname(f))
    print(f'  [{result:9s}] {borough}')

print(f'\nUpdated: {stats["ok"]}  Skipped: {stats["skip"]}  '
      f'No-BQ: {stats["no-bq"]}  Unchanged: {stats["unchanged"]}')
