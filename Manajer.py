import sqlite3
from datetime import datetime
import Toko

dbName = "toko.db"

conn = sqlite3.connect(dbName)


class Manajer(Toko.Toko):

    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def tampilkan_menu(self): #overriding
        cursor = conn.cursor().execute("select * from daftar_barang")
        print("=" * 20 + "MENU" + "=" * 20)
        print("|ID|\t|Nama Barang|\t|Harga|  \t|Stok|")
        for row in cursor:
            print(f"|{row[0]}|\t\t|{row[1]}|\t\t|{row[2]}|\t\t|{row[3]}|")

    def tambah_item(self, barang, harga, jumlah):
        res = conn.cursor().execute("select * from daftar_barang where nama = ?", (barang, ))
        if res.fetchone() is None:
            last_id = conn.cursor().execute("select max(id_barang) from daftar_barang")
            new_id = last_id.fetchone()[0] + 1
            conn.cursor().execute("insert into daftar_barang values (?, ?, ?, ?)", (new_id, barang, harga, jumlah))
            conn.commit()
            print("barang berhasil ditambahkan")
        else:
            data = conn.cursor().execute("select stok from daftar_barang where nama = ?", (barang, ))
            tambah_stok = data.fetchone()[0] + jumlah
            conn.cursor().execute("update daftar_barang set stok = ? where nama = ?", (tambah_stok, barang))
            conn.commit()
            data = conn.cursor().execute("select harga from daftar_barang where nama = ?", (barang, ))
            ganti_harga = data.fetchone()[0]
            conn.cursor().execute("update daftar_barang set harga = ?", (ganti_harga))
            conn.commit()
            print("barang sudah tersedia, program akan mengganti harga dan menambah jumlah stok")

    def ganti_diskon(self, nilai):
        Toko.Toko.diskon = (nilai/100)
        print(f"Diskon berhasil diubah menjadi {nilai}%")

    def hapus_item(self, param): #overloading
        if type(param) == str:
            self.__hapus_by_barang(param)
        elif type(param) == int:
            self.__hapus_by_id(param)

    def __hapus_by_barang(self, barang):
        res = conn.cursor().execute("select * from daftar_barang where nama = ?", (barang, ))
        if res.fetchone() is None:
            print("barang tidak ditemukan")
        else:
            data = conn.cursor().execute("select nama from daftar_barang where nama = ?", (barang, ))
            nama = data.fetchone()[0]
            conn.cursor().execute("delete from daftar_barang where nama = ?", (nama, ))
            conn.commit()
            print("barang berhasil dihapus")

    def __hapus_by_id(self, id):
        res = conn.cursor().execute("select * from daftar_barang where id_barang = ?", (id, ))
        if res.fetchone() is None:
            print("barang tidak ditemukan")
        else:
            conn.cursor().execute("delete from daftar_barang where id_barang = ?", (id, ))
            conn.commit()
            print("Barang berhasil dihapus")