# SEO Geliştirme Checkpoints — fixmytyrenow.com

**Son güncelleme:** 2026-04-19 (3. oturum)
**Audit raporu:** `docs/seo-audit-2026-04-18.md`

---

## Tamamlanan İyileştirmeler

### Kritik

- [x] **Franchise FAQPage şeması sayfa içeriğiyle eşleştirildi**
  - `franchise-registration/index.html:31`
  - Şemadaki 8 soru/cevap, sayfa HTML'indeki gerçek FAQ metinleriyle yeniden yazıldı
  - Önceki şema "No prior experience required" diyordu; sayfa "Yes — qualified technicians required" diyordu — Google penaltı riski giderildi

---

### Yüksek Öncelik

- [x] **32 ilçe sayfası başlığı kısaltıldı (64→58 char)**
  - `areas/*/index.html` — tüm 32 dosya
  - `| 24/7, 20-Min Arrival |` → `| 20-Min Arrival |`
  - title, og:title, twitter:title güncellendi
  - Barking & Dagenham özel düzeltme: `| FixMyTyreNow` eklendi

- [x] **Franchise sayfası başlığı düzeltildi (65→56 char)**
  - `franchise-registration/index.html:9`
  - `"Mobile Tyre Franchise UK | Join FixMyTyreNow | Earn Per Postcode"` → `"Mobile Tyre Franchise UK | FixMyTyreNow | From £25/Month"`

- [x] **Franchise meta description kısaltıldı (191→157 char)**
  - `franchise-registration/index.html:10`
  - Google'da kesilmeden görünecek hale getirildi
  - title, og:description, twitter:description güncellendi

---

### Orta Öncelik

- [x] **Services hub başlığı genişletildi (45→59 char)**
  - `services/index.html:9`
  - `"Our Mobile Tyre Services | FixMyTyreNow London"` → `"Mobile Tyre Services London | Emergency, Repair & Balancing"`

- [x] **Services meta description genişletildi (134→152 char)**
  - `services/index.html:10`
  - og:description ve twitter:description güncellendi

- [x] **Services sayfası AutomotiveBusiness `url` düzeltildi**
  - `services/index.html:26`
  - `"url":"https://fixmytyrenow.com/services/"` → `"url":"https://fixmytyrenow.com"`
  - Google Knowledge Graph entity bütünlüğü sağlandı

- [x] **Homepage meta description genişletildi (135→150 char)**
  - `index.html:10`
  - og:description ve twitter:description güncellendi

- [x] **About meta description düzeltildi (163→152 char)**
  - `about/index.html:10`
  - Fazla karakterler kısaltıldı

---

### Düşük Öncelik

- [x] **About sayfasına FAQPage şeması eklendi**
  - `about/index.html:31`
  - 4 soru: kuruluş tarihi, kapsama alanı, şirket kaydı, garajdan farkı
  - Rich results fırsatı ve AI citation sinyali oluşturuldu

- [x] **Sitemap'e priority değerleri eklendi (204 URL)**
  - `sitemap.xml`
  - Ana sayfa: `1.0`
  - Hub sayfalar (`/services/`, `/areas/`, `/about/`, `/franchise-registration/`): `0.9`
  - İlçe ve servis sayfaları (`/areas/barnet/`, `/services/puncture-repair/`): `0.8`
  - Combo sayfalar (`/areas/barnet/puncture-repair/`): `0.6`

---

## Bekleyen İyileştirmeler

### Yüksek Öncelik

- [x] **Emergency servis sayfasına özgün OG görseli atandı**
  - `services/emergency-tyre-replacement/index.html`
  - `hero.jpg` → `emergency.jpg` (preload, og:image, twitter:image, og:image:alt)

- [ ] **Diğer sayfa tipleri için özgün OG görseli** *(tasarımcı gerektirir)*
  - İlçe sayfaları, franchise ve diğer servis sayfaları için `hero.jpg` kullanılıyor
  - Yeni görseller hazırlandığında şu dosyalara uygulanacak:
    - `og-area.jpg` → tüm `areas/*/index.html` (32 sayfa)
    - `og-franchise.jpg` → `franchise-registration/index.html`
    - `og-service.jpg` → diğer 4 servis sayfası

- [x] **İlçe sayfası meta description'larının optimize edilmesi (32 sayfa)**
  - Tüm 32 area sayfası 150–160 char aralığına getirildi
  - Kısa olanlar: "Book with £10 deposit." → "Book in 60 seconds — no garage visit." (+15c)
  - Uzun olanlar: postcode listesi kısaltıldı, son cümle korundu
  - **og:description artık meta'dan farklı** — sosyal medya için daha kısa ve vurucu versiyon:
    `"[Borough] mobile tyre fitting — 20-minute arrival, emergency 24/7. All postcodes covered. From £25."`

---

### Orta Öncelik

- [x] **Reviews sayfası şeması** *(zaten mevcut)*
  - `/reviews/index.html`
  - `AutomotiveBusiness` şeması içinde `aggregateRating` (4.9★, 912 yorum) ve 12 adet `Review` nesnesi bulunuyor
  - Ayrıca `BreadcrumbList` şeması mevcut — tamamlanmış sayılır

- [x] **WebSite şemasına SearchAction** *(atlandı — geçerli değil)*
  - Site statik HTML; çalışan bir arama endpoint'i yok (`?s=`)
  - SearchAction olmadan bırakmak, yanlış URL işaret etmekten daha iyi

- [x] **About sayfasına founder/Person şeması eklendi**
  - `about/index.html:31`
  - `AutomotiveBusiness` şemasına `"founder"` alanı eklendi
  - Harry McKnight (IT specialist) ve Arthur Smith (automotive technician) — sayfa içeriğinden alındı

- [x] **`og:type` değerleri** *(değişiklik gerekmedi)*
  - Open Graph standardında `"service"` veya `"local_business"` type yok
  - `"website"` tüm sayfa tipleri için doğru ve standart değer

---

### Düşük Öncelik

- [x] **`fonts.css` render-blocking optimizasyonu uygulandı (207 sayfa)**
  - Tüm HTML dosyalarında `fonts.css` async yüklemeye geçirildi
  - `<link rel='preload' as='style' onload="...">` + `<noscript>` fallback pattern
  - `main.css` render-blocking olarak bırakıldı (layout CSS — deferring FOUC riski taşır)

- [x] **Bugün değiştirilen sayfaların sitemap lastmod tarihi güncellendi**
  - `sitemap.xml`
  - 37 URL → `2026-04-19` (homepage, about, services, franchise, reviews, emergency service, 32 area sayfası)
  - 166 URL → `2026-04-16` kaldı (combo sayfaları — içerik değişmedi)

- [x] **Sitemap'e `<changefreq>` değerleri eklendi (204 URL)**
  - `sitemap.xml`
  - Ana sayfa: `daily` (1 URL)
  - Hub sayfalar: `weekly` (6 URL)
  - İlçe/servis/combo sayfaları: `monthly` (197 URL)

- [ ] **İlçe sayfalarına service-specific OG açıklamaları**
  - Şu an ilçe sayfalarında og:description = meta description
  - Sosyal paylaşım için daha kısa ve dikkat çekici bir versiyon hazırlanabilir

---

## Teknik Borç

- [ ] **Favicon Apple Touch Icon güncellemesi**
  - `apple-touch-icon` şu an `favicon.ico` gösteriyor (180×180 PNG olmalı)
  - Tüm sayfalarda aynı sorun mevcut — yeni PNG dosyası oluşturulup atanmalı

- [x] **`/wp-json/` robots.txt'e eklendi**
  - `robots.txt`
  - `User-agent: *` bloğuna `Disallow: /wp-json/` satırı eklendi

---

## Skorlama

| Tarih | Tahmini Skor | Değişiklik |
|-------|-------------|------------|
| 2026-04-18 (audit) | 78/100 | Başlangıç |
| 2026-04-19 (1. oturum) | ~86/100 | +8 puan |
| 2026-04-19 (2. oturum) | ~91/100 | +5 puan |
| Kalan 3 madde tamamlanırsa | ~93/100 | +2 puan daha |

**2. oturum skor artışının dağılımı:**
- About founder şeması (E-E-A-T): +2
- fonts.css async load 207 sayfa (performance): +1
- Sitemap changefreq + robots.txt wp-json: +1
- Emergency sayfası özgün OG görseli: +1

**Kalan bekleyenler:**
- Diğer sayfa tipleri için OG görselleri (tasarımcı gerektirir)
- İlçe description optimizasyonu (manuel, 32 sayfa)
- Apple Touch Icon PNG (yeni dosya gerektirir)
- İlçe sayfaları service-specific OG açıklamaları
