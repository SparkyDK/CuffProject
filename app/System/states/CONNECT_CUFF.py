from app.System.states.State import State
from app.constants.CONSTANTS import relay_settling_time
from app.System.FSM.relay_control import set_relay
import time

class CONNECT_CUFF(State):
    def __init__(self, FSM):
        super(CONNECT_CUFF, self).__init__(FSM)

    def Enter(self):
        # Open the relay to the cuff and close the others
        # S1 Closed, S2 Open, S3 Closed
        set_relay(s1="closed", s2="open", s3="closed")
        time.sleep(relay_settling_time)  # Give the relays time to close
        #time_locally = time.asctime(time.localtime(time.time()))
        #print (time_locally,": s1(air tank)=closed s2(cuff)=open s3(vent)=closed")
        #print ("CONNECT_CUFF entered")

    def Execute(self, args):
        self.args = args
        #print ("\n* CONNECT_CUFF * \twith args:", self.args)
        if (self.args['PAIN'] == 1):
            if (self.args['PRESSURE'] < self.args['PAINL']):
                # Need to add air
                #print ("Need to add more air P=", self.args['PRESSURE'],\
                #       "Plow=", self.args['PAINL'], " and Pup=", self.args['PAINH'])
                print ("+")
                self.FSM.ToTransition("toLOAD_RESERVOIR")
            elif (self.args['PRESSURE'] >= self.args['PAINL'] and self.args['PRESSURE'] <= self.args['PAINH']):
                # In the zone
                print ("In the zone with P=", self.args['PRESSURE'])
                print (".")
                self.FSM.set_SYNC()
                self.FSM.ToTransition("toIDLE")
            elif (self.args['PRESSURE'] >= self.args['PAINL'] and self.args['PRESSURE'] > self.args['PAINH'] \
                    and self.args['PRESSURE'] <= self.args['PMAX']):
                # Overshot the maximum pain pressure value but not all the way past the maximum tolerated value
                #print ("Overshot pressure maximum with P=", self.args['PRESSURE'])
                #print ("Plow=", self.args['PAINL'], " and Pup=", self.args['PAINH'])
                print ("-")
                self.FSM.ToTransition("toRELEASE")
            elif (self.args['PRESSURE'] >= self.args['PAINL'] and self.args['PRESSURE'] > self.args['PAINH'] \
                    and self.args['PRESSURE'] >= self.args['PMAX']):
                # Overshot past all thresholds, max too, so we vent emergency-style
                print ("--")
                self.FSM.ToTransition("toVENT")
            else:
                print("Error!  Something strange going on with the pressure thresholds")
                print("Current Pressure=", self.args['PRESSURE'])
                print(" and Plow=", self.args['PAINL'], " and Pup=", self.args['PAINH'])
        else:
            # No pain required
            self.FSM.ToTransition("toISOLATE_VENT")

    def Exit(self):
        # May need to sleep here for a bit depending on how long the relay opening and air transfer takes
        # sleep (0.1)
        # S1 Closed, S2 Closed, S3 Closed
        set_relay(s1="closed", s2="closed", s3="closed")
        time.sleep(relay_settling_time)  # Give the relays time to close
        #time_locally = time.asctime(time.localtime(time.time()))
        #print (time_locally,": s1(air tank)=closed s2(cuff)=closed s3(vent)=closed")
        #print("Exiting Connect Cuff")
