#!/usr/bin/env python3
"""
Remove all WordPress/Cloudflare garbage from the static site.
"""
import os
import re
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_FILES = glob.glob(os.path.join(BASE_DIR, "**", "*.html"), recursive=True)

stats = {
    "nonce_input": 0,
    "nonce_js": 0,
    "wp_json_link": 0,
    "rss_link": 0,
    "cf_email_decode": 0,
    "cf_speculation": 0,
    "cf_email_span": 0,
    "wp_block_css": 0,
    "files_changed": 0,
}

# Patterns to remove entirely
REMOVE_PATTERNS = [
    # WP nonce hidden input
    (r'<input[^>]+type=["\']hidden["\'][^>]+name=["\']nonce["\'][^>]*>', "nonce_input"),
    # WP REST API JSON link
    (r'<link\s+rel=["\']alternate["\'][^>]+application/json[^>]+wp-json[^>]*/>', "wp_json_link"),
    # RSS feed links
    (r'<link\s+rel=["\']alternate["\'][^>]+application/rss\+xml[^>]*/>', "rss_link"),
    # Cloudflare email-decode script
    (r'<script[^>]+cdn-cgi[^>]+email-decode\.min\.js[^>]*(?:></script>|/>)', "cf_email_decode"),
    # Cloudflare speculationrules script block
    (r'<script\s+type=["\']speculationrules["\'][^>]*>[\s\S]*?</script>', "cf_speculation"),
    # WP block inline CSS (about page)
    (r'<style\s+id=["\']wp-block-(?:heading|list|paragraph)-inline-css["\'][^>]*>[\s\S]*?</style>', "wp_block_css"),
]

# nonce removal from fmtnConfig JS (keep restUrl, phone, deposit)
NONCE_JS_PATTERN = re.compile(r'"nonce"\s*:\s*"[^"]*"\s*,?\s*')

# Cloudflare __cf_email__ span → real email
CF_EMAIL_PATTERN = re.compile(
    r'<span[^>]+class=["\']__cf_email__["\'][^>]+data-cfemail=["\'][^"\']*["\'][^>]*>\[email\s*protected\]</span>'
)
CF_EMAIL_REPLACEMENT = 'hello@fixmytyrenow.com'

# Also handle variant without [email protected] text
CF_EMAIL_PATTERN2 = re.compile(
    r'<span[^>]+class=["\']__cf_email__["\'][^>]+data-cfemail=["\'][^"\']*["\'][^>]*>.*?</span>'
)

compiled_removals = [
    (re.compile(pattern, re.IGNORECASE), key)
    for pattern, key in REMOVE_PATTERNS
]

for filepath in sorted(HTML_FILES):
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    content = original

    # Apply remove patterns
    for pattern, key in compiled_removals:
        new_content, n = pattern.subn('', content)
        if n:
            stats[key] += n
            content = new_content

    # Remove nonce from fmtnConfig JS
    new_content, n = NONCE_JS_PATTERN.subn('', content)
    if n:
        stats["nonce_js"] += n
        content = new_content

    # Replace Cloudflare email obfuscation
    new_content, n = CF_EMAIL_PATTERN.subn(CF_EMAIL_REPLACEMENT, content)
    if n:
        stats["cf_email_span"] += n
        content = new_content
    else:
        new_content, n = CF_EMAIL_PATTERN2.subn(CF_EMAIL_REPLACEMENT, content)
        if n:
            stats["cf_email_span"] += n
            content = new_content

    # Clean up blank lines left by removals (max 2 consecutive blank lines)
    content = re.sub(r'\n{3,}', '\n\n', content)

    if content != original:
        stats["files_changed"] += 1
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        rel = os.path.relpath(filepath, BASE_DIR)
        print(f"  cleaned: {rel}")

print("\n=== Cleanup Summary ===")
for key, val in stats.items():
    if val:
        print(f"  {key}: {val}")
print(f"\nTotal files modified: {stats['files_changed']}")
