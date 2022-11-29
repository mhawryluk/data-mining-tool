from time import sleep
from typing import Callable

from PyQt5.QtCore import QThread, pyqtSignal


class Runner(QThread):
    signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.is_running = False
        self.step_time = 10

    def run(self):
        while self.is_running:
            self.signal.emit()
            sleep(self.step_time / 1000)


class AutomateSteps:
    def __init__(self, to_execute: Callable, when_restart: Callable):
        self.to_execute = to_execute
        self.when_restart = when_restart
        self.thread = None
        self.step_time = 10

    def set_time(self, time: int):
        self.step_time = time

    def resume(self):
        self.thread = Runner()
        self.thread.signal.connect(self.to_execute)
        self.thread.is_running = True
        self.thread.step_time = self.step_time
        self.thread.start()

    def pause(self):
        if self.thread:
            self.thread.is_running = False
            self.thread = None

    def restart(self):
        self.pause()
        self.when_restart()
