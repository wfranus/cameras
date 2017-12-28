import unittest, random
from unittest import TestCase
from unittest.mock import MagicMock, patch
from problem.SimulatedAnnealer import SimulatedAnnealer


class TestState(TestCase):

    def setUp(self):
        super(TestState, self).setUp()

        # create mocks
        patches = {
            'problem': 'problem.ProblemInstance.ProblemInstance.__init__',
            'state': 'problem.State.State.__init__',
            'camera': 'problem.Camera.Camera.__init__',
            'config': 'problem.ConfigValidator.ConfigValidator.__init__'
        }
        self.applied_patches = dict([(n, patch(p)) for n, p in patches.items()])
        self.mocks = dict([(n, p.start()) for n, p in self.applied_patches.items()])
        for n, m in self.mocks.items():
            m.return_value = None
        for n, p in self.applied_patches.items():
            self.addCleanup(p.stop)

    def testEnergy(self):
        sa = SimulatedAnnealer(self.mocks['problem'], self.mocks['config'])
        sa.getCoverage = MagicMock(return_value=0.5)
        sa.getCameraCostRatio = MagicMock(return_value=0.2)
        sa.getRedundancyParameter = MagicMock(return_value=0.1)
        sa.alpha = 2.0
        sa.beta = 3.0
        sa.r_min = 4

        self.assertAlmostEqual(sa.energy(), 0.375, delta=0.001)
        self.assertEqual(len(sa.costs), 1)
        self.assertEqual(len(sa.getCoverage.mock_calls), 1)
        self.assertEqual(len(sa.getCameraCostRatio.mock_calls), 1)
        self.assertEqual(len(sa.getRedundancyParameter.mock_calls), 1)

    def testGetCoverage(self):
        problem = self.mocks['problem']

        sa = SimulatedAnnealer(problem, self.mocks['config'])
        c1 = MagicMock()
        c2 = MagicMock()
        c1.covered_points = [(0, 0), (2, 1)]
        c2.covered_points = [(0, 0), (2, 2)]
        sa.state.cameras = [c1, c2]

        problem.inside_points = []
        self.assertRaises(RuntimeError, sa.getCoverage)

        problem.inside_points = [(0, 0), (1, 1), (2, 1), (2, 2)]
        expected_coverage = len(set(c1.covered_points + c2.covered_points))
        expected_coverage /= len(problem.inside_points)
        self.assertEqual(sa.getCoverage(), expected_coverage)

    def testGetCameraCostRatio(self):
        problem = self.mocks['problem']

        sa = SimulatedAnnealer(problem, self.mocks['config'])

        sa.state.cameras = []
        problem.min_number_of_cams = 0
        self.assertRaises(RuntimeError, sa.getCameraCostRatio)

        sa.state.cameras = [MagicMock()]
        problem.min_number_of_cams = 2
        self.assertEqual(sa.getCameraCostRatio(), 0.0)

        sa.state.cameras = [MagicMock(), MagicMock()]
        problem.min_number_of_cams = 1
        self.assertEqual(sa.getCameraCostRatio(), 1.0)

    def testGetRedundancyParameter(self):
        problem = self.mocks['problem']

        sa = SimulatedAnnealer(problem, self.mocks['config'])
        c1 = MagicMock()
        c2 = MagicMock()
        c1.covered_points = [(0, 0), (2, 1)]
        c2.covered_points = [(0, 0), (2, 2)]

        sa.r_count_method = ''
        problem.inside_points = []
        self.assertRaises(RuntimeError, sa.getRedundancyParameter)

        sa.r_count_method = 'average'
        sa.r_min = 2
        sa.state.cameras = [c1, c2]
        problem.inside_points = [(0, 0), (1, 1), (2, 1), (2, 2)]
        self.assertEqual(sa.getRedundancyParameter(), 4.0 / len(problem.inside_points))

        sa.r_count_method = 'average'
        sa.r_min = 3
        sa.state.cameras = [MagicMock(), MagicMock()]
        # cameras are fake - no points covered
        self.assertEqual(sa.getRedundancyParameter(), 12.0 / len(problem.inside_points))

        sa.r_count_method = 'max'
        sa.r_min = 4
        sa.state.cameras = [c1, c2]
        problem.inside_points = [(0, 0), (1, 1), (2, 1), (2, 2)]
        # one point not covered at all
        self.assertEqual(sa.getRedundancyParameter(), sa.r_min)

        sa.r_count_method = 'max'
        sa.r_min = 4
        sa.state.cameras = [c1, c2]
        problem.inside_points = [(0, 0), (2, 1), (2, 2)]
        # 2 points covered by 1 camera, and 1 point covered by 2 cameras
        self.assertEqual(sa.getRedundancyParameter(), 3.0)