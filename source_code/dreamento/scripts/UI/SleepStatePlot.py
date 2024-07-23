import sys

from PyQt5.QtWidgets import QApplication, QPlainTextEdit


class SleepStatePlot:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.plotWidget = QPlainTextEdit()
        self.plotWidget.setWindowTitle('Scoring Model Predictions')

        self.stagesList = ['W', 'N1', 'N2', 'N3', 'REM', 'MOVE', 'UNK']
        self.stagesListColor = ['SlateBlue', 'MediumSeaGreen', 'DodgerBlue', 'Violet', 'Tomato', 'Gray', 'LightGray']

        self.data = []

    def show(self):
        self.plotWidget.show()
        self.app.exec_()

    def stop(self):
        self.app.quit()
        self.app.exit(0)

    def setData(self, predResult, epochNum):
        self.plotWidget.appendHtml(
            f"<font style='color:{self.stagesListColor[predResult]};' size='4'>{epochNum:03}. {self.stagesList[predResult]}</font>")

