from app.System.states.State import State

class LOAD_RESERVOIR(State):
    def __init__(self, FSM):
        super(LOAD_RESERVOIR, self).__init__(FSM)

    def Enter(self):
        # Close the cuff and reservoir relays and open the tank relay
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
                print ("elapsed (", time.time() - start_time, ")")
                self.FSM.ToTransition("toCONNECT_CUFF")
            elif (self.args['PRESSURE'] >= self.args['PAINL'] and self.args['PRESSURE'] <= self.args['PAINH']):
                print ("Pain pressure looks right, so we are done with P=", self.args['RESSURE'])
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
            # We should usually never get here, without requiring pain.  This shouldn't happen, so get out safely, venting
            print ("This usually doesn't happen with P=", self.args['PRESSURE'])
            print (" and Pain=", self.args['PAIN'])
            self.FSM.ToTransition("toISOLATE_VENT")

    def Exit(self):
        # May need to sleep here for a bit depending on how long the relay opening and air transfer takes
        # sleep (0.1)
        isolate()  # close all of the relays
        sleep(0.1)  # Give the relays time to close
        print("Exiting Load Reservoir")
