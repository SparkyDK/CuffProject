from transitions import Machine, State
from CONSTANTS import *
from app.states.IDLE import IDLE
from app.states.ISOLATE_VENT import ISOLATE_VENT
# from app.states.LOAD_RESERVOIR import LOAD_RESERVOIR
# from app.states.NEW_ENTRY import NEW_ENTRY
# from app.states.RELEASE import RELEASE
# from app.states.VENT import VENT
# from app.states.CONNECT_CUFF import CONNECT_CUFF

# All the caps variables below are imported from the constants file
ALL_STATES = [
    State(CONNECT_CUFF_STATE, on_exit='exit_current_state', on_enter='enter_current_state'),
    State(IDLE_STATE, on_exit='exit_current_state', on_enter='enter_current_state'),
    State(ISOLATE_STATE, on_exit='exit_current_state', on_enter='enter_current_state'),
    State(ISOLATE_VENT_STATE, on_exit='exit_current_state', on_enter='enter_current_state'),
    State(ISOLATE_RELEASE_STATE, on_exit='exit_current_state', on_enter='enter_current_state'),
    State(ISOLATE_RESERVOIR_STATE, on_exit='exit_current_state', on_enter='enter_current_state'),
    State(LOAD_RESERVOIR_STATE, on_exit='exit_current_state', on_enter='enter_current_state'),
    State(NEW_ENTRY_STATE, on_exit='exit_current_state', on_enter='enter_current_state'),
    State(RELEASE_STATE, on_exit='exit_current_state', on_enter='enter_current_state'),
    State(VENT_STATE, on_exit='exit_current_state', on_enter='enter_current_state'),
]

class PainAdministrator(object):
    states = ALL_STATES
    # A dictonary of classes that do whatever needs to be done in each state
    state_implementers = {
        IDLE_STATE: IDLE(),
        ISOLATE_VENT_STATE: ISOLATE_VENT(),
    }

    def __init__(self, schedule, pressure_values):
        self.schedule = schedule
        self.pressure_values = pressure_values
        self.nextState = 'nil'
        self.values = {}

        # https://github.com/pytransitions/transitions
        # Initialize the state machine, gives this class (PainAdministrator extra functionality)
        self.fsm = Machine(model=self, states=PainAdministrator.states, initial=IDLE_STATE)

        # TRANSITIONS
        self.fsm.add_transition(trigger='idle_to_isolate_vent', source=IDLE_STATE, dest=ISOLATE_VENT_STATE)

    # ENTER STATE FUNCTION called all the time, will use states on enter function
    def enter_current_state(self):
        # First get the state that was entered
        print("Entering state: " + self.state)
        # Get the values as well as the next state to go to
        self.nextState, self.values = self.state_implementers[self.state].execute(self.values)
        print("stop")

    def exit_current_state(self):
        self.state_implementers[self.state].exit()
        print("exiting state:" + self.state)


    def start_experiment(self):
        # First isolate the vent
        for item in self.schedule:
            print(item)

