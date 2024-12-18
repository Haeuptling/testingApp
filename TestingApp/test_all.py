import unittest
from PyQt5.QtWidgets import QApplication
import sys
import os
import logging

def load_tests(loader, standard_tests, pattern):
    suite = unittest.TestSuite()
    test_dir = os.path.join(os.path.dirname(__file__), 'test')
    for all_test_suite in unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py'):
        for test_suite in all_test_suite:
            if isinstance(test_suite, unittest.TestSuite):
                suite.addTests(test_suite)
            else:
                print(f"Failed to load test suite: {test_suite}")
    return suite

if __name__ == '__main__':
    logging.disable(logging.CRITICAL)

    app = QApplication(sys.argv)  
    suite = load_tests(unittest.defaultTestLoader, None, None)
    runner = unittest.TextTestRunner(verbosity=2) 
    result = runner.run(suite)
    app.quit()  

