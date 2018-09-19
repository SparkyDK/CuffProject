from app.filereaders.ScheduleReader import ScheduleReader
from app.filereaders.PressureReader import PressureReader
from collections import deque

from app.constants.CONSTANTS import HISTORY_LENGTH, MAX_NUM_SCHEDULES

class pain_schedule:
    def __init__(self):
        pass

    def setup_pain_schedule(self, control_args, pressure_parameters):
        self.control_args = control_args
        self.pressure_parameters = pressure_parameters
        imported_schedule = []
        for i in range(0, MAX_NUM_SCHEDULES):
            imported_schedule.append([])

        # Returns the user-provided pressure parameter values as a dictionary
        # with keys of PMAX, PAINVALUE, PAINTOLERANCE, PATM
        self.pressure_parameters = PressureReader().read(filename="./app/input_files/Pressure_Values.txt")

        # Returns an array of tuples, with the desired action of Pain/Nil and the duration of each of those actions
        self.imported_schedule = ScheduleReader().read(filename="./app/input_files/Schedule.txt",
                                                  file_schedule=imported_schedule)
        max_num_schedules = len(imported_schedule)
        print("main read imported_schedule:", imported_schedule)
        if (MAX_NUM_SCHEDULES != max_num_schedules):
            print ("The configured number of schedules is not the required value of:", MAX_NUM_SCHEDULES)
            exit(1)

        self.current_counter = [0] * max_num_schedules

        for phase in range(0, MAX_NUM_SCHEDULES):
            self.current_counter[phase] = imported_schedule[phase][1]

        self.Global_cnt = 0
        self.schedule_finished = 0

        return (self.current_counter, self.imported_schedule, self.Global_cnt,
                self.schedule_finished, self.pressure_parameters)

    def execute_pain_schedule(self, control_args, schedule, schedule_finished, current_counter):
        self.control_args = control_args
        self.schedule = schedule
        self.schedule_finished = schedule_finished
        self.current_counter = current_counter

        pain_phase = self.control_args['SCHEDULE_INDEX']

        if (pain_phase < MAX_NUM_SCHEDULES and self.schedule_finished == 0):
            # Not finished the schedule yet
            # Don't really need to be set again every second for each phase
            # Could just do it for the very first second of each phase
            if (self.control_args['PAUSE'] == 1):
                # No pain permitted in Pause mode
                self.control_args['PAIN'] = 0
            else:
                if (self.imported_schedule[pain_phase][0] == 'PAIN'):
                    self.control_args['PAIN'] = 1
                else:
                    self.control_args['PAIN'] = 0

            if (self.current_counter[pain_phase] > 1):
                # Current schedule phase still not complete
                self.current_counter[pain_phase] -= 1
                print("\tSchedule Counter adjusted: Schedule:", pain_phase,
                      " with counter value = ", self.current_counter[pain_phase],
                      " and pain set to ", self.control_args['PAIN'])
            else:
                # Current phase is now complete (Current_counter value is zero ... or negative)
                # Reset the displayed/current value back to the starting value
                # Leave it negative to indicate overall progress (and simplify graphics processing)
                # and then go to the next phase of the schedule
                print("Finished schedule phase ", pain_phase, "\n")
                self.current_counter[pain_phase] = \
                    -1 * self.imported_schedule[pain_phase][1]
                self.control_args['SCHEDULE_INDEX'] += 1
        else:
            # Done executing the schedule sequence ... could leave most of this stuff out of here and
            # just use the schedule_finished
            self.control_args['SCHEDULE_INDEX'] = 0
            self.control_args['PAIN'] = 0
            self.control_args['STARTED'] = 0
            self.control_args['PAUSE'] = 0
            self.schedule_finished = 1

        return (self.control_args, self.schedule_finished, self.current_counter)
