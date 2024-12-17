import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.operations import Operations

class TestOperations(unittest.TestCase):

    def test_toString(self):
        self.assertEqual(Operations.toString(Operations.NONE), "NONE")
        self.assertEqual(Operations.toString(Operations.PRESSURE_SELF_TEST), "PRESSURE_SELF_TEST")
        self.assertEqual(Operations.toString(Operations.PRESSURE_TEST), "PRESSURE_TEST")

    def test_toStringLowerCase(self):
        self.assertEqual(Operations.toStringLowerCase(Operations.NONE), "None")
        self.assertEqual(Operations.toStringLowerCase(Operations.PRESSURE_SELF_TEST), "Pressure Self Test")
        self.assertEqual(Operations.toStringLowerCase(Operations.PRESSURE_TEST), "Pressure Test")

    def test_enum_values(self):
        self.assertEqual(Operations.NONE.value, 0)
        self.assertEqual(Operations.PRESSURE_SELF_TEST.value, 1)
        self.assertEqual(Operations.PRESSURE_TEST.value, 2)

    def test_enum_names(self):
        self.assertEqual(Operations.NONE.name, "NONE")
        self.assertEqual(Operations.PRESSURE_SELF_TEST.name, "PRESSURE_SELF_TEST")
        self.assertEqual(Operations.PRESSURE_TEST.name, "PRESSURE_TEST")

if __name__ == '__main__':
    unittest.main()