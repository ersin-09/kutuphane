import os
import subprocess
import datetime

# --- Ayarlanabilir Değişkenler ---
# Derlenecek ana Python dosyasının adı
ANA_DOSYA = "kutuphane.py"
# Exe dosyasının temel adı
EXE_ADI = "kutuphane"

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

    # PyInstaller komutunu oluştur
    command = [
        "pyinstaller",
        "--onefile",  # Tek bir EXE dosyası oluşturur
        "--windowed", # veya "--noconsole" Terminal penceresini engeller
        f"--name={yeni_exe_adi}",
        f"--add-data={os.path.join('.', 'db')}{os.pathsep}db",
        f"--add-data={os.path.join('.', 'yedek')}{os.pathsep}yedek",
        f"--add-data={os.path.join('.', 'disa_aktar')}{os.pathsep}disa_aktar",
        f"--add-data={os.path.join('.', 'ice_aktar')}{os.pathsep}ice_aktar",
        f"--add-data={os.path.join('.', 'raporlar')}{os.pathsep}raporlar",
        ANA_DOSYA
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