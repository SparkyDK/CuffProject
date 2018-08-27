import State


class ISOLATE(State):
    def __init__(self, FSM):
        super(ISOLATE, self).__init__(FSM)

    def Enter(self):
        pass

    def Execute(self, args):
        self.args = args
        print
        "\n* ISOLATE * \t with args:", self.args
        self.FSM.ToTransition("toLOAD_RESERVOIR")

    def Exit(self):
        print("Exiting Isolate")
