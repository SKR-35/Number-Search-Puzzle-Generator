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
