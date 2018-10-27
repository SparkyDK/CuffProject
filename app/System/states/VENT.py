from app.System.states.State import State
from app.System.FSM.relay_control import set_relay
from app.constants.CONSTANTS import ATM_TOLERANCE_LOW
from app.constants.CONSTANTS import pressure_settling_time, venting_timeout

import time

class VENT(State):
    def __init__(self, FSM):
        super(VENT, self).__init__(FSM)
        self.start_time = time.time()

    def Enter(self):
        # Open the relays to the cuff and from the reservoir, but keep the tank relay closed
        # S1 Closed, S2 Open, S3 Open
        set_relay(s1="closed", s2="open", s3="open")
        time.sleep(pressure_settling_time) # Allow air to come to rest before allowing execution to go on
        self.start_time = time.time() # Record the time when we first enter the state, for timeout purposes
        #print ("Entering VENT state")

    def Execute(self, args):
        self.args = args
        #if ( int(self.args['PRESSURE']) > (int(self.args['PATM'])+ ATM_TOLERANCE_LOW) ):
        if ( int(self.args['PRESSURE']) > (int(self.args['PATM'] + ATM_TOLERANCE_LOW)) ):
            # pass
            # Time out covers the case when atmospheric pressure shifts downwards during program execution
            self.elapsed_time = time.time() - self.start_time
            if (self.elapsed_time > venting_timeout):
                print ("VENT: Timed out ...back to IDLE! Pressure never dropped below atmospheric pressure (P=",\
                       self.args['PRESSURE'], " and Patm=", self.args['PATM'], ") with tolerance=", ATM_TOLERANCE_LOW)
                self.FSM.set_SYNC()
                self.FSM.ToTransition("toIDLE")
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
