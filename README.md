# ⚡ KageThor - Video & Müzik İndirici 

KageThor, internetin derinliklerindeki videoları yıldırım hızıyla bilgisayarınıza getiren güçlü bir masaüstü medya indirme aracıdır. PyQt6 ve yt-dlp gücüyle çalışır.

## ✨ Özellikler

* **Geniş Platform Desteği:** YouTube, Twitter, Instagram, TikTok ve 1000'den fazla siteden video/ses indirebilme.
* **Format Seçeneği:** En yüksek kalitede MP4 (Video) veya MP3 (Ses) olarak kaydetme.
* **Kullanıcı Dostu:** İndirme konumunu seçebileceğiniz modern, karanlık temalı arayüz.
* **Canlı İlerleme:** İndirme hızını, tahmini süreyi ve yüzdeyi anlık takip etme.
* **Güvenli İptal:** Yanlış tıklamalara karşı indirmeyi anında durdurabilme.

## 🚀 Kurulum ve Çalıştırma (Geliştiriciler İçin)

Eğer projeyi kaynak kodundan çalıştırmak veya geliştirmek isterseniz:

### 1. Depoyu klonlayın:
```bash
git clone https://github.com/HuriyeDursun/KageThor.git
```
### 2. Gerekli kütüphaneleri kurun:
```bash
pip install -r requirements.txt
```

### 3. (ÖNEMLİ) FFmpeg Kurulumu:
Programın görüntü ve sesi yüksek kalitede indirip birleştirebilmesi için FFmpeg aracına ihtiyacı vardır. Amacınıza göre iki farklı şekilde kurabilirsiniz:

**Seçenek A (Sadece Kodu Çalıştırmak İçin - Terminal):**
CMD veya PowerShell'i açıp şu komutu yazarak sisteminize kurabilirsiniz:
```bash
winget install ffmpeg
```

**Seçenek B (Projeyi Yeniden EXE'ye Çevirecekler İçin - Manuel):**
Eğer kodu değiştirip PyInstaller ile yeniden paketleyecekseniz:
* [Gyan.dev FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/) adresinden `ffmpeg-release-essentials.zip` dosyasını indirin.
* Zip içindeki `bin` klasöründe bulunan `ffmpeg.exe` dosyasını doğrudan projenizin ana dizinine (kodların yanına) kopyalayın.

### 4. Programı başlatın:
```bash
python main.py
```

## 📦 Doğrudan İndir (Normal Kullanıcılar İçin)

Kodlarla, kurulumlarla veya FFmpeg ile hiç uğraşmak istemiyorsanız; sağ taraftaki **Releases** bölümünden **KageThor.exe** dosyasını tek tıkla indirip, kurulum gerektirmeden hemen kullanmaya başlayabilirsiniz! (Gerekli tüm altyapı bu EXE dosyasının içine gömülmüştür).

---
*Bu proje eğitim amaçlı ve kişisel kullanım için geliştirilmiştir.*
