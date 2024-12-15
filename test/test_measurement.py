import unittest
from PyQt5.QtCore import QPointF

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

    def test_evaluate_pressure_positive_limits(self):
        time = [1, 2, 3, 4, 5, 6]
        pressure_values = [100, 99, 97, 95, 91, 90]

        max_pressure_difference = 10

        for t, value in zip(time, pressure_values):
            self.measurement.generate_pressure_values(t, value)
    
        self.measurement.set_maximum_pressure_difference_in_percent(max_pressure_difference)
        result = self.measurement.evaluate_pressure()
        self.assertTrue(result)

    def test_evaluate_pressure_false_limits_under(self):
        time = [1, 2, 3, 4, 5, 6]
        pressure_values = [100, 99, 97, 95, 91, 89]

        max_pressure_difference = 10

        for t, value in zip(time, pressure_values):
            self.measurement.generate_pressure_values(t, value)
    
        self.measurement.set_maximum_pressure_difference_in_percent(max_pressure_difference)
        result = self.measurement.evaluate_pressure()
        self.assertFalse(result)

    def test_evaluate_pressure_false_limits_over(self):
        time = [1, 2, 3, 4, 5, 6]
        pressure_values = [101, 99, 97, 95, 91, 90]

        max_pressure_difference = 10

        for t, value in zip(time, pressure_values):
            self.measurement.generate_pressure_values(t, value)
    
        self.measurement.set_maximum_pressure_difference_in_percent(max_pressure_difference)
        result = self.measurement.evaluate_pressure()
        self.assertFalse(result)

    def test_evaluate_dewpoint_positive_limits(self):
        time = [1, 2, 3, 4, 5, 6]
        dewpoint_values = [100, 99, 97, 95, 91, 90]

        max_dewpoint_difference = 10

        for t, value in zip(time, dewpoint_values):
            self.measurement.generate_relative_humidity_values(t, value)
    
        self.measurement.set_maximum_humidity_difference_in_percent(max_dewpoint_difference)
        result = self.measurement.evaluate_relative_humidity()
        self.assertTrue(result)

    def test_evaluate_dewpoint_negative_limits_under(self):
        time = [1, 2, 3, 4, 5, 6]
        dewpoint_values = [100, 99, 97, 95, 91, 89]

        max_dewpoint_difference = 10

        for t, value in zip(time, dewpoint_values):
            self.measurement.generate_relative_humidity_values(t, value)
    
        self.measurement.set_maximum_humidity_difference_in_percent(max_dewpoint_difference)
        result = self.measurement.evaluate_relative_humidity()
        self.assertFalse(result)

    def test_evaluate_dewpoint_negative_limits_over(self):
        time = [1, 2, 3, 4, 5, 6]
        dewpoint_values = [101, 99, 97, 95, 91, 90]

        max_dewpoint_difference = 10

        for t, value in zip(time, dewpoint_values):
            self.measurement.generate_relative_humidity_values(t, value)
    
        self.measurement.set_maximum_humidity_difference_in_percent(max_dewpoint_difference)
        result = self.measurement.evaluate_relative_humidity()
        self.assertFalse(result)

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

    def test_find_min_max_positive_values(self):
        points = [QPointF(0, 10), QPointF(1, 20), QPointF(2, 5), QPointF(3, 15)]
        min_max = self.measurement.find_min_max(points)
        self.assertEqual(min_max[0].y(), 5)
        self.assertEqual(min_max[1].y(), 20)

    def test_find_min_max_negative_values(self):
        points = [QPointF(0, -10), QPointF(1, -20), QPointF(2, -5), QPointF(3, -15)]
        min_max = self.measurement.find_min_max(points)
        self.assertEqual(min_max[0].y(), -20)
        self.assertEqual(min_max[1].y(), -5)

    def test_find_min_max_mixed_values(self):
        points = [QPointF(0, -10), QPointF(1, 20), QPointF(2, -5), QPointF(3, 15)]
        min_max = self.measurement.find_min_max(points)
        self.assertEqual(min_max[0].y(), -10)
        self.assertEqual(min_max[1].y(), 20)

    def test_find_min_max_zero_values(self):
        points = [QPointF(0, 0), QPointF(1, 0), QPointF(2, 0), QPointF(3, 0)]
        min_max = self.measurement.find_min_max(points)
        self.assertEqual(min_max[0].y(), 0)
        self.assertEqual(min_max[1].y(), 0)

    def test_calculate_percentage_difference_positive_values(self):
        min_value = 50
        max_value = 100
        result = self.measurement.calculate_percentage_difference(min_value, max_value)
        self.assertEqual(result, 50)

    def test_calculate_percentage_difference_negative_values(self):
        min_value = -50
        max_value = -100
        result = self.measurement.calculate_percentage_difference(min_value, max_value)
        self.assertEqual(result, 50)

    def test_calculate_percentage_difference_mixed_values(self):
        min_value = -50
        max_value = 100
        result = self.measurement.calculate_percentage_difference(min_value, max_value)
        self.assertEqual(result, 150)

    def test_calculate_percentage_difference_zero_max_value(self):
        min_value = 50
        max_value = 0
        result = self.measurement.calculate_percentage_difference(min_value, max_value)
        self.assertEqual(result, 0)

    def test_calculate_percentage_difference_zero_min_value(self):
        min_value = 0
        max_value = 100
        result = self.measurement.calculate_percentage_difference(min_value, max_value)
        self.assertEqual(result, 100)

    def test_calculate_percentage_difference_equal_values(self):
        min_value = 100
        max_value = 100
        result = self.measurement.calculate_percentage_difference(min_value, max_value)
        self.assertEqual(result, 0)

    def test_pressure_unit_multiplicator_valid_values(self):
        self.assertEqual(Measurement.pressure_unit_multiplicator(0), 1)
        self.assertEqual(Measurement.pressure_unit_multiplicator(1), 0.1)
        self.assertEqual(Measurement.pressure_unit_multiplicator(2), 0.01)
        self.assertEqual(Measurement.pressure_unit_multiplicator(3), 0.001)
        self.assertEqual(Measurement.pressure_unit_multiplicator(4), 0.0001)

    def test_pressure_unit_multiplicator_invalid_value_negative(self):
        with self.assertRaises(ValueError) as context:
            Measurement.pressure_unit_multiplicator(-1)
        self.assertEqual(str(context.exception), "Die Eingabe muss zwischen 0 und 4 liegen.")

    def test_pressure_unit_multiplicator_invalid_value_above(self):
        with self.assertRaises(ValueError) as context:
            Measurement.pressure_unit_multiplicator(5)
        self.assertEqual(str(context.exception), "Die Eingabe muss zwischen 0 und 4 liegen.")


if __name__ == '__main__':
    unittest.main()