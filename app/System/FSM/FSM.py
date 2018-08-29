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

    def process_pain_schedule(self, control_args, schedule):
        self.control_args = control_args
        self.schedule = schedule

        schedule_finished = False
        if (self.control_args['SCHEDULE_INDEX'] < MAX_NUM_SCHEDULES):
            # Not finished the schedule yet
            # Don't really need to be set again every second for each phase
            # Could just do it for the very first second of each phase
            if (self.control_args['PAUSE'] == 1):
                self.control_args['PAIN'] = 0
            else:
                self.control_args['PAIN'] = self.schedule[self.control_args['SCHEDULE_INDEX']][0]

            if (self.current_counter[self.control_args['SCHEDULE_INDEX']] > 1):
                # Current schedule phase still not complete
                self.current_counter[self.control_args['SCHEDULE_INDEX']] -= 1
                print("Schedule Counter adjusted: Schedule:", self.control_args['SCHEDULE_INDEX'])
                print(" with counter value = ", self.current_counter[self.control_args['SCHEDULE_INDEX']])
                print(" and pain set to ", self.control_args['PAIN'])
            else:
                # Current phase is now complete (Current_counter value is zero ... or negative)
                # Reset the displayed/current value back to the starting value
                # Leave it negative to indicate overall progress (and simplify graphics processing)
                # and then go to the next phase of the schedule
                print("Finished schedule phase ", self.control_args['SCHEDULE_INDEX'], "\n")
                self.current_counter[self.control_args['SCHEDULE_INDEX']] =\
                    -1 * self.schedule[self.control_args['SCHEDULE_INDEX']][1]
                self.control_args['SCHEDULE_INDEX'] += 1
        else:
            # Done executing the schedule sequence
            print("Finished executing schedule")
            self.control_args['SCHEDULE_INDEX'] = 0;
            self.control_args['PAIN'] = 0
            self.control_args['STARTED'] = 0;
            self.control_args['PAUSE'] = 0
            schedule_finished = True
        return (self.control_args, schedule_finished)

    #airctrl.FSM.ControlDecisions(current_counter, imported_schedule, control_args,
    # old_user_args, user_args, pressure_parameters, painh, painl, second_tickover, toggle)

    def ControlDecisions(self, current_counter, schedule, control_args, old_user_args, user_args,
                         pressure_parameters, painh, painl, second_tickover, toggle):
        # A FORCE is equivalent to an untimed PAIN cycle in PAUSE mode (PAUSE alone makes pressure NIL, otherwise)
        # OVERRIDE_PRESSURE (sampled from user_args) is used to create new values of PAINH and PAINL
        # STOP and ABORT both do an ABORT in the FORCE mode of operation, venting pressure, resetting index, etc.
        self.current_counter = current_counter
        self.schedule = schedule
        self.control_args = control_args
        self.old_user_args = old_user_args
        self.user_args = user_args
        self.painh = painh
        self.painl = painl
        self.second_tickover = second_tickover

        if (toggle > 0 and toggle <=1):
            toggle +=1
            print ("CTRL: user=", self.user_args, "   control=", self.control_args)
        else:
            toggle = 0

        # user_args = {'GO': 0, 'STOP': 0, 'ABORT': 0, 'UP': 0, 'DOWN': 0,
        #             'override_pressure': pressure_parameters['PAINVALUE'], 'OVERRIDE': 0}
        # control_args = {'SCHEDULE_INDEX': 0, 'PAIN': 0, 'STARTED': 0, 'PAUSE': 0, 'FORCE': 0,
        #                'PAINH': painh, 'PAINL': painl, 'PRESSURE': 0,
        #                'PATM': pressure_parameters['PATM'], 'PMAX': pressure_parameters['PMAX']}
        schedule_finished = False

        if (self.user_args['ABORT'] == 1):
            print ("CTRL: User pressed abort")
            # Highest priority user input
            self.control_args['SCHEDULE_INDEX'] = 0; self.control_args['PAIN'] = 0; self.control_args['STARTED'] = 0
            self.control_args['PAUSE'] = 0; self.control_args['FORCE'] = 0; self.user_args['ABORT'] = 0
            self.control_args['PAINL'] = int(pressure_parameters['PAINVALUE'] - pressure_parameters['PAINTOLERANCE'])
            self.control_args['PAINH'] = int(pressure_parameters['PAINVALUE'] + pressure_parameters['PAINTOLERANCE'])
            for i in range (0, MAX_NUM_SCHEDULES):
                self.current_counter[i] = schedule[i][1]
            print ("Schedule values for counter: ", schedule[i][1])
            self.SetState("ISOLATE_VENT")
        elif (self.control_args['STARTED'] == 1):
            # Pain schedule is ongoing
            if (self.control_args['PAUSE'] == 0):
                # Not in pause mode yet, but now we could be
                # Ignore the STOP, if already paused or if not running a schedule already
                #if (self.old_user_args['STOP'] == 1 and self.user_args['STOP'] == 0):
                if (self.old_user_args['STOP'] == 1):
                    self.control_args['PAUSE'] = 1
                    # If running a schedule and a pause is requested and not already paused, then we are now in pause
                    print ("CTRL: User pressed and just released STOP during an unpaused and running schedule")
                    print (" in phase ", self.control_args['SCHEDULE_INDEX'], ".... now going to pause that schedule")
                    if (self.control_args['PAIN'] == 1):
                        # Don't pause in a pain state... go backwards to the end of the nearest NIL phase
                        print ("CTRL: User attempting to pause in a pain state... going to prevent this")
                        while (self.current_counter[self.control_args['SCHEDULE_INDEX']] == 'PAIN' and
                               self.control_args['SCHEDULE_INDEX'] >= 0):
                            # Restore previous PAIN phases
                            self.current_counter[self.control_args['SCHEDULE_INDEX']] =\
                                schedule[self.control_args['SCHEDULE_INDEX']][1]
                            self.control_args['SCHEDULE_INDEX'] -= 1
                        if (self.control_args['SCHEDULE_INDEX'] >= 0):
                            # put one second back on the counter for this NIL phase
                            self.current_counter[self.control_args['SCHEDULE_INDEX']] = 1
                        else:
                            # All Pain phases, including very first phase, so start again
                            self.control_args['SCHEDULE_INDEX'] = 0
                            #print ("current_counter: ", current_counter)
                            #print ("schedule: ", schedule)
                            for i in range(0, MAX_NUM_SCHEDULES):
                                self.current_counter[i] = schedule[i][1]
                        print("CTRL: Turned off pain and going back to phase", self.control_args['SCHEDULE_INDEX'])
                        print(" of the pain schedule")
                        # Regardless, no more PAIN when paused
                        self.control_args['PAIN'] = 0
                    else:
                        # Paused in the NIL state, so do nothing
                        pass
                else:
                # In the middle of an unpaused schedule, so process it at each second tick
                    if (second_tickover == True):
                        self.control_args, schedule_finished = \
                            self.process_pain_schedule(self.control_args, self.schedule)
            else:
                # We are in pause mode
                if (self.old_user_args['GO'] == 1):
                    # pressing GO clears us out of PAUSE mode
                    self.control_args['PAUSE'] = 0
                # Make sure that no pain is applied during pause mode
                self.control_args['PAIN'] = 0
        #elif (self.old_user_args['GO'] == 1 and self.user_args['GO'] == 0):
        elif (self.old_user_args['GO'] == 1):
            # Not aborting and no schedule is currently running when user requests first starting of the schedule
            # schedule start requested
            print ("Starting a cycle")
            # No schedule started yet
            self.control_args['STARTED']=1; self.control_args['SCHEDULE_INDEX']=0; self.control_args['PAIN']=0
            self.control_args['PAUSE'] = 0
            for i in range (0, MAX_NUM_SCHEDULES):
                # Populate the timers for each phase of the schedule
                self.current_counter[i] = schedule[i][1]
        #elif (self.old_user_args['OVERRIDE'] == 1 and self.user_args['OVERRIDE'] == 0):
        elif (self.user_args['OVERRIDE'] == 1):
            # User has hit 'enter' to override the pain threshold pressure value
            # could set this value many times over... but that's OK.  When the button is released the
            # latest value will be latched finally
            print("CTRL: User changed pain pressure value to ", self.user_args['override_pressure'])
            print (" and selected the NEW/ENTER button")
            # New pain threshold value entered by user is used to adjust the pressure parameters
            pressure_parameters['PAINVALUE']=self.user_args['override_pressure']
            self.control_args['PAINL'] = int(self.user_args['override_pressure'] - pressure_parameters['PAINTOLERANCE'])
            self.control_args['PAINL'] = int(self.user_args['override_pressure'] + pressure_parameters['PAINTOLERANCE'])
            print ("Updated pain pressure values: painl=", self.control_args['PAINL'],
                   " painh=", self.control_args['PAINH'], " painvalue=", pressure_parameters['PAINVALUE'])
        else:
            pass
            #print("CTRL: Not doing anything for the case for these control arguments:", self.control_args)

        return (self.control_args, self.current_counter, schedule_finished, toggle)

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
