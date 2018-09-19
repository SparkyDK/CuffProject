# File containing all of the shared global variables
from app.constants.CONSTANTS import HISTORY_LENGTH
import collections

from app.System.pain_schedule.pain_schedule import pain_schedule
from app.System.FSM.setup_FSM_states import Setup_FSM_States
from app.System.FSM.control_decisions import ControlDecisions

control_args = {}  # SCHEDULE_INDEX','PAIN','STARTED','PAUSE','PAINH','PAINL','PRESSURE','PATM','PMAX'
current_pressure = 0
user_args = {}  # 'GO','STOP','ABORT','UP','DOWN','override_pressure','OVERRIDE'
pressure_parameters = {}  # 'PAINTOLERANCE', 'PAINVALUE', 'PATM', 'PMAX'
imported_schedule = []  # MAX_NUM_SCHEDULES tuples of: {NIL|PAIN, seconds_value}
schedule_finished = 0  # boolean to indicate pain schedule is complete

past_states = collections.deque([None] * HISTORY_LENGTH)  # queue history of past few states
start_time = None  # initial system starting time for program
elapsed_time = 0  # program execution time

Global_cnt = 0  # Counter to keep track of number of loops in the while(true): construct
toggle = 0  # used for keyboard-based debugging
current_counter = 0  # keeps track of seconds count for current phase of pain schedule

decision = ControlDecisions()
airctrl = Setup_FSM_States()  # state machine to control relays
schedule = pain_schedule()  # manages the NIL/PAIN schedule

digital_pressure_value = 16000000