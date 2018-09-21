from app.constants.CONSTANTS import MAX_NUM_PHASES, SCHEDULE_TYPES


class ScheduleReader2:
    def read(self, filename):
        with open(filename, 'r') as file:
            lines = [line.rstrip() for line in file.readlines()]
            if (len(lines) > MAX_NUM_PHASES):
                raise ValueError(self.getErrorMessage(lines))
            else:
                schedule_list = [line.split("_") for line in lines]
                schedule_dict = dict(line.strip().split("_") for line in lines)

                # Make sure that pain and nill are the only things inside of the schedule
                if set(SCHEDULE_TYPES) >= set(schedule_dict.keys()):
                    if all(int(i) > 0 for i in schedule_dict.values()) and all(
                            int(i) < 999 for i in schedule_dict.values()):
                        return schedule_list
                    else:
                        raise ValueError(self.getErrorMessage(lines))
                else:
                    raise ValueError(self.getErrorMessage(lines))

    def getErrorMessage(self, lines):
        print("There was an error parsing the file")
        print("Lines: " + str(lines))
