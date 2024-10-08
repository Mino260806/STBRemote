import shlex
import subprocess


class ProcessController:
    def __init__(self):
        self.ran_process = None

    def run(self, command):
        self.close_old_process()
        self.ran_process = subprocess.Popen(shlex.split(command), start_new_session=True)

    def close_old_process(self):
        if self.ran_process is None:
            return

        self.ran_process.terminate()
        self.ran_process = None
