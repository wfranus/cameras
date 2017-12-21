import unittest
from unittest import TestCase
from problem.ConfigValidator import ConfigValidator


class TestConfigValidator(TestCase):

    def testGetIntegerParameter(self):
        config = {'testInteger': 5}
        config_validator = ConfigValidator(config)
        parameter = config_validator.getIntegerParameter('testInteger', '-1')
        self.assertEqual(parameter, 5)

    def testGetIntegerParameterWithInvalidParameter(self):
        config = {'testInteger': 'wrong'}
        config_validator = ConfigValidator(config)
        with self.assertRaises(Exception):
            config_validator.getIntegerParameter('testInteger')

    def testGetFloatParameter(self):
        config = {'testFloat': 5.0}
        config_validator = ConfigValidator(config)
        parameter = config_validator.getDoubleParameter('testFloat')
        self.assertEqual(parameter, 5.0)

    def testGetFloatParameterWithInvalidParameter(self):
        config = {'testFloat': 'wrong'}
        config_validator = ConfigValidator(config)
        with self.assertRaises(Exception):
            config_validator.getDoubleParameter('testFloat')

if __name__ == '__main__':
    unittest.main()
