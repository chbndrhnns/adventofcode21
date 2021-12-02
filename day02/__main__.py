from pathlib import Path
from typing import List


class Position:
    available_moves = []

    def __init__(self, horizontal=0, depth=0):
        self._h = horizontal
        self._d = depth

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        cls.available_moves.append(cls)

    @property
    def horizontal(self):
        return self._h

    @property
    def depth(self):
        return self._d

    @property
    def multiple(self):
        return self.depth * self.horizontal

    @classmethod
    def parse_string(cls, val: str):
        move, amount = cls._split_string(val.strip())
        move_cls = cls._find_move_cls(move)
        return move_cls(int(amount))

    @staticmethod
    def _split_string(val):
        try:
            step, amount = val.split(" ")
            return step, amount
        except ValueError:
            raise ValueError("String needs two values, separated by space")

    @classmethod
    def _find_move_cls(cls, string: str):
        try:
            return [move for move in cls.available_moves if move.__string__ == string][
                0
            ]
        except IndexError:
            raise ValueError(f"Move '{string}' not supported")

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError()

        return self.__class__(
            horizontal=self.horizontal + other.horizontal,
            depth=self.depth + other.depth,
        )

    def __str__(self):
        return f"{self.__class__.__name__}(h={self.horizontal}, d={self.depth})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other: "Position"):
        if (
            isinstance(other, self.__class__)
            and self.depth == other.depth
            and self.horizontal == other.horizontal
        ):
            return True

        return False


class Forward(Position):

    __string__ = "forward"

    def __init__(self, horizontal=0):
        super().__init__(horizontal=horizontal)


class Down(Position):
    __string__ = "down"

    def __init__(self, depth=0):
        super().__init__(depth=depth)


class Up(Position):
    __string__ = "up"

    def __init__(self, depth=0):
        super().__init__(depth=-depth)


class Submarine:
    def __init__(self):
        self._position = Position()

    @property
    def position(self):
        return self._position

    def move(self, command: Position):
        self._position += command

    def move_multiple(self, commands: List[Position]):
        for step in commands:
            self.move(step)

    @classmethod
    def create(cls):
        return cls()


if __name__ == "__main__":
    s = Submarine.create()
    with open(Path(__file__).parent / "data.txt", "r") as f:
        moves = [Position.parse_string(s) for s in f.readlines()]
        s.move_multiple(moves)
        print(f"Position: {s.position}")
        print(f"Multiple: {s.position.multiple}")
