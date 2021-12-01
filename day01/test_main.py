import pytest

from day01 import find_naive_increases_count, find_sliding_window_increases_count


@pytest.mark.parametrize(
    "data, expected", [
        ([], 0),
        ([199], 0),
        ([199, 200], 1),
        ([199, 200, 205], 2),
        ([199, 197], 0),
        ([199, 200, 199], 1),
        ([199, 200, 197, 198, 199], 3),
        ([199, 200, 208, 210, 200, 207, 240, 269, 260, 263], 7),
        ([193, 197, 188, 170, 162, 180, 183, 211, 213, 235, 238, 237, 234], 7),
    ], ids=[
        "empty set",
        "single item",
        "one increase",
        "two increase",
        "decrease",
        "first increase is biggest",
        "second increase is biggest",
        "example",
        "first lines of real data",
    ])
def test_find_naive_increases_count(data, expected):
    assert find_naive_increases_count(data) == expected


@pytest.mark.parametrize(
    "data, expected", [
        ([], 0),
        ([199], 0),
        ([1, 2, 3], 0),
        ([1, 2, 3, 1, 2, 3], 0),
        ([1, 2, 3, 2, 2, 3], 1),
        ([1, 2, 3, 1, 2, 3], 0),
        ([1, 2, 3, 2, 2, 3, 1, 2, 3], 1),
        ([1, 2, 3, 2, 2, 3, 3, 2, 3], 2),
    ], ids=[
        "empty set",
        "single item",
        "one windows",
        "two windows, no increase",
        "two windows, increase",
        "two windows, decrease",
        "three windows, second increases",
        "three windows, all increase",
    ])
def test_sliding_window_increases_count(data, expected):
    assert find_sliding_window_increases_count(data) == expected
