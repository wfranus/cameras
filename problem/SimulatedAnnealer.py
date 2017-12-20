from simanneal import Annealer
from problem.State import State

class SimulatedAnnealer(Annealer):

    def __init__(self, problem, config):
        self.problem = problem
        self.costs = []

        try:
            self.tempMax = config['t_max']
            self.tempMin = config['t_min']
            self.steps = config['num_iterations']
        except KeyError as e:
            print("Exception. Option {} is missing in config file".format(e))

        initState = State(self.problem)
        super(SimulatedAnnealer, self).__init__(initState)

    def move(self):
        self.state = self.state.generate_neighbour()

    def energy(self):
        #TODO calculate cost fun of current state
        # append current cost to self.costs
        e = 0
        self.costs.append(e)
        return e

    def update(self, *args, **kwargs):
        pass