class kivy_color_adjustment:
    def grey_out(self, current_counter):
        self.current_counter = current_counter

        self.value1 = str(self.current_counter[0])
        self.value2 = str(self.current_counter[1])
        self.value3 = str(self.current_counter[2])
        self.value4 = str(self.current_counter[3])
        self.value5 = str(self.current_counter[4])
        self.value6 = str(self.current_counter[5])
        self.value7 = str(self.current_counter[6])
        self.value8 = str(self.current_counter[7])

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

        return(self.value1, self.colour1, self.value2, self.colour2,\
               self.value3, self.colour3, self.value4, self.colour4,\
               self.value5, self.colour5, self.value6, self.colour6,\
               self.value7, self.colour7, self.value8, self.colour8)
