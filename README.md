# Number Search Puzzle Generator

Deterministic digit-sequence puzzle generation, input-file and automatic modes, quality scoring, and difficulty estimates.

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```powershell
uv sync
uv run number-search --auto --size 20 --count 20 --length 8 --seed 42 --min-quality 80 --candidates 100
uv run number-search examples/input.txt --size 15 --count 20 --seed 42 --min-quality 80
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
```

Input files contain groups of **20 digit sequences by default**, separated by blank lines (use `--count 15` for groups of 15). Each group is assigned an internal title such as `Number Search 001`. No `topic:` headers are used. Each sequence contains 6–10 ASCII digits. Leading zeros are retained. Grids are 15×15 or 20×20. Target sequences must occur exactly once across all eight directions.

Quality measures spatial entropy (35%), direction diversity (25%), region coverage (20%), intersection quality (10%), and placement balance (10%). Difficulty is a separate heuristic incorporating reverse/diagonal placement, length, intersections, and shared contiguous digit runs. Scores are not validated measures of solving time.

PDF output requires manual print proofing.

## Phase 2: SQLite and PDF

Install dependencies with `uv sync`. To persist and export a 20×20 automatic puzzle:

```powershell
uv run number-search --auto --size 20 --count 20 --seed 42 --candidates 30 --db data/puzzles.db --pdf-dir output
```

Or use a file of number groups:

```powershell
uv run number-search examples/input.txt --size 15 --count 20 --seed 42 --candidates 30 --db data/puzzles.db --pdf-dir output
```

PDFs are `output/number-search-puzzles.pdf` and `output/number-search-solutions.pdf`. Existing identical puzzles are reused in SQLite. PDF output represents the successful puzzles from the current run, including reused records. Exporting again to the same directory overwrites the two PDFs.

```powershell
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
```

## Automatic target length (Phase 2 follow-up)

Automatic mode now creates **8-digit targets by default**, all of equal length.
Use `--length N` (6 through 10) to choose another fixed length:

```powershell
uv run number-search --auto --size 20 --count 20 --length 7 --seed 42 --db data/puzzles.db --pdf-dir output
```

For backwards compatibility, explicitly passing `--min-length 6 --max-length 10`
still produces mixed-length targets. `--length` cannot be combined with these flags.
File input continues to accept mixed lengths from 6 to 10 digits.

## Phase 2.2 — Topic-free input

Each nonempty group separated by a blank line becomes one puzzle. Comments beginning with `#` are ignored and do not separate groups. The default target count is 20 in both modes; use `--count 15` for smaller sets. Existing SQLite schema retains its internal `topic` field for compatibility, populated with `Number Search 001`, etc. No migration is required.
