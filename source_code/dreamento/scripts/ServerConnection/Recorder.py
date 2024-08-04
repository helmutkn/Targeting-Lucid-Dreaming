import sys
import threading

from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from source_code.dreamento.scripts.ServerConnection.RecorderThread import RecordThread


class Recorder(threading.Thread):
    def __init__(self):
        super().__init__()
        self.app = None
        self.recorderThread = None

    def run(self):
        self.app = QApplication(sys.argv)
        self.recorderThread = RecordThread()
        self.recorderThread.start()
        self.app.exec()

    def stop(self):
        self.recorderThread.stop()
        self.recorderThread.quit()
        self.app.quit()




