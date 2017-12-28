from simanneal import Annealer
from problem.State import State
from problem.PlotCreator import PlotCreator


class SimulatedAnnealer(Annealer):

    def __init__(self, problem, config_validator):
        self.config_validator = config_validator
        self.problem = problem
        self.costs = []
        self.state = State(self.problem)
        self.camera_move_method = config_validator.getParameter('camera_move_method', ['local', 'random'], 'local')
        self.r_count_method = config_validator.getParameter('r_count_method', ['average', 'max'], 'average')

        try:
            self.temp_max = config_validator.getIntegerParameter('t_max', 5000)
            self.temp_min = config_validator.getIntegerParameter('t_min', 50)
            self.steps = config_validator.getIntegerParameter('num_iterations', 100)
            self.updates = config_validator.getIntegerParameter('num_updates', 10)
            self.update_counter = 0

            self.r_min = config_validator.getIntegerParameter('r_min', 100)
            self.alpha = config_validator.getDoubleParameter('alpha', 100)
            self.beta = config_validator.getDoubleParameter('beta', 100)
        except KeyError as e:
            print("Exception. Option {} is missing in config file".format(e))

        super(SimulatedAnnealer, self).__init__(self.state)

    # override
    def move(self):
        self.state = self.state.generateNeighbour(self.camera_move_method)

    # override
    def energy(self):
        coverage_energy = self.alpha * self.getCoverage()
        camera_cost = self.beta * self.getCameraCostRatio()
        redundancy_cost = self.getRedundancyParameter() / self.r_min

        energy = coverage_energy - camera_cost - redundancy_cost
        energy *= -1  # use for maximization
        self.costs.append(energy)

        # save energy's components for output
        self.state.energy = energy
        self.state.coverage_energy = coverage_energy
        self.state.camera_cost = camera_cost
        self.state.redundancy_cost = redundancy_cost

        return energy

    # override
    def update(self, *args, **kwargs):
        print("========== Update annealing:", self.update_counter, " ==========")
        print("Total energy:    ", self.state.energy)
        print("coverage_energy: ", self.state.coverage_energy)
        print("camera_cost:     ", self.state.camera_cost)
        print("redundancy_cost: ", self.state.redundancy_cost)

        PlotCreator.createStatePlot("out/state_" + str(self.update_counter), self.state, room_only=False)
        self.update_counter += 1

    def getCoverage(self):
        covered_points = set()

        for c in self.state.cameras:
            covered_points.update(c.covered_points)

        if len(self.problem.inside_points) == 0:
            raise RuntimeError("number of room inside points cannot be 0!!")

        coverage = len(covered_points) / float(len(self.problem.inside_points))
        #print("Coverage: ", coverage)
        return coverage

    def getCameraCostRatio(self):
        num_cameras = len(self.state.cameras)
        ratio = max(0, num_cameras - self.problem.min_number_of_cams)

        if self.problem.min_number_of_cams == 0:
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
