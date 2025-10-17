# Kütüphane Yönetim Sistemi (PyQt5)

Python ve PyQt5 ile geliştirilmiş, SQLite veritabanı kullanan basit bir kütüphane yönetim uygulaması.

## Özellikler
- Kitap, üye ve ödünç verme işlemleri
- Excel (openpyxl) ile içe/dışa aktarma
- PDF rapor üretimi (reportlab)
- Giriş ekranı, rol tabanlı yetkilendirme (admin/görevli)
- Otomatik yedekleme ve ayar yönetimi

## Hızlı Başlangıç

Gereksinimler: Python 3.x (Windows önerilir), pip

1) Sanal ortam oluşturun ve etkinleştirin

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux (opsiyonel)
source .venv/bin/activate
```

2) Bağımlılıkları kurun

```bash
pip install -r requirements.txt
```

3) Uygulamayı çalıştırın

```bash
python kutuphane.py
```

İlk çalıştırmada veritabanı ve gerekli klasörler otomatik oluşturulur.

- Varsayılan yönetici kullanıcı: `Admin`
- Varsayılan şifre: `12345`

## Klasörler
- `db/`: Veritabanı dosyası (otomatik oluşur)
- `yedek/`: Otomatik yedekler
- `disa_aktar/`: Dışa aktarılan dosyalar
- `ice_aktar/`: İçe aktarım kaynakları
- `raporlar/`: Oluşturulan PDF raporları

Not: Bu klasörlerin içerikleri `.gitignore` ile izleme dışıdır; klasörlerin repo içinde görünmesi için `.gitkeep` yerleştirildi.

## EXE Oluşturma (Windows)
PyInstaller kullanarak tek dosya EXE üretebilirsiniz:

```bash
pip install pyinstaller
python build.py
```

Çıktı, `dist/` klasöründe `kutuphane_YYYY-MM-DD_HH-MM.exe` adıyla oluşur.

## PDF Türkçe Karakter Desteği
Uygulama PDF için Arial fontunu kullanmayı dener. Windows’ta `C:\\Windows\\Fonts\\Arial.ttf` yolunda bulunur. Sisteminizde font yoksa `kutuphane.py` içindeki `FONT_PATH` ayarını uygun bir TTF yoluna güncelleyebilirsiniz; aksi halde Helvetica kullanılır ve Türkçe karakterlerde sorun yaşanabilir.

## Sorun Giderme
- PyInstaller bulunamıyor: `pip install pyinstaller`
- Qt platform hataları: PyQt5 kurulumunu tekrar yükleyin, mümkünse temiz sanal ortamda deneyin.
- Yazma izni/klasör yok: Uygulamayı yazma izni olan bir dizinde çalıştırın.

## Geliştirme Notu
Kod düzeni veya ek test/CI ihtiyaçlarınız varsa belirtin; ilgili dosyaları ekleyebilirim.
