import State

class VENT(State):
    def Execute(self, pressure):
        print("Venting with this pressure: " + str(pressure))
        if (self.P > Patm):
            print("Need to vent, since pressure is greater than atmospheric pressure")
        else:
            self.FSM.ToTransition("toIDLE")