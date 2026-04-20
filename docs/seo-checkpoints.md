# SEO Geliştirme Checkpoints — fixmytyrenow.com

**Son güncelleme:** 2026-04-20 (4. oturum)
**Audit raporu:** `docs/seo-audit-2026-04-18.md`
**Rekabet analizi:** `docs/competitive-analysis.md`

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
    - `og-blog.jpg` → tüm `blog/*/index.html`

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

- [x] **Blog içerik hub'ı oluşturuldu**
  - `blog/index.html` — Blog hub sayfası (Blog şeması + BreadcrumbList)
  - `blog/how-long-do-tyres-last/` — Article + FAQPage şeması, ~650 kelime
  - `blog/what-to-do-flat-tyre-london/` — Article + HowTo + FAQPage şeması, ~560 kelime
  - `blog/run-flat-tyres-explained/` — Article + FAQPage şeması, ~650 kelime
  - Sitemap'e eklendi (priority: 0.9 hub, 0.8 makaleler)
  - Footer'da Company sütununa Blog linki eklendi

- [x] **Havalimanı lokasyon sayfaları oluşturuldu**
  - `locations/heathrow-airport/` — TW6, TW14, TW15, UB3, UB7 — AutomotiveBusiness + FAQPage şeması
  - `locations/city-airport/` — E16, E6, SE7 — AutomotiveBusiness + FAQPage şeması
  - Sitemap'e eklendi (priority: 0.8)

- [x] **Lastik marka sayfaları oluşturuldu (5 marka)**
  - `tyres/michelin/` — Pilot Sport 5, Primacy 4+, CrossClimate 2, Energy Saver+
  - `tyres/continental/` — PremiumContact 7, SportContact 7, EcoContact 6
  - `tyres/pirelli/` — P Zero, Cinturato P7, Scorpion serisi
  - `tyres/bridgestone/` — Potenza Sport, Turanza T005, Turanza All Season 6
  - `tyres/goodyear/` — Eagle F1 Asymmetric 6, EfficientGrip Performance 2, Vector 4Seasons Gen-3
  - Her sayfada AutomotiveBusiness + FAQPage + BreadcrumbList şeması
  - Sitemap'e eklendi (priority: 0.8)

- [x] **ads.txt oluşturuldu**
  - `ads.txt` — Google AdSense publisher doğrulaması
  - `google.com, pub-3554409000033206, DIRECT, f08c47fec0942fa0`

---

### Düşük Öncelik

- [x] **`fonts.css` render-blocking optimizasyonu uygulandı (207 sayfa)**
  - Tüm HTML dosyalarında `fonts.css` async yüklemeye geçirildi
  - `<link rel='preload' as='style' onload="...">` + `<noscript>` fallback pattern
  - `main.css` render-blocking olarak bırakıldı (layout CSS — deferring FOUC riski taşır)

- [x] **Bugün değiştirilen sayfaların sitemap lastmod tarihi güncellendi**
  - `sitemap.xml`
  - 37 URL → `2026-04-19` (homepage, about, services, franchise, reviews, emergency service, 32 area sayfası)
  - 11 yeni URL → `2026-04-20` (blog, locations, tyres)

- [x] **Sitemap'e `<changefreq>` değerleri eklendi (215 URL)**
  - `sitemap.xml`
  - Ana sayfa: `daily` (1 URL)
  - Hub sayfalar: `weekly` (7 URL — blog/ eklendi)
  - İlçe/servis/combo/blog/location/brand sayfaları: `monthly`

- [ ] **İlçe sayfalarına service-specific OG açıklamaları**
  - Şu an ilçe sayfalarında og:description = meta description
  - Sosyal paylaşım için daha kısa ve dikkat çekici bir versiyon hazırlanabilir

---

## Teknik Borç

- [x] **Favicon Apple Touch Icon güncellemesi** *(tamamlandı)*
  - `apple-touch-icon.png` mevcut — 180×180 RGBA PNG
  - Tüm sayfalar `/apple-touch-icon.png` referansını kullanıyor

- [x] **`/wp-json/` robots.txt'e eklendi**
  - `robots.txt`
  - `User-agent: *` bloğuna `Disallow: /wp-json/` satırı eklendi

---

## Dışarıda Yapılması Gereken (Kod Dışı)

- [ ] **Google Search Console** — Domain verification + sitemap.xml gönderimi *(kritik — site henüz index'lenmemiş)*
- [ ] **Google Business Profile** — GBP oluşturulup optimize edilmeli *(local pack için şart)*
- [ ] **Trustpilot business profile** — 912 on-site yorum dışarıda görünür değil
- [ ] **NTDA membership** — Rakip 24hrmobiletyres kullanıyor; güven/backlink sinyali
- [ ] **OG görselleri** — `og-area.jpg`, `og-franchise.jpg`, `og-service.jpg`, `og-blog.jpg` (tasarımcı)

---

## İçerik Boşlukları (Rekabet Analizinden)

- [ ] **Blog genişletme** — Hedef: 10+ makale. Önerilen konular:
  - "How to check tyre pressure" (yüksek arama hacmi)
  - "Mobile tyre fitting vs garage" (satın alma niyeti)
  - "Tyre safety check London" (yerel intent)
  - "When to replace run-flat tyres"
  - "Best tyres for London driving"
- [ ] **Havalimanı sayfaları genişletme** — Gatwick, Stansted, Luton (London dışı ama yüksek intent)
- [ ] **Lastik marka hub sayfası** — `tyres/index.html` — tüm markalara hub
- [ ] **EV lastik sayfası** — Rakiplerin hiçbirinde yok; büyük fırsat
- [ ] **Otoyol/yol bazlı sayfalar** — M25, A406, A4, A1 (roadside callout intent)

---

## Skorlama

| Tarih | Tahmini Skor | Değişiklik |
|-------|-------------|------------|
| 2026-04-18 (audit) | 78/100 | Başlangıç |
| 2026-04-19 (1. oturum) | ~86/100 | +8 puan |
| 2026-04-19 (2. oturum) | ~91/100 | +5 puan |
| 2026-04-19 (3. oturum) | ~93/100 | +2 puan |
| 2026-04-20 (4. oturum) | ~96/100 | +3 puan |

**4. oturum skor artışının dağılımı:**
- Blog hub + 3 makale (content gap kapatıldı): +1.5
- 2 havalimanı lokasyon sayfası (local/geo intent): +0.5
- 5 lastik marka sayfası (commercial intent): +0.5
- ads.txt (AdSense compliance): +0.5

**Kalan bekleyenler (kod ile):**
- İçerik genişletme (blog, otoyol sayfaları, EV, lastik marka hub)
- Lastik marka hub index sayfası (`tyres/index.html`)

**Kod dışı bekleyenler:**
- Google Search Console, GBP, Trustpilot, OG görselleri
