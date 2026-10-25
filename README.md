# site-yazilar

ilkerakturk.com.tr için blog yazısı taslakları. Bu depo bir köprüdür:
Claude haftalık taslağı `yazilar/` klasörüne JSON olarak bırakır; sitedeki günlük görev
(`panel/cron.php`) klasörü okur, yeni dosyaları yazı olarak ekler, `yayinda: true` olanları yayınlar.

## Dosya biçimi (`yazilar/YYYY-AA-GG-kisa-ad.json`)

```json
{
  "baslik": "Yazının başlığı",
  "ozet": "Listelerde görünen bir iki cümle.",
  "icerik": "<p>HTML paragraflar…</p>",
  "tarih": "2026-11-03",
  "kategori": "danisan | meslektas | arastirma",
  "yayinda": false,
  "yayinTarihi": "",
  "gorselUrl": "",
  "kontrol": "KONTROL NOTU ... (KONTROL.md biçiminde; panelde yazının üstünde görünür, sitede yayımlanmaz)"
}
```

- `icerik` yerine `markdown` alanı da kullanılabilir (site Markdown'ı HTML'e çevirir).
- `yayinda: false` ise yazı sitede taslak olarak bekler; `true` yapılıp gönderildiğinde bir sonraki
  görev çalışmasında yayına girer. Dosya sonradan değişirse site de güncellenir.
- `yayinTarihi` doluysa (örn. `2026-11-10`) yazı o gün otomatik yayına alınır.
- Dosya silinirse sitedeki yazı silinmez; sitedeki kaydı panelden ya da e-postadaki bağlantıyla kaldırın.

## Yazım ve kontrol
- Üslup: `STIL.md` (İlker'in dili + konuşma iskeleti + hizmet dili + arama kuralları).
- Konular: `KONULAR.md` (kategori sırası ve hedef aramalar).
- Her taslak `KONTROL.md`'deki beş adımdan geçer: bilgi doğruluğu, alıntı doğrulaması,
  İlker'e uygunluk, biçim. Sonuç `kontrol` alanına yazılır.

## Akış

1. Her hafta Claude bir taslak hazırlar, buraya `yayinda: false` ile koyar ve sohbette sorar: "Yükleyeyim mi?"
2. "Yükle" dendiğinde `yayinda: true` yapar. Alternatif: sitenin gönderdiği e-postadaki "Yayınla" bağlantısı.
3. Sitedeki günlük görev yazıyı alır ve yayınlar.

## Hosting tarafı
Depo herkese açık (public) olduğu sürece site anahtarsız okur. Depo gizliye çevrilirse okuma anahtarı gerekir:

GitHub > Settings > Developer settings > Personal access tokens > Fine-grained tokens > Generate new token:
Repository access: Only select repositories > `site-yazilar`; Permissions: Contents > Read-only.
Üretilen anahtarı sitede Panel > Otomasyon > "Erişim anahtarı" alanına yapıştırıp kaydedin.
