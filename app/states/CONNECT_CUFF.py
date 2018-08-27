import State

class CONNECT_CUFF(State):
    def __init__(self, FSM):
        super (CONNECT_CUFF, self).__init__(FSM)
    def Enter(self):
        # Open the relay to the cuff and close the others
        pass
    def Execute(self,  args):
        self.args = args
        self.P = self.args['P']
        self.Pain = self.args['PAIN']
        print "\n* CONNECT_CUFF * \twith args:",  self.args
        if (self.Pain == 1):
            if (self.P<Plow):
            # Need to add air
                print "Still need to add more air with P=",  self.P,  "Plow=",  Plow,  " and Pup=",  Pup
                self.FSM.ToTransition("toLOAD_RESERVOIR")
            elif (self.P>=Plow and self.P<=Pup):
            # In the zone
                print "In the zone with P=",  self.P
                self.FSM.ToTransition("toIDLE")
            elif (self.P>=Plow and self.P>Pup):
            # Overshot the maximum pain pressure value
                print "Overshot pressure maximum with P=",  self.P,  "Plow=",  Plow,  " and Pup=",  Pup
                self.FSM.ToTransition("toRELEASE")
            else:
                print ("Error!  Something strange going on with the pressure thresholds")
                print ("Current Pressure=", self.P," and Plow=", Plow, " and Pup=", Pup)
        else:
        # No pain required
            self.FSM.ToTransition("toVENT")
    def Exit(self):
        # May need to sleep here for a bit depending on how long the relay opening and air transfer takes
        # sleep (0.1)
        isolate()   # close all of the relays
        sleep (0.1) # Give the relays time to close

        print ("Exiting Connect Cuff")