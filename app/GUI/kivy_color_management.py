import time
class kivy_color_adjustment:
    newpressurecolour = 0, 0, 0, 1
    nopaincolour = 0, 0, 0, 1
    paincolour = 0, 0, 0, 1
    gocolour = 0, 0, 0, 1
    stopcolour = 0, 0, 0, 1
    entercolour = 1, 1, 1, 1
    time_state = ""
    def grey_out(self, current_counter, control_args, user_args, pressure_parameters, second_tickover, airctrl):
        self.current_counter = current_counter
        self.control_args = control_args
        self.user_args = user_args
        self.pressure_parameters = pressure_parameters
        self.second_tickover = second_tickover
        self.airctrl = airctrl

        self.value1 = str(self.current_counter[0])
        self.value2 = str(self.current_counter[1])
        self.value3 = str(self.current_counter[2])
        self.value4 = str(self.current_counter[3])
        self.value5 = str(self.current_counter[4])
        self.value6 = str(self.current_counter[5])
        self.value7 = str(self.current_counter[6])
        self.value8 = str(self.current_counter[7])

        # Set up grey control for pain schedule values, making them grey if negative/50% transparent, else black
        if (self.current_counter[0] < 0):
            self.colour1 = 0, 0, 0, 0.5
        else:
            self.colour1 = 0, 0, 0, 1

        if (self.current_counter[1] < 0):
            self.colour2 = 0, 0, 0, 0.5
        else:
            self.colour2 = 0, 0, 0, 1

        if (self.current_counter[2] < 0):
            self.colour3 = 0, 0, 0, 0.5
        else:
            self.colour3 = 0, 0, 0, 1

        if (self.current_counter[3] < 0):
            self.colour4 = 0, 0, 0, 0.5
        else:
            self.colour4 = 0, 0, 0, 1

        if (self.current_counter[4] < 0):
            self.colour5 = 0, 0, 0, 0.5
        else:
            self.colour5 = 0, 0, 0, 1

        if (self.current_counter[5] < 0):
            self.colour6 = 0, 0, 0, 0.5
        else:
            self.colour6 = 0, 0, 0, 1

        if (self.current_counter[6] < 0):
            self.colour7 = 0, 0, 0, 0.5
        else:
            self.colour7 = 0, 0, 0, 1

        if (self.current_counter[7] < 0):
            self.colour8 = 0, 0, 0, 0.5
        else:
            self.colour8 = 0, 0, 0, 1

        # Set colour of GO to black only if currently paused or in initial state after reset
        if ( (self.control_args['STARTED']==1 and self.control_args['PAUSE']==1) or\
                (self.control_args['STARTED']==0 and self.control_args['PAUSE']==1) ):
            self.gocolour = 0, 0, 0, 1
        else:
            self.gocolour = 0, 0, 0, 0.5

        # Set colour of STOP to black only if already running a pain schedule, else make it grey/50% transparent
        if ( self.control_args['STARTED']==1 and self.control_args['PAUSE']==0):
            self.stopcolour = 0, 0, 0, 1
        else:
            self.stopcolour = 0, 0, 0, 0.5

        if (second_tickover == True):
            if (self.control_args['PAIN'] == 0):
                self.nopaincolour = 0, 0, 0, 1
                self.paincolour = 0, 0, 0, 0
            else:
                self.nopaincolour = 0, 0, 0, 0
                self.paincolour = 0, 0, 0, 1

        localtime = time.asctime(time.localtime(time.time()))
        if (self.airctrl.FSM.GetCurState() == "IDLE"):
            self.time_state = localtime + ": " + "Normal"
        else:
            self.time_state = localtime + ": " + self.airctrl.FSM.GetCurState()

        if ( self.user_args['override_pressure'] + self.pressure_parameters['PAINTOLERANCE'] >=\
                self.pressure_parameters['PMAX'] ):
            self.entercolour = 1, 0, 0, 1
        else:
            self.entercolour = 1, 1, 1, 1

        if ( self.user_args['override_pressure'] != self.pressure_parameters['PAINVALUE'] ):
            self.newpressurecolour = 0, 0, 0, 0.5
        else:
            self.newpressurecolour = 0, 0, 0, 1

        return(self.value1, self.colour1, self.value2, self.colour2, self.value3, self.colour3,
               self.value4, self.colour4, self.value5, self.colour5, self.value6, self.colour6,
               self.value7, self.colour7, self.value8, self.colour8,
               self.gocolour, self.stopcolour, self.paincolour, self.nopaincolour, self.entercolour,
               self.newpressurecolour, self.time_state)
