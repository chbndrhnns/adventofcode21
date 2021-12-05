import pytest


class GammaRate:
    def __init__(self, values: list[str] = None):
        self._values = values or []

        if not self._values:
            self._rate = ""

        else:
            num_len = len(self._values[0])

            result = ""
            for position in range(num_len):

                ones = 0
                zeros = 0

                for item in self._values:
                    if item[position] == "1":
                        ones += 1
                    elif item[position] == "0":
                        zeros += 1
                    else:
                        raise ValueError(f"Cannot parse '{item[position]}'")

                if ones > zeros:
                    result += "1"
                else:
                    result += "0"

            self._rate = result

    @property
    def as_decimal(self):
        return int(self._rate, 2)

    def __str__(self):
        return self._rate


class EpsilonRate:
    def __init__(self, values: list[str] = None):
        self._values = values or []

        if not self._values:
            self._rate = ""

        else:
            num_len = len(self._values[0])

            result = ""
            for position in range(num_len):

                ones = 0
                zeros = 0

                for item in self._values:
                    if item[position] == "1":
                        ones += 1
                    elif item[position] == "0":
                        zeros += 1
                    else:
                        raise ValueError(f"Cannot parse '{item[position]}'")

                if ones < zeros:
                    result += "1"
                else:
                    result += "0"

            self._rate = result

    @property
    def as_decimal(self):
        return int(self._rate, 2)

    def __str__(self):
        return self._rate


class TestGammaRate:
    cls = GammaRate

    def test_empty_for_empty_input(self):
        assert str(self.cls([])) == ""

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
