class ScheduleReader:
    def read(self):
        filename = 'Schedule.txt'
        with open(filename, 'r') as f:
            f.seek(0)
            lines = f.readlines()
            num_lines = len(lines)
            print "\nRead file", filename, ": ", lines
            # print "\ndetected ",  num_lines,  " lines of schedule"
            if (num_lines > Max_num_schedules):
                # Check that there are no more than the allowed number of schedules (no blank lines are allowed in the file either)
                raise ValueError("Only a total of ", Max_num_schedules,
                                 " schedule statement lines are allowed in the file [", num_lines,
                                 " lines were detected]")
                sys.exit('Error!: Too many schedules')

            for i in range(0, Max_num_schedules):
                action, value = (lines[i].strip()).split("_", 1)
                value = int(value)
                # Before adding action, check to ensure it is either PAIN or NIL (no other labels supported)
                # Exit the program with an error message, if not
                if (action == 'PAIN' or action == 'NILL'):
                    pain_schedule.append(action)
                else:
                    raise ValueError("Only NILL or PAIN actions are allowed! [e.g. NILL_60 or PAIN_999], but [", action,
                                     "] was detected")
                    sys.exit("error!: Only NILL or PAIN actions are allowed!")
                # Before adding value, make sure that it is between 0 and 999 and exit otherwise
                # print ("value=", value)
                if (value >= 0 and value <= 999):
                    time_schedule.append(value)
                else:
                    raise ValueError("Interval values, measured in seconds, must be in range [0,999], but a value of [",
                                     value, "] was detected")
                    sys.exit('Error!: Interval value not in range [0,999]')

            print "\nPain and time schedules:"
            print (pain_schedule)
            print (time_schedule)
        # for i in range (0,7):
        # action, value = (lines[i].strip('\n')).split("_",1)
        # pain_schedule.append(action)
        # time_schedule.append(value)
        # print (pain_schedule)
        # print (time_schedule)