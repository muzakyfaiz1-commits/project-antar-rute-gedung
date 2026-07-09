# Sistem Pencarian Rute Antar-Gedung Kampus

Program console Python untuk mencari dan membandingkan rute antar gedung
di lingkungan kampus menggunakan BFS dan DFS, pada dua representasi graph
(Adjacency List dan Adjacency Matrix).

Setiap gedung diidentifikasi dengan **kode unik** (mis. `G01`) yang
dipetakan ke **nama gedung** yang mudah dibaca (mis. `Aula`) — ciri khas
project ini yang dipertahankan sejak versi awal.

## Cara menjalankan

```bash
python3 main.py
```

Tidak ada dependency eksternal (hanya Python standard library).

## Struktur folder

```
rute_antar_gedung/
├── main.py                        # Program utama (menu CRUD & pencarian rute)
├── models/
│   ├── gedung.py                  # GedungRegistry: pemetaan kode <-> nama gedung
│   ├── graph_adjacency_list.py    # Representasi Adjacency List
│   └── graph_adjacency_matrix.py  # Representasi Adjacency Matrix
├── algorithms/
│   ├── structures.py              # SimpleQueue & SimpleStack manual
│   └── search.py                  # BFS & DFS + pengukuran performa
├── data/
│   ├── campus_graph.py            # Graph kampus nyata (dataset default)
│   ├── dataset_generator.py       # Generator dataset sintetis (CSV)
│   └── dataset_eksperimen/        # Dataset CSV untuk eksperimen (50/100/250/500)
├── experiments/
│   └── experiment_runner.py       # Eksperimen otomatis & tabel hasil
└── utils/
    ├── validators.py              # Validasi input & konsistensi graph
    ├── metrics.py                 # Rata-rata metrik & pencetak tabel
    └── tampilan.py                # Format tampilan hasil rute di console
```

## Algoritma

- **BFS (Breadth First Search)** — menjelajah graph level demi level
  menggunakan queue (FIFO). Pada graph tak berbobot ini, rute pertama
  yang ditemukan BFS menuju gedung tujuan **selalu** merupakan rute
  dengan jumlah jalan (hop) paling sedikit. Kompleksitas: `O(V + E)`
  pada Adjacency List, `O(V^2)` pada Adjacency Matrix.
- **DFS (Depth First Search)** — menjelajah graph sedalam mungkin dulu
  menggunakan stack (LIFO), diimplementasikan **iteratif** (bukan
  rekursi) agar aman untuk graph besar (500+ gedung). DFS menjamin rute
  ditemukan (jika ada), tapi **tidak** menjamin rute terpendek.

Queue dan Stack dibuat manual (`algorithms/structures.py`) tanpa
`collections.deque`, untuk tujuan pembelajaran struktur data.

> **Catatan tentang "jarak":** dataset yang tersedia (baik graph kampus
> nyata maupun dataset eksperimen sintetis) hanya berisi data
> **keterhubungan** antar gedung, tanpa data jarak riil dalam meter.
> "Total jarak" pada tampilan hasil karena itu dihitung sebagai jumlah
> jalan (edge) yang dilalui. Jika suatu saat tersedia data jarak riil per
> jalan, tinggal tambahkan bobot pada edge dan ganti BFS dengan algoritma
> shortest-path berbobot (mis. Dijkstra) — arsitektur modul `algorithms/`
> sudah dirancang agar perubahan ini tidak memengaruhi `models/` maupun
> `main.py`.

## Validasi

Seluruh input pengguna divalidasi terpusat di `utils/validators.py`
sebelum diproses, mencakup: input kosong, graph kosong, gedung tidak
ditemukan, gedung asal = gedung tujuan, jalan tidak tersedia, dan
konsistensi data graph (node duplikat, edge merujuk gedung tak
terdaftar, self-loop). Program tidak pernah crash karena input tak
terduga — kesalahan selalu ditangkap dan ditampilkan sebagai pesan yang
jelas.

## Contoh penggunaan

```
Pilih menu: 10

Kode gedung asal: G01
Kode gedung tujuan: G07
Representasi (list/matrix) [list]:

============================================
PENCARIAN RUTE ANTAR GEDUNG (BFS)
============================================
Gedung Asal   : Aula
Gedung Tujuan : Gedung UKM

Rute Terbaik

Aula
   ↓
Gedung G2
   ↓
Gedung BEM
   ↓
Gedung UKM

Jumlah Jalan Dilalui   : 3 segmen
Jumlah Gedung Dilalui  : 4
Node Dikunjungi        : 6
Waktu Eksekusi         : 0.0123 ms
Estimasi Memori        : 512 bytes
============================================
```

## Menjalankan eksperimen performa langsung dari terminal

```bash
python3 -m experiments.experiment_runner
```

## Membuat ulang dataset eksperimen CSV

```bash
python3 -m data.dataset_generator
```
