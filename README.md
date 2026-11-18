# Number Search Puzzle Generator

Phase 1: deterministic digit-sequence puzzle generation, input-file and automatic modes, quality scoring, and difficulty estimates.

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```powershell
uv sync
uv run number-search --auto --size 20 --count 15 --min-length 6 --max-length 10 --seed 42 --min-quality 80 --candidates 100
uv run number-search examples/input.txt --size 15 --count 15 --seed 42 --min-quality 80
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
```

Inputs use `topic:` blocks followed by exactly 15 or 20 distinct ASCII digit sequences of length 6–10. Leading zeros are retained. Grids are 15×15 or 20×20. Target sequences must occur exactly once across all eight directions.

Quality measures spatial entropy (35%), direction diversity (25%), region coverage (20%), intersection quality (10%), and placement balance (10%). Difficulty is a separate heuristic incorporating reverse/diagonal placement, length, intersections, and shared contiguous digit runs. Scores are not validated measures of solving time.

**Phase 1 limitations:** terminal preview only; SQLite and PDF export are planned for Phase 2. No claim of print readiness.

## Phase 2: SQLite and PDF

Install dependencies with `uv sync`. To persist and export a 20×20 automatic puzzle:

```powershell
uv run number-search --auto --size 20 --count 15 --seed 42 --candidates 30 --db data/puzzles.db --pdf-dir output
```

Or use input topics:

```powershell
uv run number-search examples/input.txt --size 15 --count 15 --seed 42 --candidates 30 --db data/puzzles.db --pdf-dir output
```

PDFs are `output/number-search-puzzles.pdf` and `output/number-search-solutions.pdf`. Existing identical puzzles are reused in SQLite. PDF output represents the successful puzzles from the current run, including reused records. Exporting again to the same directory overwrites the two PDFs.

```powershell
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
```
