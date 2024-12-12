import unittest
import os
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
            "1. Connect the test system to the DUT",
            "2. Open the shut-off valve of the test system",
            "3. Check the pressure gauge until the test pressure is constantly reached",
            "4. Close the shut-off valve of the test system",
            "5. Disconnect the test system from the DUT",
            "6. Connect the hoses of the DUT to the test system",
            "7. Open the shut-off valve of the DUT",
            "8. Slowly set the pressure regulator to the test pressure of 200 mbar"
        ]
        self.assertEqual(texts, expected_texts)

    def test_overpressure_images(self):
        images = self.guidance.get_overpressure_images()
        self.assertEqual(len(images), 3)
        for image in images:
            self.assertTrue(os.path.isfile(image), f"Image file not found: {image}")

    def test_overpressure_instruction_texts(self):
        texts = self.guidance.get_overpressure_instruction_texts()
        self.assertEqual(len(texts), 3)
        expected_texts = [
            "9. Connect the hoses of the DUT to the test system",
            "10. Open the shut-off valve of the DUT",
            "11. Check the pressure gauge until the test pressure is constantly reached"
        ]
        self.assertEqual(texts, expected_texts)

    def test_overpressure_self_test_images(self):
        images = self.guidance.get_overpressure_self_test_images()
        self.assertEqual(len(images), 2)
        for image in images:
            self.assertTrue(os.path.isfile(image), f"Image file not found: {image}")

    def test_overpressure_self_test_instruction_texts(self):
        texts = self.guidance.get_overpressure_self_test_instruction_texts()
        self.assertEqual(len(texts), 2)
        expected_texts = [
            "9. Check the pressure gauge until the test pressure is constantly reached",
            "10. Close the inlet valve"
        ]
        self.assertEqual(texts, expected_texts)

if __name__ == '__main__':
    unittest.main()