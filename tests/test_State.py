import unittest, random
from unittest import TestCase
from unittest.mock import MagicMock, patch
from problem.State import State


class TestState(TestCase):

    def setUp(self):
        super(TestState, self).setUp()

        # mock Camera __init__ method for all tests
        camera_patch = patch('problem.Camera.Camera.__init__')
        camera_mock = camera_patch.start()
        camera_mock.return_value = None
        self.addCleanup(camera_patch.stop)

    def testInitWithCameras(self):
        problem = MagicMock()

        cameras = MagicMock()
        State.generateCameras = MagicMock(return_value=[])
        s = State(problem, cameras)

        self.assertEqual(s.problem, problem)
        self.assertFalse(s.generateCameras.called)
        self.assertEqual(s.cameras, cameras)

    def testInitWithoutCameras(self):
        problem = MagicMock()
        cameras = [MagicMock()]
        State.generateCameras = MagicMock(return_value=cameras)
        s = State(problem)

        self.assertEqual(s.problem, problem)
        self.assertTrue(s.generateCameras.called)
        self.assertEqual(s.cameras, cameras)

    def testGetRandomFreePointFromRoom(self):
        p1, p2, p3 = (0, 1), (2, 3), (4, 5)

        problem = MagicMock()
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

    def testGenerateCameras(self):
        problem = MagicMock()
        problem.min_number_of_cams = 2

        s = State(problem, [])
        s.getRandomFreePointFromRoom = MagicMock(return_value=(1, 1))

        cameras = s.generateCameras()

        self.assertEqual(len(cameras), problem.min_number_of_cams)
        self.assertEqual(len(s.getRandomFreePointFromRoom.mock_calls), 2)

    def testGenerateNeighbour(self):
        problem = MagicMock()

        c1 = MagicMock()
        c2 = MagicMock()
        c3 = MagicMock()
        c1.move = MagicMock()
        c2.move = MagicMock()
        c3.move = MagicMock()

        # no cameras - only insert is valid
        s1 = State(problem, [])
        s1.getRandomFreePointFromRoom = MagicMock(return_value=(1, 1))
        new_state = s1.generateNeighbour('local')
        self.assertEqual(len(new_state.cameras), 1)
        self.assertEqual(len(s1.getRandomFreePointFromRoom.mock_calls), 1)

        # one camera - insert and move are valid
        s2 = State(problem, [c1])
        s2.getRandomFreePointFromRoom = MagicMock(return_value=(1, 1))
        new_state = s2.generateNeighbour('local')
        num_cameras = len(new_state.cameras)
        if num_cameras == len(s2.cameras) + 1:
            # insert
            self.assertEqual(len(s2.getRandomFreePointFromRoom.mock_calls), 1)
        elif num_cameras == len(s2.cameras):
            # move
            self.assertEqual(len(new_state.cameras), len(s2.cameras))
            self.assertEqual(len(c1.move.mock_calls), 1)
            self.assertEqual(len(s2.getRandomFreePointFromRoom.mock_calls), 0)  # local
        else:
            self.assertTrue(False, 'Illegal camera removal')

        # two cameras - insert, remove and move are valid
        s3 = State(problem, [c2, c3])
        s3.getRandomFreePointFromRoom = MagicMock(return_value=(1, 1))
        new_state = s3.generateNeighbour('random')
        num_cameras = len(new_state.cameras)
        if num_cameras == len(s3.cameras) + 1:
            # insert
            self.assertEqual(len(s3.getRandomFreePointFromRoom.mock_calls), 1)
        elif num_cameras == len(s3.cameras):
            # move
            self.assertEqual(len(new_state.cameras), len(s3.cameras))
            self.assertEqual(len(c2.move.mock_calls) + len(c3.move.mock_calls), 1)
            self.assertEqual(len(s3.getRandomFreePointFromRoom.mock_calls), 1)  # random
        else:
            # remove
            self.assertEqual(len(new_state.cameras), len(s3.cameras) - 1)


if __name__ == '__main__':
    unittest.main()
