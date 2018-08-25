import unittest
from app.filereaders.ScheduleReader import ScheduleReader
import os

class ScheduleReaderTest(unittest.TestCase):
    def test_canReadScheduleFile(selfs):
        schedule = ScheduleReader.read("./tests/test_files/TEST_SCHEDULE_VALES.txt")
