from app.constants.CONSTANTS import MAX_NUM_PHASES, MAX_NUM_SCHEDULES

class ScheduleReader:
    # print("Created an instance of ScheduleReader")
    def read(self, filename, file_schedule):
        self.file_schedule = file_schedule
        self.filename = filename
        # print("Attempting to read file ", filename, " with file_schedule=:", self.file_schedule)
        with open(filename, 'r') as file:
            lines = [line.rstrip() for line in file.readlines()]
            num_lines = len(lines)
            # print("File ", filename, " has ", num_lines, "lines:", lines)
            if (num_lines > MAX_NUM_PHASES*MAX_NUM_SCHEDULES):
                # Check that there are no more than the allowed number of schedules (no blank lines are allowed in the file either)
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
                    #print ("schedule =", schedule, "action =", action, "value =", value)
                    # print (i, ": action=", action, ":value=", (value))
                    # Before adding schedule, check to ensure it is in the range of supported numbers of schedules
                    # Exit the program with an error message, if not
                    if (schedule > 0 and schedule <= MAX_NUM_SCHEDULES):
                        #self.file_schedule[p].append(schedule)
                        tuple.append(schedule)
                    else:
                        raise ValueError("Only a limited number of (", MAX_NUM_SCHEDULES, ") schedules are supported",
                                         "but a schedule value of ", schedule, " was found in the file outside this range")
                        sys.exit("error!: Illegal schedule number!")
                    # Before adding action, check to ensure it is either PAIN or NIL (no other labels supported)
                    # Exit the program with an error message, if not
                    if (action == 'PAIN' or action == 'NILL'):
                        #self.file_schedule[p].append(action)
                        tuple.append(action)
                    else:
                        raise ValueError("Only NILL or PAIN actions are allowed! [e.g. NILL_60 or PAIN_999], but [", action,
                                         "] was detected")
                        sys.exit("error!: Only NILL or PAIN actions are allowed!")
                    # Before adding value, make sure that it is between 0 and 999 and exit otherwise
                    # print ("value=", value)
                    if (value >= 0 and value <= 999):
                        #self.file_schedule[p].append(value)
                        tuple.append(value)
                    else:
                        raise ValueError("Interval values, measured in seconds, must be in range [0,999], but a value of [",
                                         value, "] was detected")
                        sys.exit('Error!: Interval value not in range [0,999]')
                    phases.append(tuple)
                    #print ("tuple:", tuple)
                #print ("phases:",phases)
                self.file_schedule.insert(s,phases)

            #print ("file_schedule:",self.file_schedule)

        # print ("File schedule: ", self.file_schedule)
        return (self.file_schedule)
