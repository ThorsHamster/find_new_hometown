
import os
import sys
import yaml


class YmlReader:
    def __init__(self, file):
        self._file = file

    def read(self):
        if os.path.isfile(self._file):
            with open(self._file) as file_:
                return yaml.safe_load(file_)
        else:
            print("file: " + self._file + " not found!")
            sys.exit()
