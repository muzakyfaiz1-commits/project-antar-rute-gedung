"""
tampilan.py
===========
Fungsi bantu untuk merapikan tampilan hasil pencarian rute di console,
sesuai format yang diminta:

======================================
PENCARIAN RUTE ANTAR GEDUNG
======================================
...

Catatan penting soal "Total Jarak" & "Estimasi Waktu":
Dataset gedung yang ada (baik graph kampus nyata maupun dataset eksperimen
sintetis) HANYA berisi data KETERHUBUNGAN antar gedung, tidak ada data
jarak (meter) atau kecepatan berjalan. Karena itu:
- "Total Jarak" dihitung sebagai JUMLAH JALAN (edge) yang dilalui, satuan
  "segmen jalan" -- bukan mengarang angka meter yang tidak berdasar data.
- Jika di masa depan tersedia data jarak riil per jalan, tinggal isi bobot
  edge (lihat models/graph_adjacency_list.py) dan ganti BFS dengan
  algoritma shortest-path berbobot (mis. Dijkstra) tanpa mengubah format
  tampilan ini.
"""

LEBAR = 44


def _garis():
    return "=" * LEBAR


def tampilkan_hasil_rute(nama_algoritma: str, gedung_asal_nama: str,
                          gedung_tujuan_nama: str, hasil: dict,
                          nama_dari_kode) -> str:
    """Menyusun blok teks hasil pencarian rute yang rapi dan mudah dibaca.

    nama_dari_kode: callable(kode) -> nama gedung (biasanya
    GedungRegistry.nama_dari_kode) sehingga jalur yang tadinya berupa kode
    ("G01", "G02", ...) ditampilkan sebagai nama asli gedung.
    """
    baris = [_garis(), f"PENCARIAN RUTE ANTAR GEDUNG ({nama_algoritma})", _garis()]
    baris.append(f"Gedung Asal   : {gedung_asal_nama}")
    baris.append(f"Gedung Tujuan : {gedung_tujuan_nama}")
    baris.append("")

    if not hasil["found"]:
        baris.append("Rute TIDAK ditemukan antara kedua gedung tersebut.")
        baris.append(_garis())
        return "\n".join(baris)

    baris.append("Rute Terbaik")
    baris.append("")
    nama_jalur = [nama_dari_kode(kode) for kode in hasil["path"]]
    baris.append(("\n" + " " * 3 + "\u2193\n").join(nama_jalur))
    baris.append("")
    baris.append(f"Jumlah Jalan Dilalui   : {hasil['path_length']} segmen")
    baris.append(f"Jumlah Gedung Dilalui  : {len(hasil['path'])}")
    baris.append(f"Node Dikunjungi        : {hasil['visited_count']}")
    baris.append(f"Waktu Eksekusi         : {hasil['execution_time'] * 1000:.4f} ms")
    baris.append(f"Estimasi Memori        : {hasil['memory_bytes']} bytes")
    baris.append(_garis())
    return "\n".join(baris)
