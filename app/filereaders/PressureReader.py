from app.constants.CONSTANTS import MAX_NUM_PARAMETERS, PRESSURE_TYPES


class PressureReader:
    def read(self, filename):
        with open(filename) as file:
            lines = [line.rstrip() for line in file.readlines()]
            if (len(lines) > MAX_NUM_PARAMETERS):
                raise ValueError(self.getErrorMessage(lines))
            else:
                actions_list = [line.split("_") for line in lines]
                actions = dict(line.strip().split("_") for line in lines)
                if (set(PRESSURE_TYPES) >= set(actions.keys())):
                    if (actions['PMAX'] > actions['PAINL'] and actions['PAINL'] < actions['PAINH'] and actions[
                        'PAINH'] < actions['PMAX']):
                        return actions
                    else:
                        raise ValueError(self.getErrorMessage(lines))
                else:
                    raise ValueError(self.getErrorMessage(lines))

    def getErrorMessage(self, lines):
        return str(
            "You have: " + str(len(lines)) + " lines in the file. "
                                             "Max is: " + str(MAX_NUM_PARAMETERS) + "\n"
                                                                                    "Order is " + str(lines) + "\n"
                                                                                                               "Only 4 value types are allowed [in any order]: PAINH_xxx, PAINL_xxx, PATM_xxx, PMAX_xxx [xxx is given in mm Hg]\n"
                                                                                                               "ALSO! Need PMAX > PAINH > PAINL > Patm"
        )
