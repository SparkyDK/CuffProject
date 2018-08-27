from statemachine import StateMachine, State
# https://python-statemachine.readthedocs.io/en/latest/readme.html
# class ExperimentData(object):

class ExperimentDataModel(object):
    # This model has a property called state which is the state of the statemachine
    def __init__(self, state, schedule, pressure_values):
        self.state = state
        print("This class will control the experiment")

    def administer_pain(self):
        print("administering pain")


class PainAdministratorStateMachine(StateMachine):
    # States defined here
    idle = State('IDLE', initial=True)
    pain = State('PAIN')
    nothing = State('NIL')
    paused = State("PAUSED")
    stopped = State("STOPPED")

    # Transitions between states defined here
    start_test = idle.to(pain)
    administer_pain = nothing.to(pain)
    release_pain = pain.to(nothing)
    return_to_idle = pain.to(idle)
    stop_everything = pain.to(stopped) | nothing.to(stopped)

    def on_start_test(self):
        print(self.model)
        print("stop here")
