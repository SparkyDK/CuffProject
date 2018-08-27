import State


class CONNECT_CUFF(State):
    def __init__(self, FSM):
        super(CONNECT_CUFF, self).__init__(FSM)

    def Enter(self):
        pass

    def Execute(self, args):
        self.args = args
        self.P = self.args['P']
        self.Pain = self.args['PAIN']
        print
        "\n* CONNECT_CUFF * \twith args:", self.args
        if (self.Pain == 1):
            if (self.P < Plow):
                # Need to add air
                print
                "Still need to add more air with P=", self.P, "Plow=", Plow, " and Pup=", Pup
                self.FSM.ToTransition("toISOLATE")
            elif (self.P >= Plow and self.P <= Pup):
                # In the zone
                print
                "In the zone with P=", self.P
                self.FSM.ToTransition("toIDLE")
            elif (self.P >= Plow and self.P > Pup):
                # Overshot the maximum pain pressure value
                print
                "Overshot pressure maximum with P=", self.P, "Plow=", Plow, " and Pup=", Pup
                self.FSM.ToTransition("toISOLATE_RELEASE")
        else:
            # No pain required
            self.FSM.ToTransition("toISOLATE_VENT")

    def Exit(self):
        print("Exiting Connect Cuff")
