import json, os, time
from optparse import OptionParser
from problem.ProblemInstance import ProblemInstance
from problem.SimulatedAnnealer import SimulatedAnnealer
from problem.ConfigValidator import ConfigValidator
from problem.PlotCreator import PlotCreator
import numpy
import shutil


if __name__ == '__main__':
    # parse arguments
    parser = OptionParser()
    parser.add_option('-F', '--config', action='store',
                      dest='configFile', default='config.json',
                      help='Json file with configuration')
    parser.add_option('-i', '--iterations', action='store',
                      dest='iterations', default=1, type='int',
                      help='Number of experiments')
    (options, args) = parser.parse_args()

    # check config file
    filename = options.configFile
    if not filename.endswith('.json'):
        raise ValueError('A configuration file must be a json one!')

    # read config from file
    with open(filename) as config_file:
        config = json.load(config_file)

    # define problem
    config_validator = ConfigValidator(config)
    problem = ProblemInstance(config_validator)

    # create output dir
    now = time.strftime("%Y_%m_%d_%H_%M_%S")
    out_path = os.path.join(os.getcwd(), 'out', now)
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    shutil.copy(filename, out_path)
    # create and start annealer
    all_costs = []
    for i in range(options.iterations):
        it_path = os.path.join(out_path, str(i))
        if not os.path.exists(it_path):
            os.makedirs(it_path)
        sa = SimulatedAnnealer(problem, config_validator, it_path)
        sa.anneal()
        all_costs.append(sa.costs)
        PlotCreator.createCostPlot(os.path.join(it_path, 'costs'), sa.costs)
        PlotCreator.createStatePlot(os.path.join(it_path, 'best_state'), sa.best_state)

    average_cost = numpy.mean(numpy.array(all_costs), axis=0)
    PlotCreator.createCostPlot(os.path.join(out_path, 'average_costs'), average_cost)
