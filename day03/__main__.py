import operator
from abc import ABC
from pathlib import Path

ZERO = "0"
ONE = "1"
NO_VALUES = 0
FIRST_ITEM = 0
INCREMENT_BY_ONE = 1


def null_operator(val1, val2):
    ...


class RepresentationMixin(ABC):
    @property
    def as_decimal(self):
        if not self._values:
            return 0
        return int(self._rate, 2)

    def __str__(self):
        return self._rate


class Rate(RepresentationMixin, ABC):
    __operator__ = null_operator

    def __init__(self, values: list[str] = None):
        self._values = values or []
        self._rate = ""

        if self._values:
            self._item_length = self._get_item_length()
            self._init_counts()
            self._get_frequencies()
            self._rate = self._calculate_rate()

    def _init_counts(self):
        self._ones_by_position = {pos: 0 for pos in range(self._item_length)}
        self._zeros_by_position = {pos: 0 for pos in range(self._item_length)}

    def _get_item_length(self):
        return len(self._values[FIRST_ITEM])

    def _get_frequencies(self):
        for position in range(self._item_length):
            for item in self._values:
                if item[position] == ONE:
                    self._ones_by_position[position] += INCREMENT_BY_ONE
                elif item[position] == ZERO:
                    self._zeros_by_position[position] += INCREMENT_BY_ONE
                else:
                    raise ValueError(f"Cannot parse '{item[position]}'")

    def _calculate_rate(self):
        rate = ""

        for pos in range(self._item_length):
            if self.__operator__(
                self._ones_by_position[pos], self._zeros_by_position[pos]
            ):
                rate += ONE
            else:
                rate += ZERO

        return rate


class Rating(RepresentationMixin, ABC):
    __operator__ = null_operator
    __tie_breaker__ = None

    def __init__(self, values: list[str] = None):
        self._values = values or []

        if self._values:
            self._item_length = self._get_item_length()
            self._rate = self._calculate_result()

    def _get_item_length(self):
        return len(self._values[FIRST_ITEM])

    def _calculate_result(self):
        for position in range(self._item_length):
            self._values = self._get_frequencies_at(position)
            if self._one_item_left():
                return self._values[FIRST_ITEM]

    def _one_item_left(self):
        return len(self._values) == 1

    def _get_frequencies_at(self, position):
        ones = []
        zeros = []

        for item in self._values:
            if item[position] == ONE:
                ones.append(item)
            else:
                zeros.append(item)

        if len(ones) == len(zeros):
            return locals()[self.__tie_breaker__]

        if self.__operator__(len(ones), len(zeros)):
            return ones
        return zeros


class GammaRate(Rate):
    __operator__ = operator.gt


class EpsilonRate(Rate):
    __operator__ = operator.lt


class OxygenGeneratorRating(Rating):
    __operator__ = operator.gt
    __tie_breaker__ = "ones"


class Co2ScrubberRating(Rating):
    __operator__ = operator.lt
    __tie_breaker__ = "zeros"


if __name__ == "__main__":
    with open(Path(__file__).parent / "data.txt", "r") as f:
        items = [item.strip() for item in f.readlines()]

        gamma = GammaRate(items)
        epsilon = EpsilonRate(items)

        print(f"GammaRate: {str(gamma)} ({gamma.as_decimal})")
        print(f"EpsilonRate: {str(epsilon)} ({epsilon.as_decimal})")
        print(f"Power consumption: {gamma.as_decimal * epsilon.as_decimal}")

        oxygen = OxygenGeneratorRating(items)
        co2 = Co2ScrubberRating(items)

        print(f"OxygenGeneratorRating: {str(oxygen)} ({oxygen.as_decimal})")
        print(f"Co2ScrubberRating: {str(co2)} ({co2.as_decimal})")
        print(f"Life support rating: {oxygen.as_decimal * co2.as_decimal}")
