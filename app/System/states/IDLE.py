from app.System.states.State import State
from app.System.FSM.relay_control import set_relay
from app.constants.CONSTANTS import ATM_TOLERANCE

class IDLE(State):
    def __init__(self, FSM):
        super(IDLE, self).__init__(FSM)

    def Enter(self):
        # Close all of the relays
        # S1 Closed, S2 Closed, S3 Closed
        set_relay(s1="closed", s2="closed", s3="closed")
        # Don't sleep here, because execution is in this state most of the time
        pass

    def Execute(self, args):
        # control_args = {'SCHEDULE_INDEX': 0, 'PAIN': 0, 'STARTED': 0, 'PAUSE': 0,
        #                'PAINH': painh, 'PAINL': painl, 'PRESSURE': 0,
        #                'PATM': pressure_parameters['PATM'], 'PMAX': pressure_parameters['PMAX']}
        self.args = args
        # print "\n* IDLE * \twith args=",  self.args
        if (self.args['PAIN'] == 1):
            if (self.args['STARTED'] == 1):
                # Running a schedule with PAIN requested
                if (self.args['PRESSURE'] < self.args['PAINL']):
                    # Pressure not high enough
                    self.FSM.ToTransition("toLOAD_RESERVOIR")
                else:
                    # Air pressure is greater than the low pain threshold, which is acceptable...
                    # ... but, we need to make sure that we have not exceeded the high pressure thresholds
                    if (self.args['PRESSURE'] > self.args['PAINH']):
                        # pressure is too high, for some reason
                        if (self.args['PRESSURE'] > self.args['PMAX']):
                            # Pressure has exceeded the maximum value, so do an emergency vent
                            self.FSM.ToTransition("toVENT")
                        else:
                            # otherwise, allow for a more controlled release of air
                            self.FSM.ToTransition("toCONNECT_CUFF")
                    else:
                        self.FSM.set_SYNC()
                        pass    # No problem with pain air pressure ("in the zone")
            else:
                # This should not happen (i.e. pain required outside of a schedule, so vent
                print ("Error!  Something weird happened and pain was requested outside of a schedule... venting")
                self.FSM.ToTransition("toVENT")
        else:
            # No pain required
            if (self.args['PRESSURE'] > (self.args['PATM']+ATM_TOLERANCE) ):
                # Adjust relays to vent to keep P below Patm
                self.FSM.ToTransition("toVENT")
            else:
            # Save solenoid wear and tear when idle by leaving them closed and staying in this state
                pass
                self.FSM.set_SYNC()


def Exit(self):
    # may want to close all of the relays
    # May need to sleep here for a bit depending on how long the relay opening and air transfer takes
    # sleep (9.0*refresh_period/10.0)
    pass