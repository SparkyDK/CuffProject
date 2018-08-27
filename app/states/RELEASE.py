import State


class RELEASE(State):
    def __init__(self, FSM):
        super(RELEASE, self).__init__(FSM)

    def Enter(self):
        pass

    def Execute(self, args):
        self.args = args
        self.P = self.args['P']
        self.Pain = self.args['PAIN']
        print
        "\n* RELEASE * \t with args:", self.args
        if (self.Pain == 1):
            if (self.P < Plow):
                # Need to top up pressure again
                self.FSM.ToTransition("toISOLATE")
            elif (self.P > Plow and self.P < Pup):
                # Pressure in the zone
                self.FSM.ToTransition("toIDLE")
            else:
                # Pressure is greater than Plow, but not in the zone, so it is too high
                self.FSM.ToTransition("toISOLATE_RESERVOIR")
        else:
            # Should not be here, since no pain is required so vent and go back to IDLE
            self.FSM.ToTransition("toISOLATE_VENT")

    def Exit(self):
        print("Exiting Vent")
