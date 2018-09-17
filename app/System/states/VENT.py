from app.System.states.State import State
import time

class VENT(State):
    def __init__(self, FSM):
        super(VENT, self).__init__(FSM)

    def Enter(self):
        # Open the relays to the cuff and from the reservoir, but keep the tank relay closed
        # S1 Closed, S2 Open, S3 Open
        pass

    def Execute(self, args):
        self.args = args
        if ( int(self.args['PRESSURE']) > int(self.args['PATM']) ):
            # Stay in the VENT state
            print("Still need to vent, since pressure is greater than atmospheric pressure")
        else:
            self.FSM.ToTransition("toIDLE")

    def Exit(self):
        pass
