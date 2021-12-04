from abc import ABC
from pathlib import Path
from typing import List, Type


class Command(ABC):
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

    def __str__(self):
        return f"{self.__class__.__name__}(h={self.horizontal}, d={self.depth})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if (
            isinstance(other, self.__class__)
            and self.depth == other.depth
            and self.horizontal == other.horizontal
        ):
            return True

        return False


class Position:
    def __init__(self, horizontal=0, depth=0):
        self._h = horizontal
        self._d = depth

    @property
    def horizontal(self):
        return self._h

    @property
    def depth(self):
        return self._d

    @property
    def product(self):
        return self.depth * self.horizontal

    def __add__(self, other):
        if not isinstance(other, (self.__class__, Command)):
            raise NotImplementedError()

        return self.__class__(
            horizontal=self.horizontal + other.horizontal,
            depth=self.depth + other.depth,
        )

    def __str__(self):
        return f"{self.__class__.__name__}(h={self.horizontal}, d={self.depth})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if (
            isinstance(other, self.__class__)
            and self.depth == other.depth
            and self.horizontal == other.horizontal
        ):
            return True

        return False


class PositionWithAim(Position):
    def __init__(self, horizontal=0, depth=0, aim=0):
        super().__init__(horizontal, depth)
        self._aim = aim

    @property
    def aim(self):
        return self._aim

    def __add__(self, other):
        if not isinstance(other, (self.__class__, Command)):
            raise NotImplementedError()

        instance = self.__class__(
            horizontal=self.horizontal + other.horizontal,
            depth=self.depth,
            aim=self.aim,
        )
        if isinstance(other, (Down, Up)):
            instance._aim += other.depth
        if isinstance(other, Forward):
            instance._d += instance.aim * other.horizontal

        return instance

    def __str__(self):
        return f"{self.__class__.__name__}(h={self.horizontal}, d={self.depth}, aim={self.aim})"


class Forward(Command):

    __string__ = "forward"

    def __init__(self, horizontal=0):
        super().__init__(horizontal=horizontal)


class Down(Command):
    __string__ = "down"

    def __init__(self, depth=0):
        super().__init__(depth=depth)


class Up(Command):
    __string__ = "up"

    def __init__(self, depth=0):
        super().__init__(depth=-depth)


class Submarine:
    def __init__(self, position_strategy=Position):
        self._position = position_strategy()

    @property
    def position(self):
        return self._position

    def move(self, command: Position):
        self._position += command

    def move_multiple(self, commands: List[Position]):
        for step in commands:
            self.move(step)

    @classmethod
    def create(cls, position_strategy: Type[Position] = Position):
        return cls(position_strategy=position_strategy)


if __name__ == "__main__":
    s = Submarine.create()
    with open(Path(__file__).parent / "data.txt", "r") as f:
        moves = [Position.parse_string(s) for s in f.readlines()]
        s.move_multiple(moves)
        print(f"Position: {s.position}")
        print(f"Multiple: {s.position.product}")
