from app.constants.CONSTANTS import MAX_NUM_PHASES

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

    def reset_schedule(self, control_args, current_counter, pressure_parameters, schedule):
        self.control_args = control_args
        self.current_counter = current_counter
        self.pressure_parameters = pressure_parameters
        self.schedule = schedule

        self.control_args['SCHEDULE_INDEX'] = 0
        self.control_args['PAIN'] = 0
        # self.user_args['ABORT'] = 0
        self.control_args['PAINL'] = int(pressure_parameters['PAINVALUE'] - pressure_parameters['PAINTOLERANCE'])
        self.control_args['PAINH'] = int(pressure_parameters['PAINVALUE'] + pressure_parameters['PAINTOLERANCE'])
        for schedule_phase in range(0, MAX_NUM_PHASES):
            self.current_counter[schedule_phase] = schedule[schedule_phase][1]
            print("Schedule value for phase ", schedule_phase, " reset to: ", schedule[schedule_phase][1])
        self.SetState("ISOLATE_VENT")

    def Execute(self, args):
        self.args = args
        # print "(FSM) args are:",  args
        if (self.trans):
            # State transition required (to_xxxx state defined)
            self.curState.Exit()  # Perform the exit operations of the existing/previous state
            self.trans.Execute()  # Execute the statements associated with the transition to_xxxx state, if any
            self.SetState(self.trans.toState)  # Update the current state to the new destination state
            self.curState.Enter()  # Execute the statements associated with entry into this new state
            self.trans = None  # Not a new transition anymore

        # Execute the statements associated with the specific state that we are now in
        self.curState.Execute(self.args)
