![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Database](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![PDF](https://img.shields.io/badge/PDF-ReportLab-CC0000)
[![CI](https://img.shields.io/github/actions/workflow/status/SKR-35/Number-Search-Puzzle-Generator/ci.yml?branch=master&label=CI&logo=githubactions&logoColor=white)](https://github.com/SKR-35/Number-Search-Puzzle-Generator/actions/workflows/ci.yml)

# Number Search Puzzle Generator

**Generate reproducible, quality-scored number search puzzles from digit sequences or fully automatic input.**

A Python command-line tool for generating number search grids, validating target placements, estimating puzzle difficulty, storing approved puzzles in SQLite and exporting printable puzzle and solution PDFs. Build individual puzzles from blank-line-separated number groups or generate random target sequences with a fixed seed.

## Features

- **Eight search directions:** horizontal, vertical and diagonal, forwards and backwards.
- **Two grid sizes:** 15 × 15 and 20 × 20 (default).
- **Two input modes:** UTF-8 text files or automatic target generation (`--auto`).
- **Topic-free batch input:** one puzzle per blank-line-separated group, with 20 sequences by default (15 also supported).
- **Configurable sequence length:** 6–10 digits; automatic generation defaults to **uniform 8-digit** targets. Mixed lengths remain available on request.
- **Leading-zero support:** digit sequences are handled as strings, not integers.
- **Reproducible generation:** a seed controls automatic targets and candidate search.
- **Unique-target validation:** verify that each requested sequence has a unique occurrence in the final grid.
- **Quality-gated selection:** compare candidates and reject puzzles below a configurable score.
- **Placement diagnostics:** spatial entropy, direction diversity, spatial coverage, intersection quality and placement balance.
- **Separate difficulty estimate:** a 0–100 heuristic rating and category, distinct from placement quality.
- **SQLite persistence:** retain puzzle grids, target placements and solution data; avoid duplicate puzzle records.
- **Printable PDF export:** one puzzle per US Letter page and up to four solutions per page.

## Quick start

Requires **Python 3.12+** and [uv](https://docs.astral.sh/uv/getting-started/installation/).

```powershell
uv sync
uv run number-search --auto --size 20 --count 20 --seed 42 --min-quality 80 --candidates 100
```

This prints a puzzle preview in the terminal without saving a database or PDFs.

To persist a puzzle and export PDFs:

```powershell
uv run number-search --auto --size 20 --count 20 --seed 42 --min-quality 80 --candidates 100 --db data/puzzles.db --pdf-dir output
```

To generate puzzles from a file:

```powershell
uv run number-search examples/input.txt --size 20 --count 20 --seed 42 --min-quality 80 --candidates 100 --db data/puzzles.db --pdf-dir output
```

Generated files:

```text
data/puzzles.db
output/number-search-puzzles.pdf
output/number-search-solutions.pdf
```

PDFs are exported from saved puzzle records so the solution paths correspond to the persisted grids. Repeating an identical puzzle does not create a duplicate record. **Note:** PDFs in the same output directory are overwritten by the next export; use separate output directories to retain multiple runs.

## Input format

Create a UTF-8 text file containing **one digit sequence per line**. Separate puzzles with a **blank line**. Each group must contain exactly `--count` distinct sequences (20 by default).

Example with **15 targets per group** (run with `--count 15`):

```text
261811
039316
220512
122502
470815
260626
630513
530531
220324
142406
733934
315542
343548
011727
182704
091914
140415
081404
260254
041226

58392017
72418390
61928473
83510294
10293847
90817263
47628190
23840517
69173028
50192836
38471029
72940518
16028394
84729103
29581740

022768
98834813
535425961
500265
76065242
7732107797
4428714227
2370884095
9826617575
008687
24861175
541398
1902683106
4539147811
0890407
```

```powershell
uv run number-search examples/input.txt --size 20 --count 15 --seed 42
```

Each group becomes a separate puzzle, titled `Number Search 001`, `Number Search 002` and so on. Blank lines delimit groups; `#` comment lines are ignored. Every target must contain **6–10 ASCII digits**; leading zeros are preserved. Duplicate targets or an incorrect number of targets in a group cause validation errors rather than silent splitting.

## Automatic number generation

By default, all automatically generated targets are **8 digits long**:

```powershell
uv run number-search --auto --size 20 --count 20 --seed 42
```

Choose a fixed length from 6 to 10:

```powershell
uv run number-search --auto --size 15 --count 15 --length 7 --seed 123
```

Optionally generate a mixture of lengths:

```powershell
uv run number-search --auto --size 20 --count 20 --min-length 6 --max-length 10 --seed 42
```

`--length` cannot be combined with `--min-length` or `--max-length`.

## Command-line options

| Option | Purpose | Default |
| --- | --- | --- |
| `input` | Path to a blank-line-separated number-list file | Alternative to `--auto` |
| `--auto` | Generate target sequences automatically | Off |
| `--size` | Square grid dimension (`15` or `20`) | `20` |
| `--count` | Targets per puzzle (`15` or `20`) | `20` |
| `--length` | Fixed automatic target length (6–10) | `8` (implicit) |
| `--min-length` | Minimum length for optional automatic range | `6` when range requested |
| `--max-length` | Maximum length for optional automatic range | `10` when range requested |
| `--seed` | Reproducible generation seed | `42` |
| `--min-quality` | Minimum accepted placement quality (0–100) | `80` |
| `--candidates` | Number of candidate boards to evaluate | `100` |
| `--db` | SQLite database path; enables persistence | Disabled |
| `--pdf-dir` | Puzzle/solution PDF output directory; requires `--db` | Disabled |

A puzzle that cannot meet the quality threshold is skipped and reported; generation continues for remaining input groups. Increasing `--candidates`, reducing the target count or using a larger grid may help with difficult inputs.

## How quality evaluation works

Each valid candidate receives a **placement-quality score from 0 to 100** using five weighted components:

| Component | Weight | What it measures |
| --- | ---: | --- |
| Spatial entropy | 35% | Distribution of target cells across grid regions |
| Direction diversity | 25% | Variety of placement directions |
| Spatial coverage | 20% | Coverage of different grid regions |
| Intersection quality | 10% | Shared cells between placed sequences |
| Placement balance | 10% | Avoidance of strong positional clustering |

The generator selects the highest-scoring valid candidate and applies the minimum-quality threshold. A **separate difficulty heuristic** considers reversed and diagonal placements, target length, intersections and similarities between number sequences.

**Important:** Quality and difficulty scores are engineering heuristics, not empirically validated predictions of human solving time or print attractiveness. Review PDF proofs before publication.

## Data and PDF exports

SQLite stores grids, target sequences, placements, directions, quality metrics, difficulty information and the data needed to reconstruct solutions. Duplicate detection avoids inserting the same puzzle twice. For compatibility with the original Word Search implementation, some internal schema names (including `topic`) are retained; **input files do not need topics**.

- **Puzzle PDF:** one grid per US Letter (8.5 × 11 in) page, instructions and the target-number list.
- **Solutions PDF:** up to four highlighted solution grids per page.

The PDFs are designed for printable review. Final book-production margins, trim, legibility and proofing should be checked separately.

## Development and CI

Install dependencies and run all checks locally:

```powershell
uv sync
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
```

GitHub Actions runs pytest, Ruff lint and Ruff format checks on every push and pull request, using Python 3.12 and `uv sync --frozen`.

Core modules live under `src/number_search_generator/`: parsing, automatic target generation, grid generation, quality evaluation, SQLite persistence, PDF export and CLI. Technical decisions are documented in [`DECISIONS.md`](DECISIONS.md).