from app.constants.CONSTANTS import MAX_NUM_SCHEDULES
import unittest
from app.filereaders.ScheduleReader import ScheduleReader
import_schedule = [[0.0, 0.0] * MAX_NUM_SCHEDULES]

import os

class ScheduleReaderTest(unittest.TestCase):
    def test_canReadScheduleFile(self):
        print ("Here is the input:", import_schedule)
        import_schedule = ScheduleReader().read(filename="./tests/input_files/Schedule.txt", file_schedule=import_schedule )
        print (import_schedule)
