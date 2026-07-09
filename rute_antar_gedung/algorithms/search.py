"""
search.py
=========
Implementasi manual Breadth First Search (BFS) dan Depth First Search (DFS)
untuk mencari rute antar gedung kampus.

Kedua algoritma bekerja pada objek graph APAPUN (AdjacencyListGraph maupun
AdjacencyMatrixGraph) selama memiliki method has_node(), get_neighbors(),
dan get_nodes() -> ini adalah contoh Polymorphism: fungsi BFS/DFS tidak
peduli representasi internal graph, ia hanya memakai kontrak (interface)
yang sama.

Kompleksitas waktu:
- BFS pada Adjacency List  : O(V + E)
- DFS pada Adjacency List  : O(V + E)
- BFS/DFS pada Adjacency Matrix: O(V^2) karena get_neighbors() harus
  scan satu baris penuh untuk setiap node.
"""

import sys
import time

from algorithms.structures import SimpleQueue, SimpleStack


def _estimate_memory(*objects) -> int:
    """Estimasi kasar penggunaan memori tambahan (bytes) yang dipakai
    algoritma selama proses pencarian (bukan memori graph itu sendiri)."""
    total = 0
    for obj in objects:
        total += sys.getsizeof(obj)
        if isinstance(obj, dict):
            for k, v in obj.items():
                total += sys.getsizeof(k) + sys.getsizeof(v)
        elif isinstance(obj, (list, set)):
            for v in obj:
                total += sys.getsizeof(v)
    return total


def bfs(graph, awal: str, tujuan: str) -> dict:
    """BFS memakai SimpleQueue (FIFO).

    Karena BFS mengunjungi node level per level, rute pertama yang
    ditemukan menuju `tujuan` PASTI merupakan rute dengan jumlah jalan
    (hop) paling sedikit pada graph tak berbobot ini.

    Tidak pernah melempar exception untuk kasus node tidak ditemukan;
    validasi keberadaan node sudah dilakukan lebih awal (fail-safe).
    """
    t0 = time.perf_counter()

    if not graph.has_node(awal) or not graph.has_node(tujuan):
        return _buat_hasil(False, [], 0, 0.0, 0)

    if awal == tujuan:
        return _buat_hasil(True, [awal], 1, time.perf_counter() - t0, sys.getsizeof(awal))

    dikunjungi = {awal}
    induk = {awal: None}
    antrian = SimpleQueue()
    antrian.enqueue(awal)
    jumlah_dikunjungi = 1
    ditemukan = False

    while not antrian.is_empty():
        sekarang = antrian.dequeue()
        if sekarang == tujuan:
            ditemukan = True
            break
        for tetangga in graph.get_neighbors(sekarang):
            if tetangga not in dikunjungi:
                dikunjungi.add(tetangga)
                induk[tetangga] = sekarang
                antrian.enqueue(tetangga)
                jumlah_dikunjungi += 1

    jalur = _rekonstruksi_jalur(induk, awal, tujuan) if ditemukan else []
    elapsed = time.perf_counter() - t0
    memori = _estimate_memory(dikunjungi, induk, antrian, jalur)
    return _buat_hasil(ditemukan, jalur, jumlah_dikunjungi, elapsed, memori)


def dfs(graph, awal: str, tujuan: str) -> dict:
    """DFS memakai SimpleStack (LIFO), diimplementasikan secara ITERATIF
    (bukan rekursi) agar tidak menabrak batas recursion limit Python pada
    graph besar (500 gedung ke atas). DFS tidak menjamin rute terpendek,
    hanya menjamin rute (jika ada) ditemukan."""
    t0 = time.perf_counter()

    if not graph.has_node(awal) or not graph.has_node(tujuan):
        return _buat_hasil(False, [], 0, 0.0, 0)

    if awal == tujuan:
        return _buat_hasil(True, [awal], 1, time.perf_counter() - t0, sys.getsizeof(awal))

    dikunjungi = set()
    induk = {awal: None}
    tumpukan = SimpleStack()
    tumpukan.push(awal)
    jumlah_dikunjungi = 0
    ditemukan = False

    while not tumpukan.is_empty():
        sekarang = tumpukan.pop()
        if sekarang in dikunjungi:
            continue
        dikunjungi.add(sekarang)
        jumlah_dikunjungi += 1
        if sekarang == tujuan:
            ditemukan = True
            break
        # Tetangga dibalik agar urutan eksplorasi konsisten (kiri ke kanan)
        for tetangga in reversed(graph.get_neighbors(sekarang)):
            if tetangga not in dikunjungi:
                if tetangga not in induk:
                    induk[tetangga] = sekarang
                tumpukan.push(tetangga)

    jalur = _rekonstruksi_jalur(induk, awal, tujuan) if ditemukan else []
    elapsed = time.perf_counter() - t0
    memori = _estimate_memory(dikunjungi, induk, tumpukan, jalur)
    return _buat_hasil(ditemukan, jalur, jumlah_dikunjungi, elapsed, memori)


def _rekonstruksi_jalur(induk: dict, awal: str, tujuan: str) -> list:
    jalur = [tujuan]
    while jalur[-1] != awal:
        jalur.append(induk[jalur[-1]])
    jalur.reverse()
    return jalur


def _buat_hasil(ditemukan: bool, jalur: list, jumlah_dikunjungi: int,
                 elapsed: float, memori_bytes: int) -> dict:
    return {
        "found": ditemukan,
        "path": jalur,
        "path_length": max(len(jalur) - 1, 0),  # jumlah jalan (edge) dilalui
        "visited_count": jumlah_dikunjungi,
        "execution_time": elapsed,
        "memory_bytes": memori_bytes,
    }
