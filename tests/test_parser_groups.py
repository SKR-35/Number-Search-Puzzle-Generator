import pytest

from number_search_generator.parser import parse_input


def test_two_groups_and_leading_zeros(tmp_path):
    a = [f"{i:08d}" for i in range(20)]
    b = [f"{i + 100:08d}" for i in range(20)]
    file = tmp_path / "numbers.txt"
    file.write_text("\n".join(a) + "\n\n# another puzzle\n" + "\n".join(b) + "\n")
    topics = parse_input(file)
    assert [t.name for t in topics] == ["Number Search 001", "Number Search 002"]
    assert topics[0].words[0] == "00000000"
    assert topics[1].words == tuple(b)


@pytest.mark.parametrize("count", [19, 21])
def test_reject_incomplete_groups(tmp_path, count):
    file = tmp_path / "numbers.txt"
    file.write_text("\n".join(f"{i:08d}" for i in range(count)))
    with pytest.raises(ValueError, match="requires exactly 20"):
        parse_input(file)


def test_reject_duplicate_group(tmp_path):
    file = tmp_path / "numbers.txt"
    file.write_text("\n".join(["12345678"] * 20))
    with pytest.raises(ValueError, match="Duplicate"):
        parse_input(file)


def test_optional_topic_and_untitled_groups(tmp_path):
    a = [f"{i:06d}" for i in range(20)]
    b = [f"{i + 100:08d}" for i in range(20)]
    c = [f"{i + 200:08d}" for i in range(20)]
    file = tmp_path / "numbers.txt"
    file.write_text(
        "topic: History of Philosophy\n\n"
        + "\n".join(a)
        + "\n\n"
        + "\n".join(b)
        + "\n\nTOPIC: Historical Dates\n"
        + "\n".join(c),
        encoding="utf-8",
    )
    topics = parse_input(file)
    assert [t.name for t in topics] == [
        "History of Philosophy",
        "Number Search 002",
        "Historical Dates",
    ]
    assert topics[0].words == tuple(a)


def test_reject_empty_or_orphan_topic(tmp_path):
    file = tmp_path / "numbers.txt"
    file.write_text("topic:  \n")
    with pytest.raises(ValueError, match="Empty topic"):
        parse_input(file)
    file.write_text("topic: Orphan\n")
    with pytest.raises(ValueError, match="no number group"):
        parse_input(file)


def test_reject_topic_in_middle_of_group(tmp_path):
    file = tmp_path / "numbers.txt"
    file.write_text("12345678\ntopic: Wrong place\n")
    with pytest.raises(ValueError, match="must precede"):
        parse_input(file)


def test_fifteen_targets_option(tmp_path):
    file = tmp_path / "numbers.txt"
    file.write_text("\n".join(f"{i:08d}" for i in range(15)))
    assert len(parse_input(file, words_per_topic=15)[0].words) == 15
