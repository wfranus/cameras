import json
from optparse import OptionParser
from problem.ProblemInstance import ProblemInstance
#from metaheuristics.simulated_annealing.simulated_annealing import SimulatedAnnealing


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
    with open(filename) as file:
        config = json.load(file)

    # define problem and perform algorithm
    problem = ProblemInstance(config)
    #sa = SimulatedAnnealing(config, problem)
    #sa.perform()