from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')

from app.constants.CONSTANTS import HISTORY_LENGTH, MAX_NUM_SCHEDULES, DEBUG
from app.filereaders.ScheduleReader import ScheduleReader
from app.filereaders.PressureReader import PressureReader
from app.pain_schedule.pain_schedule import pain_schedule
from app.GUI.GUI import DisplayApp

from app.System import System

import time
from collections import deque
import math

def Read_Cuff_Pressure(control_args, past_states):
    mycontrol_args = control_args
    mypast_states = past_states
    # Do the A/D conversion and read the converted value
    if (DEBUG == False):
        pass  # Add the A/D read instruction here to set up the real sampled digital_pressure_value
        digital_pressure_value = 17000
        mycontrol_args['PRESSURE'] = Convert_to_mm_Hg(digital_value=digital_pressure_value)
    else:
        # DEBUG
        pressure_value = 0.0
        if (mypast_states[4] == "CONNECT_CUFF" and mypast_states[3] == "LOAD_RESERVOIR"):
        # Controlled pressure increase
            pressure_value = int(mycontrol_args['PRESSURE']) + 25
        elif (mypast_states[4] == "RELEASE" and mypast_states[3] == "CONNECT_CUFF"):
        # Controlled pressure release path
            pressure_value = int(mycontrol_args['PRESSURE']) - 10
        elif (mypast_states[4] == "RELEASE" and mypast_states[3] == "LOAD_RESERVOIR"):
        # Controlled pressure release path (in case of leaks)
            pressure_value = int(mycontrol_args['PRESSURE']) - 10
        elif (mypast_states[4] == "VENT"):
        # Venting case
            pressure_value = int(control_args['PATM'])
        else:
        # Don't change the pressure value at all
            pressure_value = mycontrol_args['PRESSURE']
        mycontrol_args['PRESSURE'] = pressure_value

    return ( mycontrol_args )

def Convert_to_mm_Hg(digital_value):
    # Convert to mm of Hg and return the value using an interpolated table of values, determined empirically
    return (digital_value/1000)

imported_schedule = []
for i in range(0, MAX_NUM_SCHEDULES):
    imported_schedule.append([])

# Returns the user-provided pressure parameter values as a dictionary with keys of PMAX, PAINL, PAINH, PATM
pressure_parameters = PressureReader().read(filename="./tests/input_files/Pressure_Values.txt")
painl = int(pressure_parameters['PAINVALUE'] - pressure_parameters['PAINTOLERANCE'])
painh = int(pressure_parameters['PAINVALUE'] + pressure_parameters['PAINTOLERANCE'])

print ("pressure_parameters", pressure_parameters, "painh=", painh, "painl=", painl)

# Returns an array of tuples, with the desired action of Pain/Nil and the duration of each of those actions
imported_schedule = ScheduleReader().read( filename="./tests/input_files/Schedule.txt", file_schedule=imported_schedule )
max_num_schedules = len(imported_schedule)
print ("main read imported_schedule:", imported_schedule)

current_counter = [0] * max_num_schedules
for i in range(0, MAX_NUM_SCHEDULES):
    current_counter[i] = imported_schedule[i][1]

Global_cnt = 0
state_history = [None] * HISTORY_LENGTH
past_states = deque(state_history, HISTORY_LENGTH)
pain_required = False
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
#time.clock()
time.process_time()
elapsed_time = 0

gui = DisplayApp()
# Not sure why this run method is not working, but it hangs my machine
# gui.run()

while (True == True):

    Global_cnt += 1
    #print ("Global_cnt=", Global_cnt)

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
    second_tickover = False
    if ( math.floor(elapsed_time) != math.floor(old_elapsed_time) ):
        second_tickover = True
        # Only process the pain schedule each time a second ticks over to the next truncated value
        # print (control_args)
        print("*********** (", Global_cnt, ") Elapsed time:", elapsed_time)
        control_args = pain_schedule().update(current_counter, control_args, user_args)
        # print (control_args2)

    # Read the current air pressure in the patient's cuff
    control_args = Read_Cuff_Pressure(control_args, past_states)

    # Poll for user input and update the GUI based on the control arguments
    # Then update the user signals: {'GO','STOP','ABORT','override_pressure','OVERRIDE'} appropriately
    old_user_args = user_args
    user_args = gui.update(Global_cnt, current_counter, control_args, user_args)

    # Update or override the control signals: {'PAIN','STARTED','SCHEDULE_INDEX','PAUSE','FORCE'}
    # Execute the state machine that implements the control decisions with updated control signals and pressure value
    try:
        old_control_args = control_args
        control_args, current_counter, schedule_finished = \
            airctrl.FSM.ControlDecisions(current_counter, imported_schedule, control_args, old_user_args, user_args,
                                         pressure_parameters, painh, painl, second_tickover)
        if (schedule_finished == True): airctrl.FSM.SetState("ISOLATE_VENT")
        airctrl.FSM.Execute(control_args)

    except KeyboardInterrupt:
        print("\nDone")

    if (Global_cnt == 5100):
        exit(0)
