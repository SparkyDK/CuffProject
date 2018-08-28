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

    def ControlDecisions(self, current_counter, control_args, user_args, pressure_parameters, painh, painl):
        # A FORCE is equivalent to an untimed PAIN cycle in PAUSE mode (PAUSE alone makes pressure NIL, otherwise)
        # OVERRIDE_PRESSURE (sampled from user_args) is used to create new values of PAINH and PAINL
        # STOP and ABORT both do an ABORT in the FORCE mode of operation, venting pressure, resetting index, etc.

        self.current_counter = current_counter
        self.control_args = control_args
        self.user_args = user_args
        self.painh = painh
        self.painl = painl
        # user_args = {'GO': 0, 'STOP': 0, 'ABORT': 0, 'UP': 0, 'DOWN': 0,
        #             'override_pressure': pressure_parameters['PAINVALUE'], 'OVERRIDE': 0}
        # control_args = {'SCHEDULE_INDEX': 0, 'PAIN': 0, 'STARTED': 0, 'PAUSE': 0, 'FORCE': 0,
        #                'PAINH': painh, 'PAINL': painl,
        #                'PATM': pressure_parameters['PATM'], 'PMAX': pressure_parameters['PMAX']}

        if (self.user_args['ABORT'] == 1):
            # Highest priority user input
            self.control_args['SCHEDULE_INDEX'] = 0
            self.control_args['PAIN'] = 0
            self.control_args['STARTED'] = 0
            self.control_args['PAUSE'] = 0
            self.control_args['FORCE'] = 0
            self.control_args['PAINL'] = int(pressure_parameters['PAINVALUE'] - pressure_parameters['PAINTOLERANCE'])
            self.control_args['PAINH'] = int(pressure_parameters['PAINVALUE'] + pressure_parameters['PAINTOLERANCE'])
            self.SetState("ISOLATE_VENT")
        elif (self.user_args['STOP'] == 1):
            self.control_args['PAUSE'] = 1
        elif (self.user_args['OVERRIDE'] == 1):
            # New pain threshold value entered by user is used to adjust the pressure parameters
            pressure_parameters['PAINVALUE']=self.user_args['override_pressure']
            self.control_args['PAINL'] = int(self.user_args['override_pressure'] - pressure_parameters['PAINTOLERANCE'])
            self.control_args['PAINL'] = int(self.user_args['override_pressure'] + pressure_parameters['PAINTOLERANCE'])

            pressure_parameters =
        elif (self.control_args['STARTED'] == 1 and self.control_args['PAIN'] == 1):
            # If in an active pain schedule phase, go back to end of nearest 'NIL' phase

            else:
            # If not in a pain schedule, then freeze where we are currently with a PAUSE
                self.control_args['PAUSE'] = 1


        else:
            running = 0
        if (PAUSE == True):
            pause_value = 1
        else:
            pause_value = 0

        return (self.control_args)

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
