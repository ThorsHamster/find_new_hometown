
import os
import yaml


class YmlReader:
    def __init__(self, file):
        self._file = file

    def read(self) -> dict:
        if os.path.isfile(self._file):
            with open(self._file) as file_:
                return yaml.safe_load(file_)
        else:
            raise FileNotFoundError(f"file: {self._file} not found!")
