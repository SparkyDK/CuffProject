from app.CONSTANTS import IDLE_STATE
class ISOLATE_VENT:
    def execute(self, args):
        print("executing isolate event with args" + str(args))
        return IDLE_STATE, {'value': 1234}  # Can be anything

    def exit(self):
        print("Exiting ISOLATE_VENT")
