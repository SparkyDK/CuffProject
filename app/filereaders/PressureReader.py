from app.constants.CONSTANTS import MAX_NUM_PARAMETERS, PRESSURE_TYPES
class PressureReader:
    def read(self, filename):
        with open (filename) as file:
            lines = [line.rstrip() for line in file.readlines()]
            if (len(lines) > MAX_NUM_PARAMETERS):
                print("Too many parameters")
                raise ValueError(self.getErrorMessage(lines))
            else:
                actions_list = [line.split("_") for line in lines]
                actions = dict(line.strip().split("_") for line in lines)
                if (len(actions) != MAX_NUM_PARAMETERS):
                    print(len(actions), " parameters were provided, instead of ", MAX_NUM_PARAMETERS,
                          " of them!")
                print ("PRESSURE_TYPES: ", set(PRESSURE_TYPES) )
                print ("actions.keys: ", actions.keys() )
                if(set(PRESSURE_TYPES) >= set(actions.keys())):
                    painl = actions['PAINVALUE'] - actions['PAINTOLERANCE']
                    painh = actions['PAINVALUE'] + actions['PAINTOLERANCE']
                    if (actions['PMAX'] > painh and painl < painh and actions['PATM'] < painl):
                        print ("Read the pressure parametric values:", actions)
                        return actions
                    else:
                        print ("Not sure what happened here with pressure values")
                        raise ValueError(self.getErrorMessage(lines))
                else:
                    print("Not sure what happened")
                    raise ValueError(self.getErrorMessage(lines))

    def getErrorMessage(self, lines):
        return str(
            "You have: " + str(len(lines)) + " lines in the file. "
            "Require: " + str(MAX_NUM_PARAMETERS) + "\n"
            "Order is " + str(lines) + "\n"
            "Only 4 value types are allowed [in any order]: PAINVALUE_xxx, PAINTOLERANCE_xxx, PATM_xxx, PMAX_xxx [xxx is given in mm Hg]\n"
            "ALSO! Need PMAX > PAINVALUE+PAINTOLERANCE > PAINVALUE-PAINTOLERANCE > Patm"
        )