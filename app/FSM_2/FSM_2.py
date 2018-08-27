from statemachine import StateMachine, State


# https://python-statemachine.readthedocs.io/en/latest/readme.html
# class ExperimentData(object):
class PainAdministratorStateMachine(StateMachine):
    # States defined here
    connect_cuff = State('CONNECT_CUFF')
    idle = State('IDLE', initial=True)
    isolate = State('ISOLATE')
    isolate_vent = State("ISOLATE_VENT")
    isolate_release = State("ISOLATE_RELEASE")
    isolate_reservoir = State("ISOLATE_RESERVOIR")
    load_reservoir = State("LOAD_RESERVOIR")
    new_entry = State("NEW_ENTRY")
    release = State("RELEASE")
    vent = State("VENT")

    # Transitions between states defined here
    toIsolateVent = idle.to(isolate_vent)
    toVent = isolate_vent.to(vent)
    startTest = idle.to(isolate_vent)

    def on_vent(self):
        print("Venting")
        # Will only change state

        return "IDLE"

    def on_isolate_vent(self):
        print("Isolating event stuff")
        return "VENT"


class PainAdministrator(object): we


def __init__(self, schedule=[], pressure_values=[]):
    self.model = self
    self.schedule = schedule
    self.pressure_values = pressure_values
    self.fsm = PainAdministratorStateMachine()


def start_experiment(self):
    states = ["VENT", "ISOLATE_VENT", "IDLE"]
    nextState = "ISOLATE_VENT"

    while True or self.someConditionCheck():
        print("current: " + self.fsm.current_state)
        print("next: " + nextState)
        if nextState == "ISOLATE_VENT":
            nextState = self.fsm.toVent()  # dispatches action in thread and returns instantly
            continue


def someConditionCheck(self):
    return True
