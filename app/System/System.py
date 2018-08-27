from app.FSM import FSM

Char = type("Char", (object,), {})


class System(Char):
    def __init__(self):
        self.FSM = FSM(self)

        ##STATES
        self.FSM.AddState("IDLE", IDLE(self.FSM))
        self.FSM.AddState("VENT", VENT(self.FSM))
        self.FSM.AddState("LOAD_RESERVOIR", LOAD_RESERVOIR(self.FSM))
        self.FSM.AddState("CONNECT_CUFF", CONNECT_CUFF(self.FSM))
        self.FSM.AddState("RELEASE", RELEASE(self.FSM))
        self.FSM.AddState("ISOLATE_VENT", ISOLATE_VENT(self.FSM))
        self.FSM.AddState("NEW_ENTRY", NEW_ENTRY(self.FSM))

        # TRANSITIONS
        self.FSM.AddTransition("toIDLE", Transition("IDLE"))
        self.FSM.AddTransition("toVENT", Transition("VENT"))
        self.FSM.AddTransition("toLOAD_RESERVOIR", Transition("LOAD_RESERVOIR"))
        self.FSM.AddTransition("toCONNECT_CUFF", Transition("CONNECT_CUFF"))
        self.FSM.AddTransition("toRELEASE", Transition("RELEASE"))
        self.FSM.AddTransition("toISOLATE_VENT", Transition("ISOLATE_VENT"))
        self.FSM.AddTransition("toNEW_ENTRY", Transition("NEW_ENTRY"))
        # default to IDLE
        self.FSM.SetState("ISOLATE_VENT")

    def Execute(self, args):
        self.args = args
        # Want to be able to modify pressure value for debug purposes
        # self.FSM.Execute(args)

        self.FSM.Execute(self.args)

    def isolate(self):
        # function that closes all of the relay valves
        pass