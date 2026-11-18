"""Parse blank-line-separated groups of digit sequences."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Topic:
    name: str
    words: tuple[str, ...]


def normalize(word: str) -> str:
    return word.strip()


def parse_input(
    path: str | Path, *, grid_size: int = 20, words_per_topic: int = 20
) -> list[Topic]:
    if grid_size not in (15, 20) or words_per_topic not in (15, 20):
        raise ValueError("Grid size must be 15 or 20; count must be 15 or 20")
    topics: list[Topic] = []
    numbers: list[str] = []
    pending_title: str | None = None

    def finish() -> None:
        if not numbers:
            return
        number = len(topics) + 1
        if len(numbers) != words_per_topic:
            raise ValueError(
                f"Puzzle {number:03d} requires exactly {words_per_topic} sequences; "
                f"got {len(numbers)}"
            )
        if len(set(numbers)) != len(numbers):
            raise ValueError(f"Duplicate sequences in puzzle {number:03d}")
        topics.append(
            Topic(pending_title or f"Number Search {number:03d}", tuple(numbers))
        )

    for line_no, raw in enumerate(
        Path(path).read_text(encoding="utf-8-sig").splitlines(), 1
    ):
        line = raw.strip()
        if not line:
            if numbers:
                finish()
                numbers = []
                pending_title = None
            continue
        if line.startswith("#"):
            continue
        if line.lower().startswith("topic:"):
            if numbers:
                raise ValueError(
                    f"Topic heading on line {line_no} must precede its number group"
                )
            if pending_title is not None:
                raise ValueError(
                    f"Multiple topic headings before group on line {line_no}"
                )
            pending_title = line.split(":", 1)[1].strip()
            if not pending_title:
                raise ValueError(f"Empty topic heading on line {line_no}")
            continue
        if not line.isascii() or not line.isdecimal() or not 6 <= len(line) <= 10:
            raise ValueError(f"Invalid 6-10 digit sequence on line {line_no}: {line!r}")
        numbers.append(line)
    if pending_title is not None and not numbers:
        raise ValueError("Topic heading has no number group")
    finish()
    if not topics:
        raise ValueError("No number groups found")
    return topics
