"""Number Search Phase 1 preview CLI."""

import argparse

from .auto import make_topic
from .generator import generate_quality
from .parser import parse_input


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate number search puzzles")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("input", nargs="?", help="Topic file")
    source.add_argument("--auto", action="store_true", help="Generate target sequences")
    parser.add_argument("--size", type=int, choices=(15, 20), default=20)
    parser.add_argument("--count", type=int, choices=(15, 20), default=15)
    parser.add_argument("--min-length", type=int, default=6)
    parser.add_argument("--max-length", type=int, default=10)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--min-quality", type=float, default=80)
    parser.add_argument("--candidates", type=int, default=100)
    args = parser.parse_args()
    if not 6 <= args.min_length <= args.max_length <= 10:
        parser.error("Lengths must satisfy 6 <= min-length <= max-length <= 10")
    topics = (
        [
            make_topic(
                count=args.count,
                min_length=args.min_length,
                max_length=args.max_length,
                seed=args.seed,
            )
        ]
        if args.auto
        else parse_input(args.input, grid_size=args.size, words_per_topic=args.count)
    )
    success = 0
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
        print(f"\n{puzzle.topic} ({args.size}x{args.size})")
        print("\n".join(" ".join(row) for row in puzzle.grid))
        print("Targets:", ", ".join(topic.words))
        print(
            f"Quality: {report.score}/100 | Difficulty: {report.difficulty}/100 "
            f"({report.difficulty_category})"
        )
    print(f"\nSummary: {success} successful, {len(topics) - success} failed")


if __name__ == "__main__":
    main()
