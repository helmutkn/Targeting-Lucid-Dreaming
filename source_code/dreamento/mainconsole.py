import sys
import time
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from source_code.dreamento.scripts.UI.CLI import SleepRecorderCLI, CLIThread
from source_code.dreamento.scripts.UI.HBRecorderInterface import HBRecorderInterface


def main():
    app = QApplication(sys.argv)

    cliThread = CLIThread(app)
    cliThread.start()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
