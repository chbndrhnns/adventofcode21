import abc
from abc import ABC

import pytest

from day03.__main__ import EpsilonRate, GammaRate


class TestGammaRate:
    cls = GammaRate

    def test_empty_for_empty_input(self):
        actual = self.cls([])
        assert str(actual) == ""
        assert actual.as_decimal == 0

    @pytest.mark.parametrize(
        "inp,result",
        [
            (["0"], "0"),
            (["1"], "1"),
            (["0", "0"], "0"),
            (["1", "1"], "1"),
            (["0", "1", "1"], "1"),
            (["1", "0", "0"], "0"),
            (["1", "1", "1"], "1"),
        ],
    )
    def test_find_most_common_bit__single_bit(self, inp, result):
        assert str(self.cls(inp)) == result

    def test_example(self):
        data = [
            "00100",
            "11110",
            "10110",
            "10111",
            "10101",
            "01111",
            "00111",
            "11100",
            "10000",
            "11001",
            "00010",
            "01010",
        ]
        actual = self.cls(data)
        assert str(actual) == "10110"
        assert actual.as_decimal == 22


class TestEpsilonRate:
    cls = EpsilonRate

    def test_empty_for_empty_input(self):
        assert str(self.cls([])) == ""

    @pytest.mark.parametrize(
        "inp,result",
        [
            (["0"], "1"),
            (["1"], "0"),
            (["0", "0"], "1"),
            (["1", "1"], "0"),
            (["0", "1", "1"], "0"),
            (["1", "0", "0"], "1"),
            (["1", "1", "1"], "0"),
        ],
    )
    def test_find_most_common_bit__single_bit(self, inp, result):
        assert str(self.cls(inp)) == result

    @pytest.mark.parametrize(
        "inp,result",
        [
            (["01", "00", "01"], "10"),
            (["01", "00", "00"], "11"),
            (["11", "00", "00"], "11"),
            (["11", "10", "00"], "01"),
        ],
    )
    def test_find_most_common_bit__two_bits(self, inp, result):
        assert str(self.cls(inp)) == result

    def test_example(self):
        data = [
            "00100",
            "11110",
            "10110",
            "10111",
            "10101",
            "01111",
            "00111",
            "11100",
            "10000",
            "11001",
            "00010",
            "01010",
        ]
        actual = self.cls(data)
        assert str(actual) == "01001"
        assert actual.as_decimal == 9
