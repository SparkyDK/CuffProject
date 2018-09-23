from app.System.states.State import State
from app.constants.CONSTANTS import refresh_period
import time

class LOAD_RESERVOIR(State):
    def __init__(self, FSM):
        super(LOAD_RESERVOIR, self).__init__(FSM)

    def Enter(self):
        # Close the cuff and reservoir relays (keep them closed) and open the tank relay
        # S1 Open, S2 Open, S3 Closed
        pass

    def Execute(self, args):
        self.args = args
        print ("\n*LOAD_RESERVOIR \twith self.args:", self.args, " and args:", args)
        if (self.args['PAIN'] == 1):
            if (int(self.args['PRESSURE']) < self.args['PAINL']):
                # Still on track to add pain pressure
                print ("Going to add more air with P=", self.args['PRESSURE'])
                print ("Plow=", self.args['PAINL'], " and Pup=", self.args['PAINH'])
                print ("at time: ", time.asctime(time.localtime(time.time())))
                self.FSM.ToTransition("toCONNECT_CUFF")
            elif (self.args['PRESSURE'] >= self.args['PAINL'] and self.args['PRESSURE'] <= self.args['PAINH']):
                print ("Pain pressure looks right, so we are done with P=", self.args['PRESSURE'])
                self.FSM.set_SYNC()
                self.FSM.ToTransition("toIDLE")
            else:
                # Pressure is above the min and max pain thresholds
                print ("Not sure how we got here with P=", self.args['PRESSURE'])
                print ("but pain pressure is too high")
                if (self.args['PRESSURE'] > self.args['PMAX']):
                    print ("Emergency venting P=", self.args['PRESSURE'])
                    self.FSM.ToTransition("toVENT")
                else:
                    print ("Controlled venting P=", self.args['PRESSURE'], "Plow=", self.args['PAINL'])
                    print (" and Pup=", self.args['PAINH'])
                    self.FSM.ToTransition("toRELEASE")
        else:
            # We should usually never get here, without requiring pain.  This shouldn't happen; get out safely, venting
            print ("This usually doesn't happen with P=", self.args['PRESSURE'])
            print (" and Pain=", self.args['PAIN'])
            self.FSM.ToTransition("toISOLATE_VENT")

    def Exit(self):
        # May need to sleep here for a bit longer, depending on how long the relay opening and air transfer takes
        # close all of the relays
        # S1 Closed, S2 Closed, S3 Closed

        time.sleep(9.0*refresh_period/10.0)  # Give the relays and solenoids time to actually close
        # need to determine this value, by experiment, but they are specified as having a response time less than 20ms
        print("Exiting Load Reservoir")
