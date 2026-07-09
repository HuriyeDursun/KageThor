import sys
import os
import yt_dlp
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QComboBox, QLabel, QProgressBar, QFileDialog)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QIcon

def kaynak_yolu(goreceli_yol):
    """ PyInstaller ile paketlendiğinde geçici klasördeki dosyaları bulur """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, goreceli_yol)


# --- İNDİRME İŞLEMİNİ ARKA PLANDA YAPACAK İŞ PARÇACIĞI ---
class IndirmeGorevi(QThread):
    ilerleme_sinyali = pyqtSignal(int)
    durum_sinyali = pyqtSignal(str)

    def __init__(self, url, format_secimi, hedef_klasor):
        super().__init__()
        self.url = url
        self.format_secimi = format_secimi
        self.hedef_klasor = hedef_klasor
        self.iptal_edildi = False  # İptal kontrolü için flag

    def iptal_et(self):
        self.iptal_edildi = True

    def ilerleme_kancasi(self, d):
        # Eğer kullanıcı "İptal" butonuna bastıysa, yt-dlp'yi zorla durduruyoruz
        if self.iptal_edildi:
            raise Exception("KULLANICI_IPTAL_ETTI")

        if d['status'] == 'downloading':
            yuzde_str = d.get('_percent_str', '0.0%').replace('%', '').strip()
            yuzde_str = ''.join([c for c in yuzde_str if c in '0123456789.'])

            hiz = d.get('_speed_str', '~')
            kalan_sure = d.get('_eta_str', '~')

            try:
                yuzde = int(float(yuzde_str))
                self.ilerleme_sinyali.emit(yuzde)
                self.durum_sinyali.emit(f"İndiriliyor... %{yuzde}  |  Hız: {hiz}  |  Kalan: {kalan_sure}")
            except:
                pass
        elif d['status'] == 'finished':
            self.ilerleme_sinyali.emit(100)
            self.durum_sinyali.emit("İndirme bitti, video işleniyor (Lütfen bekleyin)...")

    def run(self):
        try:
            self.durum_sinyali.emit("Bağlantı kuruluyor...")

            # İnecek dosyanın tam yolunu ayarlıyoruz
            cikis_yolu = os.path.join(self.hedef_klasor, '%(title)s.%(ext)s')

            if "MP4" in self.format_secimi:
                ydl_opts = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'format_sort': ['vcodec:h264'],  # Her cihazda açılması için
                    'outtmpl': cikis_yolu,
                    'merge_output_format': 'mp4',
                    'noplaylist': True,
                    'progress_hooks': [self.ilerleme_kancasi],
                    'extractor_args': {'youtube': {'player_client': ['default', '-android_sdkless']}},
                }
            else:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': cikis_yolu,
                    'noplaylist': True,
                    'progress_hooks': [self.ilerleme_kancasi],
                    'extractor_args': {'youtube': {'player_client': ['default', '-android_sdkless']}},
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])

            self.durum_sinyali.emit("İşlem başarıyla tamamlandı!")

        except Exception as e:
            # Hata mesajı iptalden mi kaynaklandı yoksa normal bir hata mı kontrol ediyoruz
            if str(e) == "KULLANICI_IPTAL_ETTI":
                self.durum_sinyali.emit("İndirme işlemi iptal edildi.")
                self.ilerleme_sinyali.emit(0)
            else:
                self.durum_sinyali.emit(f"Hata: {str(e)}")


# --- ARAYÜZ ---
class AnaPencere(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Video & Müzik İndirici ")
        self.setWindowIcon(QIcon(kaynak_yolu("app.ico")))
        self.setFixedSize(600, 380)

        # Koyu Tema
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E2E;
                color: #CDD6F4;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-weight: bold;
                margin-bottom: 5px;
            }
            QLineEdit, QComboBox {
                background-color: #313244;
                border: 2px solid #45475A;
                border-radius: 8px;
                padding: 10px;
                color: #CDD6F4;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #89B4FA;
            }
            QPushButton {
                background-color: #89B4FA;
                color: #1E1E2E;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #B4BEFE;
            }
            QPushButton:disabled {
                background-color: #45475A;
                color: #A6ADC8;
            }
            /* İptal Butonu için Özel Tasarım */
            QPushButton#iptalBtn {
                background-color: #F38BA8;
            }
            QPushButton#iptalBtn:hover {
                background-color: #F9A8D4;
            }
            QPushButton#iptalBtn:disabled {
                background-color: #45475A;
            }
            /* Gözat Butonu için Özel Tasarım */
            QPushButton#gozatBtn {
                background-color: #A6E3A1;
            }
            QPushButton#gozatBtn:hover {
                background-color: #CBA6F7;
            }
            QProgressBar {
                border: 2px solid #45475A;
                border-radius: 8px;
                text-align: center;
                color: white;
                font-weight: bold;
                background-color: #1E1E2E;
            }
            QProgressBar::chunk {
                background-color: #A6E3A1;
                border-radius: 6px;
            }
        """)

        ana_duzen = QVBoxLayout()
        ana_duzen.setContentsMargins(25, 25, 25, 25)
        ana_duzen.setSpacing(15)

        # 1. Konum Seçme Alanı
        self.konum_etiketi = QLabel("İndirilecek Konum:")
        ana_duzen.addWidget(self.konum_etiketi)

        konum_duzeni = QHBoxLayout()
        self.konum_kutusu = QLineEdit()
        # Varsayılan olarak bilgisayarın "İndirilenler" klasörünü ayarla
        varsayilan_konum = os.path.join(os.path.expanduser('~'), 'Downloads')
        self.konum_kutusu.setText(varsayilan_konum)
        self.konum_kutusu.setReadOnly(True)  # Kullanıcı elle yazamasın, butonla seçsin

        self.gozat_butonu = QPushButton("Gözat")
        self.gozat_butonu.setObjectName("gozatBtn")
        self.gozat_butonu.setCursor(Qt.CursorShape.PointingHandCursor)
        self.gozat_butonu.clicked.connect(self.klasor_sec)

        konum_duzeni.addWidget(self.konum_kutusu)
        konum_duzeni.addWidget(self.gozat_butonu)
        ana_duzen.addLayout(konum_duzeni)

        # 2. Link Giriş Alanı
        self.bilgi_etiketi = QLabel("İndirmek istediğiniz videonun linkini yapıştırın:")
        ana_duzen.addWidget(self.bilgi_etiketi)

        self.link_kutusu = QLineEdit()
        self.link_kutusu.setPlaceholderText("https://www.youtube.com/watch?v=...")
        ana_duzen.addWidget(self.link_kutusu)

        # 3. İndirme Butonları ve Format
        alt_duzen = QHBoxLayout()
        alt_duzen.setSpacing(10)

        self.format_kutusu = QComboBox()
        self.format_kutusu.addItems([" MP4 (Video) ", " MP3 (Ses) "])
        self.format_kutusu.setFixedWidth(140)
        alt_duzen.addWidget(self.format_kutusu)

        self.indir_butonu = QPushButton("İNDİR")
        self.indir_butonu.setCursor(Qt.CursorShape.PointingHandCursor)
        self.indir_butonu.clicked.connect(self.indirmeyi_baslat)
        alt_duzen.addWidget(self.indir_butonu)

        self.iptal_butonu = QPushButton("İPTAL")
        self.iptal_butonu.setObjectName("iptalBtn")
        self.iptal_butonu.setEnabled(False)  # İndirme başlamadan iptal butonu pasiftir
        self.iptal_butonu.setCursor(Qt.CursorShape.PointingHandCursor)
        self.iptal_butonu.clicked.connect(self.indirmeyi_iptal_et)
        alt_duzen.addWidget(self.iptal_butonu)

        ana_duzen.addLayout(alt_duzen)

        # 4. İlerleme Çubuğu ve Durum Mesajı
        self.ilerleme_cubugu = QProgressBar()
        self.ilerleme_cubugu.setValue(0)
        self.ilerleme_cubugu.setFixedHeight(25)
        ana_duzen.addWidget(self.ilerleme_cubugu)

        self.durum_etiketi = QLabel("Hazır. Link yapıştırıp indirmeye başlayabilirsiniz.")
        self.durum_etiketi.setStyleSheet("color: #A6ADC8; font-weight: bold; font-size: 13px;")
        self.durum_etiketi.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ana_duzen.addWidget(self.durum_etiketi)

        self.setLayout(ana_duzen)

    def klasor_sec(self):
        klasor = QFileDialog.getExistingDirectory(self, "İndirme Klasörünü Seç")
        if klasor:
            # Seçilen klasörün yolunu düzeltip kutuya yaz
            self.konum_kutusu.setText(os.path.normpath(klasor))

    def indirmeyi_baslat(self):
        url = self.link_kutusu.text().strip()
        hedef_klasor = self.konum_kutusu.text()

        if not url:
            self.durum_etiketi.setText("Lütfen geçerli bir link girin!")
            return
        if not os.path.exists(hedef_klasor):
            self.durum_etiketi.setText("Seçilen klasör bulunamadı!")
            return

        secilen_format = self.format_kutusu.currentText()

        # Butonları ayarla
        self.indir_butonu.setEnabled(False)
        self.link_kutusu.setEnabled(False)
        self.iptal_butonu.setEnabled(True)
        self.ilerleme_cubugu.setValue(0)

        # Görevi başlat
        self.gorev = IndirmeGorevi(url, secilen_format, hedef_klasor)
        self.gorev.ilerleme_sinyali.connect(self.ilerleme_guncelle)
        self.gorev.durum_sinyali.connect(self.durum_guncelle)
        self.gorev.finished.connect(self.gorev_bitti)
        self.gorev.start()

    def indirmeyi_iptal_et(self):
        if hasattr(self, 'gorev') and self.gorev.isRunning():
            self.durum_etiketi.setText("İptal ediliyor, lütfen bekleyin...")
            self.iptal_butonu.setEnabled(False)
            self.gorev.iptal_et()

    def ilerleme_guncelle(self, deger):
        self.ilerleme_cubugu.setValue(deger)

    def durum_guncelle(self, mesaj):
        self.durum_etiketi.setText(mesaj)
        if "Hata" in mesaj or "iptal" in mesaj.lower():
            self.durum_etiketi.setStyleSheet("color: #F38BA8; font-weight: bold; font-size: 13px;")
        elif "başarıyla" in mesaj:
            self.durum_etiketi.setStyleSheet("color: #A6E3A1; font-weight: bold; font-size: 13px;")
        else:
            self.durum_etiketi.setStyleSheet("color: #89B4FA; font-weight: bold; font-size: 13px;")

    def gorev_bitti(self):
        # Arayüzü eski haline döndür
        self.indir_butonu.setEnabled(True)
        self.link_kutusu.setEnabled(True)
        self.iptal_butonu.setEnabled(False)
        self.link_kutusu.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pencere = AnaPencere()
    pencere.show()
    sys.exit(app.exec())