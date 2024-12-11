from PyQt5.QtCore import QObject, QTimer, QElapsedTimer, pyqtSignal

class TimerHandler(QObject):
    intervalElapsed = pyqtSignal(int)
    timerFinished = pyqtSignal()

    msMultiplier = 1000
    minMultiplier = 60
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_totalDuration = 0
        self.m_intervalTimer = QTimer(self)
        self.m_elapsedTimer = QElapsedTimer()
        self.m_intervalTimer.timeout.connect(self.on_interval)

    def start_timer(self, duration_ms, interval_ms):
        self.m_totalDuration = duration_ms
        self.m_elapsedTimer.start()
        self.m_intervalTimer.start(interval_ms)
        print(f"Timer started for {duration_ms} ms with an interval of {interval_ms} ms.")

    def stop_timer(self):
        self.m_intervalTimer.stop()

    def on_interval(self):
        elapsed_ms = self.m_elapsedTimer.elapsed()
        self.intervalElapsed.emit(elapsed_ms)
        print(f"Interval elapsed: {elapsed_ms} ms.")

        if elapsed_ms >= self.m_totalDuration:
            self.m_intervalTimer.stop()
            self.timerFinished.emit()
            print("Timer finished.")