from datetime import datetime


class Logging():
    def __init__(self, start_time, verbose):
        self.start_time = start_time
        self.verbose = verbose

    def log(self, message):
        if self.verbose:
            print(f"[{datetime.now() - self.start_time}] {message}")
