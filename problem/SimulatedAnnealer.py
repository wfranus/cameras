from simanneal import Annealer
from problem.State import State
from problem.ConfigValidator import ConfigValidator
from pprint import pprint


class SimulatedAnnealer(Annealer):

    def __init__(self, problem, config_validator):
        self.config_validator = config_validator
        self.problem = problem
        self.costs = []
        self.updates = 10
        self.camera_move_method = config_validator.getParameter('camera_move_method', ['local', 'random'], 'local')

        try:
            self.temp_max = config_validator.getIntegerParameter('t_max', 5000)
            self.temp_min = config_validator.getIntegerParameter('t_min', 50)
            self.steps = config_validator.getIntegerParameter('num_iterations', 100)
            self.r_min = config_validator.getIntegerParameter('r_min', 100)
            self.alpha = config_validator.getDoubleParameter('alpha', 100)
            self.beta = config_validator.getDoubleParameter('beta', 100)
        except KeyError as e:
            print("Exception. Option {} is missing in config file".format(e))

        init_state = State(self.problem)
        super(SimulatedAnnealer, self).__init__(init_state)

    def move(self):
        self.state = self.state.generateNeighbour(self.camera_move_method)

    def energy(self):
        e = self.alpha * self.getCoverage() \
            - self.beta * self.getCameraCostRatio() \
            - self.getRedundancyParameter()/self.r_min

        self.costs.append(e)
        return e

    def update(self, *args, **kwargs):
        for c in self.state.cameras:
            print(c.x, c.y)

    def getCoverage(self):
        room_points = [copy.copy(c) for c in self.problem.inside_points]

        for c in self.state.cameras:
            p = (c.x, c.y)
            pass

        return 1.0

    def getCameraCostRatio(self):
        return 1.0

    def getRedundancyParameter(self):
        return 1.0