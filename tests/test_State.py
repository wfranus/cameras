from unittest import TestCase
from unittest.mock import patch, MagicMock
import unittest
from problem.State import State


class TestState(TestCase):

    @patch('problem.ProblemInstance')
    def testInitWithCameras(self, MockProblemInstance):
        problem = MockProblemInstance()

        cameras = MagicMock()
        State.generateCameras = MagicMock(return_value=[])
        s = State(problem, cameras)

        self.assertEqual(s.problem, problem)
        self.assertFalse(s.generateCameras.called)
        self.assertEqual(s.cameras, cameras)

    @patch('problem.ProblemInstance')
    @patch('problem.Camera')
    def testInitWithoutCameras(self, MockCamera, MockProblemInstance):
        problem = MockProblemInstance()

        cameras = [MockCamera()]
        State.generateCameras = MagicMock(return_value=cameras)
        s = State(problem)

        self.assertEqual(s.problem, problem)
        self.assertTrue(s.generateCameras.called)
        self.assertEqual(s.cameras, cameras)

    @patch('problem.ProblemInstance')
    def testGetRandomFreePointFromRoom(self, MockProblemInstance):
        p1, p2, p3 = (0, 1), (2, 3), (4, 5)

        problem = MockProblemInstance()
        problem.inside_points = [p1, p2, p3]

        c1 = MagicMock()
        c1.problem = problem
        c1.x, c1.y = p1

        c2 = MagicMock()
        c2.problem = problem
        c2.x, c2.y = p2

        c3 = MagicMock()
        c3.problem = problem
        c3.x, c3.y = p3

        s1 = State(problem, [])
        self.assertIn(s1.getRandomFreePointFromRoom(), problem.inside_points)

        s2 = State(problem, [c1])
        self.assertIn(s2.getRandomFreePointFromRoom(), [p2, p3])

        s3 = State(problem, [c1, c2])
        self.assertEqual(s3.getRandomFreePointFromRoom(), p3)

        s3 = State(problem, [c1, c2, c3])
        self.assertRaises(RuntimeError, s3.getRandomFreePointFromRoom)


    @patch('problem.ProblemInstance')
    def testGenerateCameras(self, MockProblemInstance):
        problem = MockProblemInstance()
        problem.min_number_of_cams = 2

        s = State(problem, [])
        s.getRandomFreePointFromRoom = MagicMock(return_value=(1, 1))

        cameras = s.generateCameras()

        self.assertEqual(len(cameras), problem.min_number_of_cams)
        self.assertEqual(len(s.getRandomFreePointFromRoom.mock_calls), 2)

if __name__ == '__main__':
    unittest.main()