import unittest
from models.operations import Operations

class TestOperations(unittest.TestCase):

    def test_toString(self):
        self.assertEqual(Operations.toString(Operations.NONE), "NONE")
        self.assertEqual(Operations.toString(Operations.PRESSURE_SELF_TEST), "PRESSURE_SELF_TEST")
        self.assertEqual(Operations.toString(Operations.PRESSURE_TEST), "PRESSURE_TEST")

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