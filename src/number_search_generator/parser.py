"""Parse number-search topic blocks and validate digit sequences."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Topic:
    name: str
    words: tuple[str, ...]


def normalize(word: str) -> str:
    return word.strip()


def parse_input(
    path: str | Path, *, grid_size: int = 20, words_per_topic: int = 15
) -> list[Topic]:
    if grid_size not in (15, 20) or words_per_topic not in (15, 20):
        raise ValueError("Grid size must be 15 or 20; count must be 15 or 20")
    topics: list[Topic] = []
    name: str | None = None
    numbers: list[str] = []

    def finish() -> None:
        if name is None:
            return
        if len(numbers) != words_per_topic:
            raise ValueError(
                f"Topic {name!r} requires exactly {words_per_topic} sequences"
            )
        if len(set(numbers)) != len(numbers):
            raise ValueError(f"Duplicate sequences in topic {name!r}")
        topics.append(Topic(name, tuple(numbers)))

    for line_no, raw in enumerate(
        Path(path).read_text(encoding="utf-8-sig").splitlines(), 1
    ):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.lower().startswith("topic:"):
            finish()
            name = line.partition(":")[2].strip()
            if not name:
                raise ValueError(f"Empty topic on line {line_no}")
            numbers = []
        else:
            if name is None:
                raise ValueError(f"Number before topic on line {line_no}")
            if not line.isascii() or not line.isdecimal() or not 6 <= len(line) <= 10:
                raise ValueError(
                    f"Invalid 6-10 digit sequence on line {line_no}: {line!r}"
                )
            numbers.append(line)
    finish()
    if not topics:
        raise ValueError("No topics found")
    return topics
