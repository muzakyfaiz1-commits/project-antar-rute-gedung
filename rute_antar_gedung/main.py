"""
main.py
=======
Sistem Pencarian Rute Antar-Gedung Kampus
Program console utama: menu CRUD dataset graph, pencarian BFS/DFS,
perbandingan performa, dan eksperimen otomatis.

Jalankan: python main.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from algorithms.search import bfs, dfs
from data.campus_graph import muat_graph_kampus
from data.dataset_generator import (
    DENSITAS_RATA_RATA_KONEKSI,
    generate_dataset,
    muat_gedung_csv,
    muat_jalan_csv,
    nama_file_gedung,
    nama_file_jalan,
    simpan_ke_csv,
)
from experiments.experiment_runner import run_full_experiment, simpan_hasil_csv
from models.gedung import GedungRegistry
from models.graph_adjacency_list import AdjacencyListGraph
from models.graph_adjacency_matrix import AdjacencyMatrixGraph
from utils.metrics import print_table
from utils.tampilan import tampilkan_hasil_rute
from utils.validators import validasi_pencarian_rute

DATASET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "dataset_eksperimen")


class RuteAntarGedungApp:
    """Kelas utama aplikasi. Menyimpan state graph aktif dalam DUA
    representasi sekaligus (Adjacency List & Adjacency Matrix) yang selalu
    disinkronkan setiap ada operasi CRUD, agar pengguna bisa membandingkan
    performa pencarian pada representasi berbeda dari data yang identik.

    `self.gedung` menyimpan pemetaan kode_gedung -> nama_gedung, terpisah
    dari graph, sehingga tampilan selalu memakai nama gedung yang mudah
    dibaca meskipun struktur graph bekerja dengan kode.
    """

    def __init__(self):
        self.list_graph = AdjacencyListGraph()
        self.matrix_graph = AdjacencyMatrixGraph()
        self.gedung = GedungRegistry()
        self.dataset_name = None
        self._muat_graph_default()

    def _muat_graph_default(self):
        """Memuat graph kampus nyata sebagai dataset default saat program mulai."""
        kode_list, daftar_jalan, nama_gedung = muat_graph_kampus()
        self.list_graph = AdjacencyListGraph.from_edges(kode_list, daftar_jalan)
        self.matrix_graph = AdjacencyMatrixGraph.from_edges(kode_list, daftar_jalan)
        self.gedung = GedungRegistry.from_dict(nama_gedung)
        self.dataset_name = "Graph Kampus (default)"

    # ---------------- Menu 1: Buat dataset eksperimen ----------------
    def menu_buat_dataset(self):
        print("\n-- Membuat Dataset Eksperimen Baru --")
        try:
            n = int(input("Jumlah gedung [50/100/250/500 atau bebas]: ").strip())
            if n <= 0:
                raise ValueError
        except ValueError:
            print("Input tidak valid. Jumlah gedung harus bilangan bulat positif.")
            return

        densitas = input("Tingkat kepadatan (jarang/padat) [padat]: ").strip().lower() or "padat"
        if densitas not in DENSITAS_RATA_RATA_KONEKSI:
            print("Kepadatan tidak dikenal, memakai 'padat'.")
            densitas = "padat"

        nama_gedung, daftar_jalan = generate_dataset(n, DENSITAS_RATA_RATA_KONEKSI[densitas])
        self.list_graph = AdjacencyListGraph.from_edges(nama_gedung.keys(), daftar_jalan)
        self.matrix_graph = AdjacencyMatrixGraph.from_edges(nama_gedung.keys(), daftar_jalan)
        self.gedung = GedungRegistry.from_dict(nama_gedung)
        self.dataset_name = f"{n} gedung ({densitas})"

        path_gedung = os.path.join(DATASET_DIR, nama_file_gedung(n))
        path_jalan = os.path.join(DATASET_DIR, nama_file_jalan(n, densitas))
        simpan_ke_csv(nama_gedung, daftar_jalan, path_gedung, path_jalan)
        print(f"Dataset dibuat: {n} gedung, {len(daftar_jalan)} jalan, kepadatan={densitas}.")
        print(f"Disimpan sebagai: {nama_file_gedung(n)} & {nama_file_jalan(n, densitas)}")

    # ---------------- Menu 2: Muat dataset eksperimen ----------------
    def menu_muat_dataset(self):
        print("\n-- Memuat Dataset Eksperimen --")
        if not os.path.isdir(DATASET_DIR) or not any(f.startswith("gedung_") for f in os.listdir(DATASET_DIR)):
            print("Belum ada dataset tersimpan. Buat dataset terlebih dahulu (menu 1).")
            return
        file_gedung = sorted(f for f in os.listdir(DATASET_DIR) if f.startswith("gedung_"))
        for i, f in enumerate(file_gedung, 1):
            print(f"  {i}. {f}")
        pilihan = input("Pilih nomor file gedung: ").strip()
        try:
            nama_file = file_gedung[int(pilihan) - 1]
        except (ValueError, IndexError):
            print("Pilihan tidak valid.")
            return

        n = nama_file.replace("gedung_", "").replace(".csv", "")
        densitas = input("Kepadatan jalan (jarang/padat) [padat]: ").strip().lower() or "padat"
        path_jalan = os.path.join(DATASET_DIR, f"jalan_{n}_{densitas}.csv")
        if not os.path.isfile(path_jalan):
            print(f"File jalan tidak ditemukan: jalan_{n}_{densitas}.csv")
            return

        nama_gedung = muat_gedung_csv(os.path.join(DATASET_DIR, nama_file))
        daftar_jalan = muat_jalan_csv(path_jalan)
        self.list_graph = AdjacencyListGraph.from_edges(nama_gedung.keys(), daftar_jalan)
        self.matrix_graph = AdjacencyMatrixGraph.from_edges(nama_gedung.keys(), daftar_jalan)
        self.gedung = GedungRegistry.from_dict(nama_gedung)
        self.dataset_name = f"{nama_file} + jalan_{n}_{densitas}.csv"
        print(f"Dataset dimuat: {len(nama_gedung)} gedung, {len(daftar_jalan)} jalan.")

    # ---------------- Menu 3: Tampilkan graph ----------------
    def menu_tampilkan_graph(self):
        if self.list_graph.num_nodes() == 0:
            print("\nBelum ada graph aktif. Buat/muat dataset terlebih dahulu.")
            return
        print(f"\n-- Graph Aktif ({self.dataset_name}) --")
        print(f"Jumlah gedung: {self.list_graph.num_nodes()}, jumlah jalan: {self.list_graph.num_edges()}")
        print(f"Semua gedung terhubung: {'Ya' if self.list_graph.is_connected() else 'TIDAK (ada gedung terisolasi!)'}")
        rep = input("Tampilkan sebagai (list/matrix) [list]: ").strip().lower() or "list"
        if self.list_graph.num_nodes() > 30:
            print("(Graph besar, tampilan mungkin panjang)")
        print(self.matrix_graph.display() if rep == "matrix" else self.list_graph.display())

    # ---------------- Menu 4-9: CRUD gedung & jalan ----------------
    def menu_tambah_gedung(self):
        kode = input("\nKode gedung baru: ").strip().upper()
        nama = input("Nama gedung: ").strip()
        if not kode or not nama:
            print("Gagal: kode dan nama tidak boleh kosong.")
            return
        ok1 = self.list_graph.add_node(kode)
        ok2 = self.matrix_graph.add_node(kode)
        ok3 = self.gedung.add(kode, nama)
        print("Gedung berhasil ditambahkan." if ok1 and ok2 and ok3 else "Gagal: kode gedung sudah ada.")

    def menu_tambah_jalan(self):
        a = input("\nKode gedung asal: ").strip().upper()
        b = input("Kode gedung tujuan: ").strip().upper()
        ok1 = self.list_graph.add_edge(a, b)
        ok2 = self.matrix_graph.add_edge(a, b)
        print("Jalan berhasil ditambahkan." if ok1 and ok2 else "Gagal: pastikan kedua kode gedung ada.")

    def menu_ubah_nama_gedung(self):
        kode = input("\nKode gedung: ").strip().upper()
        nama_baru = input("Nama baru: ").strip()
        ok = self.gedung.rename(kode, nama_baru)
        print("Nama gedung berhasil diubah." if ok else "Gagal: kode gedung tidak ditemukan.")

    def menu_ubah_jalan(self):
        a = input("\nJalan dari gedung (kode): ").strip().upper()
        b_lama = input("ke gedung (kode lama): ").strip().upper()
        b_baru = input("Ubah tujuan jalan menjadi kode gedung: ").strip().upper()
        ok1 = self.list_graph.update_edge(a, b_lama, b_baru)
        ok2 = self.matrix_graph.update_edge(a, b_lama, b_baru)
        print("Jalan berhasil diubah." if ok1 and ok2 else "Gagal: cek kode jalan/gedung.")

    def menu_hapus_gedung(self):
        kode = input("\nKode gedung yang dihapus: ").strip().upper()
        ok1 = self.list_graph.remove_node(kode)
        ok2 = self.matrix_graph.remove_node(kode)
        self.gedung.remove(kode)
        print("Gedung dihapus." if ok1 and ok2 else "Gagal: kode gedung tidak ditemukan.")

    def menu_hapus_jalan(self):
        a = input("\nKode gedung asal: ").strip().upper()
        b = input("Kode gedung tujuan: ").strip().upper()
        ok1 = self.list_graph.remove_edge(a, b)
        ok2 = self.matrix_graph.remove_edge(a, b)
        print("Jalan dihapus." if ok1 and ok2 else "Gagal: jalan tidak ditemukan.")

    # ---------------- Menu 10 & 11: BFS / DFS ----------------
    def _jalankan_pencarian(self, nama_algoritma: str, fungsi):
        awal = input("\nKode gedung asal: ").strip().upper()
        tujuan = input("Kode gedung tujuan: ").strip().upper()

        valid, pesan = validasi_pencarian_rute(self.list_graph, awal, tujuan)
        if not valid:
            print(f"\nInput tidak valid: {pesan}")
            return None

        rep = input("Representasi (list/matrix) [list]: ").strip().lower() or "list"
        graph_obj = self.matrix_graph if rep == "matrix" else self.list_graph

        hasil = fungsi(graph_obj, awal, tujuan)
        print("\n" + tampilkan_hasil_rute(
            nama_algoritma,
            self.gedung.nama_dari_kode(awal),
            self.gedung.nama_dari_kode(tujuan),
            hasil,
            self.gedung.nama_dari_kode,
        ))
        return hasil

    def menu_bfs(self):
        self._jalankan_pencarian("BFS", bfs)

    def menu_dfs(self):
        self._jalankan_pencarian("DFS", dfs)

    # ---------------- Menu 12: Bandingkan BFS vs DFS ----------------
    def menu_bandingkan(self):
        awal = input("\nKode gedung asal: ").strip().upper()
        tujuan = input("Kode gedung tujuan: ").strip().upper()

        valid, pesan = validasi_pencarian_rute(self.list_graph, awal, tujuan)
        if not valid:
            print(f"\nInput tidak valid: {pesan}")
            return

        baris = []
        for nama_algo, fungsi in (("BFS", bfs), ("DFS", dfs)):
            for nama_rep, graph_obj in (("List", self.list_graph), ("Matrix", self.matrix_graph)):
                r = fungsi(graph_obj, awal, tujuan)
                baris.append([
                    nama_algo, nama_rep, r["found"], r["path_length"],
                    r["visited_count"], f"{r['execution_time'] * 1000:.4f} ms",
                    f"{r['memory_bytes']} B",
                ])
        headers = ["Algoritma", "Representasi", "Ditemukan", "Panjang Jalur",
                   "Gedung Dikunjungi", "Waktu", "Memori"]
        print("\n" + print_table(headers, baris))

    # ---------------- Menu 13: Eksperimen performa otomatis ----------------
    def menu_jalankan_eksperimen(self):
        print("\n-- Menjalankan Eksperimen Otomatis (50/100/250/500 gedung, 5x ulangan) --")
        print("Mohon tunggu, proses ini menjalankan banyak pencarian...")
        try:
            tabel, baris, _ = run_full_experiment()
        except FileNotFoundError as e:
            print(f"Dataset eksperimen belum lengkap: {e}")
            print("Jalankan 'python -m data.dataset_generator' terlebih dahulu.")
            return
        print("\n" + tabel)
        simpan_hasil_csv(baris, os.path.join(os.path.dirname(__file__), "hasil_eksperimen.csv"))
        print("\nHasil lengkap disimpan ke hasil_eksperimen.csv")

    def run(self):
        menu_text = """
==================================================
 SISTEM PENCARIAN RUTE ANTAR-GEDUNG KAMPUS
==================================================
 1. Membuat dataset eksperimen baru
 2. Memuat dataset eksperimen
 3. Menampilkan graph aktif
 4. Menambah gedung
 5. Menambah jalan
 6. Mengubah nama gedung
 7. Mengubah jalan
 8. Menghapus gedung
 9. Menghapus jalan
10. Menjalankan BFS
11. Menjalankan DFS
12. Membandingkan hasil BFS vs DFS
13. Menjalankan eksperimen performa otomatis
 0. Keluar
==================================================
"""
        actions = {
            "1": self.menu_buat_dataset,
            "2": self.menu_muat_dataset,
            "3": self.menu_tampilkan_graph,
            "4": self.menu_tambah_gedung,
            "5": self.menu_tambah_jalan,
            "6": self.menu_ubah_nama_gedung,
            "7": self.menu_ubah_jalan,
            "8": self.menu_hapus_gedung,
            "9": self.menu_hapus_jalan,
            "10": self.menu_bfs,
            "11": self.menu_dfs,
            "12": self.menu_bandingkan,
            "13": self.menu_jalankan_eksperimen,
        }
        while True:
            print(menu_text)
            pilihan = input("Pilih menu: ").strip()
            if pilihan == "0":
                print("Terima kasih telah menggunakan program ini.")
                break
            aksi = actions.get(pilihan)
            if aksi:
                try:
                    aksi()
                except Exception as e:
                    # Fail-safe terakhir: program TIDAK BOLEH crash apapun yang terjadi.
                    print(f"Terjadi error tak terduga: {e}")
            else:
                print("Pilihan tidak valid.")


if __name__ == "__main__":
    RuteAntarGedungApp().run()
