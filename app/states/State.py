class State(object):
    def __init__(self, FSM):
        self.FSM = FSM
    def Enter(self):
        pass
    def Execute(self,  args):
        self.args=args
    def Exit(self):
        pass