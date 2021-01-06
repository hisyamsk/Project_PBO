import sqlite3
from datetime import datetime
import Toko
import Manajer
import Pembeli

dbName = "toko.db"

conn = sqlite3.connect(dbName)

conn.execute(
    "CREATE TABLE IF NOT EXISTS daftar_barang (id_barang integer primary key, nama text, harga integer, stok integer)"
)

conn.execute(
    "CREATE TABLE IF NOT EXISTS manajer (username text primary key, password text)"
)

daftarBarang = [
    # [Nama Barang, Harga, Stok]
    Toko.Toko(1, "Wafer", 8000, 35),
    Toko.Toko(2, "Biskuit", 5000, 24),
    Toko.Toko(3, "Keripik", 10000, 44),
    Toko.Toko(4, "Coklat", 12000, 15),
    Toko.Toko(5, "Tortilla", 9000, 18)
]

for barang in daftarBarang:
    res = conn.cursor().execute("select * from daftar_barang where id_barang = ?", (barang.get_id(), ))
    if res.fetchone() is None:
        conn.cursor().execute("insert into daftar_barang values (?, ?, ?, ?)", (barang.get_id(), barang.get_nama(), barang.get_harga(), barang.get_jumlah()))
        conn.commit()

daftar_manajer = [
    Manajer.Manajer("hisyamsk", "abcdef123"),
    Manajer.Manajer("adit", "password123")
]

for manajer in daftar_manajer:
    res = conn.cursor().execute("select * from manajer where username = ?", (manajer.get_username(), ))
    if res.fetchone() is None:
        conn.cursor().execute("insert into manajer values (?, ?)", (manajer.get_username(), manajer.get_password()))
        conn.commit()

menu = int(input("1. Pembeli\n2. Manajer\nSilahkan pilih nomor user: "))
if menu == 1:
    pembeli = Pembeli.Pembeli(input("Silahkan masukkan nama anda: "))
    print("""Fitur
     1. Tampilkan Menu
     2. Tambahkan ke keranjang
     3. Total belanja
     4. Bayar
     5. Exit""")
    while True:
        menu_pembeli = int(input("Masukkan pilihan nomor: "))
        if menu_pembeli == 1:
            pembeli.tampilkan_menu()
        elif menu_pembeli == 2:
            pembeli.tambah_keranjang(int(input("masukkan id barang: ")), int(input("masukkan jumlah: ")))
        elif menu_pembeli == 3:
            pembeli.total_belanja()
        elif menu_pembeli == 4:
            pembeli.bayar(int(input("masukkan nominal uang: ")))
            break
        else:
            break
elif menu == 2:
    logged = False
    while True:
        if logged == False:
            manajer = Manajer.Manajer(input("username: "), input("password: "))
            login = conn.cursor().execute("select * from manajer where username = ? and password = ?", (manajer.get_username(), manajer.get_password(), ))
            if login.fetchone() is None:
                print("incorrect username or password")
            else:
                logged = True
        else:
            menu_manajer = int(input("""Fitur
 1. Tambah Item
 2. Hapus Item
 3. Ganti Diskon
 4. Tampilkan Menu
 5. Exit
 Pilih nomor: """))
            if menu_manajer == 1:
                manajer.tambah_item(input("masukkan nama barang: "), int(input("masukkan harga: ")), int(input("masukkan jumlah: ")))
            elif menu_manajer == 2:
                inputan = input(("""1. Hapus by id
2. Hapus by nama
Pilih no: """))
                if inputan == "1":
                    val = int(input("masukkan id: "))
                    manajer.hapus_item(val)
                elif inputan == "2":
                    val = input("masukkan nama barang: ")
                    manajer.hapus_item(val)
            elif menu_manajer == 3:
                print(f"current discount = {manajer.diskon * 100}%")
                manajer.ganti_diskon(int(input("masukkan jumlah diskon (dalam %): ")))
            elif menu_manajer == 4:
                manajer.tampilkan_menu()
            else:
                logged = False
                break

conn.close()