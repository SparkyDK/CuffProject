class A_to_D_lookup:
    def read(self, filename):
        # read the lookup file values
        # print ("Reading file ", filename, " to obtain the A/D lookup values")
        f = open(filename, 'r')
        digital_value = []
        mm_Hg = []

        for line in f:
            columns = line.split()
            digital_value.append(columns[0])
            mm_Hg.append(columns[1])

        return (digital_value, mm_Hg)
