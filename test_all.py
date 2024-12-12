import unittest

def load_tests(loader, standard_tests, pattern):
    suite = unittest.TestSuite()
    for all_test_suite in unittest.defaultTestLoader.discover('test', pattern='test_*.py'):
        for test_suite in all_test_suite:
            if isinstance(test_suite, unittest.TestSuite):
                suite.addTests(test_suite)
            else:
                print(f"Failed to load test suite: {test_suite}")
    return suite

if __name__ == '__main__':
    unittest.main()