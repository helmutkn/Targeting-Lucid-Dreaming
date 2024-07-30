import cmd

from source_code.dreamento.scripts.UI.HBRecorderInterface import HBRecorderInterface


class SleepRecorderCLI(cmd.Cmd):
    prompt = '>> '
    intro = 'Welcome to the sleep recoder CLI. type "help" for available commands.'

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.headbandinterface = HBRecorderInterface()

    def do_hello(self, line):
        """Print a greeting."""
        print("Hello, World!")

    def do_quit(self, line):
        """Exit the CLI."""
        self.headbandinterface.quit()
        return True

    def do_connect(self, line):
        """Connect the recorder"""
        self.headbandinterface.connectToSoftware()

    def do_start(self, line):
        """Start the recoring"""
        self.headbandinterface.startRecording()

    def do_stop(self, line):
        """Stop the recording"""
        self.headbandinterface.stopRecording()

    def do_show_signal(self, line):
        """Shoe the eeg signal"""
        try:
            self.headbandinterface.show_eeg_signal()
        except Exception as e:
            print(e)

    def do_start_scoring(self, line):
        """start scoring the eeg signal using the specified model"""
        self.headbandinterface.start_scoring()

    def do_show_scoring(self, line):
        """visualize the predictions of the scoring model"""
        self.headbandinterface.show_scoring_predictions()

    def do_start_webhook(self, line):
        """start the webhook so other programs can red the prediction status from the port 5000"""
        self.headbandinterface.start_webhook()

    def do_stop_webhook(self, line):
        """stop the webhook"""
        self.headbandinterface.stop_webhook()

    def do_set_signaltype(self, line):
        """set the signals that should be recorded. pass as a comma separated numbers. For possible signals type 'show_possible_signals'"""
        numbers = line.split(',')
        try:
            numbers = [int(n) for n in numbers]
            self.headbandinterface.set_signaltype(numbers)
            print('the server has to be restarted for this change to have an effect!')
        except Exception:
            print('pass signals as integers according to "show_possible_signals", e.g. " set_signaltype 1,2,3"')

    def do_show_possible_signals(self, line):
        mes = '[0=eegr, 1=eegl, 2=dx, 3=dy, 4=dz, 5=bodytemp, 6=bat, 7=noise, 8=light, 9=nasal_l, 10=nasal_r, 11=oxy_ir_ac, 12=oxy_r_ac, 13=oxy_dark_ac, 14=oxy_ir_dc, 15=oxy_r_dc, 16=oxy_dark_dc]'
        print(mes)

