import os

class Guidance:
    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Gehe ein Verzeichnis nach oben
        self.preparation_overpressure_images = [
            os.path.join(base_path, "images/Guidance_preparation_overpressure_1.png"),
            os.path.join(base_path, "images/Guidance_preparation_overpressure_2.png"),
            os.path.join(base_path, "images/Guidance_preparation_overpressure_3.png"),
            os.path.join(base_path, "images/Guidance_preparation_overpressure_4.png"),
            os.path.join(base_path, "images/Guidance_preparation_overpressure_5.png"),
            os.path.join(base_path, "images/Guidance_preparation_overpressure_6.png"),
            os.path.join(base_path, "images/Guidance_preparation_overpressure_7.png"),
            os.path.join(base_path, "images/Guidance_preparation_overpressure_8.png")
        ]

        self.preparation_overpressure_instruction_texts = [
            "1. Connect the test system to the DUT",
            "2. Open the shut-off valve of the test system",
            "3. Check the pressure gauge until the test pressure is constantly reached",
            "4. Close the shut-off valve of the test system",
            "5. Disconnect the test system from the DUT",
            "6. Connect the hoses of the DUT to the test system",
            "7. Open the shut-off valve of the DUT",
            "8. Slowly set the pressure regulator to the test pressure of 200 mbar"
        ]

        self.overpressure_images = [
            os.path.join(base_path, "images/Guidance_overpressure_1.png"),
            os.path.join(base_path, "images/Guidance_overpressure_2.png"),
            os.path.join(base_path, "images/Guidance_overpressure_3.png")
        ]

        self.overpressure_instruction_texts = [
            "9. Connect the hoses of the DUT to the test system",
            "10. Open the shut-off valve of the DUT",
            "11. Check the pressure gauge until the test pressure is constantly reached"
        ]

        self.overpressure_self_test_images = [
            os.path.join(base_path, "images/Guidance_selftest_overpressure_1.png"),
            os.path.join(base_path, "images/Guidance_selftest_overpressure_2.png")
        ]

        self.overpressure_self_test_instruction_texts = [
            "9. Check the pressure gauge until the test pressure is constantly reached",
            "10. Close the inlet valve"
        ]

        self.set_overpressure_self_test_images(self.preparation_overpressure_images + self.overpressure_self_test_images)
        self.set_overpressure_self_test_instruction_texts(self.preparation_overpressure_instruction_texts + self.overpressure_self_test_instruction_texts)

        self.set_overpressure_images(self.preparation_overpressure_images + self.overpressure_images)
        self.set_overpressure_instruction_texts(self.preparation_overpressure_instruction_texts + self.overpressure_instruction_texts)

    def get_preparation_overpressure_images(self):
        return self.preparation_overpressure_images

    def get_preparation_overpressure_instruction_texts(self):
        return self.preparation_overpressure_instruction_texts

    def get_overpressure_images(self):
        return self.overpressure_images

    def get_overpressure_instruction_texts(self):
        return self.overpressure_instruction_texts

    def get_overpressure_self_test_images(self):
        return self.overpressure_self_test_images

    def get_overpressure_self_test_instruction_texts(self):
        return self.overpressure_self_test_instruction_texts

    def set_overpressure_self_test_images(self, images):
        self.overpressure_self_test_images = images

    def set_overpressure_self_test_instruction_texts(self, texts):
        self.overpressure_self_test_instruction_texts = texts

    def set_overpressure_images(self, images):
        self.overpressure_images = images

    def set_overpressure_instruction_texts(self, texts):
        self.overpressure_instruction_texts = texts