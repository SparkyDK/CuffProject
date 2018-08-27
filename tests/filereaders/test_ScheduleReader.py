from app.constants.CONSTANTS import MAX_NUM_SCHEDULES
import unittest
from app.filereaders.ScheduleReader import ScheduleReader

import os

class ScheduleReaderTest(unittest.TestCase):
    def test_canReadScheduleFile(self):
        import_schedule = []
        for i in range(0, MAX_NUM_SCHEDULES): import_schedule.append([])
        #print("TEST2:", import_schedule)
        #print ("Here is the input:", import_schedule)
        import_schedule = ScheduleReader().read(filename="./tests/input_files/Schedule.txt", file_schedule=import_schedule )
        print ("Test reader read:", import_schedule)
        self.assertEqual('PAINTOLERANCE': 10, 'PAINVALUE': 910, 'PATM': 750, 'PMAX': 970}, import_schedule)

