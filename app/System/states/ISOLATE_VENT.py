from app.System.states.State import State
import time

class ISOLATE_VENT(State):
    def __init__(self, FSM):
        super(ISOLATE_VENT, self).__init__(FSM)

    def Enter(self):
        # May need to sleep here for a bit longer, depending on how long previous relay opening and air transfer takes
        # close all of the relays, especially the tank relay
        # S1 Closed, S2 Closed, S3 Closed

        time.sleep(0.1)  # Give the relays time to close
        pass

    def Execute(self, args):
        self.args = args
        self.FSM.ToTransition("toVENT")

    def Exit(self):
        print("Exiting ISOLATE_VENT")
