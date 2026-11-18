import pytest

from number_search_generator.auto import make_topic
from number_search_generator.generator import generate, generate_quality, occurrences
from number_search_generator.parser import parse_input
from number_search_generator.quality import WEIGHTS, evaluate


@pytest.mark.parametrize("size,count", [(15, 15), (20, 15), (20, 20)])
def test_generation(size, count):
    topic = make_topic(count=count, min_length=7, max_length=7, seed=123)
    puzzle = generate(topic, size=size, seed=456)
    assert len(puzzle.grid) == size
    assert all(len(row) == size and row.isdecimal() for row in puzzle.grid)
    assert all(len(occurrences(puzzle.grid, p.word)) == 1 for p in puzzle.placements)
    assert puzzle == generate(topic, size=size, seed=456)


def test_file_and_leading_zero(tmp_path):
    topic = make_topic(seed=7)
    numbers = ("01234567", *topic.words[1:])
    file = tmp_path / "numbers.txt"
    file.write_text("topic: Zero\n" + "\n".join(numbers))
    parsed = parse_input(file)[0]
    assert parsed.words[0] == "01234567"


def test_auto_and_quality():
    topic = make_topic(seed=42)
    assert topic == make_topic(seed=42)
    puzzle, report = generate_quality(topic, candidates=3, min_quality=0)
    assert report == evaluate(puzzle)
    assert sum(WEIGHTS.values()) == pytest.approx(1)
    assert 0 <= report.score <= 100
    assert 0 <= report.difficulty <= 100


def test_reject_invalid(tmp_path):
    file = tmp_path / "invalid.txt"
    file.write_text("topic: Invalid\n12345\n")
    with pytest.raises(ValueError, match="6-10"):
        parse_input(file)
    with pytest.raises(ValueError):
        make_topic(min_length=11)


def test_default_auto_length_is_eight():
    topic = make_topic(seed=42)
    assert len(topic.words) == 15
    assert all(len(number) == 8 for number in topic.words)
    assert len(set(topic.words)) == 15


@pytest.mark.parametrize("length", range(6, 11))
def test_fixed_auto_length(length):
    topic = make_topic(min_length=length, max_length=length, seed=42)
    assert all(len(number) == length for number in topic.words)
