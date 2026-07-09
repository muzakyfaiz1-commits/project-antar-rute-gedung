"""
metrics.py
==========
Fungsi bantu untuk merata-ratakan hasil pengujian berulang dan menampilkan
hasil dalam bentuk tabel teks rapi (tanpa library eksternal).
"""


def average_runs(results: list) -> dict:
    """Merata-ratakan beberapa hasil BFS/DFS (list of dict dari algorithms/search.py)."""
    n = len(results)
    if n == 0:
        raise ValueError("Tidak ada hasil untuk dirata-ratakan.")

    ditemukan = sum(1 for r in results if r["found"])
    return {
        "runs": n,
        "found_rate": ditemukan / n,
        "avg_execution_time": sum(r["execution_time"] for r in results) / n,
        "avg_visited_count": sum(r["visited_count"] for r in results) / n,
        "avg_path_length": sum(r["path_length"] for r in results) / n,
        "avg_memory_bytes": sum(r["memory_bytes"] for r in results) / n,
    }


def print_table(headers: list, rows: list) -> str:
    """Mencetak tabel teks rapi rata kolom, tanpa dependency eksternal."""
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    def fmt_row(row):
        return " | ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row))

    sep = "-+-".join("-" * w for w in widths)
    lines = [fmt_row(headers), sep]
    for row in rows:
        lines.append(fmt_row(row))
    return "\n".join(lines)
