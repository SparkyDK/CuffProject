import unittest
from app.filereaders.ScheduleReader2 import ScheduleReader2


class ScheduleReaderTestCase(unittest.TestCase):
    def test_canReadPressureFile(self):
        actions = ScheduleReader2().read("./tests/test_files/TEST_SCHEDULE_VALUES.txt")
        self.assertEqual([
            ['NILL', '361'],
            ['PAIN', '362'],
            ['NILL', '363'],
            ['PAIN', '364'],
            ['NILL', '365'],
            ['PAIN', '366'],
            ['NILL', '367'],
            ['PAIN', '368']], actions)


if __name__ == '__main__':
    unittest.main()
