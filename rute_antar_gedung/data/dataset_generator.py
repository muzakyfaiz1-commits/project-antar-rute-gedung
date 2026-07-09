"""
dataset_generator.py
=====================
Membuat & memuat dataset graph gedung sintetis (untuk eksperimen performa)
dalam format CSV, diadaptasi dari `dataset.py` versi awal.

Format CSV dipertahankan (bukan diganti ke JSON) karena:
- ini adalah identitas asli project ini (berbeda dari campus_route yang
  memakai JSON),
- CSV lebih mudah dibuka langsung di Excel/Spreadsheet untuk keperluan
  laporan (lihat Hasil_Eksperimen_Rute_Kampus..xlsx pada project awal).

Ukuran yang didukung: 50, 100, 250, 500 gedung.
Tingkat kepadatan: "jarang" (sparse) dan "padat" (dense).
"""

import csv
import os
import random

from utils.validators import validasi_data_graph

DENSITAS_RATA_RATA_KONEKSI = {
    "jarang": 2.5,
    "padat": 6.0,
}


def generate_dataset(jumlah_gedung: int, rata_rata_koneksi: float, seed: int = None):
    """Membuat dataset gedung & jalan fiktif.

    Graph dijamin TERHUBUNG (connected): tahap pertama membangun random
    spanning tree (n-1 jalan), baru menambah jalan ekstra acak sesuai
    target kepadatan.

    Returns:
        (nama_gedung: dict[kode, nama], daftar_jalan: list[tuple[kode, kode]])
    """
    if jumlah_gedung <= 0:
        raise ValueError("Jumlah gedung harus lebih dari 0.")

    rng = random.Random(seed)

    daftar_kode = [f"G{i:04d}" for i in range(1, jumlah_gedung + 1)]
    nama_gedung = {kode: f"Gedung {kode[1:]}" for kode in daftar_kode}

    # 1) Random spanning tree -> menjamin graph terhubung, O(n) jalan
    jalan = set()
    for i in range(1, jumlah_gedung):
        gedung_baru = daftar_kode[i]
        gedung_lama = daftar_kode[rng.randint(0, i - 1)]
        jalan.add(tuple(sorted((gedung_baru, gedung_lama))))

    # 2) Tambah jalan ekstra acak sampai rata-rata koneksi mendekati target
    target_jumlah_jalan = int(jumlah_gedung * rata_rata_koneksi / 2)
    percobaan_maks = target_jumlah_jalan * 20 + 100
    percobaan = 0
    while len(jalan) < target_jumlah_jalan and percobaan < percobaan_maks:
        a, b = rng.sample(daftar_kode, 2)
        jalan.add(tuple(sorted((a, b))))
        percobaan += 1

    daftar_jalan = sorted(jalan)
    valid, pesan = validasi_data_graph(daftar_kode, daftar_jalan)
    if not valid:
        raise ValueError(f"Dataset yang dihasilkan tidak valid: {pesan}")

    return nama_gedung, daftar_jalan


def simpan_ke_csv(nama_gedung: dict, daftar_jalan: list, path_gedung: str, path_jalan: str):
    os.makedirs(os.path.dirname(path_gedung) or ".", exist_ok=True)
    with open(path_gedung, "w", newline="", encoding="utf-8") as f:
        penulis = csv.writer(f)
        penulis.writerow(["kode_gedung", "nama_gedung"])
        for kode, nama in nama_gedung.items():
            penulis.writerow([kode, nama])

    with open(path_jalan, "w", newline="", encoding="utf-8") as f:
        penulis = csv.writer(f)
        penulis.writerow(["gedung_asal", "gedung_tujuan"])
        for asal, tujuan in daftar_jalan:
            penulis.writerow([asal, tujuan])


def muat_gedung_csv(path: str) -> dict:
    """Memuat pemetaan kode_gedung -> nama_gedung dari file CSV."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File dataset gedung tidak ditemukan: {path}")
    with open(path, newline="", encoding="utf-8") as f:
        return {row["kode_gedung"]: row["nama_gedung"] for row in csv.DictReader(f)}


def muat_jalan_csv(path: str) -> list:
    """Memuat daftar jalan (pasangan kode gedung) dari file CSV."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File dataset jalan tidak ditemukan: {path}")
    with open(path, newline="", encoding="utf-8") as f:
        return [(row["gedung_asal"], row["gedung_tujuan"]) for row in csv.DictReader(f)]


def nama_file_gedung(n: int) -> str:
    return f"gedung_{n}.csv"


def nama_file_jalan(n: int, densitas: str) -> str:
    return f"jalan_{n}_{densitas}.csv"


if __name__ == "__main__":
    # Membuat ulang seluruh dataset eksperimen (50/100/250/500, jarang/padat)
    output_dir = os.path.join(os.path.dirname(__file__), "dataset_eksperimen")
    for n in (50, 100, 250, 500):
        for label, rata_rata in DENSITAS_RATA_RATA_KONEKSI.items():
            nama_gedung, daftar_jalan = generate_dataset(n, rata_rata, seed=42)
            simpan_ke_csv(
                nama_gedung, daftar_jalan,
                os.path.join(output_dir, nama_file_gedung(n)),
                os.path.join(output_dir, nama_file_jalan(n, label)),
            )
            print(f"Dataset {n} gedung ({label}) dibuat: {len(daftar_jalan)} jalan.")
