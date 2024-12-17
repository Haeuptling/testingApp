from PyQt5.QtCore import QObject, QTimer, QElapsedTimer, pyqtSignal

class Timer(QObject):
    interval_elapsed = pyqtSignal(int)
    timer_finished = pyqtSignal()

    msMultiplier = 1000
    minMultiplier = 60
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.total_duration = 0
        self.interval_timer = QTimer(self)
        self.elapsed_timer = QElapsedTimer()
        self.interval_timer.timeout.connect(self.on_interval)

    def start_timer(self, duration_ms, interval_ms):
        self.total_duration = duration_ms
        self.elapsed_timer.start()
        self.interval_timer.start(interval_ms)
        print(f"Timer started for {duration_ms} ms with an interval of {interval_ms} ms.")

    def stop_timer(self):
        self.interval_timer.stop()

    def on_interval(self):
        elapsed_ms = self.elapsed_timer.elapsed()
        self.interval_elapsed.emit(elapsed_ms)
        print(f"Interval elapsed: {elapsed_ms} ms.")

        if elapsed_ms >= self.total_duration:
            self.interval_timer.stop()
            self.timer_finished.emit()
            print("Timer finished.")