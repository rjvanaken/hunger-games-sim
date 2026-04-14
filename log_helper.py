MAX_LINES = 800000
TRIM_THRESHOLD = 900000

"""
log_helper.py - Defines the TrimmedFile class, which assists in writing training results to a 
file, trimming from the top when it exceeds a size threshold.
"""


class TrimmedFile:
    """
    Wraps a file for writing training logs. Automatically trims the file 
    back to MAX_LINES when it exceeds TRIM_THRESHOLD lines, preventing 
    runaway log sizes during long training runs.
    """
    def __init__(self, path):
        self.path = path
        self._count = 0
        self._file = None

    def __enter__(self):
        self._file = open(self.path, "w")
        self._count = 0
        return self

    def write(self, msg):
        self._file.write(msg)
        self._count += msg.count("\n")
        if self._count >= TRIM_THRESHOLD:
            self._trim()

    def flush(self):
        self._file.flush()

    def _trim(self):
        self._file.flush()
        with open(self.path, "r") as f:
            lines = f.readlines()
        lines = lines[-MAX_LINES:]
        self._file.seek(0)
        self._file.truncate()
        self._file.writelines(lines)
        self._count = len(lines)

    def __exit__(self, *args):
        self._file.close()