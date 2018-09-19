class kivy_color_adjustment:
    def grey_out(self, current_counter, control_args, user_args):
        self.current_counter = current_counter
        self.control_args = control_args
        self.user_args = user_args

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

        # Set colour of GO to grey/50% transparent, if already in a running schedule, else make it black
        if (self.control_args['STARTED']==1 and self.control_args['PAUSE']==0):
            self.gocolour = 0, 0, 0, 0.5
        else:
            self.gocolour = 0, 0, 0, 1

        # Set colour of STOP to grey/50% transparent, if paused in a schedule, else make it black
        if (self.control_args['STARTED']==1 and self.control_args['PAUSE']==1):
            self.stopcolour = 0, 0, 0, 0.5
        else:
            self.stopcolour = 0, 0, 0, 1

        return(self.value1, self.colour1, self.value2, self.colour2,\
               self.value3, self.colour3, self.value4, self.colour4,\
               self.value5, self.colour5, self.value6, self.colour6,\
               self.value7, self.colour7, self.value8, self.colour8,\
               self.gocolour, self.stopcolour)
