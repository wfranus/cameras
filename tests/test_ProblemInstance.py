import unittest
from unittest import TestCase
from src.ProblemInstance import ProblemInstance
from src.ConfigValidator import ConfigValidator


class TestProblemInstance(TestCase):

    def test_PolygonArea(self):
        camera_side = 2
        room_area = 48
        camera_area = camera_side * camera_side
        expected_min_number_of_cameras = room_area / camera_area
        expected_inside_points_len = 33
        config = {
            "camera_side": camera_side,
            "room": [
                {
                    "x": 0,
                    "y": 0
                },
                {
                    "x": 0,
                    "y": 4
                },
                {
                    "x": 4,
                    "y": 4
                },
                {
                    "x": 4,
                    "y": 8
                },
                {
                    "x": 8,
                    "y": 8
                },
                {
                    "x": 8,
                    "y": 0
                },
                {
                    "x": 0,
                    "y": 0
                }
            ]
        }
        config_validator = ConfigValidator(config)
        pi = ProblemInstance(config_validator)
        self.assertEqual(pi.camera_side, camera_side)
        self.assertEqual(pi.min_number_of_cams, expected_min_number_of_cameras)
        self.assertEqual(len(pi.inside_points), expected_inside_points_len)


if __name__ == '__main__':
    unittest.main()
