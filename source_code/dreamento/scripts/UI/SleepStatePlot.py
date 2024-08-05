import sys
import threading

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit


class SleepStateWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stagesList = ['W', 'N1', 'N2', 'N3', 'REM', 'MOVE', 'UNK']
        self.stagesListColor = ['SlateBlue', 'MediumSeaGreen', 'DodgerBlue', 'Violet', 'Tomato', 'Gray', 'LightGray']

        self.setWindowTitle('Sleep State Prediction')

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        self.textWidget = QPlainTextEdit()
        self.layout.addWidget(self.textWidget)

    def update_text(self, state: str):
        self.textWidget.setPlainText(state)


class SleepStateThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.app = None
        self.window = None

    def run(self):
        self.app = QApplication(sys.argv)

        self.window = SleepStateWindow()
        self.window.show()

        sys.exit(self.app.exec_())

    def update_text(self, state: str):
        if self.window:
            self.window.update_text(state)

    def stop(self):
        if self.app:
            self.app.quit()


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

