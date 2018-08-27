import unittest
from app.filereaders.ScheduleReader import ScheduleReader
from app.main.main import time_schedule
import os

class ScheduleReaderTest(unittest.TestCase):
    def test_canReadScheduleFile(self):
        schedule = ScheduleReader().read(time_schedule, filename="./tests/input_files/Schedule.txt")
