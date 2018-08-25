import State

class ISOLATE_VENT(State):
    def __init__(self, FSM):
        super (ISOLATE_VENT, self).__init__(FSM)
    def Enter(self):
        pass
    def Execute(self,  args):
        self.args = args
        print "\n* ISOLATE_VENT * \twith args:",  self.args
        self.FSM.ToTransition("toVENT")
    def Exit(self):
        print ("Exiting ISOLATE_VENT")