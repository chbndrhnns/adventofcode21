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


if __name__ == "__main__":
    with open(Path(__file__).parent / "data.txt", "r") as f:
        items = [item.strip() for item in f.readlines()]

        gamma = GammaRate(items)
        epsilon = EpsilonRate(items)

        print(f"GammaRate: {str(gamma)} ({gamma.as_decimal})")
        print(f"EpsilonRate: {str(epsilon)} ({epsilon.as_decimal})")
        print(f"Result: {gamma.as_decimal * epsilon.as_decimal}")
