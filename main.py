import json
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

    # define problem and perform algorithm
    config_validator = ConfigValidator(config)
    problem = ProblemInstance(config_validator)
    sa = SimulatedAnnealer(problem, config_validator)

    PlotCreator.createStatePlot("out/room", sa.state, room_only=True)
    PlotCreator.createStatePlot("out/initial_state", sa.state, room_only=False)

    sa.anneal()

    PlotCreator.createStatePlot("out/final_state", sa.state, room_only=False)
    PlotCreator.createCostPlot("out/costs", sa.costs)
