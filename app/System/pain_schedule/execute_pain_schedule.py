def execute_pain_schedule(self, control_args, schedule, schedule_finished):
    self.control_args = control_args
    self.schedule = schedule
    self.schedule_finished = schedule_finished

    if (self.control_args['SCHEDULE_INDEX'] < MAX_NUM_SCHEDULES and schedule_finished == False):
        # Not finished the schedule yet
        # Don't really need to be set again every second for each phase
        # Could just do it for the very first second of each phase
        if (self.control_args['PAUSE'] == 1):
            # No pain permitted in Pause mode
            self.control_args['PAIN'] = 0
        else:
            if (self.schedule[self.control_args['SCHEDULE_INDEX']][0] == 'PAIN'):
                self.control_args['PAIN'] = 1
            else:
                self.control_args['PAIN'] = 0

        if (self.current_counter[self.control_args['SCHEDULE_INDEX']] > 1):
            # Current schedule phase still not complete
            self.current_counter[self.control_args['SCHEDULE_INDEX']] -= 1
            print("\tSchedule Counter adjusted: Schedule:", self.control_args['SCHEDULE_INDEX'],
                  " with counter value = ", self.current_counter[self.control_args['SCHEDULE_INDEX']],
                  " and pain set to ", self.control_args['PAIN'])
        else:
            # Current phase is now complete (Current_counter value is zero ... or negative)
            # Reset the displayed/current value back to the starting value
            # Leave it negative to indicate overall progress (and simplify graphics processing)
            # and then go to the next phase of the schedule
            print("Finished schedule phase ", self.control_args['SCHEDULE_INDEX'], "\n")
            self.current_counter[self.control_args['SCHEDULE_INDEX']] = \
                -1 * self.schedule[self.control_args['SCHEDULE_INDEX']][1]
            self.control_args['SCHEDULE_INDEX'] += 1
    else:
        # Done executing the schedule sequence ... could leave most of this stuff out of here and
        # just use the schedule_finished
        print("Finished executing schedule")
        self.control_args['SCHEDULE_INDEX'] = 0
        self.control_args['PAIN'] = 0
        self.control_args['STARTED'] = 0
        self.control_args['PAUSE'] = 0
        self.schedule_finished = True
    return (self.control_args, self.schedule_finished)
