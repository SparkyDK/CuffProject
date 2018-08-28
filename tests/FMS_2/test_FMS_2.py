import unittest
from app.FSM_2.FSM_2 import PainAdministrator
from app.filereaders.ScheduleReader2 import ScheduleReader2
from app.filereaders.PressureReader2 import *


class FSM2_TESTCASE(unittest.TestCase):

    def test_start_experiment(self):
        schedule = ScheduleReader2().read("./tests/test_files/TEST_SCHEDULE_VALUES.txt")
        pressure_values = read_config("./tests/test_files/TEST_Pressure_Config.ini")
        pA = PainAdministrator(schedule, pressure_values)
        self.assertTrue(pA.is_IDLE())
        pA.start_experiment()

        # # pA.start_experiment()
        pA.idle_to_isolate_vent();
        # self.assertTrue(pA.is_IDLE())

if __name__ == '__main__':
    unittest.main()
