"""
validators.py
=============
Lapisan validasi terpusat. Semua pengecekan input pengguna & konsistensi
graph dikumpulkan di sini agar:
- pesan error konsisten di seluruh aplikasi,
- main.py tetap ramping (tidak dipenuhi if/else validasi),
- program TIDAK PERNAH crash karena input tak terduga.

Setiap fungsi mengembalikan tuple (valid: bool, pesan_error: str).
Jika valid=True, pesan_error selalu string kosong.
"""


def validasi_input_tidak_kosong(nilai: str, label: str) -> tuple[bool, str]:
    if nilai is None or not nilai.strip():
        return False, f"{label} tidak boleh kosong."
    return True, ""


def validasi_graph_tidak_kosong(graph) -> tuple[bool, str]:
    if graph is None or graph.num_nodes() == 0:
        return False, "Belum ada graph aktif. Buat atau muat dataset terlebih dahulu."
    return True, ""


def validasi_node_ada(graph, kode: str, label: str) -> tuple[bool, str]:
    if not graph.has_node(kode):
        return False, f"{label} '{kode}' tidak ditemukan pada graph aktif."
    return True, ""


def validasi_asal_tujuan_berbeda(awal: str, tujuan: str) -> tuple[bool, str]:
    if awal == tujuan:
        return False, "Gedung asal dan gedung tujuan tidak boleh sama."
    return True, ""


def validasi_edge_tersedia(graph, a: str, b: str) -> tuple[bool, str]:
    if not graph.has_edge(a, b):
        return False, f"Jalan langsung antara '{a}' dan '{b}' tidak ditemukan."
    return True, ""


def validasi_data_graph(nodes: list, edges: list) -> tuple[bool, str]:
    """Memvalidasi konsistensi data mentah SEBELUM dibangun jadi objek graph:
    - tidak boleh ada node kosong / duplikat
    - setiap edge harus merujuk ke node yang benar-benar ada
    - tidak boleh ada self-loop (gedung terhubung ke dirinya sendiri)
    """
    if not nodes:
        return False, "Data gedung kosong."

    if len(set(nodes)) != len(nodes):
        return False, "Terdapat kode gedung duplikat pada data."

    node_set = set(nodes)
    for a, b in edges:
        if a not in node_set or b not in node_set:
            return False, f"Jalan ({a}, {b}) merujuk ke gedung yang tidak terdaftar."
        if a == b:
            return False, f"Gedung '{a}' tidak boleh memiliki jalan menuju dirinya sendiri."

    return True, ""


def validasi_pencarian_rute(graph, awal: str, tujuan: str) -> tuple[bool, str]:
    """Gabungan seluruh validasi yang dibutuhkan sebelum menjalankan BFS/DFS.
    Mengembalikan pesan error pertama yang gagal, atau (True, "") jika semua lolos."""
    for cek in (
        lambda: validasi_graph_tidak_kosong(graph),
        lambda: validasi_input_tidak_kosong(awal, "Gedung asal"),
        lambda: validasi_input_tidak_kosong(tujuan, "Gedung tujuan"),
    ):
        ok, pesan = cek()
        if not ok:
            return ok, pesan

    ok, pesan = validasi_node_ada(graph, awal, "Gedung asal")
    if not ok:
        return ok, pesan

    ok, pesan = validasi_node_ada(graph, tujuan, "Gedung tujuan")
    if not ok:
        return ok, pesan

    return validasi_asal_tujuan_berbeda(awal, tujuan)
