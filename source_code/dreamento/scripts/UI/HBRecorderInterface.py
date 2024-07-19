import json

from source_code.dreamento.scripts.RecorderThread import RecordThread
from source_code.dreamento.scripts.UI.EEGPlotWindow import EEGPlotWindow
from source_code.dreamento.scripts.UI.utility_functions import threaded
from source_code.dreamento.scripts.ZmaxHeadband import ZmaxHeadband


class HBRecorderInterface:
    def __init__(self):
        self.hb = None
        self.sample_rate = 256
        self.recordingThread = None

        self.isRecording = False
        self.firstRecording = True

        self.stimulationDataBase = {}  # have info of all triggered stimulations
        self.scoring_predictions = []

        self.epochCounter = 0

        self.eegPlot = None

    def connectToSoftware(self):
        self.hb = ZmaxHeadband()
        if self.hb.readSocket is None or self.hb.writeSocket is None:  # HDServer is not running
            print('Sockets can not be initialized.')
        else:
            print('Connected')

    def startRecording(self):
        if self.isRecording:
            return

        self.recordingThread = RecordThread()

        if self.firstRecording:
            # TODO: init sleep scoring model here

            self.firstRecording = False

        self.recordingThread.start()

        self.isRecording = True

        self.recordingThread.finished.connect(self.onRecordingFinished)
        self.recordingThread.recordingFinishedSignal.connect(self.onRecordingFinishedWriteStimulationDB)
        self.recordingThread.sendEEGdata2MainWindow.connect(
            self.getEEG_from_thread)  # sending data for plotting, scoring, etc.

        print('recording started')

    def stopRecording(self):
        if not self.isRecording:
            return

        self.recordingThread.stop()
        self.isRecording = False
        print('recording stopped')

    def onRecordingFinished(self):
        # when the recording is finished, this function is called
        self.isRecording = False
        print('recording finished')

    def onRecordingFinishedWriteStimulationDB(self, fileName):
        # save triggered stimulation information on disk:
        with open(f'{fileName}-markers.json', 'w') as fp:
            json.dump(self.stimulationDataBase, fp, indent=4, separators=(',', ': '))

        with open(f"{fileName}-predictions.txt", "a") as outfile:
            if self.scoring_predictions:
                # stagesList = ['W', 'N1', 'N2', 'N3', 'REM', 'MOVE', 'UNK']
                self.scoring_predictions.insert(0, -1)  # first epoch is not predicted, therefore put -1 instead
                outfile.write("\n".join(str(item) for item in self.scoring_predictions))

    def getEEG_from_thread(self, eegSignal_r, eegSignal_l,
                           plot_EEG=False, plot_periodogram=False,
                           plot_spectrogram=False, sleep_scoring=True,
                           epoch_counter=0):

        self.epochCounter = epoch_counter
        if plot_EEG:
            sigR = eegSignal_r
            sigL = eegSignal_l
            t = [number / self.sample_rate for number in range(len(eegSignal_r))]
            self.eegPlot.setData(t, sigR, sigL)

    @threaded
    def show_eeg_signal(self):
        if self.eegPlot:
            self.eegPlot.stop()
            self.eegPlot = None
        else:
            self.eegPlot = True
            self.eegPlot = EEGPlotWindow(self.sample_rate)
            self.eegPlot.show()
