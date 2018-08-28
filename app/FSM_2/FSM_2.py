from transitions import Machine, State
from CONSTANTS import *
# from app.states.IDLE import IDLE
# from app.states.ISOLATE_VENT import ISOLATE_VENT
# from app.states.LOAD_RESERVOIR import LOAD_RESERVOIR
# from app.states.NEW_ENTRY import NEW_ENTRY
# from app.states.RELEASE import RELEASE
# from app.states.VENT import VENT
# from app.states.CONNECT_CUFF import CONNECT_CUFF

ALL_STATES = [
    State(CONNECT_CUFF_STATE, on_exit='exit_state', on_enter='enter_state'),
    State(IDLE_STATE, on_exit='exit_state', on_enter='enter_state'),
    State(ISOLATE_STATE, on_exit='exit_state', on_enter='enter_state'),
    State(ISOLATE_VENT_STATE, on_exit='exit_state', on_enter='enter_state'),
    State(ISOLATE_RELEASE_STATE, on_exit='exit_state', on_enter='enter_state'),
    State(ISOLATE_RESERVOIR_STATE, on_exit='exit_state', on_enter='enter_state'),
    State(LOAD_RESERVOIR_STATE, on_exit='exit_state', on_enter='enter_state'),
    State(NEW_ENTRY_STATE, on_exit='exit_state', on_enter='enter_state'),
    State(RELEASE_STATE, on_exit='exit_state', on_enter='enter_state'),
    State(VENT_STATE, on_exit='exit_state', on_enter='enter_state'),
]

class PainAdministrator(object):
    states = ALL_STATES

    def __init__(self, schedule, pressure_values):
        self.schedule = schedule
        self.pressure_values = pressure_values

        # https://github.com/pytransitions/transitions
        # Initialize the state machine, gives this class (PainAdministrator extra functionality)
        self.fsm = Machine(model=self, states=PainAdministrator.states, initial=IDLE_STATE)

        # TRANSITIONS
        self.fsm.add_transition('idle_to_isolate_vent',IDLE_STATE, ISOLATE_VENT_STATE)

        # ENTER STATE FUNCTION called all the time, will use states on enter function
        def enter_state(self):
            # First get the state that was entered
            print("entering state: " + self.state)

        def exit_state(self):
            print("exiting state:" + self.state)


    def start_experiment(self):
        # First isolate the vent
        for item in self.schedule:
            print(item)

