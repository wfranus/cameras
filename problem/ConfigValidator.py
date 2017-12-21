
class ConfigValidator:
    def __init__(self, config):
        self.config = config

    def getIntegerParameter(self, parameter, default_value=None):
        value = self.config.get(parameter, default_value)
        print(value)
        if not ConfigValidator.isInteger(value) or value <= 0:
            ConfigValidator.raiseError(parameter, value)
        return value

    def getDoubleParameter(self, parameter, default_value=None):
        value = self.config.get(parameter, default_value)
        if not ConfigValidator.isFloat(value):
            ConfigValidator.raiseError(parameter, value)
        return value

    def getParameter(self, parameter, validate_possible_values=None, default_value=None):
        if default_value:
            move = self.config.get(parameter, default_value)
        else:
            move = self.config[parameter]

        if validate_possible_values:
            if move not in validate_possible_values:
                ConfigValidator.raiseError(parameter, move)
        return move

    @staticmethod
    def raiseError(parameter, value):
        print("Wrong parameter: {} got value: {} ", parameter, value)
        raise RuntimeError

    @staticmethod
    def isFloat(var):
        try:
            float(var)
            return True
        except ValueError:
            return False

    @staticmethod
    def isInteger(var):
        try:
            int(var)
            return True
        except ValueError:
            return False
