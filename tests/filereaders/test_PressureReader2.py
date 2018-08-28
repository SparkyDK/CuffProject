import unittest
from app.filereaders.PressureReader2 import *
import os

class PressureTestReaderCase(unittest.TestCase):
    def test_canReadPressureFile(self):
        actions = read_config("./tests/test_files/TEST_Pressure_Config.ini")
        self.assertEqual({'pmax': '970', 'painvalue': '910', 'paintolerance': '10', 'patm': '750'}, actions)
