"""
L-2: Add url property to Service schema on 5 service pages
L-4: Add address to footer HTML on all pages
"""
import glob, re, sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── Service slug -> canonical URL ─────────────────────────────────────────────
SERVICE_URLS = {
    'emergency-tyre-replacement': 'https://fixmytyrenow.com/services/emergency-tyre-replacement/',
    'standard-tyre-fitting':      'https://fixmytyrenow.com/services/standard-tyre-fitting/',
    'puncture-repair':            'https://fixmytyrenow.com/services/puncture-repair/',
    'wheel-balancing':            'https://fixmytyrenow.com/services/wheel-balancing/',
    'run-flat-replacement':       'https://fixmytyrenow.com/services/run-flat-replacement/',
}

stats = {'l2': 0, 'l4': 0, 'files': 0}

# ── L-2: Service pages only ────────────────────────────────────────────────────
for slug, url in SERVICE_URLS.items():
    filepath = f'services/{slug}/index.html'
    if not os.path.exists(filepath):
        print(f'  [missing] {filepath}')
        continue
    content = open(filepath, encoding='utf-8').read()
    if f'"url":"{url}"' in content:
        print(f'  [skip-l2] {filepath} — url already present')
        continue
    # Insert "url" right after the "name" field in the Service schema block
    # Pattern: "name":"<service name>","provider"
    old = f'"@type":"Service","name":'
    # Find the Service schema block and insert url after the name value
    pat = re.compile(r'("@type":"Service","name":"[^"]+")("provider")')
    new_content = pat.sub(r'\1,"url":"' + url + r'"\2', content, count=1)
    if new_content != content:
        open(filepath, 'w', encoding='utf-8').write(new_content)
        stats['l2'] += 1
        print(f'  [l2 ok] {filepath}')
    else:
        print(f'  [l2 no-match] {filepath}')

# ── L-4: All HTML pages — add address to footer ────────────────────────────────
ADDRESS_HTML = '<span class="footer-address">86-90 Paul Street, London EC2A 4NE</span>'
# Marker: the "All 32 London Boroughs" link is always the last item in footer-contact
# We insert ADDRESS_HTML after it, before </div>
# The link text is always "📍 All 32 London Boroughs" but href varies by depth
FOOTER_PAT = re.compile(
    r'(<a href="[^"]*areas[^"]*">📍 All 32 London Boroughs</a>)(\s*</div>)',
    re.DOTALL
)

for filepath in sorted(glob.glob('**/*.html', recursive=True)):
    content = open(filepath, encoding='utf-8').read()
    if ADDRESS_HTML in content:
        continue  # already done
    if 'footer-contact' not in content:
        continue
    new_content = FOOTER_PAT.sub(
        r'\1\n          ' + ADDRESS_HTML + r'\2',
        content, count=1
    )
    if new_content != content:
        open(filepath, 'w', encoding='utf-8').write(new_content)
        stats['l4'] += 1
        stats['files'] += 1

print(f'\nL-2 (service url): {stats["l2"]} pages')
print(f'L-4 (footer address): {stats["l4"]} pages')
