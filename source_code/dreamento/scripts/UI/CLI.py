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

