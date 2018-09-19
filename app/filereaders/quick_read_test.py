class quick_read:
    # Put values of  17300000 or 14000000 in this file to simulate converted digital pressure values
    def read(self, filename):
        self.filename = filename
        # read the lookup file values
        # print ("Reading file ", filename, " to obtain the A/D lookup values")
        f = open(filename, 'r')
        pressure = 0

        for line in f:
            pressure = int(line)
            #print ("quick read of a value of:", pressure)

        return (pressure)