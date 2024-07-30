import os
from datetime import datetime  # for saving files with exact time
import time
from PyQt5.QtCore import QThread, pyqtSignal
from pathlib import Path
import numpy as np

from source_code.dreamento.scripts.ServerConnection.ZmaxHeadband import ZmaxDataID, ZmaxHeadband


class RecordThread(QThread):
    recordingProgessSignal = pyqtSignal(
        int)  # a sending signal to mainWindow - sends time info of ongoing recording to mainWindow
    recordingFinishedSignal = pyqtSignal(
        str)  # a sending signal to mainWindow - sends name of stored file to mainWindow
    epochPredictionResultSignal = pyqtSignal(int, int)
    sendEEGdata2MainWindow = pyqtSignal(object, object, bool, bool, bool, bool, int)
    sendData2MainWindow = pyqtSignal(object, object)

    def __init__(self, parent=None, signalType: list = [0, 1, 5, 2, 3, 4]):
        super(RecordThread, self).__init__(parent)
        self.model_CNNLSTM = None
        self.threadactive = True
        self.signalType = signalType  # "EEGR, EEGL, TEMP, DX, DY, DZ"
        self.stimulationType = ""
        self.secondCounter = 0
        self.dataSampleCounter = 0
        self.totalDataSampleCounter = 0
        self.epochCounter = 0
        self.samples_db = []
        self.sample_rate = 256

    def getSignalTypeFromUI(self, sig_type):
        # to know which signals to record, based on user interface's choice in comboBox
        if sig_type == "EEGR":
            self.signalType = [ZmaxDataID.eegr.value]
        elif sig_type == "EEGL":
            self.signalType = [ZmaxDataID.eegl.value]
        elif sig_type == "TEMP":
            self.signalType = [ZmaxDataID.bodytemp.value]
        elif sig_type == "EEGR, EEGL":
            self.signalType = [ZmaxDataID.eegr.value, ZmaxDataID.eegl.value]
        elif sig_type == "DX, DY, DZ":
            self.signalType = [ZmaxDataID.dx.value, ZmaxDataID.dy.value, ZmaxDataID.dz.value]
        elif sig_type == "EEGR, EEGL, TEMP":
            self.signalType = [ZmaxDataID.eegr.value, ZmaxDataID.eegl.value, ZmaxDataID.bodytemp.value]
        elif sig_type == "EEGR, EEGL, TEMP, DX, DY, DZ":
            self.signalType = [ZmaxDataID.eegr.value, ZmaxDataID.eegl.value, ZmaxDataID.bodytemp.value, \
                               ZmaxDataID.dx.value, ZmaxDataID.dy.value, ZmaxDataID.dz.value]

    def getCurrentSampleInformation(self):
        return [self.dataSampleCounter, self.secondCounter,
                self.totalDataSampleCounter]  # returns time info of stimulation, when called

    def sendData2main(self, data=None, columns=None):
        self.sendData2MainWindow.emit(data, columns)

    def sendEEGdata2main(self,
                         eegSigR=None, eegSigL=None,
                         plot_EEG=False, plot_periodogram=False, plot_spectrogram=False,
                         score_sleep=False):
        self.sendEEGdata2MainWindow.emit(eegSigR, eegSigL, plot_EEG, plot_periodogram, plot_spectrogram,
                                         score_sleep, self.epochCounter)

    def run(self):
        # This part of the cord RECORDS signal.
        # In each second, also calculates the sampling rate (# of samples received by program over stream)
        recording = []
        cols = self.signalType
        cols.extend([999, 999])  # add two columns for sample number, sample time
        # cols = [ZmaxDataID.eegr.value, ZmaxDataID.eegl.value, ZmaxDataID.bodytemp.value, 999, 999]  # eegr, eegl, temp, sample number, sample time
        recording.append(cols)  # first row of received data is the col_id. eg: 0 => eegr
        hb = ZmaxHeadband()  # create a new client on the server, therefore we use it only for reading the stream

        now = datetime.now()  # for file name
        dt_string = now.strftime("recording-date-%Y-%m-%d-time-%H-%M-%S")
        file_path = f".\\recordings\\{dt_string}"
        file_name = f"{file_path}\\complete.txt"
        Path(f"{file_path}").mkdir(parents=True, exist_ok=True)  # ensures directory exists

        actual_start_time = time.time()
        print(f'actual start time {actual_start_time}')

        buffer2analyzeIsReady = False
        dataSamplesToAnalyzeCounter = 0  # count samples, when reach 30*256, feed all to deep learning model
        dataSamplesToAnalyzeBeginIndex = 0
        self.secondCounter = 0
        self.epochCounter = 0

        sigR_accumulative = []  # accumulate 256*30 data samples and empty it afterward
        sigL_accumulative = []

        while True:
            if self.epochCounter % 60 == 0 and dataSamplesToAnalyzeCounter == 0:
                del hb
                hb = ZmaxHeadband()
                #print("New HB created after 60 epochs")

            self.dataSampleCounter = 0  # count samples in each second
            self.secondCounter += 1
            self.recordingProgessSignal.emit(
                self.secondCounter)  # send second counter to the mainWindow (then show on button)

            t_end = time.time() + 1

            #print(f'{self.secondCounter} start')
            while time.time() < t_end:
                x = hb.read(cols[:-2])
                if x:
                    for line in x:
                        dataEntry = line
                        dataEntry.extend([self.dataSampleCounter, self.secondCounter])
                        self.dataSampleCounter += 1
                        self.totalDataSampleCounter += 1
                        recording.append(dataEntry)
                        if not buffer2analyzeIsReady:
                            if self.secondCounter >= 2:  # ignore 1st second for analysis, because it is unstable
                                dataSamplesToAnalyzeCounter += 1
                                if dataSamplesToAnalyzeCounter == 1:  # x[dataSamplesToAnalyzeIDXbegin:dataSamplesToAnalyzeIDXbegin+30*256]
                                    sigR_accumulative = []
                                    sigL_accumulative = []

                                if dataSamplesToAnalyzeCounter <= 30 * self.sample_rate:
                                    sigR_accumulative.append(line[ZmaxDataID.eegr.value])
                                    sigL_accumulative.append(line[ZmaxDataID.eegl.value])

                                    if dataSamplesToAnalyzeCounter % self.sample_rate/2 == 0:  # send EEG data for plotting to mainWindow
                                        self.sendEEGdata2main(eegSigR=sigR_accumulative, eegSigL=sigL_accumulative,
                                                              plot_EEG=True)

                                else:
                                    buffer2analyzeIsReady = True
                                    self.epochCounter += 1
                        self.sendData2main(dataEntry, cols)

                else:
                    sig = [1,2,3,4]
                    self.sendData2main(data=sig, columns=cols)
                    #print("[] data")
                    continue

            self.samples_db.append(self.dataSampleCounter)
            #print(f'{self.dataSampleCounter} samples')
            if buffer2analyzeIsReady:
                # send eeg data of last 30 seconds (30*256 samples) to mainWindow for plotting (spectrogram and periodogram) and sleep scoring
                self.sendEEGdata2main(eegSigR=sigR_accumulative, eegSigL=sigL_accumulative,
                                      plot_periodogram=True, plot_spectrogram=True, score_sleep=True)
                dataSamplesToAnalyzeCounter = 0
                buffer2analyzeIsReady = False

            if self.threadactive is False:
                break  # break the loop if record button is pressed again, recording stops

        actual_end_time = time.time()
        print(f'actual end time {actual_end_time}')
        time_diff = actual_end_time - actual_start_time
        minute = time_diff / 60
        seconds = time_diff % 60
        print(f"actual {minute} minute, {seconds} seconds")

        np.savetxt(file_name, recording, delimiter=',')  # save recording as txt
        print(f"Recording saved to {file_name}")
        np.save(os.path.join(file_path, 'samples_db.npy'), self.samples_db)

        self.recordingFinishedSignal.emit(f"{file_path}\\{dt_string}")  # send path of recorded file to mainWindow

    def stop(self):
        self.threadactive = False
        self.wait()
