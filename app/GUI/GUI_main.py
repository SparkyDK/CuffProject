from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
#kivy.require("1.10.1")

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App

from datetime import datetime

# Allows interpolation between empirically-determined pressure transducer values and mm_Hg values
from scipy import interpolate

from app.System import run_system
from app.constants.CONSTANTS import DEBUG

import math

state = 0

class Display(FloatLayout):  # intro <display> and tells actions/functions
    def __init__(self, **kwargs):
        super(Display, self).__init__(**kwargs)
        print(kwargs)
        self.txt = 170
        print ("Started up the Display")
        run_system()

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
        #user_args{'ABORT'} = 1


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

        def kbd_input(*args, **kwargs):
            with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()

    def on_press(key):
        try:
            pass
            # print('alphanumeric key {0} pressed'.format(key.char))
        except AttributeError:
            pass
            # print('special key {0} pressed'.format(key))

    keypress = None
    old_keypress = None
    toggle = 0

    def on_release(key):
        global keypress
        # print('{0} released'.format(key))
        keypress = format(key)
        # keypress = key
        if key == keyboard.Key.esc:
            # Stop listener
            return False


class DisplayApp(App):  # defines app and returns display

    disp = Display()

    from kivy.config import Config
    Config.set('kivy', 'keyboard_mode', 'systemandmulti')


    from app.System import Setup_FSM_States
    from app.System.pain_schedule import setup_pain_schedule, execute_pain_schedule

    import time

    import threading

    # Initial PAUSE state is not active, and there is no running schedule.
    # PAIN mode is disabled and all user inputs default to OFF or 0
    control_args = {'SCHEDULE_INDEX': 0, 'PAIN': 0, 'STARTED': 0, 'PAUSE': 0,
                    'PAINH': painh, 'PAINL': painl, 'PRESSURE': 0,
                    'PATM': pressure_parameters['PATM'], 'PMAX': pressure_parameters['PMAX']}
    user_args = {'GO': 0, 'STOP': 0, 'ABORT': 0, 'UP': 0, 'DOWN': 0,
                 'override_pressure': pressure_parameters['PAINVALUE'], 'OVERRIDE': 0}
    old_user_args = user_args.copy()

    current_pressure = 0

    setup_pain_schedule()

    execute_pain_schedule()

    # Create the system state machine that implements the pain control decision and times the relay opening/closing
    airctrl = Setup_FSM_States()
    # Vent the cuff first
    airctrl.FSM.SetState("ISOLATE_VENT")
    airctrl.Execute(control_args)

    # Initialize the timers
    start_time = time.time()
    time.process_time()
    elapsed_time = 0

    kw_args = dict(value=0)
    args = []

    threads = []
    t = threading.Timer(0.01, kbd_input, args, kw_args)
    t.start()
    threads.append(t)

    # g = threading.Thread(target=gui.run())
    # g = threading.Timer(0.01, DisplayApp().run, )
    # g = threading.Timer(0.01, gui.run(), )

    # g = threading.Thread(name='Display',target=DisplayApp)
    # threads.append(g)
    # g.start()
    # print (threads)


    #def build(self):
    #return DisplayApp.disp

    def build(self):
        return Display()
