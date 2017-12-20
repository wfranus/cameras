
class ConfigValidator:
    def __init__(self):
        pass
    
    @staticmethod
    def validateIntegerParameter(config, parameter, default_value):
        value = config.get(parameter, default_value)
        if not ConfigValidator.isInteger(value) or value <= 0:
            ConfigValidator.raiseError(parameter, value)
        return value

    @staticmethod
    def validateDoubleParameter(config, parameter, default_value):
        value = config.get(parameter, default_value)
        if not ConfigValidator.isFloat(value):
            ConfigValidator.raiseError(parameter, value)
        return value

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