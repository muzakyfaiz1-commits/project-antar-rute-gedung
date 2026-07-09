"""
gedung.py
=========
Registry pemetaan kode_gedung <-> nama_gedung.

Ini adalah ciri khas "Project Rute Antar Gedung" yang dipertahankan dari
versi awal: setiap gedung punya KODE unik (mis. "G01") sekaligus NAMA
yang bisa dibaca manusia (mis. "Aula"). Node pada graph selalu memakai
kode sebagai identitas, sedangkan nama hanya dipakai untuk ditampilkan.

Pemisahan ini sengaja dijaga (bukan sekadar meniru campus_route yang
memakai nama sebagai node) karena:
- kode singkat & unik -> aman dipakai sebagai key dictionary/matrix index
- nama bisa berubah (renovasi/relokasi) tanpa mengubah struktur graph
"""


class GedungRegistry:
    """Menyimpan dan memvalidasi pasangan kode_gedung -> nama_gedung."""

    def __init__(self):
        self._nama: dict[str, str] = {}

    def add(self, kode: str, nama: str) -> bool:
        kode = kode.strip().upper()
        nama = nama.strip()
        if not kode or not nama:
            raise ValueError("Kode dan nama gedung tidak boleh kosong.")
        if kode in self._nama:
            return False
        self._nama[kode] = nama
        return True

    def remove(self, kode: str) -> bool:
        kode = kode.strip().upper()
        if kode not in self._nama:
            return False
        del self._nama[kode]
        return True

    def rename(self, kode: str, nama_baru: str) -> bool:
        kode = kode.strip().upper()
        if kode not in self._nama:
            return False
        self._nama[kode] = nama_baru.strip()
        return True

    def has(self, kode: str) -> bool:
        return kode.strip().upper() in self._nama

    def nama_dari_kode(self, kode: str) -> str:
        """Mengembalikan nama gedung; jika kode tak dikenal, kembalikan kode itu
        sendiri agar tampilan tidak pernah crash karena KeyError."""
        return self._nama.get(kode.strip().upper(), kode)

    def semua_kode(self) -> list[str]:
        return list(self._nama.keys())

    def semua_item(self):
        return list(self._nama.items())

    def __len__(self) -> int:
        return len(self._nama)

    @classmethod
    def from_dict(cls, mapping: dict) -> "GedungRegistry":
        reg = cls()
        for kode, nama in mapping.items():
            reg.add(kode, nama)
        return reg
