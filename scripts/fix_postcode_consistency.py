"""
M-4: Fix postcode inconsistencies across all 32 area pages.

Strategy:
- For each borough, build authoritative PC list = union of meta description PCs + chip PCs
- Westminster exception: chips are wrong (EC1-4, E1 = City of London) — use meta only
- Update: area page chips, area page meta description, script BOROUGHS pc field
"""
import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── Westminster override (chips were wrong — City of London PCs) ───────────────
WESTMINSTER_PCS = ['SW1', 'W1', 'W2', 'WC1', 'WC2']

# ── Postcode sort key: letters first, then number ────────────────────────────
def pc_sort_key(pc):
    m = re.match(r'([A-Z]+)(\d+)', pc)
    if m: return (m.group(1), int(m.group(2)))
    return (pc, 0)


def get_meta_pcs(content):
    m = re.search(r'<meta name="description"[^>]*content="([^"]+)"', content)
    if not m: return []
    return sorted(set(re.findall(r'\b([A-Z]{1,2}[0-9]{1,2}[A-Z]?)\b', m.group(1))), key=pc_sort_key)


def get_chip_pcs(content):
    return sorted(set(re.findall(r'<span class="postcode-chip">([A-Z0-9]+)</span>', content)), key=pc_sort_key)


def build_chips_html(pcs):
    return ''.join(f'<span class="postcode-chip">{pc}</span>' for pc in pcs)


def update_meta_pcs(content, borough_name, new_pcs):
    """Replace postcode portion in meta description."""
    pc_str = ', '.join(new_pcs)
    # Pattern: "We cover/reach POSTCODES in 20 minutes" or similar
    # Replace the postcode list between "cover" or "reach" and "in 20"
    new_content = re.sub(
        r'(We (?:cover|reach) )[^.]+?( in 20 minutes)',
        r'\g<1>' + pc_str + r'\2',
        content,
    )
    if new_content == content:
        # Try alternate pattern with hyphen ranges like BR1-BR7, SE20
        new_content = re.sub(
            r'(We (?:cover|reach) )[\w, -]+?( in 20)',
            r'\g<1>' + pc_str + r'\2',
            content,
        )
    return new_content


import glob
boroughs = [
    (os.path.basename(os.path.dirname(f)), f)
    for f in sorted(glob.glob('areas/*/index.html'))
]

stats = {'updated': 0, 'no-change': 0}

for slug, filepath in boroughs:
    content = open(filepath, encoding='utf-8').read()
    original = content

    is_westminster = slug == 'city-of-westminster'

    meta_pcs = get_meta_pcs(content)
    chip_pcs = get_chip_pcs(content)

    if is_westminster:
        # Chips are wrong — use hardcoded correct list
        auth_pcs = WESTMINSTER_PCS
    else:
        # Merge meta + chips, deduplicate, sort
        auth_pcs = sorted(set(meta_pcs) | set(chip_pcs), key=pc_sort_key)

    # ── Update chips ─────────────────────────────────────────────────────────
    new_chips_html = build_chips_html(auth_pcs)
    old_chips_html = build_chips_html(chip_pcs)

    if old_chips_html in content:
        content = content.replace(old_chips_html, new_chips_html, 1)
    else:
        # Try replacing the entire postcode-chips div content
        content = re.sub(
            r'(<div class="postcode-chips">).*?(</div>)',
            r'\1' + new_chips_html + r'\2',
            content, count=1, flags=re.DOTALL,
        )

    # ── Update meta description ───────────────────────────────────────────────
    content = update_meta_pcs(content, slug, auth_pcs)

    if content != original:
        open(filepath, 'w', encoding='utf-8').write(content)
        print(f'  [ok] {slug:35s} {sorted(chip_pcs)} -> {auth_pcs}')
        stats['updated'] += 1
    else:
        print(f'  [--] {slug:35s} no change')
        stats['no-change'] += 1

print(f'\nUpdated: {stats["updated"]}  No-change: {stats["no-change"]}')
