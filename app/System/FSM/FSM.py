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

    def process_pain_schedule(self, control_args, schedule, schedule_finished):
        self.control_args = control_args
        self.schedule = schedule
        self.schedule_finished = schedule_finished

        if (self.control_args['SCHEDULE_INDEX'] < MAX_NUM_SCHEDULES and schedule_finished == False):
            # Not finished the schedule yet
            # Don't really need to be set again every second for each phase
            # Could just do it for the very first second of each phase
            if (self.control_args['PAUSE'] == 1):
                # No pain permitted in Pause mode
                self.control_args['PAIN'] = 0
            else:
                if (self.schedule[self.control_args['SCHEDULE_INDEX']][0] == 'PAIN'):
                    self.control_args['PAIN'] = 1
                else:
                    self.control_args['PAIN'] = 0

            if (self.current_counter[self.control_args['SCHEDULE_INDEX']] > 1):
                # Current schedule phase still not complete
                self.current_counter[self.control_args['SCHEDULE_INDEX']] -= 1
                print("\tSchedule Counter adjusted: Schedule:", self.control_args['SCHEDULE_INDEX'],
                      " with counter value = ", self.current_counter[self.control_args['SCHEDULE_INDEX']],
                      " and pain set to ", self.control_args['PAIN'])
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
            # Done executing the schedule sequence ... could leave most of this stuff out of here and
            # just use the schedule_finished
            print("Finished executing schedule")
            self.control_args['SCHEDULE_INDEX'] = 0
            self.control_args['PAIN'] = 0
            self.control_args['STARTED'] = 0
            self.control_args['PAUSE'] = 0
            self.schedule_finished = True
        return (self.control_args, self.schedule_finished)

    def reset_schedule(self, control_args, current_counter, pressure_parameters, schedule):
        self.control_args = control_args
        self.current_counter = current_counter
        self.pressure_parameters = pressure_parameters
        self.schedule = schedule

        self.control_args['SCHEDULE_INDEX'] = 0
        self.control_args['PAIN'] = 0
        # self.control_args['FORCE'] = 0;
        # self.user_args['ABORT'] = 0
        self.control_args['PAINL'] = int(pressure_parameters['PAINVALUE'] - pressure_parameters['PAINTOLERANCE'])
        self.control_args['PAINH'] = int(pressure_parameters['PAINVALUE'] + pressure_parameters['PAINTOLERANCE'])
        for schedule_phase in range(0, MAX_NUM_SCHEDULES):
            self.current_counter[schedule_phase] = schedule[schedule_phase][1]
            print("Schedule value for phase ", schedule_phase, " reset to: ", schedule[schedule_phase][1])
        self.SetState("ISOLATE_VENT")


    def ControlDecisions(self, current_counter, schedule, control_args, old_user_args, user_args,
                         pressure_parameters, second_tickover, schedule_finished, toggle):
        # A FORCE is equivalent to an untimed PAIN cycle in PAUSE mode (PAUSE alone makes pressure NIL, otherwise)
        # OVERRIDE_PRESSURE (sampled from user_args) is used to create new values of PAINH and PAINL
        # STOP and ABORT both do an ABORT in the FORCE mode of operation, venting pressure, resetting index, etc.
        self.current_counter = current_counter
        self.schedule = schedule
        self.control_args = control_args
        self.old_user_args = old_user_args
        self.user_args = user_args
        self.pressure_parameters = pressure_parameters
        self.second_tickover = second_tickover
        self.schedule_finished = schedule_finished
        self.toggle = toggle

        if (self.toggle > 0 and self.toggle <=1):
            self.toggle +=1
            print ("CTRL: user=", self.user_args, "   control=", self.control_args)
        else:
            self.toggle = 0

        # {STARTED, PAUSE} states are as follows:
        # {0,1} is the initial default state
        # {0,0} is the final state, once the pain schedule has been run
        # {1,0} is the "running" state, where the pain schedule is executed
        # {1,1} is the "paused" state, where the pain schedule has been suspended temporarily

        if (self.user_args['ABORT'] == 1):
            # "reset" back to a starting state
            # Highest priority user input
            if (second_tickover == True):
                # Only display this useful message once a second
                print ("CTRL: User pressed abort; resetting pain schedule")
                self.reset_schedule(self.control_args, self.current_counter, pressure_parameters, self.schedule)
            # initial state has an automatic pause (final state does not)
            self.control_args['STARTED'] = 0; self.control_args['PAUSE'] = 1
            self.schedule_finished = False
        elif (self.control_args['STARTED'] == 0 and self.control_args['PAUSE'] == 1 and self.user_args['GO'] == 1):
            # Initial start of the pain schedule (start "running" for the first time)
            if (second_tickover == True):
                # Synchronize the pain schedule counting to the seconds tickover points
                print("CTRL: Pain schedule being started for the first time; now running the pain schedule")
                self.control_args['STARTED'] = 1; self.control_args['PAUSE'] = 0
                self.control_args, self.schedule_finished =\
                    self.process_pain_schedule(self.control_args, self.schedule, self.schedule_finished)
        elif (self.control_args['STARTED'] == 1 and self.control_args['PAUSE'] == 0 and self.user_args['STOP'] == 1):
            # "pause"
            # In the "running" state, a STOP button means that a pause is required (STOP ignored otherwise)
            print("CTRL: Pain schedule being paused (and we disable pain too, in this state)")
            self.control_args['PAUSE'] = 1
            self.control_args['PAIN'] = 0 # We don't permit PAIN to be administered in the "paused" state
        elif (self.control_args['STARTED'] == 1 and self.control_args['PAUSE'] == 1 and self.user_args['GO'] == 1):
            # resume "running"
            # In the "paused" state, GO means that the pause is ended and processing resumes (GO ignored otherwise)
            if (second_tickover == True):
                # Synchronize the pain schedule counting to the seconds tickover points
                print("CTRL: Pain schedule being resumed")
                self.control_args['PAUSE'] = 0
                self.control_args, self.schedule_finished =\
                    self.process_pain_schedule(self.control_args, self.schedule, self.schedule_finished)
        elif (self.control_args['STARTED'] == 1 and self.control_args['PAUSE'] == 0):
            # keep on "running"
            # Continue processing of the the pain schedule
            if (second_tickover == True):
                # Execute on the seconds tickover points
                # print("CTRL: Pain schedule continues")
                self.control_args, self.schedule_finished =\
                    self.process_pain_schedule(self.control_args, self.schedule, self.schedule_finished)
                # eventually, schedule will be finished
        else:
            # All other cases, do nothing.
            # This includes the final case when the schedule is finished: {STARTED, PAUSE} = {0,0}
            # If we have finished the schedule, then the user must press ABORT again to set PAUSE=1 and enable GO
            # The schedule cannot be restarted just with the GO button alone (this is a feature)
            pass

        if (self.user_args['OVERRIDE'] == 1):
            # User has hit 'enter' to override the pain threshold pressure value (lowest priority activity)
            # could set this value many times over... but that's OK.  When the button is released the
            # latest value will be latched finally
            # New pain threshold value entered by user is used to adjust the pressure parameters

            # We could prevent changes during a pain schedule by setting this to False
            allow_pain_value_changes_during_pain_schedule = True  # Allow adjustments at any time
            if(self.control_args['STARTED'] == 0 or allow_pain_value_changes_during_pain_schedule == True):
                print("CTRL: User requested pain pressure value change to ", self.user_args['override_pressure'])
                print(" by changing the value and pressing the NEW/ENTER button")
                override_value = int(self.user_args['override_pressure'])
                painl = override_value - self.pressure_parameters['PAINTOLERANCE']
                painh = override_value + self.pressure_parameters['PAINTOLERANCE']
                patm = self.pressure_parameters['PATM']
                pmax = self.pressure_parameters['PMAX']
                if (pmax > painh and painl < painh and patm < painl):
                    self.pressure_parameters['PAINVALUE'] = override_value
                    self.control_args['PAINL'] = override_value - self.pressure_parameters['PAINTOLERANCE']
                    self.control_args['PAINH'] = override_value + self.pressure_parameters['PAINTOLERANCE']
                    print("Updated pain pressure values: PAINL=", self.control_args['PAINL'])
                    print(" PAINH=", self.control_args['PAINH'], " PAINVALUE=", pressure_parameters['PAINVALUE'])
                else:
                    print ("Something wrong with the following pressure values (they should decrease monotonically):")
                    print ("Pmax=", pmax, "painh=", painh, "painl=", painl, "Patm=", patm)
                    print ("Not going to change anything....")

        if (self.schedule_finished == True and self.control_args['STARTED'] == 0 and self.control_args['PAUSE'] == 0):
        # We can repair the schedule index, so that it is not left out of range after pain schedule completion
        # We have also left the counters as negative versions of their original, starting values
        # This way, we can display all negative numbers as grayed-out records of progress made through the schedule
            self.control_args['SCHEDULE_INDEX'] = 0
            self.control_args['PAIN'] = 0  # We don't permit PAIN to be administered once the schedule is completed

        return (self.control_args, self.current_counter, self.pressure_parameters, self.schedule_finished, self.toggle)


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
