import pytest

from day02.__main__ import (
    Command,
    Down,
    Forward,
    Position,
    PositionWithAim,
    Submarine,
    Up,
)


class TestPosition:
    def test_eq(self):
        assert Position() == Position()
        assert Position() != Position(1, 0)
        assert Position(1, 1) + Position(2, 3) == Position(3, 4)

    def test_add(self):
        assert Position() + Position() == Position()
        assert Position(1, 0) + Position(-1, 0) == Position()


class TestPositionWithAim:
    def test_has_aim(self):
        assert PositionWithAim().aim == 0

    def test_down_increases_aim(self):
        actual = PositionWithAim() + Down(1)
        assert actual.aim == 1

    def test_up_decreases_aim(self):
        actual = PositionWithAim() + Up(1)
        assert actual.aim == -1

    class TestScenarioFromText:
        def test_forward_does_not_change_initial_aim(self):
            actual = PositionWithAim() + Forward(5)
            assert actual.horizontal == 5
            assert actual.aim == 0
            assert actual.depth == 0

        def test_down_adds_to_aim(self):
            actual = PositionWithAim(5, 0, 0) + Down(5)
            assert actual.horizontal == 5
            assert actual.aim == 5

        def test_forward_multiplies_aim(self):
            actual = PositionWithAim(5, 0, 5) + Forward(8)
            assert actual.horizontal == 13
            assert actual.depth == 40
            assert actual.aim == 5

        def test_up_decreases_aim(self):
            actual = PositionWithAim(13, 40, 5) + Up(3)
            assert actual.horizontal == 13
            assert actual.depth == 40
            assert actual.aim == 2

        def test_down_increases_aim(self):
            actual = PositionWithAim(13, 40, 2) + Down(8)
            assert actual.horizontal == 13
            assert actual.depth == 40
            assert actual.aim == 10

        def test_forward_multiplies_aim_2(self):
            actual = PositionWithAim(13, 40, 10) + Forward(2)
            assert actual.horizontal == 15
            assert actual.depth == 60
            assert actual.aim == 10


class TestSteps:
    def test_up_decreases_depth(self):
        assert Position() + Up(1) == Position(0, -1)

    def test_down_increases_depth(self):
        assert Position() + Down(1) == Position(0, 1)

    @pytest.mark.parametrize(
        "step, expected",
        [("forward 5", Forward(5)), ("up 0", Up(0)), ("down 5", Down(5))],
    )
    def test_from_string_ok(self, step, expected):
        assert Command.parse_string(step) == expected

    @pytest.mark.parametrize(
        "step,expected_error",
        [("f 5", "'f' not supported"), ("", "two"), ("down", "two")],
    )
    def test_from_string_error(self, step, expected_error):
        with pytest.raises(ValueError) as err:
            Command.parse_string(step)

        assert expected_error in err.value.args[0]


def test_initial_position_is_0():
    s = Submarine.create()
    assert s.position == Position(0, 0)


def test_can_move_submarine():
    s = Submarine.create()
    s.move(Forward(1))
    assert s.position == Position(1, 0)


def test_can_move_multiple_steps__empty():
    s = Submarine.create()
    s.move_multiple([])
    assert s.position == Position(0, 0)


def test_can_move_multiple_steps__single():
    s = Submarine.create()
    s.move_multiple([Forward(4)])
    assert s.position == Position(4, 0)


def test_can_move_multiple_steps__two():
    s = Submarine.create()
    s.move_multiple([Forward(4)])
    assert s.position == Position(4, 0)


@pytest.mark.parametrize(
    "strategy,position,product",
    [
        (Position, Position(15, 10), 150),
        (PositionWithAim, PositionWithAim(15, 60), 900),
    ],
)
def test_example(strategy, position, product):
    steps = [
        Forward(5),
        Down(5),
        Forward(8),
        Up(3),
        Down(8),
        Forward(2),
    ]
    s = Submarine.create(position_strategy=strategy)
    s.move_multiple(steps)
    assert s.position == position
    assert s.position.product == product
