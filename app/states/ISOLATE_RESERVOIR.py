import State


class ISOLATE_RESERVOIR(State):
    def __init__(self, FSM):
        super(ISOLATE_RESERVOIR, self).__init__(FSM)

    def Enter(self):
        pass

    def Execute(self, args):
        self.args = args
        print
        "\n* ISOLATE_RESERVOIR * \twith args:", self.args
        self.FSM.ToTransition("toCONNECT_CUFF")

    def Exit(self):
        print("Exiting Isolate Reservoir")
