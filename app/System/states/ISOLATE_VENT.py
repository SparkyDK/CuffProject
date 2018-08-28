from app.System.states.State import State

class ISOLATE_VENT(State):
    def __init__(self, FSM):
        super(ISOLATE_VENT, self).__init__(FSM)

    def Enter(self):
        # May need to sleep here for a bit depending on how long previous relay opening and air transfer takes
        # sleep (0.1)
        isolate()  # close all of the relays, specifically the tank relay
        sleep(0.1)  # Give the relays time to close
        # Open the relays to the cuff and from the reservoir, but keep the tank relay closed
        pass

    def Execute(self, args):
        self.args = args
        print
        "\n* ISOLATE_VENT * \twith args:", self.args
        self.FSM.ToTransition("toVENT")

    def Exit(self):
        print("Exiting ISOLATE_VENT")
