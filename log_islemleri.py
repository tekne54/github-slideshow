import sqlite3
import re
from datetime import datetime

DB_DOSYASI = "deneme.sqlite"
LOG_DOSYASI = "test.log"

def ayristir_log_satiri(satir):
    """
    Verilen bir log satırını Regex kullanarak ayrıştırır.
    Eğer satır beklenen formata uyuyorsa, verileri bir demet (tuple) olarak döndürür.
    Uymuyorsa None döndürür.
    """
    desen = re.compile(
        r"<(\d+)>"
        r"([A-Za-z]{3})\s+"
        r"(\d{1,2})\s+"
        r"([\d:]{8})\s+"
        r"(\d{4})\s+"
        r"([\w\s.-]+?)\s+"  # Makine adı (tembel eşleşme)
        r"((?:src|dst|msg|note)=.*)"  # Satırın geri kalanı bilinen bir anahtarla başlamalı
    )
    eslesme = desen.match(satir)
    if not eslesme:
        return None

    gruplar = eslesme.groups()
    ay, gun, saat, yil, makine, kalan_kisim = gruplar[1], gruplar[2], gruplar[3], gruplar[4], gruplar[5].strip(), gruplar[6]
    tarih = f"{gun} {ay} {yil}"
    detaylar = dict(re.findall(r'(\w+)="([^"]*)"', kalan_kisim))
    kaynak = detaylar.get("src", "")
    hedef = detaylar.get("dst", "")
    mesaj = detaylar.get("msg", "")
    not_ = detaylar.get("note", "")

    if "dhcp" in mesaj and "src_mac" in kalan_kisim:
        mac_eslesme = re.search(r'src_mac=([\w:]+)', kalan_kisim)
        if mac_eslesme:
            mesaj = f"dhcp request mac={mac_eslesme.group(1)}"

    return (tarih, saat, makine, kaynak, hedef, mesaj, not_)

def veritabani_baglantisi_kur(db_dosyasi=DB_DOSYASI):
    """Verilen SQLite veritabanı dosyasına bir bağlantı ve imleç oluşturur."""
    baglanti = sqlite3.connect(db_dosyasi)
    imlec = baglanti.cursor()
    return baglanti, imlec

def tabloyu_olustur(imlec):
    """'zyxel_log' tablosunu, eğer mevcut değilse, oluşturur ve geliştirir."""
    imlec.execute("""
        CREATE TABLE IF NOT EXISTS zyxel_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarih TEXT,
            saat TEXT,
            makine TEXT,
            sourge TEXT,
            destination TEXT,
            mesagge TEXT,
            note TEXT,
            islenme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

def log_kaydini_ekle(imlec, log_verisi):
    """Veritabanına tek bir log kaydı ekler."""
    sorgu = "INSERT INTO zyxel_log (tarih, saat, makine, sourge, destination, mesagge, note) VALUES (?, ?, ?, ?, ?, ?, ?)"
    imlec.execute(sorgu, log_verisi)

def loglari_isle_ve_kaydet(log_dosyasi=LOG_DOSYASI, db_dosyasi=DB_DOSYASI):
    """
    Log dosyasını okur, ayrıştırır ve veritabanına kaydeder.
    Başarıyla eklenen kayıt sayısını döndürür.
    """
    baglanti, imlec = veritabani_baglantisi_kur(db_dosyasi)
    tabloyu_olustur(imlec)

    kayit_sayaci = 0
    try:
        with open(log_dosyasi, "r", encoding="utf-8") as fp:
            for satir in fp:
                if not satir.strip():
                    continue

                log_verisi = ayristir_log_satiri(satir)
                if log_verisi:
                    log_kaydini_ekle(imlec, log_verisi)
                    kayit_sayaci += 1
        baglanti.commit()
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        baglanti.rollback() # Hata durumunda değişiklikleri geri al
    finally:
        baglanti.close() # Bağlantıyı her durumda kapat

    print(f"{kayit_sayaci} adet kayıt veritabanına başarıyla aktarıldı.")
    return kayit_sayaci
