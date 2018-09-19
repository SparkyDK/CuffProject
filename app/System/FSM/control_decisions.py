class ControlDecisions:
    def respond_to_user_inputs(self, current_counter, imported_schedule, control_args, user_args, pressure_parameters,
                               second_tickover, schedule_finished, airctrl, schedule, toggle):
        # A pain schedule must be initialized or restarted by pressing ABORT, then GO.
        # This is required on power-up and also once the pain schedule has been completed.
        # This extra button press inconvenience is an extra control fail-safe requirement
        # In the future, the GO command might be given by another machine
        # The Reset/Abort command must first be initiated by a person, effectively enabling the GO button
        # After that, STOP can be used to pause the schedule and the GO button can be used to "unpause"
        # Pain is disabled during pause mode
        # ABORT also disables pain and resets the pain schedule back to the beginning
        # OVERRIDE_PRESSURE (sampled from user_args) is used to create new values of PAINH and PAINL, initially
        # derived from PAINVALUE and PAINTOLERANCE data taken from a fixed configuration file
        self.current_counter = current_counter
        self.imported_schedule = imported_schedule
        self.control_args = control_args
        self.user_args = user_args
        self.pressure_parameters = pressure_parameters
        self.second_tickover = second_tickover
        self.schedule_finished = schedule_finished
        self.airctrl = airctrl
        self.schedule = schedule
        self.toggle = toggle

        print ("\nCTRL: User_args are:", self.user_args, "and state machine in state:", self.airctrl.FSM.GetCurState())

        if (self.toggle > 0 and self.toggle <= 1):
            self.toggle += 1
            print("CTRL: user=", self.user_args, "   control=", self.control_args)
        else:
            self.toggle = 0

        # {STARTED, PAUSE} states are as follows:
        # {0,1} is the initial state, required before the schedule can be started.
        # {0,0} is the final state, once the pain schedule has been run and also at initial power-up
        # {1,0} is the "running" state, where the pain schedule is executed
        # {1,1} is the "paused" state, where the pain schedule has been suspended temporarily

        # At initial power-up, or if we have finished the schedule, then the user must first press Reset/ABORT
        # This sets PAUSE=1 and enables the use of the GO button, which is disabled until the RESET button is pressed
        # The schedule cannot be restarted just with the GO button alone (this is a feature!)
        if (self.user_args['ABORT'] == 1):      # Highest priority user input
            # "reset" back to a starting state
            self.current_counter, self.imported_schedule, self.Global_cnt,\
            self.schedule_finished, self.pressure_parameters = \
                self.schedule.setup_pain_schedule(self.control_args, self.pressure_parameters)
            self.control_args['STARTED'] = 0
            self.control_args['PAUSE'] = 1      # Requested feature requires Reset/Abort, before GO button will work
            self.schedule_finished = 0
            self.user_args['ABORT'] = 0        # Clear the button signal back to the GUI
        elif (self.control_args['STARTED'] == 0 and self.control_args['PAUSE'] == 1 and self.user_args['GO'] == 1):
            # Initial start of the pain schedule (start "running" for the first time)
            print ("Starting the schedule for the first time")
            if (self.second_tickover == True and self.airctrl.FSM.GetCurState()=="IDLE"):
                # Synchronize the pain schedule counting to the seconds tickover points
                # and wait for state machine to settle in IDLE state
                print("CTRL: Pain schedule being started for the first time; now running the pain schedule")
                self.control_args['STARTED'] = 1
                self.control_args['PAUSE'] = 0
                self.control_args, self.schedule_finished, self.current_counter = \
                    self.schedule.execute_pain_schedule(self.control_args, self.schedule,
                                                        self.schedule_finished, self.current_counter)
                self.user_args['GO'] = 0  # Clear the button signal back to the GUI
        elif (self.control_args['STARTED'] == 1 and self.control_args['PAUSE'] == 0 and self.user_args['STOP'] == 1):
            # "pause"
            # In the "running" state, a STOP button means that a pause is required (STOP ignored otherwise)
            print("CTRL: Pain schedule being paused (and we disable pain too, in this state)")
            self.control_args['PAUSE'] = 1
            self.control_args['PAIN'] = 0  # We don't permit PAIN to be administered in the "paused" state
            self.user_args['STOP'] = 0  # Clear the button signal back to the GUI
        elif (self.control_args['STARTED'] == 1 and self.control_args['PAUSE'] == 1 and self.user_args['GO'] == 1):
            # resume "running"
            # In the "paused" state, GO means that the pause is ended and processing resumes (GO ignored otherwise)
            if (self.second_tickover == True and self.airctrl.FSM.GetCurState()=="IDLE"):
                # Synchronize the pain schedule counting to the seconds tickover points
                # and wait for the state machine to be settled in the IDLE state
                print("CTRL: Pain schedule being resumed")
                self.control_args['PAUSE'] = 0
                self.control_args, self.schedule_finished, self.current_counter = \
                    self.schedule.execute_pain_schedule(self.control_args, self.schedule,
                                                        self.schedule_finished, self.current_counter)
                self.user_args['GO'] = 0  # Clear the button signal back to the GUI
        elif (self.control_args['STARTED'] == 1 and self.control_args['PAUSE'] == 0):
            # keep on "running"
            # Continue processing of the the pain schedule
            if (self.second_tickover == True  and self.airctrl.FSM.GetCurState()=="IDLE"):
                # Execute once each second tickover, provided state machine is settled in the IDLE state
                self.control_args, self.schedule_finished, self.current_counter = \
                    self.schedule.execute_pain_schedule(self.control_args, self.schedule,
                                                        self.schedule_finished, self.current_counter)
                self.user_args['STOP'] = 0  # Clear the button signal back to the GUI (in case of nuisance-pressing)
                self.user_args['GO'] = 0    # Clear the button signal back to the GUI (in case of nuisance-pressing)
                # eventually, schedule will be finished, as indicated by boolean schedule_finished
                if (self.schedule_finished == 1):
                    print ("Schedule now finished")
        else:
            # All other cases, do nothing.
            # This includes initial power-up and the final case when the schedule is finished
            # Also includes cases where GO and STOP buttons are ignored appropriately
           if (self.second_tickover == True):
                self.user_args['GO'] = 0
                self.user_args['STOP'] = 0

        if (self.user_args['OVERRIDE'] == 1):
            # User has hit 'enter' to override the pain threshold pressure value (lowest priority activity)
            # New pain threshold value entered by user is used to adjust the pressure parameters

            # We could prevent changes during an executing pain schedule by setting this to False
            allow_pain_value_changes_during_pain_schedule = True  # Allow adjustments at any time
            if (self.control_args['STARTED'] == 0 or allow_pain_value_changes_during_pain_schedule == True):
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
                    print("Something wrong with the following pressure values (they should decrease monotonically):")
                    print("Pmax=", pmax, "painh=", painh, "painl=", painl, "Patm=", patm)
                    print("Not going to change anything....")
            self.user_args['OVERRIDE'] = 0  # Clear the button signal back to the GUI

        if (self.schedule_finished == 1 and self.control_args['STARTED'] == 0 and self.control_args['PAUSE'] == 0):
            # Repair the schedule index, so that it is not left out of range after pain schedule completion
            # Leave the counters as negative versions of their original, starting values
            # Display all negative numbers as grayed-out records of progress made through the schedule
            self.control_args['SCHEDULE_INDEX'] = 0
            self.control_args['PAIN'] = 0  # We don't permit PAIN to be administered once the schedule is completed

        #print ("CTRL (2) user_args: ", self.user_args)

        #print ("CTRL out: schedule_finished=", self.schedule_finished)

        return (self.user_args, self.control_args, self.current_counter, self.pressure_parameters,\
                self.schedule_finished, self.toggle)