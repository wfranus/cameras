import json, os, time
from optparse import OptionParser
from problem.ProblemInstance import ProblemInstance
from problem.SimulatedAnnealer import SimulatedAnnealer
from problem.ConfigValidator import ConfigValidator
from problem.PlotCreator import PlotCreator


if __name__ == '__main__':
    # parse arguments
    parser = OptionParser()
    parser.add_option('-F', '--config', action='store',
                      dest='configFile', default='config.json',
                      help='Json file with configuration')
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

    # create and start annealer
    sa = SimulatedAnnealer(problem, config_validator, out_path)
    sa.anneal()

    PlotCreator.createCostPlot(os.path.join(out_path, 'costs'), sa.costs)
