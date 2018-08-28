from app.constants.CONSTANTS import MAX_NUM_SCHEDULES

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

    def ControlDecisions(self, current_counter, schedule, control_args, user_args, pressure_parameters, painh, painl):
        # A FORCE is equivalent to an untimed PAIN cycle in PAUSE mode (PAUSE alone makes pressure NIL, otherwise)
        # OVERRIDE_PRESSURE (sampled from user_args) is used to create new values of PAINH and PAINL
        # STOP and ABORT both do an ABORT in the FORCE mode of operation, venting pressure, resetting index, etc.

        self.current_counter = current_counter
        self.schedule = schedule
        self.control_args = control_args
        self.user_args = user_args
        self.painh = painh
        self.painl = painl
        # user_args = {'GO': 0, 'STOP': 0, 'ABORT': 0, 'UP': 0, 'DOWN': 0,
        #             'override_pressure': pressure_parameters['PAINVALUE'], 'OVERRIDE': 0}
        # control_args = {'SCHEDULE_INDEX': 0, 'PAIN': 0, 'STARTED': 0, 'PAUSE': 0, 'FORCE': 0,
        #                'PAINH': painh, 'PAINL': painl, 'PRESSURE': 0,
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
            for i in range (0, MAX_NUM_SCHEDULES):
                self.current_counter[i][1] = schedule[i][1]
            print ("Schedule values for counter: ", schedule[1])
            self.SetState("ISOLATE_VENT")
        elif (self.user_args['STOP'] == 1 and self.control_args['PAUSE'] == 0 and self.control_args['STARTED'] == 1):
            # If running a schedule and a pause is requested and not already paused, then pause
            # Ignore the STOP, if already paused or if not running a schedule already
            self.control_args['PAUSE'] = 1
            if (self.control_args['PAIN']==1):
                # Don't pause in a pain state... go backwards to the end of the nearest NIL phase
                current_index = self.control_args['SCHEDULE_INDEX']
                while (self.current_counter[current_index][0] == 'PAIN' and current_index >= 0):
                    # Restore previous PAIN phases
                    self.current_counter[current_index][1] = schedule[current_index][1]
                    current_index -= 1
                if (current_index >= 0):
                    self.control_args['SCHEDULE_INDEX'] = current_index
                    # put one second back on the counter for this NIL phase
                    self.current_counter[current_index][1] = 1
                else:
                    # All Pain phases, including very first phase, so start again
                    self.control_args['SCHEDULE_INDEX'] = 0
                    for i in range(0, MAX_NUM_SCHEDULES):
                        self.current_counter[i][1] = schedule[i][1]
            # Regardless, no more PAIN when paused
            self.control_args['PAIN'] = 0
        elif (self.user_args['GO'] == 1):
            # schedule start requested
            if (self.control_args['STARTED'] == 0):
                # No schedule started yet, but ignore GO button if already started
                self.control_args['STARTED'] = 1
                self.control_args['SCHEDULE_INDEX'] = 0
                self.control_args['PAIN'] = 0
                self.control_args['PAUSE'] = 0
                self.control_args['FORCE'] = 0
                for i in range (0, MAX_NUM_SCHEDULES):
                    self.current_counter[i][1] = schedule[i][1]
        elif (self.user_args['OVERRIDE'] == 1):
            # New pain threshold value entered by user is used to adjust the pressure parameters
            pressure_parameters['PAINVALUE']=self.user_args['override_pressure']
            self.control_args['PAINL'] = int(self.user_args['override_pressure'] - pressure_parameters['PAINTOLERANCE'])
            self.control_args['PAINL'] = int(self.user_args['override_pressure'] + pressure_parameters['PAINTOLERANCE'])
            print ("Updated pain pressure values: painl=", self.control_args['PAINL'],
                   " painh=", self.control_args['PAINH'], " painvalue=", self.control_args['PAINVALUE'])
        else:
            print("Not doing anything for the case for the control arguments:", control_args)

        return (self.control_args, self.current_counter)

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
