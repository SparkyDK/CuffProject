from app.System.states.State import State
import time

class CONNECT_CUFF(State):
    def __init__(self, FSM):
        super(CONNECT_CUFF, self).__init__(FSM)

    def Enter(self):
        # Open the relay to the cuff and close the others
        # S1 Closed, S2 Open, S3 Closed
        pass

    def Execute(self, args):
        self.args = args
        print ("\n* CONNECT_CUFF * \twith args:", self.args)
        if (self.args['PAIN'] == 1):
            if (self.args['PRESSURE'] < self.args['PAINL']):
                # Need to add air
                print ("Still need to add more air with P=", self.args['PRESSURE'])
                print ("Plow=", self.args['PAINL'], " and Pup=", self.args['PAINH'])
                self.FSM.ToTransition("toLOAD_RESERVOIR")
            elif (self.args['PRESSURE'] >= self.args['PAINL'] and self.args['PRESSURE'] <= self.args['PAINH']):
                # In the zone
                print ("In the zone with P=", self.args['PRESSURE'])
                self.FSM.ToTransition("toIDLE")
            elif (self.args['PRESSURE'] >= self.args['PAINL'] and self.args['PRESSURE'] > self.args['PAINH']):
                # Overshot the maximum pain pressure value
                print ("Overshot pressure maximum with P=", self.args['PRESSURE'])
                print ("Plow=", self.args['PAINL'], " and Pup=", self.args['PAINH'])
                self.FSM.ToTransition("toRELEASE")
            else:
                print("Error!  Something strange going on with the pressure thresholds")
                print("Current Pressure=", self.args['PRESSURE'])
                print(" and Plow=", self.args['PAINL'], " and Pup=", self.args['PAINH'])
        else:
            # No pain required
            self.FSM.ToTransition("toVENT")

    def Exit(self):
        # May need to sleep here for a bit depending on how long the relay opening and air transfer takes
        # sleep (0.1)
        # S1 Closed, S2 Closed, S3 Closed
        pass
        time.sleep(0.1)  # Give the relays time to close

        print("Exiting Connect Cuff")
