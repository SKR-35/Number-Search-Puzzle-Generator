"""Number Search CLI with optional SQLite persistence and PDF export."""

import argparse

from .auto import make_topic
from .database import connect, load_puzzle, save_many
from .generator import generate_quality
from .parser import parse_input
from .pdf_export import export_pdfs


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate number search puzzles")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("input", nargs="?", help="Topic file")
    source.add_argument("--auto", action="store_true", help="Generate target sequences")
    parser.add_argument("--size", type=int, choices=(15, 20), default=20)
    parser.add_argument("--count", type=int, choices=(15, 20), default=15)
    parser.add_argument(
        "--length",
        type=int,
        default=None,
        help="Fixed auto sequence length (6-10; default 8)",
    )
    parser.add_argument(
        "--min-length", type=int, default=None, help="Legacy auto range minimum"
    )
    parser.add_argument(
        "--max-length", type=int, default=None, help="Legacy auto range maximum"
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--min-quality", type=float, default=80)
    parser.add_argument("--candidates", type=int, default=100)
    parser.add_argument("--db", help="SQLite path for saving approved puzzles")
    parser.add_argument("--pdf-dir", help="PDF output directory; requires --db")
    args = parser.parse_args()
    if args.pdf_dir and not args.db:
        parser.error("--pdf-dir requires --db")
    if args.length is not None and (
        args.min_length is not None or args.max_length is not None
    ):
        parser.error("--length cannot be combined with --min-length or --max-length")
    if args.length is not None:
        min_length = max_length = args.length
    elif args.min_length is not None or args.max_length is not None:
        min_length = args.min_length if args.min_length is not None else 6
        max_length = args.max_length if args.max_length is not None else 10
    else:
        min_length = max_length = 8
    if not 6 <= min_length <= max_length <= 10:
        parser.error("Lengths must satisfy 6 <= min-length <= max-length <= 10")
    topics = (
        [
            make_topic(
                count=args.count,
                min_length=min_length,
                max_length=max_length,
                seed=args.seed,
            )
        ]
        if args.auto
        else parse_input(args.input, grid_size=args.size, words_per_topic=args.count)
    )
    success = 0
    generated = []
    for index, topic in enumerate(topics):
        try:
            puzzle, report = generate_quality(
                topic,
                size=args.size,
                seed=args.seed + index * 100000,
                min_quality=args.min_quality,
                candidates=args.candidates,
            )
        except RuntimeError as exc:
            print(f"[SKIPPED] {topic.name}: {exc}")
            continue
        success += 1
        generated.append((topic, puzzle, report))
        print(f"\n{puzzle.topic} ({args.size}x{args.size})")
        print("\n".join(" ".join(row) for row in puzzle.grid))
        print("Targets:", ", ".join(topic.words))
        print(
            f"Quality: {report.score}/100 | Difficulty: {report.difficulty}/100 "
            f"({report.difficulty_category})"
        )
    if args.db and generated:
        with connect(args.db) as conn:
            saved = save_many(conn, generated, min_quality=args.min_quality)
            pdf_items = (
                [
                    (puzzle_id, *load_puzzle(conn, puzzle_id)[:2])
                    for puzzle_id, _ in saved
                ]
                if args.pdf_dir
                else []
            )
        for (topic, _, _), (puzzle_id, inserted) in zip(generated, saved):
            print(
                f"{topic.name}: puzzle #{puzzle_id} "
                f"({'saved' if inserted else 'already exists'})"
            )
        if args.pdf_dir:
            for path in export_pdfs(pdf_items, args.pdf_dir):
                print(f"PDF export: {path}")
    print(f"\nSummary: {success} successful, {len(topics) - success} failed")


if __name__ == "__main__":
    main()
