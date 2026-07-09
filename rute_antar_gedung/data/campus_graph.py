"""
campus_graph.py
================
Data gedung & jalan KAMPUS NYATA (bukan sintetis), diadaptasi dari versi
awal project (`skeletonrutegedung.py`). Ini dijadikan dataset default yang
langsung bisa dipakai saat program pertama kali dijalankan, tanpa harus
generate/muat dataset eksperimen terlebih dahulu.

Sumber data: diagram tata letak kampus yang telah dikonfirmasi tim
(lihat komentar asli pada skeletonrutegedung.py).
"""

NAMA_GEDUNG: dict[str, str] = {
    "G01": "Aula",
    "G02": "Lobi",
    "G03": "Gedung G2",
    "G04": "Gedung G3",
    "G05": "Mushola",
    "G06": "Gedung BEM",
    "G07": "Gedung UKM",
    "G08": "Kantin",
}

# Setiap pasangan berarti ada jalan dua arah yang menghubungkan
# langsung dua gedung tersebut.
DAFTAR_JALAN: list[tuple[str, str]] = [
    ("G04", "G02"),  # Gedung G3 - Lobi
    ("G04", "G05"),  # Gedung G3 - Mushola
    ("G05", "G03"),  # Mushola - Gedung G2
    ("G05", "G06"),  # Mushola - Gedung BEM
    ("G06", "G03"),  # Gedung BEM - Gedung G2
    ("G03", "G01"),  # Gedung G2 - Aula
    ("G01", "G02"),  # Aula - Lobi
    ("G06", "G07"),  # Gedung BEM - Gedung UKM
    ("G03", "G08"),  # Gedung G2 - Kantin
    ("G01", "G08"),  # Aula - Kantin
    ("G07", "G08"),  # Gedung UKM - Kantin
]


def muat_graph_kampus():
    """Mengembalikan (daftar_kode_gedung, daftar_jalan, nama_gedung) untuk
    graph kampus nyata di atas."""
    return list(NAMA_GEDUNG.keys()), list(DAFTAR_JALAN), dict(NAMA_GEDUNG)
