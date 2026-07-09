"""
graph_adjacency_list.py
========================
Representasi graph rute antar-gedung menggunakan Adjacency List.

Setiap node diidentifikasi dengan `kode_gedung` (mis. "G01"), BUKAN nama
gedung, karena kode bersifat unik sedangkan nama bisa saja mirip/berubah.
Pemetaan kode -> nama gedung ditangani terpisah oleh `models.gedung.GedungRegistry`.

Cocok untuk graph sparse (jarang) karena hanya menyimpan koneksi yang
benar-benar ada.

Kompleksitas ruang : O(V + E)
Kompleksitas waktu  : add_edge O(1), get_neighbors O(1) (mengembalikan referensi list)
"""

import sys


class AdjacencyListGraph:
    """Graph tak berarah (undirected) berbasis adjacency list."""

    def __init__(self):
        # dict: kode_gedung -> list kode_gedung tetangga
        self._adj: dict[str, list[str]] = {}

    # ---------- CRUD Node (Gedung) ----------
    def add_node(self, kode: str) -> bool:
        """Menambahkan gedung baru. Return False jika kode sudah dipakai."""
        if kode in self._adj:
            return False
        self._adj[kode] = []
        return True

    def remove_node(self, kode: str) -> bool:
        """Menghapus gedung beserta seluruh jalan yang terhubung dengannya."""
        if kode not in self._adj:
            return False
        del self._adj[kode]
        for node in self._adj:
            if kode in self._adj[node]:
                self._adj[node].remove(kode)
        return True

    def rename_node(self, kode_lama: str, kode_baru: str) -> bool:
        """Mengubah kode gedung, mempertahankan seluruh koneksi jalan yang ada."""
        if kode_lama not in self._adj or kode_baru in self._adj:
            return False
        self._adj[kode_baru] = self._adj.pop(kode_lama)
        for node in self._adj:
            self._adj[node] = [kode_baru if n == kode_lama else n for n in self._adj[node]]
        return True

    def has_node(self, kode: str) -> bool:
        return kode in self._adj

    # ---------- CRUD Edge (Jalan) ----------
    def add_edge(self, a: str, b: str) -> bool:
        """Menambahkan jalan dua arah a<->b. Kedua gedung harus sudah ada."""
        if a not in self._adj or b not in self._adj:
            return False
        if b not in self._adj[a]:
            self._adj[a].append(b)
        if a not in self._adj[b]:
            self._adj[b].append(a)
        return True

    def remove_edge(self, a: str, b: str) -> bool:
        if a not in self._adj or b not in self._adj:
            return False
        changed = False
        if b in self._adj[a]:
            self._adj[a].remove(b)
            changed = True
        if a in self._adj[b]:
            self._adj[b].remove(a)
            changed = True
        return changed

    def update_edge(self, a: str, b: str, tujuan_baru: str) -> bool:
        """Mengubah jalan a-b menjadi a-tujuan_baru."""
        if not self.has_edge(a, b) or tujuan_baru not in self._adj:
            return False
        self.remove_edge(a, b)
        self.add_edge(a, tujuan_baru)
        return True

    def has_edge(self, a: str, b: str) -> bool:
        return a in self._adj and b in self._adj.get(a, [])

    # ---------- Query ----------
    def get_neighbors(self, kode: str) -> list[str]:
        return list(self._adj.get(kode, []))

    def get_nodes(self) -> list[str]:
        return list(self._adj.keys())

    def num_nodes(self) -> int:
        return len(self._adj)

    def num_edges(self) -> int:
        return sum(len(v) for v in self._adj.values()) // 2

    def to_edge_list(self) -> list[tuple[str, str]]:
        edges = set()
        for a in self._adj:
            for b in self._adj[a]:
                edges.add(tuple(sorted((a, b))))
        return list(edges)

    def is_connected(self) -> bool:
        """Mengecek apakah seluruh gedung saling terhubung (tidak ada node mati)."""
        if not self._adj:
            return True
        start = next(iter(self._adj))
        visited = {start}
        queue = [start]
        while queue:
            current = queue.pop(0)
            for neighbor in self._adj[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return len(visited) == len(self._adj)

    def memory_estimate(self) -> int:
        """Estimasi penggunaan memori (bytes) struktur adjacency list."""
        total = sys.getsizeof(self._adj)
        for key, value in self._adj.items():
            total += sys.getsizeof(key) + sys.getsizeof(value)
            total += sum(sys.getsizeof(v) for v in value)
        return total

    def display(self) -> str:
        lines = []
        for node in self._adj:
            tetangga = ", ".join(self._adj[node]) if self._adj[node] else "(tidak ada jalan)"
            lines.append(f"  {node} -> {tetangga}")
        return "\n".join(lines)

    @classmethod
    def from_edges(cls, nodes, edges):
        g = cls()
        for n in nodes:
            g.add_node(n)
        for a, b in edges:
            g.add_edge(a, b)
        return g
