from app.System.states.State import State
from app.System.FSM.relay_control import set_relay
from app.constants.CONSTANTS import ATM_TOLERANCE
from app.constants.CONSTANTS import pressure_settling_time

import time

class VENT(State):
    def __init__(self, FSM):
        super(VENT, self).__init__(FSM)

    def Enter(self):
        # Open the relays to the cuff and from the reservoir, but keep the tank relay closed
        # S1 Closed, S2 Open, S3 Open
        set_relay(s1="closed", s2="open", s3="open")
        time.sleep(pressure_settling_time) # Allow air to come to rest before allowing execution to go on

        #print ("Entering VENT state")

    def Execute(self, args):
        self.args = args
        #if ( int(self.args['PRESSURE']) > (int(self.args['PATM'])+ ATM_TOLERANCE) ):
        if ( int(self.args['PRESSURE']) > (int(self.args['PATM'] + ATM_TOLERANCE)) ):
            pass
            #set_relay(s1="closed", s2="open", s3="open")
            # Stay in the VENT state
            #print("Stay in vent because pressure=", self.args['PRESSURE'],\
            #      " is greater than atmospheric pressure", self.args['PATM'], "+ tolerance=", ATM_TOLERANCE)
        else:
            self.FSM.set_SYNC()
            self.FSM.ToTransition("toIDLE")

    def Exit(self):
        #print ("Venting complete with pressure ", self.args['PRESSURE'])
        set_relay(s1="closed", s2="open", s3="open")
        #pass
