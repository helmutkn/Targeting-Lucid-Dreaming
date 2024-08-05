import sys
import time
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from source_code.dreamento.scripts.UI.CLI import SleepRecorderCLI, CLIThread
from source_code.dreamento.scripts.UI.HBRecorderInterface import HBRecorderInterface


def main():
    app = QApplication(sys.argv)

    cliThread = CLIThread()
    cliThread.start()

    sys.exit(app.exec_())

def test():
    hb = HBRecorderInterface()
    hb.connectToSoftware()
    hb.startRecording()
    time.sleep(5)
    hb.stopRecording()

if __name__ == '__main__':
    main() #  test()
