import sys

from PyQt5.QtWidgets import QApplication
from scripts.UI.CLI import CLIThread

from scripts.Connection.HBRecorderInterface import HBRecorderInterface


class CommunicationLogic:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.cliThread = CLIThread()
        self.hbif = HBRecorderInterface()

    def start(self):
        self.cliThread.start()

        self._connectSignals()

        self.app.exec_()

    def _connectSignals(self):
        # CLI
        self.cliThread.cli.connect_signal.connect(self.connectHeadband)
        self.cliThread.cli.start_signal.connect(self.startRecording)
        self.cliThread.cli.stop_signal.connect(self.stopRecording)
        self.cliThread.cli.show_eeg_signal.connect(self.showEEG)
        self.cliThread.cli.start_scoring_signal.connect(self.startScoring)
        self.cliThread.cli.stop_scoring_signal.connect(self.stopScoring)
        self.cliThread.cli.start_webhook_signal.connect(self.startWebhook)
        self.cliThread.cli.stop_webhook_signal.connect(self.stopWebhook)
        self.cliThread.cli.set_signaltype_signal.connect(self.setSignaltype)
        self.cliThread.cli.quit_signal.connect(self.quit)

    def connectHeadband(self, _: bool):
        self.hbif.connect_to_software()

    def startRecording(self):
        if self.hbif.isConnected:
            self.hbif.start_recording()
        else:
            print('Not connected! call "connect" first.')

    def stopRecording(self):
        self.hbif.stop_recording()

    def showEEG(self):
        self.hbif.show_eeg_signal()

    def startScoring(self):
        self.hbif.start_scoring()

    def stopScoring(self):
        self.hbif.stop_scoring()

    def startWebhook(self):
        self.hbif.start_webhook()

    def stopWebhook(self):
        self.hbif.stop_webhook()

    def setSignaltype(self, signalTypes: list):
        self.hbif.set_signaltype(signalTypes)

    def quit(self, _: bool):
        self.hbif.quit()

        self.cliThread.stop()
        self.cliThread.quit()

        self.app.quit()






