from simanneal import Annealer
from problem.State import State


class SimulatedAnnealer(Annealer):

    def __init__(self, problem, config_validator):
        self.config_validator = config_validator
        self.problem = problem
        self.costs = []
        self.updates = 10
        self.camera_move_method = config_validator.getParameter('camera_move_method', ['local', 'random'], 'local')
        self.r_count_method = config_validator.getParameter('r_count_method', ['average', 'max'], 'average')

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
        covered_points = set()

        for c in self.state.cameras:
            covered_points.update(c.covered_points)

        if len(self.problem.inside_points) == 0.0:
            raise RuntimeError("number of room inside points cannot be 0!!")

        coverage = len(covered_points) / float(len(self.problem.inside_points))
        #print("Coverage: ", coverage)
        return coverage

    def getCameraCostRatio(self):
        num_cameras = len(self.state.cameras)
        ratio = max(0, num_cameras - self.problem.min_number_of_cams)

        if self.problem.min_number_of_cams == 0.0:
            raise RuntimeError("k_min cannot be 0!")

        ratio /= float(self.problem.min_number_of_cams)
        #print("k = ", ratio)
        return ratio

    def getRedundancyParameter(self):
        def count_redundancy():
            redundancy_list = []
            for p in self.problem.inside_points:
                r_x = 0
                for c in self.state.cameras:
                    if p in c.covered_points:
                        r_x += 1
                redundancy_list.append(max(0, self.r_min - r_x))
            return redundancy_list

        if len(self.problem.inside_points) == 0.0:
            raise RuntimeError("number of room inside points cannot be 0!!")

        if self.r_count_method == 'average':
            r_sum = sum(count_redundancy())
            return r_sum / float(len(self.problem.inside_points))
        elif self.r_count_method == 'max':
            return max(count_redundancy())
        else:
            raise RuntimeError("Unrecognized r_count_method!")
