import json

import numpy as np

import realTimeAutoScoring
from source_code.dreamento.scripts.ServerConnection.RecorderThread import RecordThread
from source_code.dreamento.scripts.UI.EEGPlotWindow import EEGPlotWindow
from source_code.dreamento.scripts.UI.SleepStatePlot import SleepStatePlot
from source_code.dreamento.scripts.UI.utility_functions import threaded
from source_code.dreamento.scripts.ServerConnection.ZmaxHeadband import ZmaxHeadband


class HBRecorderInterface:
    def __init__(self):
        self.hb = None
        self.sample_rate = 256
        self.recordingThread = None

        self.isRecording = False
        self.firstRecording = True

        # stimulations
        self.stimulationDataBase = {}  # have info of all triggered stimulations

        # scoring
        self.sleepScoringModel = None
        self.scoring_predictions = []
        self.epochCounter = 0
        self.sleepScoringModelPath = None

        # visualization
        self.eegPlot = None
        self.scorePlot = None

        # program parameters
        self.plotEEG = False
        self.scoreSleep = False
        self.plotScore = False

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

    def setSleepScoringModel(self, path):
        self.sleepScoringModelPath = path

    def getEEG_from_thread(self, eegSignal_r, eegSignal_l, epoch_counter=0):

        self.epochCounter = epoch_counter
        if self.plotEEG:
            sigR = eegSignal_r
            sigL = eegSignal_l
            t = [number / self.sample_rate for number in range(len(eegSignal_r))]
            self.eegPlot.setData(t, sigR, sigL)

        if self.scoreSleep:
            if self.sleepScoringModel is None:
                self.sleepScoringModel = realTimeAutoScoring.importModel(self.sleepScoringModelPath)
            # 30 seconds, each 256 samples... send recording for last 30 seconds to model for prediction
            sigRef = np.asarray(eegSignal_r)
            sigReq = np.asarray(eegSignal_l)
            sigRef = sigRef.reshape((1, sigRef.shape[0]))
            sigReq = sigReq.reshape((1, sigReq.shape[0]))
            modelPrediction = realTimeAutoScoring.Predict_array(
                output_dir="./DataiBand/output/Fp1-Fp2_filtered",
                args_log_file="info_ch_extract.log", filtering_status=True,
                lowcut=0.3, highcut=30, fs=256, signal_req=sigReq, signal_ref=sigRef, model=self.sleepScoringModel)

            #self.displayEpochPredictionResult(int(modelPrediction[0]),
            #                                  int(self.epochCounter))  # display prediction result on mainWindow
            self.scoring_predictions.append(int(modelPrediction[0]))
            self.scorePlot.setData(int(modelPrediction[0]))

    @threaded
    def show_eeg_signal(self):
        print('still here')
        if self.plotEEG:
            self.eegPlot.stop()
            self.eegPlot = None
            self.plotEEG = False
        else:
            self.plotEEG = True
            self.eegPlot = EEGPlotWindow(self.sample_rate)
            self.eegPlot.show()
        print('still here')

    @threaded
    def show_scoring_predictions(self):
        if self.plotScore:
            self.scorePlot.stop()
            self.scorePlot = None
            self.plotScore = False
        else:
            self.plotScore = True
            self.scorePlot = SleepStatePlot()
            self.scorePlot.show()

    def start_scoring(self):
        self.scoreSleep = True

    def stop_scoring(self):
        self.scoreSleep = False

    def quit(self):
        self.eegPlot.stop()
        self.scorePlot.stop()






