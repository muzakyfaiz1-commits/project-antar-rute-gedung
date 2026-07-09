"""
structures.py
=============
Implementasi manual struktur data Queue (FIFO) dan Stack (LIFO) tanpa
menggunakan collections.deque atau queue.Queue bawaan Python.

Dipakai oleh algoritma BFS (Queue) dan DFS iteratif (Stack) pada
algorithms/search.py.
"""


class SimpleQueue:
    """Antrian FIFO sederhana berbasis list Python.

    enqueue() -> O(1) amortized
    dequeue() -> O(n) karena pop(0) menggeser seluruh elemen.
                 (Dibuat manual demi tujuan pembelajaran struktur data;
                 untuk data sangat besar sebaiknya pakai collections.deque.)
    """

    def __init__(self):
        self._items = []

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue kosong, tidak bisa dequeue")
        return self._items.pop(0)

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)


class SimpleStack:
    """Tumpukan LIFO sederhana berbasis list Python.

    push() -> O(1) amortized
    pop()  -> O(1)
    """

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack kosong, tidak bisa pop")
        return self._items.pop()

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)
