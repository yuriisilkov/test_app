import logging
import os
from datetime import datetime


class MyLogs():

    def initial_logs(self, name="", level="DEBUG", path=None):
        # Init log name
        logger = logging.getLogger(name=name)

        # Init log level
        numeric_level = getattr(logging, level.upper(), None)
        logger.setLevel(numeric_level)

        # Init format logs
        _format = logging.Formatter("[%(asctime)s]%(levelname)s: %(message)s")

        # Init log file name and storage path
        if not path:
            root_path = os.path.dirname(os.path.realpath(__file__))
            logs_storage_directory = "/test_logs"
            path = f"{root_path}{logs_storage_directory}"
        log = os.path.join(path, "%s_%s.log" % (name, datetime.now().strftime('%Y-%m-%d_%H-%M')))

        # Init log file handler
        fh = logging.FileHandler(log, "w")
        fh.setFormatter(_format)
        logger.addHandler(fh)

        # Init log file to stdout
        ch = logging.StreamHandler()
        ch.setFormatter(_format)
        logger.addHandler(ch)

        return logger
