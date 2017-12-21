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
            self.tempMax = config_validator.getIntegerParameter('t_max', 5000)
            self.tempMin = config_validator.getIntegerParameter('t_min', 50)
            self.steps = config_validator.getIntegerParameter('num_iterations', 100)
        except KeyError as e:
            print("Exception. Option {} is missing in config file".format(e))

        init_state = State(self.problem)
        super(SimulatedAnnealer, self).__init__(init_state)

    def move(self):
        self.state = self.state.generateNeighbour(self.camera_move_method)

    def energy(self):
        #TODO calculate cost fun of current state
        # append current cost to self.costs
        e = 0
        self.costs.append(e)
        return e

    def update(self, *args, **kwargs):
        for c in self.state.cameras:
            print(c.x, c.y)