import os
import subprocess
import datetime

# İkon ayarları
ICON_DIR = os.path.join("assets")
ICON_PATH = os.path.join(ICON_DIR, "book.ico")

# --- Ayarlanabilir Değişkenler ---
# Derlenecek ana Python dosyasının adı
ANA_DOSYA = "kutuphane.py"
# Exe dosyasının temel adı
EXE_ADI = "kutuphane"


def ensure_book_icon() -> str:
    """
    'assets/book.ico' mevcut değilse, PyQt5 ile basit bir kitap ikonu üretir.
    Başarılıysa ikon yolunu, aksi halde boş string döner.
    """
    try:
        if os.path.exists(ICON_PATH):
            return ICON_PATH

        # Klasörü oluştur
        os.makedirs(ICON_DIR, exist_ok=True)

        # PyQt5 ile basit bir ikon çiz
        from PyQt5.QtGui import QImage, QPainter, QColor, QBrush, QPen
        from PyQt5.QtCore import Qt, QPoint
        try:
            # QImage/QPainter için QApplication şart değil; ancak bazı ortamlarda
            # ihtiyaç duyulabilir. Gerekirse oluştur.
            from PyQt5.QtWidgets import QApplication
            _app = QApplication.instance() or QApplication([])
        except Exception:
            _app = None

        size = 256
        img = QImage(size, size, QImage.Format_ARGB32)
        img.fill(Qt.transparent)

        p = QPainter(img)
        p.setRenderHint(QPainter.Antialiasing, True)

        # Arka plan gölge (hafif)
        shadow = QColor(0, 0, 0, 40)
        p.setBrush(QBrush(shadow))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(30, 36, 196, 196, 12, 12)

        # Kitap sırtı
        spine = QColor("#0D47A1")
        p.setBrush(QBrush(spine))
        p.setPen(QPen(QColor("#08306B"), 3))
        p.drawRoundedRect(40, 40, 36, 180, 8, 8)

        # Kapak
        cover = QColor("#1565C0")
        p.setBrush(QBrush(cover))
        p.setPen(QPen(QColor("#0E4FA8"), 3))
        p.drawRoundedRect(70, 40, 140, 180, 10, 10)

        # Sayfa kenar çizgileri
        p.setPen(QPen(QColor("#E0E0E0"), 2))
        for x in (190, 200, 210):
            p.drawLine(x, 52, x, 206)

        # Ayraç (bookmark)
        p.setBrush(QBrush(QColor("#E53935")))
        p.setPen(Qt.NoPen)
        p.drawPolygon(
            QPoint(170, 40), QPoint(190, 40), QPoint(180, 90)
        )

        p.end()

        # ICO olarak kaydet
        if img.save(ICON_PATH, "ICO"):
            return ICON_PATH
        else:
            # Bazı ortamlarda ICO kaydı başarısız olabilir
            return ""
    except Exception:
        return ""

def build_executable_with_timestamp():
    """
    Ana Python dosyasını PyInstaller ile derler,
    oluşturulan EXE dosyasına tarih ve saat damgası ekler ve
    terminal penceresinin açılmasını engeller.
    """
    if not os.path.exists(ANA_DOSYA):
        print(f"Hata: '{ANA_DOSYA}' dosyası bulunamadı.")
        return

    # Geçerli tarih ve saati YYYY-MM-DD_HH-MM formatında al
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    # Yeni EXE dosyasının adını oluştur
    yeni_exe_adi = f"{EXE_ADI}_{timestamp}"
    
    print(f"Derleme işlemi başlatılıyor: {ANA_DOSYA}")
    print(f"Oluşturulacak EXE adı: {yeni_exe_adi}.exe")
    print("Not: Bu işlem sırasında terminal penceresi açılmayacaktır.")

    # İkonu hazırla (varsa kullan, yoksa üret)
    icon_path = ensure_book_icon()
    if icon_path:
        print(f"İkon kullanılacak: {icon_path}")
    else:
        print("Uyarı: .ico oluşturulamadı ya da bulunamadı; ikonsuz derlenecek.")

    # PyInstaller komutunu oluştur
    command = [
        "pyinstaller",
        "--onefile",  # Tek bir EXE dosyası oluşturur
        "--windowed", # veya "--noconsole" Terminal penceresini engeller
        f"--name={yeni_exe_adi}",
    ]

    # İkon parametresi
    if icon_path:
        command.append(f"--icon={icon_path}")

    # Veri klasörlerini ekle
    command += [
        f"--add-data={os.path.join('.', 'db')}{os.pathsep}db",
        f"--add-data={os.path.join('.', 'yedek')}{os.pathsep}yedek",
        f"--add-data={os.path.join('.', 'disa_aktar')}{os.pathsep}disa_aktar",
        f"--add-data={os.path.join('.', 'ice_aktar')}{os.pathsep}ice_aktar",
        f"--add-data={os.path.join('.', 'raporlar')}{os.pathsep}raporlar",
        ANA_DOSYA,
    ]

    try:
        # Komutu çalıştır ve çıktıyı göster
        subprocess.run(command, check=True)
        print("\nDerleme başarıyla tamamlandı!")
        print(f"Çıktı dosyası: dist/{yeni_exe_adi}.exe")
    except subprocess.CalledProcessError as e:
        print("\nDerleme hatası oluştu:")
        print(e)
    except FileNotFoundError:
        print("\nHata: PyInstaller bulunamadı.")
        print("Lütfen 'pip install pyinstaller' komutu ile kurduğunuzdan emin olun.")
        
if __name__ == "__main__":
    build_executable_with_timestamp()
