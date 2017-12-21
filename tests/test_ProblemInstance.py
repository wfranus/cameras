import unittest
from unittest import TestCase
from problem.ProblemInstance import ProblemInstance

class TestProblemInstance(TestCase):
    def test_PolygonArea(self):
        cameraRange = 2
        roomArea = 48
        expectedMinNumberOfCameras = roomArea / cameraRange
        config = {
            "camera_range": cameraRange,
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
        pi = ProblemInstance(config)
        self.assertEqual(pi.camera_range, cameraRange)
        self.assertEqual(pi.minNumberOfCams, expectedMinNumberOfCameras)

if __name__ == '__main__':
    unittest.main()