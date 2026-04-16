# SEO Indexing Fix — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Google'ın tüm 207 sayfayı doğru şekilde bulmasını, crawl etmesini ve indexlemesini sağlamak.

**Architecture:** robots.txt → sitemap.xml → per-page meta → schema → içerik kalitesi sıralamasında yük taşıyan her katman düzeltilir. Her task kendi commit'ini alır.

**Tech Stack:** Static HTML, Python (toplu düzenleme scriptleri), XML (sitemap)

---

## Tespit Edilen Sorunlar

| # | Sorun | Etki | Öncelik |
|---|-------|------|---------|
| 1 | `robots.txt` `wp-sitemap.xml`'e işaret ediyor (mevcut değil) | Google sayfaları sitemap üzerinden keşfedemiyor | 🔴 KRİTİK |
| 2 | OG image path yanlış: `FixMyTyreNow/` → dosya `FixMyTyreNow_edit/`'de | Sosyal medya önizlemeleri kırık, CTR düşük | 🔴 KRİTİK |
| 3 | Sitemap'te 206 URL var ama 207 HTML sayfa var (`franchise-registration` eksik) | Bir sayfa hiç keşfedilemiyor | 🔴 KRİTİK |
| 4 | 206 URL'den sadece 14'ünde `<lastmod>` var | Google içerik tazeliğini ölçemiyor | 🟠 YÜKSEK |
| 5 | `booking/` sayfası sitemap'te — form sayfası indexlenmemeli | Crawl bütçesi boşa harcanıyor | 🟠 YÜKSEK |
| 6 | `booking/` ve `franchise-registration/` sayfalarında `noindex` yok | Form sayfaları arama sonuçlarına karışıyor | 🟠 YÜKSEK |
| 7 | Bazı sayfalarda hâlâ WP nav class kalıntıları (`menu-item-type-custom` vb.) | Küçük gürültü, temiz HTML değil | 🟡 ORTA |
| 8 | Hiçbir sayfada `BreadcrumbList` schema yok | Arama sonuçlarında breadcrumb gösterilmiyor | 🟡 ORTA |
| 9 | `robots.txt`'de `Disallow: /wp-admin/` (artık yok) + sitemap satırı yanlış | Yanıltıcı direktifler | 🟡 ORTA |
| 10 | Area+service alt sayfaları (`/areas/barnet/standard-tyre-fitting/`) ince içerik | Duplicate content riski, 160 sayfa | 🟡 ORTA |
| 11 | Schema `image` URL'si `wp-content/themes/FixMyTyreNow/` (yanlış path) | Schema validator hatası, rich result riski | 🟡 ORTA |
| 12 | `fmtnConfig.restUrl` hâlâ `wp-json/fmtn/v1/`'e işaret ediyor | Rezervasyon formu çalışmıyor | 🟡 ORTA |
| 13 | CSS stylesheet `id='fmtn-main-css'` WP attribute kaldı | Küçük noise | 🟢 DÜŞÜK |

---

## Dosya Haritası

```
fixmytyrenowcom/
├── robots.txt                        ← Task 1: yeniden yaz
├── sitemap.xml                       ← Task 2: tam yeniden oluştur
├── index.html                        ← Task 3,4,5,7: meta + schema
├── booking/index.html                ← Task 4: noindex ekle
├── franchise-registration/index.html ← Task 4: noindex ekle
├── privacy-policy/index.html         ← Task 4: noindex ekle
├── terms/index.html                  ← Task 4: noindex ekle
├── about/index.html                  ← Task 5,7: OG image + schema
├── reviews/index.html                ← Task 5,7: OG image + schema
├── contact/index.html                ← Task 5,7: OG image + schema
├── services/*/index.html             ← Task 5,6,7: OG image + breadcrumb schema
├── areas/*/index.html                ← Task 5,6,7: OG image + breadcrumb schema
├── areas/*/*/index.html              ← Task 5,6,7: OG image + breadcrumb schema (160 sayfa)
└── docs/plans/
    └── 2026-04-16-seo-indexing-fix.md  ← bu dosya
```

---

## Task 1: robots.txt'yi Düzelt

**Files:**
- Modify: `robots.txt`

**Sorun:** `Sitemap: https://fixmytyrenow.com/wp-sitemap.xml` mevcut değil. Cloudflare managed blok gereksiz uzun. `Disallow: /wp-admin/` statik sitede anlamsız.

- [ ] **Step 1: robots.txt'yi yeniden yaz**

```
User-agent: *
Allow: /
Disallow: /booking/
Disallow: /franchise-registration/

Sitemap: https://fixmytyrenow.com/sitemap.xml
```

> Not: `booking/` ve `franchise-registration/` hem `noindex` hem `Disallow` alacak (Task 4).
> Cloudflare managed blok kaldırılıyor — statik sunucuda Cloudflare yönetmez.

- [ ] **Step 2: Değişikliği doğrula**

Dosyayı aç, içeriğin doğru olduğunu kontrol et.

- [ ] **Step 3: Commit**

```bash
git add robots.txt
git commit -m "fix: robots.txt — point to correct sitemap, remove WP/Cloudflare directives"
git push
```

---

## Task 2: sitemap.xml'i Yeniden Oluştur

**Files:**
- Modify: `sitemap.xml`

**Sorunlar:**
- 206 URL var ama `franchise-registration/` eksik
- Sadece 14 URL'de `<lastmod>` var, 192 tanesinde yok
- `booking/` sitemap'te olmamalı (noindex sayfalar sitemap'e dahil edilmez)
- `privacy-policy/` ve `terms/` de sitemap'ten çıkmalı (noindex olacaklar)

- [ ] **Step 1: Python scripti ile sitemap oluştur**

`generate_sitemap.py` dosyasını oluştur:

```python
#!/usr/bin/env python3
"""
Tum index.html dosyalarini tarayarak temiz sitemap.xml olusturur.
noindex sayfalar ve form sayfalar haric tutulur.
"""
import os, glob
from datetime import date

BASE = r'C:/Users/Administrator/Nextcloud/FIX-MY-TYRE-NOW/website/fixmytyrenowcom'
BASE_URL = 'https://fixmytyrenow.com'
TODAY = date.today().isoformat()

# Sitemap'e DAHIL EDILMEYECEK dizinler
EXCLUDE = [
    'wp-json', 'wp-content', 'cdn-cgi', 'feed',
    'booking',              # form sayfasi - noindex
    'franchise-registration', # form sayfasi - noindex
    'privacy-policy',       # legal - noindex
    'terms',                # legal - noindex
]

# Oncelik haritasi
def priority(path):
    parts = path.strip('/').split('/')
    depth = len(parts)
    if path == '/': return '1.0'
    if depth == 1 and parts[0] in ('services', 'areas', 'reviews', 'about', 'contact'):
        return '0.9'
    if depth == 2 and parts[0] == 'services': return '0.85'
    if depth == 2 and parts[0] == 'areas': return '0.8'
    if depth == 3 and parts[0] == 'areas': return '0.7'
    return '0.6'

def changefreq(path):
    parts = path.strip('/').split('/')
    if path == '/' or (len(parts) == 1 and parts[0] in ('services', 'areas')):
        return 'weekly'
    if len(parts) <= 2: return 'monthly'
    return 'monthly'

# HTML dosyalarini topla
files = glob.glob(os.path.join(BASE, '**', 'index.html'), recursive=True)
files += [os.path.join(BASE, 'index.html')]

urls = []
for fpath in sorted(set(files)):
    rel = fpath.replace(BASE, '').replace('\\', '/').lstrip('/')
    # Dizin kontrolu
    parts = rel.split('/')
    skip = False
    for ex in EXCLUDE:
        if ex in parts:
            skip = True
            break
    if skip:
        continue

    # URL'i olustur
    if rel == 'index.html':
        url_path = '/'
    else:
        url_path = '/' + '/'.join(parts[:-1]) + '/'

    urls.append(url_path)

# XML yaz
lines = ['<?xml version="1.0" encoding="UTF-8"?>']
lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
for path in sorted(set(urls)):
    full_url = BASE_URL + path
    pri = priority(path)
    freq = changefreq(path)
    lines.append('  <url>')
    lines.append(f'    <loc>{full_url}</loc>')
    lines.append(f'    <lastmod>{TODAY}</lastmod>')
    lines.append(f'    <changefreq>{freq}</changefreq>')
    lines.append(f'    <priority>{pri}</priority>')
    lines.append('  </url>')
lines.append('</urlset>')

out = '\n'.join(lines) + '\n'
sitemap_path = os.path.join(BASE, 'sitemap.xml')
with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write(out)

print(f'sitemap.xml olusturuldu: {len(urls)} URL')
```

- [ ] **Step 2: Scripti calistir**

```bash
cd fixmytyrenowcom
python generate_sitemap.py
```

Beklenen çıktı: `sitemap.xml olusturuldu: 203 URL` (207 - booking - franchise - privacy - terms = 203)

- [ ] **Step 3: Doğrula**

```bash
grep -c "<loc>" sitemap.xml
grep "franchise-registration" sitemap.xml  # boş çıkmalı
grep "booking" sitemap.xml                 # boş çıkmalı
grep "lastmod" sitemap.xml | head -3       # tüm satırlarda olmalı
```

- [ ] **Step 4: Scripti sil ve commit**

```bash
rm generate_sitemap.py
git add sitemap.xml
git commit -m "fix: rebuild sitemap — 203 URLs, all with lastmod, exclude form/legal pages"
git push
```

---

## Task 3: OG Image ve Schema Image Path Düzelt

**Files:**
- Modify: Tüm 207 `index.html` (Python script ile)

**Sorun:** Tüm sayfalarda OG image ve schema JSON-LD `wp-content/themes/FixMyTyreNow/` kullanıyor ama dosyalar `wp-content/themes/FixMyTyreNow_edit/` içinde. Broken image = sosyal paylaşım önizlemesi yok.

- [ ] **Step 1: fix_image_paths.py oluştur**

```python
#!/usr/bin/env python3
"""OG image ve schema image path'lerini duzelt."""
import glob, os

BASE = r'C:/Users/Administrator/Nextcloud/FIX-MY-TYRE-NOW/website/fixmytyrenowcom'
SKIP = ['wp-json', 'wp-content', 'cdn-cgi', 'feed']

files = glob.glob(os.path.join(BASE, '**', 'index.html'), recursive=True)
files += [os.path.join(BASE, 'index.html')]
files = [f for f in files if not any(s in f.replace('\\','/') for s in SKIP)]

OLD = 'fixmytyrenow.com/wp-content/themes/FixMyTyreNow/assets/images/'
NEW = 'fixmytyrenow.com/wp-content/themes/FixMyTyreNow_edit/assets/images/'

cleaned = 0
for fpath in sorted(set(files)):
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    if OLD in content:
        content = content.replace(OLD, NEW)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        cleaned += 1

print(f'{cleaned} dosya guncellendi.')
```

- [ ] **Step 2: Calistir**

```bash
python fix_image_paths.py
```

- [ ] **Step 3: Doğrula**

```bash
grep -r "themes/FixMyTyreNow/" fixmytyrenowcom --include="index.html" --exclude-dir=wp-content | wc -l
# 0 çıkmalı
grep "og:image" fixmytyrenowcom/index.html
# FixMyTyreNow_edit göstermeli
```

- [ ] **Step 4: Sil ve commit**

```bash
rm fix_image_paths.py
git add -A
git commit -m "fix: correct OG/schema image paths — FixMyTyreNow -> FixMyTyreNow_edit"
git push
```

---

## Task 4: Noindex Sayfaları İşaretle

**Files:**
- Modify: `booking/index.html`, `franchise-registration/index.html`, `privacy-policy/index.html`, `terms/index.html`

**Sorun:** Rezervasyon formu ve yasal sayfalar arama sonuçlarına giriyor, crawl bütçesi boşa harcanıyor.

- [ ] **Step 1: 4 dosyada robots meta'yı güncelle**

Her dosyada bu satırı bul:
```html
<meta name="robots" content="index,follow">
```

Şununla değiştir:
```html
<meta name="robots" content="noindex,nofollow">
```

4 dosya: `booking/index.html`, `franchise-registration/index.html`, `privacy-policy/index.html`, `terms/index.html`

- [ ] **Step 2: Doğrula**

```bash
grep "robots" fixmytyrenowcom/booking/index.html
grep "robots" fixmytyrenowcom/franchise-registration/index.html
# Her ikisi de noindex,nofollow göstermeli
```

- [ ] **Step 3: Commit**

```bash
git add booking/index.html franchise-registration/index.html privacy-policy/index.html terms/index.html
git commit -m "fix: noindex,nofollow for form and legal pages"
git push
```

---

## Task 5: BreadcrumbList Schema Ekle

**Files:**
- Modify: Tüm `index.html` dosyaları (Python script ile)

**Sorun:** Arama sonuçlarında breadcrumb gösterilmiyor. Google breadcrumb rich result için `BreadcrumbList` schema şart.

**Format örnekleri:**
- Ana sayfa: breadcrumb yok
- `/services/` → `Home > Services`
- `/services/standard-tyre-fitting/` → `Home > Services > Standard Tyre Fitting`
- `/areas/barnet/` → `Home > Areas > Barnet`
- `/areas/barnet/standard-tyre-fitting/` → `Home > Areas > Barnet > Standard Tyre Fitting`

- [ ] **Step 1: add_breadcrumbs.py oluştur**

```python
#!/usr/bin/env python3
"""Tum sayfalara BreadcrumbList JSON-LD schema ekle."""
import glob, os, re, json

BASE = r'C:/Users/Administrator/Nextcloud/FIX-MY-TYRE-NOW/website/fixmytyrenowcom'
BASE_URL = 'https://fixmytyrenow.com'
SKIP = ['wp-json', 'wp-content', 'cdn-cgi', 'feed']

# Guzel isimler
LABELS = {
    'services': 'Services',
    'areas': 'Areas',
    'about': 'About Us',
    'reviews': 'Reviews',
    'contact': 'Contact',
    'booking': 'Book Now',
    'emergency-tyre-replacement': 'Emergency Tyre Replacement',
    'standard-tyre-fitting': 'Standard Tyre Fitting',
    'puncture-repair': 'Puncture Repair',
    'wheel-balancing': 'Wheel Balancing',
    'run-flat-replacement': 'Run-Flat Replacement',
    'barking-and-dagenham': 'Barking and Dagenham',
    'barnet': 'Barnet', 'bexley': 'Bexley', 'brent': 'Brent',
    'bromley': 'Bromley', 'camden': 'Camden',
    'city-of-westminster': 'City of Westminster',
    'croydon': 'Croydon', 'ealing': 'Ealing', 'enfield': 'Enfield',
    'greenwich': 'Greenwich', 'hackney': 'Hackney',
    'hammersmith-and-fulham': 'Hammersmith and Fulham',
    'haringey': 'Haringey', 'harrow': 'Harrow', 'havering': 'Havering',
    'hillingdon': 'Hillingdon', 'hounslow': 'Hounslow',
    'islington': 'Islington',
    'kensington-and-chelsea': 'Kensington and Chelsea',
    'kingston-upon-thames': 'Kingston upon Thames',
    'lambeth': 'Lambeth', 'lewisham': 'Lewisham', 'merton': 'Merton',
    'newham': 'Newham', 'redbridge': 'Redbridge',
    'richmond-upon-thames': 'Richmond upon Thames',
    'southwark': 'Southwark', 'sutton': 'Sutton',
    'tower-hamlets': 'Tower Hamlets', 'waltham-forest': 'Waltham Forest',
    'wandsworth': 'Wandsworth',
}

files = glob.glob(os.path.join(BASE, '**', 'index.html'), recursive=True)
files += [os.path.join(BASE, 'index.html')]
files = [f for f in files if not any(s in f.replace('\\','/') for s in SKIP)]

updated = 0
for fpath in sorted(set(files)):
    rel = fpath.replace(BASE, '').replace('\\', '/').lstrip('/')
    parts = [p for p in rel.split('/') if p and p != 'index.html']

    # Ana sayfa - breadcrumb gereksiz
    if not parts:
        continue

    # Breadcrumb listesi olustur
    items = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE_URL + '/'}]
    for i, part in enumerate(parts):
        path_so_far = BASE_URL + '/' + '/'.join(parts[:i+1]) + '/'
        name = LABELS.get(part, part.replace('-', ' ').title())
        items.append({'@type': 'ListItem', 'position': i + 2, 'name': name, 'item': path_so_far})

    schema = {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': items
    }
    schema_tag = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'

    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Zaten breadcrumb var mi?
    if 'BreadcrumbList' in content:
        continue

    # Son </script> etiketinden onceki schema blogunun ardindan ekle
    # </head> den once ekle
    content = content.replace('</head>', schema_tag + '\n</head>', 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    updated += 1

print(f'{updated} sayfaya BreadcrumbList schema eklendi.')
```

- [ ] **Step 2: Calistir**

```bash
python add_breadcrumbs.py
```

Beklenen: `206 sayfaya BreadcrumbList schema eklendi.`

- [ ] **Step 3: Doğrula**

```bash
# services/standard-tyre-fitting/ kontrolu
python3 -c "
import json, re
with open('fixmytyrenowcom/services/standard-tyre-fitting/index.html') as f:
    c = f.read()
schemas = re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>', c, re.DOTALL)
for s in schemas:
    d = json.loads(s)
    if d.get('@type') == 'BreadcrumbList':
        print(json.dumps(d, indent=2))
"
```

Beklenen çıktı:
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://fixmytyrenow.com/"},
    {"@type": "ListItem", "position": 2, "name": "Services", "item": "https://fixmytyrenow.com/services/"},
    {"@type": "ListItem", "position": 3, "name": "Standard Tyre Fitting", "item": "https://fixmytyrenow.com/services/standard-tyre-fitting/"}
  ]
}
```

- [ ] **Step 4: Sil ve commit**

```bash
rm add_breadcrumbs.py
git add -A
git commit -m "feat: add BreadcrumbList JSON-LD schema to all 206 pages"
git push
```

---

## Task 6: Kalan WP HTML Kalıntılarını Temizle

**Files:**
- Modify: Tüm `index.html` dosyaları (Python script ile)

**Sorun:** Bazı sayfalarda hâlâ `menu-item-type-custom`, `menu-item-object-custom`, `menu-item-home` class'ları ve `id='fmtn-main-css'` attribute'u var.

- [ ] **Step 1: cleanup_remaining_wp.py oluştur**

```python
#!/usr/bin/env python3
"""Kalan WP kalintilari temizle."""
import glob, os, re

BASE = r'C:/Users/Administrator/Nextcloud/FIX-MY-TYRE-NOW/website/fixmytyrenowcom'
SKIP = ['wp-json', 'wp-content', 'cdn-cgi', 'feed']

files = glob.glob(os.path.join(BASE, '**', 'index.html'), recursive=True)
files += [os.path.join(BASE, 'index.html')]
files = [f for f in files if not any(s in f.replace('\\','/') for s in SKIP)]

cleaned = 0
for fpath in sorted(set(files)):
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    original = content

    # WP nav class kalintilari
    content = re.sub(
        r' class="menu-item menu-item-type-custom menu-item-object-custom menu-item-home menu-item-\d+"',
        ' class="menu-item active"', content
    )
    content = re.sub(
        r' class="menu-item menu-item-type-custom menu-item-object-custom menu-item-\d+"',
        ' class="menu-item"', content
    )
    # CSS link id attribute
    content = content.replace(" id='fmtn-main-css'", '')
    content = content.replace(' id="fmtn-main-css"', '')

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        cleaned += 1

print(f'{cleaned} dosya temizlendi.')
```

- [ ] **Step 2: Calistir ve doğrula**

```bash
python cleanup_remaining_wp.py
grep -r "menu-item-type-custom" fixmytyrenowcom --include="index.html" --exclude-dir=wp-content | wc -l
# 0 çıkmalı
```

- [ ] **Step 3: Sil ve commit**

```bash
rm cleanup_remaining_wp.py
git add -A
git commit -m "fix: remove remaining WP nav classes and id attributes"
git push
```

---

## Task 7: WebSite + SiteNavigationElement Schema Ekle (Ana Sayfa)

**Files:**
- Modify: `index.html`

**Sorun:** Ana sayfa `WebSite` schema'sı yok. Bu schema Google'ın site-links arama kutusunu (SearchAction) tanıması için önemli.

- [ ] **Step 1: index.html'de `</head>` den önce ekle**

Mevcut JSON-LD bloklarının hemen ardından, `</head>`'den önce:

```html
<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","name":"FixMyTyreNow","url":"https://fixmytyrenow.com","description":"London's fastest mobile tyre fitting service. 20-minute arrival across all 32 boroughs.","potentialAction":{"@type":"SearchAction","target":{"@type":"EntryPoint","urlTemplate":"https://fixmytyrenow.com/?s={search_term_string}"},"query-input":"required name=search_term_string"}}</script>
```

- [ ] **Step 2: Doğrula**

```bash
grep "WebSite" fixmytyrenowcom/index.html
```

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add WebSite schema with SearchAction to homepage"
git push
```

---

## Task 8: CSS `id` Attribute Kalıntısını ve `media='all'` Kaldır

**Files:**
- Modify: Tüm `index.html` (Python script)

**Sorun:** `<link rel='stylesheet' id='fmtn-main-css' ... media='all'>` — `id` ve `media='all'` WP kalıntısı. `media='all'` render-blocking için gereksiz (default zaten `all`).

- [ ] **Step 1: Python ile toplu temizle**

```python
#!/usr/bin/env python3
import glob, os

BASE = r'C:/Users/Administrator/Nextcloud/FIX-MY-TYRE-NOW/website/fixmytyrenowcom'
SKIP = ['wp-json', 'wp-content', 'cdn-cgi', 'feed']
files = glob.glob(os.path.join(BASE, '**', 'index.html'), recursive=True)
files += [os.path.join(BASE, 'index.html')]
files = [f for f in files if not any(s in f.replace('\\','/') for s in SKIP)]

n = 0
for fpath in sorted(set(files)):
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    orig = c
    c = c.replace(" id='fmtn-main-css'", '').replace(' id="fmtn-main-css"', '')
    c = c.replace(" media='all'", '').replace(' media="all"', '')
    if c != orig:
        with open(fpath, 'w', encoding='utf-8') as f: f.write(c)
        n += 1
print(f'{n} guncellendi')
```

- [ ] **Step 2: Calistir, doğrula, commit**

```bash
python fix_css_attrs.py
grep -r "media='all'" fixmytyrenowcom --include="index.html" --exclude-dir=wp-content | wc -l  # 0
rm fix_css_attrs.py
git add -A
git commit -m "fix: remove WP id and media=all from stylesheet link tags"
git push
```

---

## Task 9: Sitemap'i Google Search Console'a Bildir

**Bu task manuel — yazılım değil.**

- [ ] **Step 1:** Google Search Console → `fixmytyrenow.com` property aç
- [ ] **Step 2:** Sol menü → `Sitemaps`
- [ ] **Step 3:** `https://fixmytyrenow.com/sitemap.xml` gir → `Submit`
- [ ] **Step 4:** Eski `wp-sitemap.xml` varsa sil (Remove butonuyla)
- [ ] **Step 5:** URL Inspection tool ile `https://fixmytyrenow.com/` test et → `Request Indexing`

---

## Doğrulama Kontrol Listesi

Tüm task'lar bitince:

```bash
# 1. Dis kaynak kalmamis mi?
grep -r "googleapis\|googletagmanager\|pagead2\|merchant\.revolut\.com" \
  fixmytyrenowcom --include="index.html" --exclude-dir=wp-content -l

# 2. index.html URL'de kalmamis mi?
grep -r 'href="[^"]*index\.html"' fixmytyrenowcom --include="index.html" \
  --exclude-dir=wp-content -l

# 3. WP class kalintisi?
grep -r "menu-item-type-custom\|wp-theme\|wp-singular" fixmytyrenowcom \
  --include="index.html" --exclude-dir=wp-content -l

# 4. Broken OG image path?
grep -r 'themes/FixMyTyreNow/' fixmytyrenowcom --include="index.html" \
  --exclude-dir=wp-content -l

# 5. Sitemap URL sayisi
grep -c "<loc>" fixmytyrenowcom/sitemap.xml   # 203 olmali

# 6. Breadcrumb schema var mi?
grep -c "BreadcrumbList" fixmytyrenowcom/services/standard-tyre-fitting/index.html  # 1

# 7. noindex sayfalar
grep "noindex" fixmytyrenowcom/booking/index.html
grep "noindex" fixmytyrenowcom/franchise-registration/index.html
```

---

## Tahmini Etki

| Task | Beklenen Etki |
|------|---------------|
| Task 1-2 | Google tüm 203 sayfayı sitemap'ten keşfeder, crawl bütçesi doğru dağılır |
| Task 3 | OG image önizlemeleri düzelir → sosyal paylaşım CTR artar |
| Task 4 | Form/legal sayfalar arama sonuçlarından kaybolur |
| Task 5 | Arama sonuçlarında breadcrumb gösterilmeye başlar |
| Task 6-8 | Sayfa kalitesi sinyali artar (clean HTML) |
| Task 9 | Google yeni sitemap'i haftalarca beklemek yerine anında işler |
