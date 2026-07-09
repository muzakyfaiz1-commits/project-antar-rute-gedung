"""
graph_adjacency_matrix.py
==========================
Representasi graph rute antar-gedung menggunakan Adjacency Matrix.

Cocok untuk graph padat (dense) dan ketika pengecekan "apakah jalan (a,b)
ada?" harus sangat cepat, O(1). Namun butuh ruang O(V^2) tanpa peduli
jumlah jalan sebenarnya, dan get_neighbors() harus scan satu baris penuh
(O(V)) -> inilah trade-off dibanding Adjacency List.

Kompleksitas ruang : O(V^2)
"""

import sys


class AdjacencyMatrixGraph:
    """Graph tak berarah (undirected) berbasis adjacency matrix."""

    def __init__(self):
        self._nodes: list[str] = []      # kode_gedung, urutan = index matrix
        self._index: dict[str, int] = {}  # kode_gedung -> index baris/kolom
        self._matrix: list[list[int]] = []  # matrix[i][j] = 1 jika terhubung

    # ---------- CRUD Node ----------
    def add_node(self, kode: str) -> bool:
        if kode in self._index:
            return False
        self._index[kode] = len(self._nodes)
        self._nodes.append(kode)
        for row in self._matrix:
            row.append(0)
        self._matrix.append([0] * len(self._nodes))
        return True

    def remove_node(self, kode: str) -> bool:
        if kode not in self._index:
            return False
        idx = self._index[kode]
        del self._nodes[idx]
        del self._matrix[idx]
        for row in self._matrix:
            del row[idx]
        self._index = {n: i for i, n in enumerate(self._nodes)}
        return True

    def rename_node(self, kode_lama: str, kode_baru: str) -> bool:
        if kode_lama not in self._index or kode_baru in self._index:
            return False
        idx = self._index.pop(kode_lama)
        self._nodes[idx] = kode_baru
        self._index[kode_baru] = idx
        return True

    def has_node(self, kode: str) -> bool:
        return kode in self._index

    # ---------- CRUD Edge ----------
    def add_edge(self, a: str, b: str) -> bool:
        if a not in self._index or b not in self._index:
            return False
        i, j = self._index[a], self._index[b]
        self._matrix[i][j] = 1
        self._matrix[j][i] = 1
        return True

    def remove_edge(self, a: str, b: str) -> bool:
        if a not in self._index or b not in self._index:
            return False
        i, j = self._index[a], self._index[b]
        changed = self._matrix[i][j] == 1
        self._matrix[i][j] = 0
        self._matrix[j][i] = 0
        return changed

    def update_edge(self, a: str, b: str, tujuan_baru: str) -> bool:
        if not self.has_edge(a, b) or tujuan_baru not in self._index:
            return False
        self.remove_edge(a, b)
        self.add_edge(a, tujuan_baru)
        return True

    def has_edge(self, a: str, b: str) -> bool:
        if a not in self._index or b not in self._index:
            return False
        i, j = self._index[a], self._index[b]
        return self._matrix[i][j] == 1

    # ---------- Query ----------
    def get_neighbors(self, kode: str) -> list[str]:
        if kode not in self._index:
            return []
        i = self._index[kode]
        return [self._nodes[j] for j in range(len(self._nodes)) if self._matrix[i][j] == 1]

    def get_nodes(self) -> list[str]:
        return list(self._nodes)

    def num_nodes(self) -> int:
        return len(self._nodes)

    def num_edges(self) -> int:
        return sum(sum(row) for row in self._matrix) // 2

    def is_connected(self) -> bool:
        if not self._nodes:
            return True
        visited = {self._nodes[0]}
        queue = [self._nodes[0]]
        while queue:
            current = queue.pop(0)
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return len(visited) == len(self._nodes)

    def memory_estimate(self) -> int:
        """Estimasi penggunaan memori (bytes) struktur adjacency matrix."""
        total = sys.getsizeof(self._nodes) + sys.getsizeof(self._index) + sys.getsizeof(self._matrix)
        total += sum(sys.getsizeof(n) for n in self._nodes)
        for row in self._matrix:
            total += sys.getsizeof(row)
            total += sum(sys.getsizeof(v) for v in row)
        return total

    def display(self) -> str:
        header = "      " + " ".join(f"{n[:6]:>6}" for n in self._nodes)
        lines = [header]
        for i, n in enumerate(self._nodes):
            row_str = " ".join(f"{v:>6}" for v in self._matrix[i])
            lines.append(f"{n[:6]:>6} {row_str}")
        return "\n".join(lines)

    @classmethod
    def from_edges(cls, nodes, edges):
        g = cls()
        for n in nodes:
            g.add_node(n)
        for a, b in edges:
            g.add_edge(a, b)
        return g
