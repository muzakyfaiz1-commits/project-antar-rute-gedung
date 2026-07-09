"""
experiment_runner.py
=====================
Menjalankan eksperimen performa otomatis: untuk setiap kombinasi ukuran
dataset (50/100/250/500 gedung) x kepadatan (jarang/padat), bangun graph
pada Adjacency List & Adjacency Matrix, jalankan BFS dan DFS dengan
pasangan asal-tujuan acak yang SAMA untuk seluruh kombinasi (agar
perbandingan adil / apple-to-apple), ulangi 5 kali, lalu rata-ratakan.

Hasil akhir disimpan ke `hasil_eksperimen.csv` (format dipertahankan agar
kompatibel dengan laporan Excel yang sudah ada) dan juga dikembalikan
sebagai tabel teks untuk ditampilkan di console.
"""

import csv
import os
import random

from algorithms.search import bfs, dfs
from data.dataset_generator import muat_gedung_csv, muat_jalan_csv, nama_file_gedung, nama_file_jalan
from models.graph_adjacency_list import AdjacencyListGraph
from models.graph_adjacency_matrix import AdjacencyMatrixGraph
from utils.metrics import average_runs, print_table

DATASET_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "dataset_eksperimen")
UKURAN = [50, 100, 250, 500]
KEPADATAN = ["jarang", "padat"]
JUMLAH_PENGULANGAN = 5


def run_full_experiment(ukuran=None, kepadatan=None, pengulangan=JUMLAH_PENGULANGAN, seed=42):
    ukuran = ukuran or UKURAN
    kepadatan = kepadatan or KEPADATAN
    rng = random.Random(seed)
    semua_baris = []
    detail_mentah = {}

    for n in ukuran:
        path_gedung = os.path.join(DATASET_DIR, nama_file_gedung(n))
        nama_gedung = muat_gedung_csv(path_gedung)
        daftar_kode = list(nama_gedung.keys())

        for densitas in kepadatan:
            path_jalan = os.path.join(DATASET_DIR, nama_file_jalan(n, densitas))
            daftar_jalan = muat_jalan_csv(path_jalan)

            list_graph = AdjacencyListGraph.from_edges(daftar_kode, daftar_jalan)
            matrix_graph = AdjacencyMatrixGraph.from_edges(daftar_kode, daftar_jalan)

            # Pasangan asal-tujuan yang sama dipakai untuk semua kombinasi
            pasangan = [tuple(rng.sample(daftar_kode, 2)) for _ in range(pengulangan)]

            kombinasi = {
                ("BFS", "Adjacency List"): (bfs, list_graph),
                ("DFS", "Adjacency List"): (dfs, list_graph),
                ("BFS", "Adjacency Matrix"): (bfs, matrix_graph),
                ("DFS", "Adjacency Matrix"): (dfs, matrix_graph),
            }

            for (nama_algo, nama_rep), (fungsi, graph_obj) in kombinasi.items():
                hasil = [fungsi(graph_obj, a, b) for a, b in pasangan]
                rata_rata = average_runs(hasil)
                detail_mentah[(n, densitas, nama_algo, nama_rep)] = (hasil, rata_rata)
                semua_baris.append([
                    n, densitas, nama_algo, nama_rep,
                    f"{rata_rata['avg_execution_time'] * 1000:.4f}",
                    f"{rata_rata['avg_visited_count']:.1f}",
                    f"{rata_rata['avg_path_length']:.1f}",
                    f"{rata_rata['avg_memory_bytes']:.0f}",
                    f"{rata_rata['found_rate'] * 100:.0f}%",
                ])

    headers = [
        "N (gedung)", "Kepadatan", "Algoritma", "Representasi",
        "Waktu (ms, avg)", "Node Dikunjungi (avg)", "Panjang Jalur (avg)",
        "Memori (bytes, avg)", "Tingkat Ditemukan",
    ]
    tabel = print_table(headers, semua_baris)
    return tabel, semua_baris, detail_mentah


def simpan_hasil_csv(baris_hasil: list, path_output: str):
    with open(path_output, "w", newline="", encoding="utf-8") as f:
        penulis = csv.writer(f)
        penulis.writerow([
            "jumlah_gedung", "kepadatan", "algoritma", "representasi",
            "rata_rata_waktu_ms", "rata_rata_node_dikunjungi",
            "rata_rata_panjang_jalur", "rata_rata_memori_bytes",
            "tingkat_ditemukan",
        ])
        penulis.writerows(baris_hasil)


if __name__ == "__main__":
    tabel, baris, detail = run_full_experiment()
    print(tabel)
    output_path = os.path.join(os.path.dirname(__file__), "..", "hasil_eksperimen.csv")
    simpan_hasil_csv(baris, output_path)
    print(f"\nHasil lengkap disimpan ke {output_path}")
