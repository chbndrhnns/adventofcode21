import abc
from abc import ABC
from pathlib import Path


class Rate(ABC):
    def __init__(self, values: list[str] = None):
        self._values = values or []
        self._rate = ""

        if self._values:
            self._len = len(self._values[0]) if self._values else 0
            self._ones_by_position = {pos: 0 for pos in range(self._len)}
            self._zeros_by_position = {pos: 0 for pos in range(self._len)}

            self._get_frequencies()
            self._rate = self._calculate_rate()

    @property
    def as_decimal(self):
        if not self._values:
            return 0
        return int(self._rate, 2)

    def _get_frequencies(self):
        for position in range(self._len):
            for item in self._values:
                if item[position] == "1":
                    self._ones_by_position[position] += 1
                elif item[position] == "0":
                    self._zeros_by_position[position] += 1
                else:
                    raise ValueError(f"Cannot parse '{item[position]}'")

    @abc.abstractmethod
    def _calculate_rate(self):
        ...

    def __str__(self):
        return self._rate


class GammaRate(Rate):
    def _calculate_rate(self):
        rate = ""

        for pos in range(self._len):
            if self._ones_by_position[pos] > self._zeros_by_position[pos]:
                rate += "1"
            else:
                rate += "0"

        return rate


class EpsilonRate(Rate):
    def _calculate_rate(self):
        rate = ""

        for pos in range(self._len):
            if self._ones_by_position[pos] > self._zeros_by_position[pos]:
                rate += "0"
            else:
                rate += "1"

        return rate


class Rating(ABC):
    __winner__ = None
    __loser__ = None

    def __init__(self, values: list[str] = None):
        self._values = values or []

        if self._values:
            self._len = len(self._values[0])
            self._rate = self._calculate_rating()

    def _calculate_rating(self):
        for position in range(self._len):
            self._values = self._get_frequencies_at(position)
            if len(self._values) == 1:
                return self._values[0]

    def _get_frequencies_at(self, position):
        items_with_one = []
        items_with_zero = []

        for item in self._values:
            if item[position] == "1":
                items_with_one.append(item)
            elif item[position] == "0":
                items_with_zero.append(item)
            else:
                raise ValueError(f"Cannot parse '{item[position]}'")

        if len(items_with_one) >= len(items_with_zero):
            return locals()[self.__winner__]
        return locals()[self.__loser__]

    @property
    def as_decimal(self):
        if not self._values:
            return 0
        return int(self._rate, 2)

    def __str__(self):
        return self._rate


class OxygenGeneratorRating(Rating):
    __winner__ = "items_with_one"
    __loser__ = "items_with_zero"


class Co2ScrubberRating(Rating):
    __winner__ = "items_with_zero"
    __loser__ = "items_with_one"


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
