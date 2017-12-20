from simanneal import Annealer

class SimulatedAnnealer(Annealer):

    def __init__(self, problemInstance, config):
        self.problem = problemInstance
        self.costs = []

        try:
            self.tempMax = config['t_max']
            self.tempMin = config['t_min']
            self.steps = config['num_iterations']
        except KeyError as e:
            print("Exception. Option {} is missing in config file".format(e))

        initState = self.problem.getInitialState()
        super(SimulatedAnnealer, self).__init__(initState)

    def move(self):
        #TODO modify current state
        pass

    def energy(self):
        #TODO calculate cost fun of current state
        # append current cost to self.costs
        pass