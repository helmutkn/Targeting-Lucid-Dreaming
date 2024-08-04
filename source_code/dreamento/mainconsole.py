import sys
import time
from PyQt5 import QtCore

from source_code.dreamento.scripts.UI.CLI import SleepRecorderCLI
from source_code.dreamento.scripts.UI.HBRecorderInterface import HBRecorderInterface


def main():
    cli = SleepRecorderCLI()
    cli.cmdloop()

def test():
    hb = HBRecorderInterface()
    hb.connectToSoftware()
    hb.startRecording()
    time.sleep(5)
    hb.stopRecording()

if __name__ == '__main__':
    main() #  test()
