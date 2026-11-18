from pathlib import Path

import pytest

from number_search_generator.auto import make_topic
from number_search_generator.database import connect, load_puzzle, save_many
from number_search_generator.generator import generate_quality
from number_search_generator.pdf_export import export_pdfs


def sample():
    topic = make_topic(count=15, min_length=6, max_length=10, seed=42)
    puzzle, report = generate_quality(
        topic, size=20, seed=42, candidates=8, min_quality=0
    )
    return topic, puzzle, report


def test_roundtrip_and_deduplication(tmp_path: Path):
    item = sample()
    with connect(tmp_path / "puzzles.db") as conn:
        assert save_many(conn, [item], min_quality=0) == [(1, True)]
        assert save_many(conn, [item], min_quality=0) == [(1, False)]
        assert load_puzzle(conn, 1) == (item[1], item[0], item[2])


def test_rejection_is_atomic(tmp_path: Path):
    item = sample()
    with connect(tmp_path / "puzzles.db") as conn:
        with pytest.raises(ValueError, match="threshold"):
            save_many(conn, [item], min_quality=100)
        assert conn.execute("SELECT COUNT(*) FROM puzzles").fetchone()[0] == 0


def test_pdf_page_counts(tmp_path: Path):
    from pypdf import PdfReader

    topic, puzzle, _ = sample()
    paths = export_pdfs([(1, puzzle, topic)] * 5, tmp_path)
    assert [len(PdfReader(str(p)).pages) for p in paths] == [5, 2]
    assert all(p.read_bytes().startswith(b"%PDF") for p in paths)


def test_empty_pdf_export(tmp_path: Path):
    with pytest.raises(ValueError):
        export_pdfs([], tmp_path)
