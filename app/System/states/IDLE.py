from app.System.states.State import State
import time

class IDLE(State):
    def __init__(self, FSM):
        super(IDLE, self).__init__(FSM)

    def Enter(self):
        # Close all of the relays

        # Don't sleep here, because in this state most of the time
        pass

    def Execute(self, args):
        # control_args = {'SCHEDULE_INDEX': 0, 'PAIN': 0, 'STARTED': 0, 'PAUSE': 0, 'FORCE': 0,
        #                'PAINH': painh, 'PAINL': painl, 'PRESSURE': 0,
        #                'PATM': pressure_parameters['PATM'], 'PMAX': pressure_parameters['PMAX']}
        self.args = args
        # print "\n* IDLE * \twith args=",  self.args
        if (self.args['PRESSURE'] == 1):
            if (self.Running == 1):
                # Running a schedule
                if (self.args['PRESSURE'] < self.args['PAINL']):
                    # Pressure not high enough
                    self.FSM.ToTransition("toLOAD_RESERVOIR")
            else:
                # This shouldn't happen (i.e. PAIN required but not in a schedule, so we should vent
                self.FSM.ToTransition("toVENT")
        else:
            # No pain required
            if (self.args['STARTED'] == 1):
                # No pain required in this schedule phase.
                if (self.args['PRESSURE'] > self.args['PATM']):
                    # Adjust relays to vent to keep P below Patm
                    self.FSM.ToTransition("toVENT")
                else:
                # Save solenoid wear and tear when idle by leaving them closed and staying in this state
                    pass
            else:
                # Don't let the user adjust the pain threshold if running a schedule.
                # Stay in IDLE, unless a new entry is being entered by the user or if pressure creeps above atmospheric
                pass
        if (self.args['PRESSURE'] > self.args['PATM']):
            # Keep pressure at atmospheric pressure anyway, even if not running a schedule
            self.FSM.ToTransition("toVENT")
        else:
            # Stay in IDLE
            pass


def Exit(self):
    # May need to sleep here for a bit depending on how long the relay opening and air transfer takes
    # sleep (0.1)
    # close all of the relays

    time.sleep(0.1)  # Give the relays time to close, although they usually will have had lots of time to do this
    print("Exiting Idle")
