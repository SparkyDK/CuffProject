from app.constants.CONSTANTS import MAX_NUM_PARAMETERS
from app.filereaders.ScheduleReader import ScheduleReader
from app.filereaders.PressureReader import PressureReader

# Returns the user-provided pressure parameter values as a dictionary with keys of PMAX, PAINL, PAINH, PATM
pressure_parameters = PressureReader().read(filename="./tests/input_files/Pressure_Values.txt")

# Returns an array of tuples, with the desired action of Pain/Nil and the duration of each of those actions
schedule = ScheduleReader().read(time_schedule, filename="./tests/input_files/Schedule.txt")
max_num_schedules = len(schedule)

DEBUG = True
Global_cnt = 0
past_states = [] * 5
pain_required = False
current_counter = [] * max_num_schedules
control_args = {'SCHEDULE_INDEX': 0, 'PAIN': 0, 'STARTED':0, 'PAUSE':0, 'FORCE':0}
user_args = {'GO' : 0, 'STOP': 0, 'ABORT': 0, 'override_pressure': pressure_parameters['PATM'], 'OVERRIDE':0}
current_pressure = None

try:
    # Create the system state machine
    sm = System()
    # Vent the cuff first
    sm.FSM.SetState("ISOLATE_VENT")
except KeyboardInterrupt:
    print("\nDone")

# Initialize the timers
start_time = time.time()
time.clock()
elapsed_time = 0

while (True == True):

    # Keep a state history
    returned_state = sm.FSM.GetCurState()
    # pop out the highest-index entry from the state history
    past_states.popleft()
    # Add the newest state value to the lowest-index entry of the state history
    past_states.append(returned_state)

    # localtime = time.asctime(time.localtime(time.time()) )
    old_elapsed_time = elapsed_time
    elapsed_time = time.time() - start_time
    if ( math.floor(elapsed_time) != math.floor(old_elapsed_time) ):
        # Only process the schedule every new second tick
        # Update the PAIN, STARTED, SCHEDULE_INDEX, PAUSE fields of the control arguments and current_counter values
        (control_args) = schedule.Execute(current_counter, control_args, user_args)

    # Read the current air pressure in the patient's cuff
    current_pressure = Read_Cuff_Pressure()

    # Poll for user input and update the GUI based on the control arguments
    # Then update the user signals: {'GO','STOP','ABORT','override_pressure','OVERRIDE'} appropriately
    (user_args) = GUI.Execute(current_counter, control_args, user_args)

    # Update or override the control signals: {'PAIN','STARTED','SCHEDULE_INDEX','PAUSE','FORCE'}
    # NOTE: A FORCE is equivalent to an untimed PAIN cycle in PAUSE mode (PAUSE alone makes pressure NIL, otherwise)
    #       OVERRIDE_PRESSURE (sampled from user_args) is used to create new values of PAINH and PAINL
    #       STOP and ABORT both do an ABORT in the FORCE mode of operation, venting pressure, resetting index, etc.
    old_control_args = control_args
    (control_args) = state_machine_overrides(current_counter, control_args, user_args)

    # Execute the state machine with the new control signals and pressure value
    try:
        sm.Execute(current_pressure, control_args )
    except KeyboardInterrupt:
        print ("\nDone")





