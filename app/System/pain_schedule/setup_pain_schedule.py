from app.constants.CONSTANTS import HISTORY_LENGTH, MAX_NUM_SCHEDULES, DEBUG
from app.filereaders.ScheduleReader import ScheduleReader
from app.filereaders.PressureReader import PressureReader
from collections import deque

from app.constants.CONSTANTS import HISTORY_LENGTH, MAX_NUM_SCHEDULES

imported_schedule = []
for i in range(0, MAX_NUM_SCHEDULES):
    imported_schedule.append([])

# Returns the user-provided pressure parameter values as a dictionary with keys of PMAX, PAINL, PAINH, PATM
pressure_parameters = PressureReader().read(filename="./app/input_files/Pressure_Values.txt")
painl = int(pressure_parameters['PAINVALUE'] - pressure_parameters['PAINTOLERANCE'])
painh = int(pressure_parameters['PAINVALUE'] + pressure_parameters['PAINTOLERANCE'])

print("pressure_parameters", pressure_parameters, "painh=", painh, "and painl=", painl)

# Returns an array of tuples, with the desired action of Pain/Nil and the duration of each of those actions
imported_schedule = ScheduleReader().read(filename="./app/input_files/Schedule.txt",
                                          file_schedule=imported_schedule)
max_num_schedules = len(imported_schedule)
print("main read imported_schedule:", imported_schedule)

current_counter = [0] * max_num_schedules
for phase in range(0, MAX_NUM_SCHEDULES):
    current_counter[phase] = imported_schedule[phase][1]

Global_cnt = 0
state_history = [None] * HISTORY_LENGTH
past_states = deque(state_history, HISTORY_LENGTH)
schedule_finished = False


