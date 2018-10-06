from app.System.states.State import State
from app.constants.CONSTANTS import refresh_period
from app.System.FSM.relay_control import set_relay
import time

class ISOLATE_VENT(State):
    def __init__(self, FSM):
        super(ISOLATE_VENT, self).__init__(FSM)

    def Enter(self):
        # May need to sleep here for a bit longer, depending on how long previous relay opening and air transfer takes
        # close all of the relays, especially the tank relay
        # S1 Closed, S2 Closed, S3 Closed
        set_relay(s1="closed", s2="closed", s3="closed")
        time.sleep(9.0*refresh_period/10.0)  # Give the relays time to close
        pass

    def Execute(self, args):
        self.args = args
        self.FSM.ToTransition("toVENT")

    def Exit(self):
        pass
        #print("Exiting ISOLATE_VENT")
