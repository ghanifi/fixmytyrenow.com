import glob, re, sys, os
sys.stdout.reconfigure(encoding='utf-8')

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

html_files = glob.glob('**/*.html', recursive=True)
stats = {'og_alt': 0, 'noscript': 0, 'revolut_removed': 0, 'files': 0}

OG_IMAGE_ALT = '<meta property="og:image:alt" content="FixMyTyreNow mobile tyre fitting technician at work in London">'
NOSCRIPT_BLOCK = '<noscript><p style="padding:1rem;background:#fff3cd;border:1px solid #ffc107;border-radius:6px;text-align:center">JavaScript is required for online booking. Please call <a href="tel:07340645595">07340 645595</a> to book directly.</p></noscript>'

# Pages that KEEP revolut-embed.js (have booking form)
BOOKING_PAGES = set()
for f in glob.glob('areas/*/*/index.html'):
    BOOKING_PAGES.add(f.replace('\\', '/'))
for f in glob.glob('areas/*/index.html'):
    BOOKING_PAGES.add(f.replace('\\', '/'))
for f in glob.glob('services/*/index.html'):
    BOOKING_PAGES.add(f.replace('\\', '/'))
BOOKING_PAGES.add('index.html')
BOOKING_PAGES.add('booking/index.html')

REVOLUT_PATTERN = re.compile(r'\s*<script[^>]+revolut-embed\.js[^>]+></script>')

for f in html_files:
    f_norm = f.replace('\\', '/')
    content = open(f, encoding='utf-8').read()
    original = content

    # 1. Add og:image:alt after og:image:height
    if 'og:image:alt' not in content and 'og:image:height' in content:
        content = content.replace(
            '<meta property="og:image:height"',
            OG_IMAGE_ALT + '\n<meta property="og:image:height"',
            1
        )
        stats['og_alt'] += 1

    # 2. Remove revolut-embed.js from non-booking pages
    if f_norm not in BOOKING_PAGES and 'revolut-embed.js' in content:
        new_content = REVOLUT_PATTERN.sub('', content)
        if new_content != content:
            content = new_content
            stats['revolut_removed'] += 1

    # 3. Add noscript fallback to pages with booking form
    if 'fmtn-booking-section' in content and '<noscript>' not in content:
        content = content.replace(
            '<section class="fmtn-booking-section"',
            NOSCRIPT_BLOCK + '\n<section class="fmtn-booking-section"',
            1
        )
        stats['noscript'] += 1

    if content != original:
        stats['files'] += 1
        open(f, 'w', encoding='utf-8').write(content)

print('=== Results ===')
for k, v in stats.items():
    print(f'  {k}: {v}')
