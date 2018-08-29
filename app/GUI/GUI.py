#kivy.require("1.8.0")
from kivy.base import runTouchApp

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import ListProperty

from kivy.app import App

from kivy.clock import Clock

from datetime import datetime
from app.constants.CONSTANTS import DEBUG

state = 0

class Display(FloatLayout):  # intro <display> and tells actions/functions
    def __init__(self, **kwargs):
        super(Display, self).__init__(**kwargs)
        print(kwargs)
        self.txt = 170
        print ("Started up the Display")

    def count(self, *varargs):
        pass
        #self.start = datetime.now()
        #Clock.schedule_interval(self.on_timeout, 1)

    def on_timeout(self, *args):
        d = datetime.now() - self.start
        self.ids.schedule1.text = datetime.utcfromtimestamp(d.total_seconds()).strftime("%S")

    def abort_function(self):
        print ("Aborting...")
        self.ids.abort.text = "Clicked"

    def enter_function(self):
        self.ids.enter.text = "Clicked"

    def go_function(self):
        print ("Starting a schedule")
        self.ids.go.text = "Clicked"  # changes go to clicked when clicked

    def stop_function(self):
        print ("Stopping/pausing a schedule")
        self.ids.stop.text = "Clicked"

    def newpressureup(self):
        pass

    def newpressure_function(self, direction, desired_pressure):
        #app = App.get_running_app()
        # self.direction = direction
        # self.desired_pressure = desired_pressure

        if (direction == "up"):
            pass
            #app.desired_pressure += 1
        elif (direction == "down"):
            pass
            #app.desired_pressure -= 1
        else:
            print("Error! newpressure_function: We should not be here (expecting 'up' or 'down' only)")

        #self.ids.newpressure.text = "%d" % app.desired_pressure
        #print("New desired pressure is now ", app.desired_pressure)


class DisplayApp(App):  # defines app and returns display
    # desired_pressure = Patm
    desired_pressure = 0
    ENTER = 0
    STOP = 0
    GO = 0
    ABORT = 0
    current_pressure = 0
    disp = Display()

    def update(self, Global_cnt, current_counter, control_args, user_args):
        self.Global_cnt = Global_cnt
        self.current_counter = current_counter
        self.control_args = control_args
        self.user_args = user_args
        # current_counter = [] * max_num_schedules
        # control_args = {'SCHEDULE_INDEX': 0, 'PAIN': 0, 'STARTED': 0, 'PAUSE': 0, 'FORCE': 0,
        #                'PAINH': painh, 'PAINL': painl, 'PRESSURE': 0,
        #                'PATM': pressure_parameters['PATM'], 'PMAX': pressure_parameters['PMAX']}
        # user_args = {'GO': 0, 'STOP': 0, 'ABORT': 0, 'UP': 0, 'DOWN': 0,
        #             'override_pressure': pressure_parameters['PAINVALUE'], 'OVERRIDE': 0}

        #print ("Updating user values with cnt=", self.Global_cnt)
        if (DEBUG == True and self.Global_cnt == 20):
            # debug statement only!
            self.user_args['STOP'] = 1
            print ("\tDebug: Stop activated with Global count = ", Global_cnt)
            print ("User args now:", self.user_args)

        if (DEBUG == True and (self.Global_cnt == 30 or self.Global_cnt == 2)):
            # debug statement only!
            self.user_args['STOP'] = 0
            print ("\tDebug: Stop de-activated with Global count = ", self.Global_cnt)
            print ("User args now:", self.user_args)

        if (DEBUG == True and (self.Global_cnt == 500 or self.Global_cnt == 4000 or self.Global_cnt == 5000)):
            # debug statement only!
            self.user_args['GO'] = 1
            print ("\tDebug: Go activated with Global count = ", self.Global_cnt)
            print ("User args now:", self.user_args)

        if (DEBUG == True and (self.Global_cnt == 1000 or self.Global_cnt == 4500)):
            # debug statement only!
            self.user_args['GO'] = 0
            print ("\tDebug: Go de-ctivated with Global count = ", self.Global_cnt)
            print ("User args now:", self.user_args)

        #print ("Control args now:", self.control_args)
        #print ("User args now:", self.user_args)
        return (self.user_args)



def build(self):
    return DisplayApp.disp

# if __name__ == "__main__":
#    gui = DisplayApp()
#    gui.run()
# DisplayApp().run()
