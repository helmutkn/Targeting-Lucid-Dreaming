import sys
import threading

from PyQt5.QtWidgets import QApplication
from scripts.ServerConnection.RecorderThread import RecordThread


class Recorder(threading.Thread):
    def __init__(self, signalType):

        super().__init__()

        self.signalType = signalType
        self.recorderThread = RecordThread(signalType=self.signalType)
        self.app = None

    def run(self):
        self.app = QApplication(sys.argv)
        self.recorderThread.start()
        sys.exit(self.app.exec())

    def stop(self):
        print('Recorder termination started')
        self.recorderThread.stop()
        print('recorderThread stopped')
        self.recorderThread.quit()
        print('recorderThread quit')
        if self.app:
            self.app.quit()
            print('app quit')





