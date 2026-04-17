"""
Update BOROUGHS pc field in rewrite_combo_pages.py to match the
authoritative postcode chips now on each area page.
Then re-run rewrite_combo_pages to refresh combo page chips.
"""
import re, glob, os, sys, ast
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── Step 1: extract authoritative PCs from area pages ────────────────────────
def pc_sort_key(pc):
    m = re.match(r'([A-Z]+)(\d+)', pc)
    if m: return (m.group(1), int(m.group(2)))
    return (pc, 0)

authority = {}
for f in sorted(glob.glob('areas/*/index.html')):
    slug = os.path.basename(os.path.dirname(f))
    c = open(f, encoding='utf-8').read()
    pcs = re.findall(r'<span class="postcode-chip">([A-Z0-9]+)</span>', c)
    authority[slug] = sorted(set(pcs), key=pc_sort_key)

print(f'Loaded PC data for {len(authority)} boroughs')

# ── Step 2: update rewrite_combo_pages.py BOROUGHS data ──────────────────────
script_path = 'scripts/rewrite_combo_pages.py'
script = open(script_path, encoding='utf-8').read()
original = script

updated = 0
for slug, new_pcs in authority.items():
    # Match: 'pc': ['XX1', 'XX2', ...] for this borough
    # We find the borough entry and update its pc field
    new_pc_str = repr(new_pcs)
    # Pattern: finds 'pc': [...] inside the borough dict for this slug
    # The slug appears on a line like: ('barnet', {
    # Then within that dict block, 'pc': [...]
    # We use a targeted approach: find the borough slug, then the next 'pc' occurrence

    # Build pattern that finds 'pc' array within the borough's dict block
    # Approach: find slug, then find and replace the 'pc': [...] that follows
    pat = re.compile(
        r"('" + re.escape(slug) + r"',\s*\{[^}]*?'pc':\s*)(\[[^\]]+\])",
        re.DOTALL
    )
    new_script = pat.sub(r'\g<1>' + new_pc_str, script, count=1)
    if new_script != script:
        script = new_script
        updated += 1
    else:
        print(f'  [no-match] {slug}')

if script != original:
    open(script_path, 'w', encoding='utf-8').write(script)
    print(f'\nUpdated {updated} borough pc fields in script')
else:
    print('No changes made to script')
