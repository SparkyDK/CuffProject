from app.System.states.State import State
import time

class RELEASE(State):
    def __init__(self, FSM):
        super(RELEASE, self).__init__(FSM)

    def Enter(self):
        # Close the relays to the tank and for the reservoir vent, but open the cuff relay
        pass

    def Execute(self, args):
        self.args = args
        print ("\n* RELEASE * \t with args:", self.args)
        if (self.args['PAIN'] == 1):
            if (self.args['PRESSURE'] < self.args['PAINL']):
                # Need to top up pressure again
                self.FSM.ToTransition("toLOAD_RESERVOIR")
            elif (self.args['PRESSURE'] > self.args['PAINL'] and self.args['PRESSURE'] < self.args['PAINH']):
                # Pressure in the zone
                self.FSM.ToTransition("toIDLE")
            else:
                # Pressure is greater than Plow, but not in the zone, so it is too high
                self.FSM.ToTransition("toCONNECT_CUFF")
        else:
            # Should not be here, since no pain is required so vent and go back to IDLE
            self.FSM.ToTransition("toVENT")

    def Exit(self):
        # May need to sleep here for a bit depending on how long the relay opening and air transfer takes
        # sleep (0.1)
        # close all of the relays

        time.sleep(0.1)  # Give the relays time to close
        print("Exiting Vent")
