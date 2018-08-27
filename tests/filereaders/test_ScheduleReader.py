import unittest
from app.filereaders.ScheduleReader import ScheduleReader

import os

class ScheduleReaderTest(unittest.TestCase):
    def test_canReadScheduleFile(self):
        schedule = ScheduleReader().read(time_schedule, pain_schedule, filename="./tests/input_files/Schedule.txt")
        print (schedule)
