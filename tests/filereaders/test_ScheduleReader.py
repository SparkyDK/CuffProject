from app.constants.CONSTANTS import MAX_NUM_SCHEDULES
import unittest
from app.filereaders.ScheduleReader import ScheduleReader

import os

class ScheduleReaderTest(unittest.TestCase):
    def test_canReadScheduleFile(self):
        self.import_schedule = []
        for i in range(0, MAX_NUM_SCHEDULES): self.import_schedule.append([])
        #print("TEST2:", import_schedule)
        #print ("Here is the input:", import_schedule)
        self.import_schedule = ScheduleReader().read(filename="./tests/input_files/Schedule.txt", file_schedule=self.import_schedule )
        #print ("Test reader read:", self.import_schedule)
        self.assertEqual([['NILL', 361], ['PAIN', 362], ['NILL', 363], ['PAIN', 364], ['NILL', 365],
                          ['PAIN', 366], ['NILL', 367], ['PAIN', 368]], self.import_schedule)

