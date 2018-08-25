import State

class VENT(State):
    def __init__(self, FSM):
        super (VENT, self).__init__(FSM)
    def Enter(self):
        pass
    def Execute(self,  args):
        self.args = args
        self.P = self.args['P']
        print "\n* VENT * \t with args:",  self.args
        #while (self.P>Patm):
        if (self.P>Patm):
            print ("Need to vent, since pressure is greater than atmospheric pressure")
        else:
            self.FSM.ToTransition("toIDLE")
    def Exit(self):
        print("Exiting Vent")