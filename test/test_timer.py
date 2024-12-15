import unittest
from PyQt5.QtCore import QCoreApplication, QTimer
from PyQt5.QtTest import QTest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controls.timer import Timer

class TestTimer(unittest.TestCase):

    def setUp(self):
        self.app = QCoreApplication([])
        self.timer = Timer()

    def test_start_timer(self):
        duration_ms = 1000
        interval_ms = 200

        self.timer.start_timer(duration_ms, interval_ms)
        self.assertTrue(self.timer.interval_timer.isActive())
        self.assertEqual(self.timer.total_duration, duration_ms)

    def test_stop_timer(self):
        self.timer.start_timer(1000, 200)
        self.timer.stop_timer()
        self.assertFalse(self.timer.interval_timer.isActive())

    def test_interval_elapsed_signal(self):
        duration_ms = 1000
        interval_ms = 200

        def on_interval_elapsed(elapsed_ms):
            self.assertGreaterEqual(elapsed_ms, interval_ms)

        self.timer.interval_elapsed.connect(on_interval_elapsed)
        self.timer.start_timer(duration_ms, interval_ms)
        QTest.qWait(interval_ms + 100) 

    def test_timer_finished_signal(self):
        duration_ms = 500

        def on_timer_finished():
            self.assertFalse(self.timer.interval_timer.isActive())

        self.timer.timer_finished.connect(on_timer_finished)
        self.timer.start_timer(duration_ms, 100)
        QTest.qWait(duration_ms + 100)  

if __name__ == '__main__':
    unittest.main()