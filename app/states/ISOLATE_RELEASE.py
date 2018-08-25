import State
class ISOLATE_RELEASE(State):
    def __init__(self, FSM):
        super (ISOLATE_RELEASE, self).__init__(FSM)
    def Enter(self):
        pass
    def Execute(self,  args):
        self.args = args
        self.P = self.args['P']
        self.Pain = self.args['PAIN']
        print "\n* ISOLATE_RELEASE * \t with args:",  self.args
        if self.P>Pup:
            self.FSM.ToTransition("toRELEASE")
        #if (self.Pain == 1 and P<Plow):
        #    self.FSM.ToTransition("toISOLATE")
        if (self.Pain == 1 and self.P>Plow and self.P<Pup):
            self.FSM.ToTransition("toIDLE")
    def Exit(self):
        print ("Exiting Isolate Release")