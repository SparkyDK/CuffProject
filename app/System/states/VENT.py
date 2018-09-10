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
        if ( self.args['STARTED'] == 1 ):
            # Only print this message when running a schedule
            print ("* VENT * \t with args:", self.args)
        # while (self.P>Patm):
        if ( int(self.args['PRESSURE']) > int(self.args['PATM']) ):
            # Stay in the VENT state
            print("Still need to vent, since pressure is greater than atmospheric pressure")
        else:
            self.FSM.ToTransition("toIDLE")

    def Exit(self):
        # Does not hurt to take some time before leaving the vent state
        # This will give the air a chance to exit the tubing and also prevent relay wear and tear
        # at the end of a pain schedule, since this state is held in a forced way
        print ("Allowing some time for venting to take place")
        time.sleep(3)
        if ( self.args['STARTED'] == 1 or True==True):
            # Only print this message when running a schedule
            print("Exiting Vent")
