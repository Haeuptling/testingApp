import unittest
from PyQt5.QtCore import QPointF
from models.measurement import Measurement

class TestMeasurement(unittest.TestCase):
    def setUp(self):
        self.measurement = Measurement()

    def test_generate_pressure_values(self):
        self.measurement.generate_pressure_values(120, 50)
        pressure_values = self.measurement.get_pressure_values()
        self.assertEqual(len(pressure_values), 1)
        self.assertEqual(pressure_values[0].x(), 2.0)  # 120 seconds = 2 minutes
        self.assertEqual(pressure_values[0].y(), 50)

    def test_generate_relative_humidity_values(self):
        self.measurement.generate_relative_humidity_values(180, 60)
        humidity_values = self.measurement.get_relative_humidity_values()
        self.assertEqual(len(humidity_values), 1)
        self.assertEqual(humidity_values[0].x(), 3.0)  # 180 seconds = 3 minutes
        self.assertEqual(humidity_values[0].y(), 60)

    def test_evaluate_pressure(self):
        self.measurement.generate_pressure_values(0, 50)
        self.measurement.generate_pressure_values(60, 55)
        self.measurement.set_maximum_pressure_difference_in_percent(10)
        result = self.measurement.evaluate_pressure()
        self.assertTrue(result)

    def test_evaluate_relative_humidity(self):
        self.measurement.generate_relative_humidity_values(0, 40)
        self.measurement.generate_relative_humidity_values(60, 44)
        self.measurement.set_maximum_humidity_difference_in_percent(10)
        result = self.measurement.evaluate_relative_humidity()
        self.assertTrue(result)

    def test_find_min_max(self):
        points = [QPointF(0, 10), QPointF(1, 20), QPointF(2, 5), QPointF(3, 15)]
        min_max = self.measurement.find_min_max(points)
        self.assertEqual(min_max[0].y(), 5)
        self.assertEqual(min_max[1].y(), 20)

if __name__ == '__main__':
    unittest.main()