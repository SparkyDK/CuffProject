from app.constants.CONSTANTS import MAX_NUM_PHASES, MAX_NUM_SCHEDULES

class ScheduleReader:
    # print("Created an instance of ScheduleReader")
    def read(self, filename, all_schedules, file_schedule):
        self.all_schedules = all_schedules
        self.file_schedule = file_schedule
        self.filename = filename
        # print("Attempting to read file ", filename, " with file_schedule=:", self.file_schedule)
        with open(filename, mode='r', encoding='utf-8-sig') as file:
            lines = [line.replace(r'\r', '') for line in file.readlines()]
            lines = [line.rstrip() for line in file.readlines()]
            print ("lines:\n", lines)
            exit(0)
            num_lines = len(lines)
            # print("File ", filename, " has ", num_lines, "lines:", lines)
            if (num_lines > MAX_NUM_PHASES*MAX_NUM_SCHEDULES):
                # Check that there are no more than the allowed number of schedules
                # (no blank lines are allowed in the file either)
                raise ValueError("Only a total of ", MAX_NUM_PHASES*MAX_NUM_SCHEDULES,
                                 " schedule statement lines are allowed in the file [", num_lines,
                                 " lines were detected]")
                sys.exit('Error!: Too many schedules')

            for s in range(0, MAX_NUM_SCHEDULES):
                phases = []
                for p in range(0, MAX_NUM_PHASES):
                    #print ("Processing line[",s,"][",p,"] :", lines[s*MAX_NUM_PHASES+p])
                    tuple = []
                    action, value = (lines[s*MAX_NUM_PHASES+p].strip()).split("_", 1)
                    schedule, action = (action.strip()).split(":", 1)
                    value = int(value)
                    schedule = int(schedule)
                    if (schedule != s+1):
                        raise ValueError("Schedule numbers read from the file need to increase monotonically from 1",
                                         "A value of ", schedule, " was read from the file, but", s+1, " was expected")
                        sys.exit("error!: Non-sequential schedule number!")

                    #print ("schedule =", schedule, "action =", action, "value =", value)
                    # print (i, ": action=", action, ":value=", (value))
                    # Before adding schedule, check to ensure it is in the range of supported numbers of schedules
                    # Exit the program with an error message, if not
                    if (schedule > 0 and schedule <= MAX_NUM_SCHEDULES):
                        tuple.append(schedule)
                    else:
                        raise ValueError("Only a limited number (", MAX_NUM_SCHEDULES, ") of schedules are supported",
                                         "but a schedule value of ", schedule, " found in the file outside this range")
                        sys.exit("error!: Illegal schedule number!")
                    # Before adding action, check to ensure it is either PAIN or NIL (no other labels supported)
                    # Exit the program with an error message, if not
                    if (action == 'PAIN' or action == 'NILL'):
                        tuple.append(action)
                    else:
                        raise ValueError("Only NILL or PAIN actions allowed! [e.g. NILL_60 or PAIN_999], but [", action,
                                         "] was detected")
                        sys.exit("error!: Only NILL or PAIN actions are allowed!")
                    # Before adding value, make sure that it is between 0 and 999 and exit otherwise
                    # print ("value=", value)
                    if (value >= 0 and value <= 999):
                        tuple.append(value)
                    else:
                        raise ValueError("Interval values, measured in seconds, in range [0,999], but a value of [",
                                         value, "] was detected")
                        sys.exit('Error!: Interval value not in range [0,999]')
                    phases.append(tuple)
                self.all_schedules.insert(s,phases)
                if (s == 0):
                     self.file_schedule = phases

        #print ("File schedule: ", self.file_schedule)
        #print ("All schedules: ", self.all_schedules)
        return (self.all_schedules, self.file_schedule)
