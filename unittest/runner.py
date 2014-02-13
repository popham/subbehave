from unittest.runner import TextTestRunner

from .result import PyunitResult

class PyunitRunner(TextTestRunner):
    resultclass = PyunitResult
