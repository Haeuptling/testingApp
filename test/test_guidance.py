import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.guidance import Guidance

class TestGuidance(unittest.TestCase):
    def setUp(self):
        self.guidance = Guidance()

    def test_preparation_overpressure_images(self):
        images = self.guidance.get_preparation_overpressure_images()
        self.assertEqual(len(images), 8)
        for image in images:
            self.assertTrue(os.path.isfile(image), f"Image file not found: {image}")

    def test_preparation_overpressure_instruction_texts(self):
        texts = self.guidance.get_preparation_overpressure_instruction_texts()
        self.assertEqual(len(texts), 8)
        expected_texts = [
        "1. Close all shut-off valves",
        "2. Set the three-way valve to overpressure",
        "3. Set the pressure regulator to 0 mbar",
        "4. Connect the pressure reducer to the nitrogen supply  and the nitrogen inlet of the test system",
        "5. Open the gas supply to the nitrogen supply",
        "6. Slowly set the pressure reducer to the inlet pressure of 1 bar",
        "7. Open the inlet valve of the test system",
        "8. Slowly set the pressure regulator  to the test pressure of 200 mbar"
        ]
        self.assertEqual(texts, expected_texts)

    def test_overpressure_images(self):
        images = self.guidance.get_overpressure_images()
        self.assertEqual(len(images), 11)
        for image in images:
            self.assertTrue(os.path.isfile(image), f"Image file not found: {image}")

    def test_overpressure_instruction_texts(self):
        texts = self.guidance.get_overpressure_instruction_texts()
        self.assertEqual(len(texts), 11)
        expected_texts = [
             "1. Close all shut-off valves",
        "2. Set the three-way valve to overpressure",
        "3. Set the pressure regulator to 0 mbar",
        "4. Connect the pressure reducer to the nitrogen supply  and the nitrogen inlet of the test system",
        "5. Open the gas supply to the nitrogen supply",
        "6. Slowly set the pressure reducer to the inlet pressure of 1 bar",
        "7. Open the inlet valve of the test system",
        "8. Slowly set the pressure regulator  to the test pressure of 200 mbar",
            "9. Connect the hoses of the DUT to the test system",
            "10. Open the shut-off valve of the DUT",
            "11. Check the pressure gauge until the test pressure is constantly reached"
        ]
        self.assertEqual(texts, expected_texts)

    def test_overpressure_self_test_images(self):
        images = self.guidance.get_overpressure_self_test_images()
        self.assertEqual(len(images), 10)
        for image in images:
            self.assertTrue(os.path.isfile(image), f"Image file not found: {image}")


    def test_overpressure_self_test_instruction_texts(self):
        texts = self.guidance.get_overpressure_self_test_instruction_texts()
        expected_texts = [
        "1. Close all shut-off valves",
        "2. Set the three-way valve to overpressure",
        "3. Set the pressure regulator to 0 mbar",
        "4. Connect the pressure reducer to the nitrogen supply  and the nitrogen inlet of the test system",
        "5. Open the gas supply to the nitrogen supply",
        "6. Slowly set the pressure reducer to the inlet pressure of 1 bar",
        "7. Open the inlet valve of the test system",
        "8. Slowly set the pressure regulator  to the test pressure of 200 mbar",
        "9. Check the pressure gauge until the test pressure is constantly reached",
        "10. Close the inlet valve"
        ]
        self.assertEqual(texts, expected_texts)

if __name__ == '__main__':
    unittest.main()