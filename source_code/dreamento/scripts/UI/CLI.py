import cmd
from PyQt5.QtCore import QObject, pyqtSignal, QThread


class CLIThread(QThread):
    def __init__(self):
        super().__init__()
        self.cli = SleepRecorderCLI()

    def run(self):
        self.cli.cmdloop()

    def stop(self):
        self.cli.stop()
        self.quit()


class SleepRecorderCLI(cmd.Cmd, QObject):
    prompt = '>> '
    intro = 'Welcome to the sleep recoder CLI. type "help" for available commands.'

    connect_signal = pyqtSignal(bool)
    start_signal = pyqtSignal(bool)
    stop_signal = pyqtSignal(bool)
    show_eeg_signal = pyqtSignal(bool)
    start_scoring_signal = pyqtSignal(bool)
    stop_scoring_signal = pyqtSignal(bool)
    start_webhook_signal = pyqtSignal(bool)
    stop_webhook_signal = pyqtSignal(bool)
    set_signaltype_signal = pyqtSignal(list)
    quit_signal = pyqtSignal(bool)

    def __init__(self):
        cmd.Cmd.__init__(self)
        QObject.__init__(self)  # Initialize QObject

        self._is_running = True

    def stop(self):
        self._is_running = False
        return True

    def do_quit(self, line):
        """Exit the CLI."""
        self.quit_signal.emit(True)

    def do_connect(self, line):
        """Connect the recorder"""
        self.connect_signal.emit(True)

    def do_start(self, line):
        """Start the recoring"""
        self.start_signal.emit(True)

    def do_stop(self, line):
        """Stop the recording"""
        self.stop_signal.emit(True)

    def do_show_signal(self, line):
        """Shoe the eeg signal. This is a experimental feature, known to have bugs and preventing the application from
        terminating. It should not interfere with recording, but resize and move the window carefully and slowly. It
        crashes the whole application sometimes."""
        self.show_eeg_signal.emit(True)

    def do_start_scoring(self, line):
        """start scoring the eeg signal using the specified model"""
        self.start_scoring_signal.emit(True)

    def do_stop_scoring(self, line):
        """stops scoring the eeg signal"""
        self.stop_scoring_signal.emit(True)

    def do_start_webhook(self, line):
        """start the webhook so other programs can read the prediction status from the port 5000. This recorder sends the data there every 30 seconds."""
        self.start_webhook_signal.emit(True)

    def do_stop_webhook(self, line):
        """stop the webhook"""
        self.stop_webhook_signal.emit(True)
        #self.headbandinterface.stop_webhook()

    def do_set_signaltype(self, line):
        """set the signals that should be recorded. pass as a comma separated numbers. For possible signals type 'show_possible_signals'"""
        numbers = line.split(',')
        try:
            numbers = [int(n) for n in numbers]
            self.set_signaltype_signal.emit(numbers)
            print('the recording has to be restarted for this change to have an effect!')
        except Exception:
            print('pass signals as integers according to "show_possible_signals", e.g. " set_signaltype 1,2,3"')

    def do_show_possible_signals(self, line):
        """shows all possible eeg signals to be set by 'set_signaltype'."""
        mes = '[0=eegr, 1=eegl, 2=dx, 3=dy, 4=dz, 5=bodytemp, 6=bat, 7=noise, 8=light, 9=nasal_l, 10=nasal_r, 11=oxy_ir_ac, 12=oxy_r_ac, 13=oxy_dark_ac, 14=oxy_ir_dc, 15=oxy_r_dc, 16=oxy_dark_dc]'
        print(mes)
