import unittest
from app.filereaders.PressureReader import PressureReader
import os

class PressureTestReaderCase(unittest.TestCase):
    def test_canReadPressureFile(self):
        actions = PressureReader().read("./tests/test_files/TEST_Pressure_Values.txt")
        self.assertEqual([['PMAX', '970'], ['PAINH', '920'], ['PAINL', '900'], ['PATM', '750']], actions)
if __name__ == '__main__':
    unittest.main()
