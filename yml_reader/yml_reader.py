
import os
import sys
import yaml


class YmlReader:
    def __init__(self, file):
        self._file = file

    def read(self):
        if not os.path.isfile(self._file):
            print("file: " + self._file + " not found!")
            sys.exit()

        with open(self._file) as file_:
            return yaml.safe_load(file_)
