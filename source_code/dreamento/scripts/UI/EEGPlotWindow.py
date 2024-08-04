import sys
import threading
import time

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import numpy as np

import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal, QObject
import pyqtgraph as pg
import numpy as np


class PlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle('Plotting Example')
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget and set the layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create a PlotWidget and add it to the layout
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)

        # Create an empty plot
        self.plot = self.plot_widget.plot()

    def update_plot(self, x, y):
        """Update the plot with new data."""
        self.plot.setData(x, y)


class GuiThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.app = None
        self.window = None

    def run(self):
        # Create the application instance
        self.app = QApplication(sys.argv)

        # Create and show the main window
        self.window = PlotWindow()
        self.window.show()

        # Execute the application
        sys.exit(self.app.exec_())

    def update_plot(self, x, y):
        print('update_plot called')
        if self.window:
            self.window.update_plot(x, y)


if __name__ == '__main__':
    # Create the GUI thread
    gui_thread = GuiThread()

    # Start the GUI thread
    gui_thread.start()

    time.sleep(2)
    # Example data to update the plot with
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    gui_thread.update_plot(x, y)
    time.sleep(3)

    # Run the CLI loop
    #cli_loop(gui_thread)

    # Ensure the GUI thread is properly cleaned up on exit
    gui_thread.app.quit()
    gui_thread.join()





class EEGPlotWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        self.sample_rate = 256
        self.desiredXrange = 60

        QWidget.__init__(self, parent)
        self.setFixedSize(1000, 500)

        self.plotWidget = pg.PlotWidget()

        self.EEGLinePen1 = pg.mkPen(color=(100, 90, 150), width=1.5)
        self.EEGLinePen2 = pg.mkPen(color=(90, 170, 160), width=1.5)

        t = [number / self.sample_rate for number in range(self.sample_rate * 30)]

        self.eegLine1 = self.plotWidget.plot(t, np.random.randn(30 * self.sample_rate), self.EEGLinePen1)
        self.eegLine2 = self.plotWidget.plot(t, np.random.randn(30 * self.sample_rate), self.EEGLinePen2)

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.addWidget(QtWidgets.QLabel("EEG"))
        self.mainLayout.addWidget(self.plotWidget)

        self.setLayout(self.mainLayout)
        #self.show()

    def setData(self, t, sigR, sigL):
        self.eegLine1.setData(t, sigR, pen=self.EEGLinePen1)
        self.eegLine2.setData(t, sigL, pen=self.EEGLinePen2)

        self.displayedXrangeCounter = len(sigL)  # for plotting Xrange — number of displayed samples on screen

        sec = int(np.floor(self.displayedXrangeCounter / self.sample_rate))
        if sec % self.desiredXrange == 0:
            random_reset_timer_variable = 30
            k = int(np.floor(sec / self.desiredXrange))
            if self.desiredXrange * k < random_reset_timer_variable:
                xMin = self.desiredXrange * k
                xMax = self.desiredXrange * (k + 1)
            else:
                xMin = 0
                xMax = self.desiredXrange
            a_X = self.plotWidget.getAxis('bottom')
            ticks = range(xMin, xMax, 1)
            a_X.setTicks([[(v, str(v)) for v in ticks]])
            self.plotWidget.setXRange(xMin, xMax, padding=0)

    def present(self):
        self.show()

    def remove(self):
        self.hide()

class EEGPlotWindow:
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
        self.desiredXrange = 5  # set default (0,5) - (5,10) - (10-15) - ...
        self.desiredYrange = 60  # set default (-60,60)

        self.app = QApplication(sys.argv)

        self.plotWidget = pg.PlotWidget(background=[255, 255, 255])

        self.EEGLinePen1 = pg.mkPen(color=(100, 90, 150), width=1.5)
        self.EEGLinePen2 = pg.mkPen(color=(90, 170, 160), width=1.5)

        t = [number / self.sample_rate for number in range(self.sample_rate * 30)]

        self.eegLine1 = self.plotWidget.plot(t, np.random.randn(30 * self.sample_rate), self.EEGLinePen1)
        self.eegLine2 = self.plotWidget.plot(t, np.random.randn(30 * self.sample_rate), self.EEGLinePen2)

    def show(self):
        self.plotWidget.show()
        self.app.exec_()

    def stop(self):
        self.app.quit()
        self.app.exit(0)

    def setData(self, t, sigR, sigL):
        self.eegLine1.setData(t, sigR, pen=self.EEGLinePen1)
        self.eegLine2.setData(t, sigL, pen=self.EEGLinePen2)

        self.displayedXrangeCounter = len(sigL)  # for plotting Xrange — number of displayed samples on screen

        sec = int(np.floor(self.displayedXrangeCounter / self.sample_rate))
        if sec % self.desiredXrange == 0:
            random_reset_timer_variable = 30
            k = int(np.floor(sec / self.desiredXrange))
            if self.desiredXrange * k < random_reset_timer_variable:
                xMin = self.desiredXrange * k
                xMax = self.desiredXrange * (k + 1)
            else:
                xMin = 0
                xMax = self.desiredXrange
            a_X = self.plotWidget.getAxis('bottom')
            ticks = range(xMin, xMax, 1)
            a_X.setTicks([[(v, str(v)) for v in ticks]])
            self.plotWidget.setXRange(xMin, xMax, padding=0)
