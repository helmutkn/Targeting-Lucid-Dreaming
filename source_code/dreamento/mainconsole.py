import sys
import time
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from scripts.UI.CLI import SleepRecorderCLI, CLIThread
from scripts.UI.HBRecorderInterface import HBRecorderInterface


def main():
    app = QApplication(sys.argv)

    cliThread = CLIThread(app)
    cliThread.start()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


# TODO:
#   load / import SleePyCo model
#   check if it can handle a single epoch of len == 30 sec
#   make sure the received data is split into 30 sec epochs before feeding the model
#   insert model in HBRecorderInterface
