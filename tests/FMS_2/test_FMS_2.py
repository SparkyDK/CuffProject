import unittest
from app.FSM_2.FSM_2 import PainAdministratorStateMachine, ExperimentDataModel
from app.filereaders.ScheduleReader import ScheduleReader
from app.filereaders.PressureReader import PressureReader

class FSM2_TESTCASE(unittest.TestCase):

    def test_normal_fsm_transitions(self):
        e = ExperimentDataModel(state="idle")
        fsm = PainAdministratorStateMachine(e)
        self.assertTrue(fsm.is_idle)

        fsm.start_test()
        self.assertTrue(fsm.is_pain)

        fsm.release_pain()
        self.assertTrue(fsm.nothing)

    def test_stop_everything(self):
        e = ExperimentDataModel(state="idle")
        fsm = PainAdministratorStateMachine(e)

        fsm.start_test()
        self.assertTrue(fsm.is_pain)

        fsm.stop_everything()
        self.assertTrue(fsm.is_stopped)

    def test_start_experiment(self):
        schedule = ScheduleReader.
        e = ExperimentDataModel(state="idle")
        fsm = PainAdministratorStateMachine(e)
        fsm.start_test()


if __name__ == '__main__':
    unittest.main()
