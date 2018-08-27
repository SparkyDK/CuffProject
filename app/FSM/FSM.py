class FSM(object):
    def __init__(self, character):
        self.char = character
        self.states = {}
        self.transitions = {}
        self.curState = None
        self.trans = None
        self.args = []
        self.names = {}

    def AddTransition(self, transName, transition):
        self.transitions[transName] = transition

    def AddState(self, stateName, state):
        self.states[stateName] = state
        self.names[state] = stateName

    def SetState(self, stateName):
        self.curState = self.states[stateName]

    def GetCurState(self):
        # self.name = self.curState
        return (self.names[self.curState])

    def ToTransition(self, toTrans):
        self.trans = self.transitions[toTrans]

    def ControlDecisions(self, current_counter, control_args, user_args):
        self.args = args


        return (control_args)

    def Execute(self, args):
        self.args = args
        # print "(FSM) args are:",  args
        if (self.trans):
            # State transition required (to_xxxx state defined)
            self.curState.Exit()    # Perform the exit operations of the existing/previous state
            self.trans.Execute()    # Execute the statements associated with the transition to_xxxx state, if any
            self.SetState(self.trans.toState)   # Update the current state to the new destination state
            self.curState.Enter()   # Execute the statements associated with entry into this new state
            self.trans = None       # Not a new transition anymore

        # Execute the statements associated with the specific state that we are now in
        self.curState.Execute(self.args)