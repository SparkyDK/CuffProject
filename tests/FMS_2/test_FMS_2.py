import unittest
from app.FSM_2.FSM_2 import PainAdministrator
from app.filereaders.ScheduleReader2 import ScheduleReader2
from app.filereaders.PressureReader import PressureReader


class FSM2_TESTCASE(unittest.TestCase):

    def test_start_experiment(self):
        schedule = ScheduleReader2().read("app/input_files/Schedule.txt")
        pressure_values = PressureReader().read("app/input_files/Pressure_Values.txt")
        pA = PainAdministrator(schedule, pressure_values)
        pA.start_experiment()
        self.assertTrue(pA.fsm.isolate_vent)

if __name__ == '__main__':
    unittest.main()
