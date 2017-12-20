from unittest import TestCase
import unittest
from ProblemInstance import ProblemInstance

class TestProblemInstance(TestCase):
    def testInit(self):
        pi = ProblemInstance({})
        print("TEST OK")

if __name__ == '__main__':
    unittest.main()