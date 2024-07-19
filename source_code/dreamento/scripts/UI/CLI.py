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
        self.headbandinterface.show_eeg_signal()

