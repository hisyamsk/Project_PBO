import sqlite3
from datetime import datetime
import Toko

dbName = "toko.db"

conn = sqlite3.connect(dbName)

class Pembeli(Toko.Toko):

    __keranjang = []
    total = 0

    def __init__(self, nama):
        self._nama = nama

    def tampilkan_menu(self): #overriding
        Toko.Toko.cek_tgl()
        cursor = conn.cursor().execute("select * from daftar_barang")
        print("="*20+"MENU"+"="*20)
        print("|ID|\t|Nama Barang|\t|Harga|  \t|Stok|")
        for row in cursor:
            print(f"|{row[0]}|\t\t|{row[1]}|\t\t|{row[2]}|\t\t|{row[3]}|")

    def tambah_keranjang(self, id, jumlah):
        cursor = conn.cursor().execute("select * from daftar_barang where id_barang = ?", (id, ))
        if cursor.fetchone() is None:
            print("barang tidak ditemukan")
        else:
            data = conn.execute("select * from daftar_barang where id_barang = ?", (id, ))
            data_stok = data.fetchone()[3]
            data = conn.execute("select * from daftar_barang where id_barang = ?", (id,))
            data_nama = data.fetchone()[1]
            data = conn.execute("select * from daftar_barang where id_barang = ?", (id,))
            data_harga = data.fetchone()[2]
            if jumlah > data_stok:
                print("stok tidak mencukupi")
            else:
                if Toko.Toko.status_diskon == True:
                    temp = [data_nama, jumlah, (jumlah * (data_harga*(1 - Toko.Toko.diskon)))]
                else:
                    temp = [data_nama, jumlah, jumlah*data_harga]
                self.__keranjang.append(temp)
                conn.cursor().execute("update daftar_barang set stok = ? where id_barang = ?", ((data_stok - jumlah), id))
                conn.commit()
                print("barang berhasil ditambahkan ke keranjang")

    def total_belanja(self):
        print("="*20+"Total Belanja"+"="*20)
        print(f"|No.|\t|Barang|\t|Jumlah|\t|Harga|")
        for i in range(0, len(self.__keranjang)):
            self.total += self.__keranjang[i][2]
            print(f"|{i+1}  |\t|{self.__keranjang[i][0]}| \t|  {self.__keranjang[i][1]}  |  \t|{self.__keranjang[i][2]}|")
        print("="*50)
        print(f"Total : {self.total}")
        print("="*50)

    def bayar(self, uang):
        if uang < self.total:
            print("uang tidak mecukupi")
        else:
            for barang in self.__keranjang:
                last_id = conn.cursor().execute("select max(id_transaksi) from transaksi")
                new_id = last_id.fetchone()[0] + 1
                getId_barang = conn.cursor().execute("select id_barang from daftar_barang where nama = ?", (barang[0], ))
                id_barang = getId_barang.fetchone()[0]
                conn.execute("insert into transaksi values (?, ?, ?, ?, ?, ?)", (new_id, self._nama, id_barang, barang[1], barang[2], Toko.Toko.current_date()))
                conn.commit()
            print(f"Pembelian atas nama {self._nama}, berhasil.\nKembalian : {uang-self.total}")