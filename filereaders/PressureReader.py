class PressureReader:

    def read(self):
        filename = 'Pressure_Values.txt'
        with open(filename, 'r') as file:
            file.seek(0)
            lines = file.readlines()
            num_lines = len(file.readlines())
            print "\nRead file ", filename, ": ", lines, "\n"
            if (num_lines > Max_num_Parameters):
                # Check that there are no more than the allowed number of parameter entries (no blank lines are allowed in the file either)
                raise ValueError("Only a total of ", Max_num_Parameters, " lines allowed in the file")
                sys.exit('Error!: Too many parameters lines provided in the file')

            for i in range(0, Max_num_Parameters):
                action, value = (lines[i].strip()).split("_", 1)
                if (action in d):
                    # Check that the action is one that is supported
                    d[action] = value
                    i += 1
                else:
                    # Exit the program with an appropriate error message, if not
                    raise ValueError(
                        "Only 4 value types are allowed [in any order]: PAINH_xxx, PAINL_xxx, PATM_xxx, PMAX_xxx [xxx is given in mm Hg]")
                    sys.exit('Error!: Not a supported pressure parameter type')
                    # Use these variables instead of the dictionary entry values, as a short-form convenience
            print "d:", d
            Pmax = int(d['PMAX'])
            Pup = int(d['PAINH'])
            Plow = int(d['PAINL'])
            Patm = int(d['PATM'])

            # print "Pmax=",  Pmax,  " Pup=",  Pup,  " Plow=",  Plow,  "Patm=",  Patm

            if (Patm < Plow and Plow < Pup and Pup < Pmax):
                # Ensure that the values are correctly sized, relative to each other (i.e. Pmax is bigger than Pup, Pup is bigger than Plow,... etc.)
                print "Pmax=", Pmax, " Pup=", Pup, " Plow=", Plow, " and Patm=", Patm
            else:
                raise ValueError("Need Pmax > Pup > Plow > Patm but, instead, have Pmax=", Pmax, "Pup=", Pup, " Plow=",
                                 Plow, " and Patm=", Patm)
                sys.exit('Error!: Need Pmax > Pup > Plow > Patm')

            print "\n"