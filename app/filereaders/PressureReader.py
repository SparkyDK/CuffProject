from app.constants.CONSTANTS import MAX_NUM_PARAMETERS, PRESSURE_TYPES

class PressureReader:
    def read(self, filename):
        with open(filename) as file:
            lines = [line.rstrip() for line in file.readlines()]
            print (lines)
            if (len(lines) > MAX_NUM_PARAMETERS):
                print("Too many parameters")
                raise ValueError(self.getErrorMessage(lines))
            else:
                actions_list = [line.split("_") for line in lines]
                actions = dict(line.strip().split("_") for line in lines)
                if (len(actions) != MAX_NUM_PARAMETERS):
                    print(len(actions), " parameters were provided, instead of ", MAX_NUM_PARAMETERS,
                          " of them!")
                    raise ValueError(self.getErrorMessage(lines))
                self.invalid_key = False
                for key, value in actions.items():
                    # Make sure that the actions in the file are exactly the ones expected
                    key = key.replace(u'\ufeff', '')
                    value = value.replace(u'\ufeff', '')
                    print ("DEBUG: key=", key, " and value=", value)
                    if key in PRESSURE_TYPES:
                        print ("key=", key, "and value=", value)
                    else:
                        print("No pressure type match for: ", key)
                        self.invalid_key = True
                        raise ValueError(self.getErrorMessage(lines))
                    actions[key] = int(value)

                if (self.invalid_key == False):
                    # if (set(PRESSURE_TYPES) >= set(actions.keys())):
                    painl = int(actions['PAINVALUE'] - actions['PAINTOLERANCE'])
                    painh = int(actions['PAINVALUE'] + actions['PAINTOLERANCE'])
                    #actions['PAINL'] = painl
                    #actions['PAINH'] = painh
                    print("Calculated upper pain threshold=", painh, " and lower threshold=", painl)
                    if (int(actions['PMAX']) > painh and painl < painh and int(actions['PATM']) < painl):
                        # print ("Read the pressure parametric values:", actions)
                        return actions
                    else:
                        print("Not sure what happened here with the pressure values")
                        raise ValueError(self.getErrorMessage(lines))
                else:
                    print("Not sure what happened here, but input file has issues")
                    raise ValueError(self.getErrorMessage(lines))

    def getErrorMessage(self, lines):
        return str(
            "You have: " + str(len(lines)) + " lines in the file. "
        "Require: " + str(MAX_NUM_PARAMETERS) + "\n"
        "Order is " + str(lines) + "\n"
        "Only 4 value types are allowed [in any order]: PAINVALUE_xxx, PAINTOLERANCE_xxx, PATM_xxx, PMAX_xxx [xxx is given in mm Hg]\n"
        "ALSO! Need PMAX > PAINVALUE+PAINTOLERANCE > PAINVALUE-PAINTOLERANCE > Patm"
        )
