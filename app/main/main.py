from app.constants.CONSTANTS import HISTORY_LENGTH, MAX_NUM_SCHEDULES, DEBUG
from app.filereaders.ScheduleReader import ScheduleReader
from app.filereaders.PressureReader import PressureReader
from app.pain_schedule.pain_schedule import pain_schedule
from app.GUI.GUI import Display

from app.System import System

import time
from collections import deque
import math

def Read_Cuff_Pressure():
    # Do the A/D conversion and read the converted value
    pressure_value = 50
    converted_value = Convert_to_mm_Hg(digital_value=pressure_value)
    return (converted_value)

def Convert_to_mm_Hg(digital_value):
    # Convert to mm of Hg and return the value using an interpolated table of values, determined empirically
    return (3*digital_value)

imported_schedule = []
for i in range(0, MAX_NUM_SCHEDULES):
    imported_schedule.append([])
print("TEST:", imported_schedule)

# Returns the user-provided pressure parameter values as a dictionary with keys of PMAX, PAINL, PAINH, PATM
pressure_parameters = PressureReader().read(filename="./tests/input_files/Pressure_Values.txt")
painl = int(pressure_parameters['PAINVALUE'] - pressure_parameters['PAINTOLERANCE'])
painh = int(pressure_parameters['PAINVALUE'] + pressure_parameters['PAINTOLERANCE'])

print ("pressure_parameters", pressure_parameters, "painh=", painh, "painl=", painl)

# Returns an array of tuples, with the desired action of Pain/Nil and the duration of each of those actions
imported_schedule = ScheduleReader().read( filename="./tests/input_files/Schedule.txt", file_schedule=imported_schedule )
max_num_schedules = len(imported_schedule)
print ("main read imported_schedule:", imported_schedule)

Global_cnt = 0
state_history = [None] * HISTORY_LENGTH
past_states = deque(state_history, HISTORY_LENGTH)
pain_required = False
current_counter = [0] * max_num_schedules
control_args = {'SCHEDULE_INDEX': 0, 'PAIN': 0, 'STARTED': 0, 'PAUSE': 0, 'FORCE': 0,
                'PAINH': painh, 'PAINL': painl, 'PRESSURE': 0,
                'PATM': pressure_parameters['PATM'], 'PMAX': pressure_parameters['PMAX']}
user_args = {'GO': 0, 'STOP': 0, 'ABORT': 0, 'UP': 0, 'DOWN': 0,
             'override_pressure': pressure_parameters['PAINVALUE'], 'OVERRIDE': 0}
current_pressure = 0

try:
    # Create the system state machine that implements the control decisions
    airctrl = System.System()
    # Vent the cuff first
    airctrl.FSM.SetState("ISOLATE_VENT")
    airctrl.Execute(control_args)
except KeyboardInterrupt:
    print("\nDone")

# Initialize the timers
start_time = time.time()
time.clock()
elapsed_time = 0

gui = Display()
gui.__init__()

while (True == True):

    # Keep a state history
    returned_state = airctrl.FSM.GetCurState()
    # pop out the highest-index entry from the state history
    past_states.popleft()
    # Add the newest state value to the lowest-index entry of the state history
    past_states.append(returned_state)

    localtime = time.asctime(time.localtime(time.time()))
    if (DEBUG == True and True == False):
    #if (DEBUG == True):
        #    if (DEBUG==True):
        print (localtime, " (elapsed=", elapsed_time)

    # localtime = time.asctime(time.localtime(time.time()) )
    old_elapsed_time = elapsed_time
    elapsed_time = time.time() - start_time
    if ( math.floor(elapsed_time) != math.floor(old_elapsed_time) ):
        # Only process the pain schedule every time a second ticks
        print (control_args)
        control_args2 = pain_schedule().update(current_counter, control_args, user_args)
        print (control_args2)

    # Read the current air pressure in the patient's cuff
    control_args['Pressure'] = Read_Cuff_Pressure()

    # Poll for user input and update the GUI based on the control arguments
    # Then update the user signals: {'GO','STOP','ABORT','override_pressure','OVERRIDE'} appropriately
    old_user_args = user_args
    user_args = gui.update(current_counter, control_args, user_args)

    # Update or override the control signals: {'PAIN','STARTED','SCHEDULE_INDEX','PAUSE','FORCE'}
    # Execute the state machine that implements the control decisions with updated control signals and pressure value
    try:
        old_control_args = control_args
        control_args, current_counter = airctrl.FSM.ControlDecisions(current_counter, imported_schedule,
                                                                     control_args, user_args,
                                                                     pressure_parameters, painh, painl)
        airctrl.FSM.Execute(control_args)

    except KeyboardInterrupt:
        print("\nDone")
