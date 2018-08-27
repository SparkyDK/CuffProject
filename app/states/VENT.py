import State

class VENT(State):
    def __init__(self, FSM):
        super (VENT, self).__init__(FSM)
    def Enter(self):
        # open the venting relay for the reservoir and to the cuff, but close the tank relay
        pass
    def Execute(self,  args):
        self.args = args
        self.P = self.args['P']
        print "\n* VENT * \t with args:",  self.args
        #while (self.P>Patm):
        if (self.P>Patm):
            # Stay in the VENT state
            print ("Still need to vent, since pressure is greater than atmospheric pressure")
        else:
            self.FSM.ToTransition("toIDLE")
    def Exit(self):
        print("Exiting Vent")