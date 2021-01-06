import sqlite3
from datetime import datetime

dbName = "toko.db"

conn = sqlite3.connect(dbName)


class Toko:

    def __init__(self, id, nama, harga, jumlah):
        self._id = id
        self._nama = nama
        self._harga = harga
        self._jumlah = jumlah

    def get_id(self):
        return self._id

    def get_nama(self):
        return self._nama

    def get_harga(self):
        return self._harga

    def get_jumlah(self):
        return self._jumlah

    def tampilkan_menu(self):
        pass

    @staticmethod
    def current_date():
        date = datetime.now()
        return date

    diskon = 0.15
    # tglSekarang = datetime.now()
    tglSekarang = datetime(2020, 12, 12)
    status_diskon = False

    @classmethod
    def cek_tgl(cls):
        if cls.tglSekarang.day == cls.tglSekarang.month:
            print(
                f"sekarang tanggal {cls.tglSekarang.day}-{cls.tglSekarang.month}, berlaku diskon sebesar {cls.diskon * 100}% untuk semua produk")
            cls.status_diskon = True