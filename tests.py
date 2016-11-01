from unittest import TestCase, main as test_all
from metro_routes import *


class TesStopMatchesCurrent(TestCase):
    def test_not_same_station_but_same_line(self):
        stop = Stop("A", "A")
        current = Stop("B", "A")

        self.assertFalse(stop_matches_current(stop, current))

    def test_not_same_station_not_same_line(self):
        stop = Stop("A", "A")
        current = Stop("B", "B")

        self.assertFalse(stop_matches_current(stop, current))

    def test_not_same_station_current_line_not_set(self):
        stop = Stop("A", "A")
        current = Stop("B", None)

        self.assertFalse(stop_matches_current(stop, current))

    def test_same_station_same_line_current_set(self):
        stop = Stop("A", "A")
        current = Stop("A", "A")

        self.assertTrue(stop_matches_current(stop, current))

    def test_same_station_not_same_line_current_not_set(self):
        stop = Stop("A", "A")
        current = Stop("A", None)

        self.assertTrue(stop_matches_current(stop, current))

    def test_same_station_not_same_line_current_set(self):
        stop = Stop("A", "A")
        current = Stop("A", "B")

        self.assertFalse(stop_matches_current(stop, current))


class TestCanMoveToNextStop(TestCase):
    def test_lines_greater_than_2(self):
        self.assertFalse(
            can_move_to_next_stop(3, Stop(None, None), Stop(None, None))
        )

    def test_lines_2_lines_same(self):
        self.assertTrue(
            can_move_to_next_stop(
                2,
                Stop(None, "GREEN"),
                Stop(None, "GREEN")
            )
        )

    def test_lines_2_lines_not_same(self):
        self.assertFalse(
            can_move_to_next_stop(
                2,
                Stop(None, "BLUE"),
                Stop(None, "GREEN")
            )
        )

    def test_lines_1_lines_same(self):
        self.assertTrue(
            can_move_to_next_stop(
                1,
                Stop(None, "BLUE"),
                Stop(None, "BLUE")
            )
        )

    def test_lines_1_lines_not_same(self):
        self.assertTrue(
            can_move_to_next_stop(
                1,
                Stop(None, "BLUE"),
                Stop(None, "GREEN")
            )
        )


if __name__ == '__main__':
    test_all()
