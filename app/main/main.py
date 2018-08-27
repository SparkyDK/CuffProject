from app.constants.CONSTANTS import MAX_NUM_PARAMETERS
from app.filereaders.ScheduleReader import ScheduleReader
from app.filereaders.PressureReader import PressureReader

DEBUG = True
Global_cnt = 0
past_states = [] * 5
pain_required = False
control_args = {'GO' : 0, 'STOP': 0,  'PAIN': 0,  'P': Patm,  'RUNNING': 0,  'PAUSE':0}
current_counter = [] * max_num_schedules
schedule_index = 0

# Returns the user-provided pressure parameter values as a dictionary with keys of PMAX, PAINL, PAINH, PATM
pressure_parameters = PressureReader().read(filename="./tests/input_files/Pressure_Values.txt")

# Returns an array of tuples, with the desired action of Pain/Nil and the duration of each of those actions
schedule = ScheduleReader().read(time_schedule, filename="./tests/input_files/Schedule.txt")
max_num_schedules = len(schedule)

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
    returned_state =   sm.FSM.GetCurState()
    # pop out the highest-index entry from the state history
    past_states.popleft()
    # Add the newest state value to the lowest-index entry of the state history
    past_states.append(returned_state)

    # localtime = time.asctime(time.localtime(time.time()) )
    old_elapsed_time = elapsed_time
    elapsed_time = time.time() - start_time
    if ( math.floor(elapsed_time) != math.floor(old_elapsed_time) ):
        # Only process the schedule every new second
        second_tickover = True
        pain_required = schedule.Execute(control_args)
    else:
        second_tickover = False

    # Poll for user input and update the GUI
    (control_args) = GUI.Execute

    # Execute the state machine
    try:
        sm.Execute( control_args )
    except KeyboardInterrupt:
        print ("\nDone")





