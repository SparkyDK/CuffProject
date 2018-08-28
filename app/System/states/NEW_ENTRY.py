import State


class NEW_ENTRY(State):
    def __init__(self, FSM):
        super(NEW_ENTRY, self).__init__(FSM)

    def Enter(self):
        pass

    def Execute(self, args):
        self.args = args
        print
        "\n* NEW_ENTRY *"
        Pmax = int(Pnew)
        Plow = int(Pmax - 20)
        # Pnew = 0
        self.FSM.ToTransition("toIdle")

    def Exit(self):
        print("Exiting New Entry")
