import unittest
from app.filereaders.PressureReader import PressureReader
import os

class PressureTestReaderCase(unittest.TestCase):
    def test_canReadPressureFile(self):
        actions = PressureReader().read("./tests/test_files/TEST_Pressure_Values.txt")
        self.assertEqual({'PAINVALUE': '910', 'PAINTOLERANCE': '10', 'PATM': '750', 'PMAX': '970'}, actions)
if __name__ == '__main__':
    unittest.main()
