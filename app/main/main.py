#from kivy.config import Config
#Config.set('kivy', 'keyboard_mode', 'systemandmulti')


from app.constants.CONSTANTS import HISTORY_LENGTH, MAX_NUM_SCHEDULES, DEBUG
from app.filereaders.ScheduleReader import ScheduleReader
from app.filereaders.PressureReader import PressureReader
from app.filereaders.A_to_D_lookup_table import A_to_D_lookup
from app.GUI.GUI import DisplayApp
from app.System.A_to_D.pyads1256 import ADS1256

from app.GUI.HelloWorldGraphic import HelloWorldApp

from app.System import System

import time
from collections import deque
import math

#import sys
#from ADS1256_definitions import *
#from pipyadc import ADS1256

# Allows interpolation between empirically-determined pressure transducer values and mm_Hg values
from scipy import interpolate
# import numpy as np

import threading
#import msvcrt

from pynput import keyboard

def kbd_input(*args, **kwargs):
    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()

def on_press(key):
    try:
        pass
        #print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        pass
        #print('special key {0} pressed'.format(key))

keypress = None
old_keypress = None
toggle = 0

def on_release(key):
    global keypress
    #print('{0} released'.format(key))
    keypress = format(key)
    #keypress = key
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def Read_Cuff_Pressure(control_args, past_states):
    mycontrol_args = control_args
    mypast_states = past_states

    # Do the A/D conversion and read the converted value
    if (DEBUG == False):
        pass  # Add the A/D read instruction here to set up the real sampled digital_pressure_value
        # digital_pressure_value = polled value or handled interrupt value after sensing and A/D conversion
        # It may also be necessary to average/filter the value, depending on its stability/performance ... TBD
        digital_pressure_value = 16000000  # debug only!
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

        # test_value = 16000000
        # interpolated_value = Convert_to_mm_Hg(digital_value=test_value)

    return ( mycontrol_args )

def Convert_to_mm_Hg(digital_value):
    digital_input = digital_value
    # Convert to mm of Hg and return the value using an interpolated table of values, determined empirically
    # Assume that we have a 24-bit A/D, which results in values in a range of [0, 16777216]
    digital_values, mmHg_values = A_to_D_lookup().read(filename="./app/input_files/A_to_D_lookup_table.txt")

    length = len(digital_values)
    for i in range (0, length):
    # convert to integers
        digital_values[i] = int(digital_values[i])
        mmHg_values[i] = int(mmHg_values[i])

    interpolation_function = interpolate.interp1d(digital_values, mmHg_values)

    #print ("Starting lookup table values are:", digital_values, mmHg_values)
    interpolated_value = math.floor( interpolation_function(digital_input) )
    #print ("Took in ", digital_input, " and interpolated it to a corresponding mm Hg value of", interpolated_value)

    return ( interpolated_value )

# old_keypress, user_args, control_args, toggle = \
#    keyboard_test(keypress, old_keypress, user_args, old_user_args, control_args, pressure_parameters, toggle)
# return (old_keypress, user_args, control_args, toggle)
def keyboard_test(keypress, old_keypress, user_args, old_user_args, control_args, pressure_parameters, toggle):
    # Use the keyboard to simulate user inputs from the touch screen

    if (keypress != old_keypress):
        old_keypress = keypress
        print("New key pressed: ", keypress)
    # user_args = {'GO': 0, 'STOP': 0, 'ABORT': 0, 'UP': 0, 'DOWN': 0,
    #             'override_pressure': pressure_parameters['PAINVALUE'], 'OVERRIDE': 0}

        if (keypress == "'x'"):
            print("'x' pressed")
            exit(0)
        elif (keypress == "'g'"):
            print("'g' pressed")
            if (user_args['GO'] == 1):
                user_args['GO'] = 0
            else:
                user_args['GO'] = 1
        elif (keypress == "'s'"):
            print("'s' pressed")
            if (user_args['STOP'] == 1):
                user_args['STOP'] = 0
            else:
                user_args['STOP'] = 1
        elif (keypress == "'a'"):
            print("'a' pressed")
            if (user_args['ABORT'] == 1):
                user_args['ABORT'] = 0
            else:
                user_args['ABORT'] = 1
        elif (keypress == "'u'"):
            print("'u' pressed")
            if (user_args['UP'] == 1):
                user_args['UP'] = 0
            else:
                user_args['UP'] = 1
        elif (keypress == "'d'"):
            print("'d' pressed")
            if (user_args['DOWN'] == 1):
                user_args['DOWN'] = 0
            else:
                user_args['DOWN'] = 1
        elif (keypress == "'r'"):
            control_args['PRESSURE'] += pressure_parameters['PAINTOLERANCE']
            print("'r' pressed to raise the pressure value to ", control_args['PRESSURE'])
        elif (keypress == "'l'"):
            control_args['PRESSURE'] -= pressure_parameters['PAINTOLERANCE']
            print("'l' pressed to lower the pressure value to ", control_args['PRESSURE'])
        elif (keypress == "'o'"):
            print("'o' pressed")
            user_args['override_pressure'] = 850
            if (user_args['OVERRIDE'] == 1):
                user_args['OVERRIDE'] = 0
            else:
                user_args['OVERRIDE'] = 1
        else:
            pass
        print("____________________________________________")
        print("Toggled something (old):", old_user_args)
        print("Toggled something (new):", user_args)
        print("____________________________________________")
        toggle += 1
        time.sleep(1)
    return(old_keypress, user_args, control_args, toggle)

# _____________________________________________________________________________________________________

imported_schedule = []
for i in range(0, MAX_NUM_SCHEDULES):
    imported_schedule.append([])

# Returns the user-provided pressure parameter values as a dictionary with keys of PMAX, PAINL, PAINH, PATM
pressure_parameters = PressureReader().read(filename="./app/input_files/Pressure_Values.txt")
painl = int(pressure_parameters['PAINVALUE'] - pressure_parameters['PAINTOLERANCE'])
painh = int(pressure_parameters['PAINVALUE'] + pressure_parameters['PAINTOLERANCE'])

print ("pressure_parameters", pressure_parameters, "painh=", painh, "and painl=", painl)

# Returns an array of tuples, with the desired action of Pain/Nil and the duration of each of those actions
imported_schedule = ScheduleReader().read( filename="./app/input_files/Schedule.txt", file_schedule=imported_schedule )
max_num_schedules = len(imported_schedule)
print ("main read imported_schedule:", imported_schedule)

current_counter = [0] * max_num_schedules
for phase in range(0, MAX_NUM_SCHEDULES):
    current_counter[phase] = imported_schedule[phase][1]

Global_cnt = 0
state_history = [None] * HISTORY_LENGTH
past_states = deque(state_history, HISTORY_LENGTH)
schedule_finished = False

# Initial PAUSE state is active, but not running a schedule.  A pain schedule can be restarted by pressing ABORT
control_args = {'SCHEDULE_INDEX': 0, 'PAIN': 0, 'STARTED': 0, 'PAUSE': 1, 'FORCE': 0,
                'PAINH': painh, 'PAINL': painl, 'PRESSURE': 0,
                'PATM': pressure_parameters['PATM'], 'PMAX': pressure_parameters['PMAX']}
user_args = {'GO': 0, 'STOP': 0, 'ABORT': 0, 'UP': 0, 'DOWN': 0,
             'override_pressure': pressure_parameters['PAINVALUE'], 'OVERRIDE': 0}
old_user_args = user_args.copy()

current_pressure = 0

# Create the system state machine that implements the control decisions
airctrl = System.System()
# Vent the cuff first
airctrl.FSM.SetState("ISOLATE_VENT")
airctrl.Execute(control_args)

# Initialize the timers
start_time = time.time()
time.process_time()
elapsed_time = 0

gui = DisplayApp()
# Not sure why this run method is not working, but it hangs my machine
gui.run()

kw_args = dict(value=0)
args = []
t = threading.Timer(0.01, kbd_input, args, kw_args)
t.start()

# Code from: https://github.com/ul-gh/PiPyADC/blob/master/example.py
# Set up the A/D
#ads = ADS1256()
### STEP 2: Gain and offset self-calibration:
#ads.cal_self()

# Using code taken from: https://github.com/SeanDHeath/PyADS1256
ads = ADS1256()
# Do a test read of the A/D ID register
myid = ads.ReadID()
if (DEBUG == True):
    print("A/D ID:", myid)

# Specify here an arbitrary length list (tuple) of arbitrary input channel pair
# eight-bit code values to scan sequentially from index 0 to last.
# Eight channels fit on the screen nicely for this example..
# CH_SEQUENCE = (POTI, LDR, EXT2, EXT3, EXT4, EXT7, POTI_INVERTED, SHORT_CIRCUIT)
# CH_SEQUENCE = (EXT2)

# works fine, but blocks
#gui2 = HelloWorldApp()
#gui2.run()

# Does not work
#g = threading.Timer(0.01, HelloWorldApp,)
#g.start()

while ( True == True ):

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
    if math.floor(elapsed_time) != math.floor(old_elapsed_time):
        # Only process the pain schedule each time a second ticks to the next truncated value
        second_tickover = True

        # Read pressure value here
        # Use the code example in: https://github.com/ul-gh/PiPyADC/blob/master/example.py
        ### STEP 3: Get data:
        # raw_channels = ads.read_sequence(CH_SEQUENCE)
        # voltages = [i * ads.v_per_digit for i in raw_channels]
        # print raw_channels, voltages

        pressure_value = ads.ReadADC()
        print ("Pressure value read at:", localtime, " =", pressure_value)

        print("*** <", old_keypress, ">a Elapsed: {0:.4f}".format(elapsed_time,), "\tctrl:", control_args)

        if (DEBUG == True):
        # Simulate user touch screen input with a regular keyboard
            old_keypress, user_args, control_args, toggle = \
                keyboard_test(keypress, old_keypress, user_args, old_user_args, control_args, pressure_parameters, toggle)

    # Read the current air pressure in the patient's cuff
    control_args = Read_Cuff_Pressure(control_args, past_states)

    # Poll for user input and update the GUI based on the control arguments
    # Then update the user signals: {'GO','STOP','ABORT','override_pressure','OVERRIDE'} appropriately
    old_user_args = user_args.copy()
    #user_args = gui.update(Global_cnt, current_counter, control_args, user_args)

    # Update or override the control signals: {'PAIN','STARTED','SCHEDULE_INDEX','PAUSE','FORCE'}
    # Execute the asynchronous part of the state machine that implements the control decisions
    # with the newly-updated control signals and newly-sampled pressure value
    try:
        old_control_args = control_args.copy()
        control_args, current_counter, pressure_parameters, schedule_finished, toggle = \
            airctrl.FSM.ControlDecisions(current_counter, imported_schedule, control_args, old_user_args, user_args,
                                         pressure_parameters, second_tickover, schedule_finished, toggle)
        if (schedule_finished == True):
            # At the end of the pain schedule, hold the state machine in the vent state and turn off pain
            # Could send it back to IDLE, as an alternative, but what if there is some residual pressure
            # in the cuff at the end of the experiment...
            airctrl.FSM.SetState("VENT")
            control_args['PAIN'] = 0

        # Execute the state machine
        airctrl.FSM.Execute(control_args)

    except KeyboardInterrupt:
        print("\nDone")
