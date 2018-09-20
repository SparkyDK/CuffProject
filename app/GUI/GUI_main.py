from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
#kivy.require("1.10.1")

from functools import partial

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty
# from kivy.properties import NumericProperty

from app.GUI import g
from app.constants.CONSTANTS import refresh_period
from app.GUI.kivy_color_management import kivy_color_adjustment

from datetime import datetime
from app.System.pressure_measurement.pressure_sampling import Read_Cuff_Pressure

import math
import time

class Display(FloatLayout):  # intro <display> and tells actions/functions
    # Pressure values (current value from sensor and adjustable pain value)
    current_pressure = StringProperty('---')
    new_pressure = StringProperty('---')

    # Schedule values
    schedule1_pressure = StringProperty('---')
    schedule2_pressure = StringProperty('---')
    schedule3_pressure = StringProperty('---')
    schedule4_pressure = StringProperty('---')
    schedule5_pressure = StringProperty('---')
    schedule6_pressure = StringProperty('---')
    schedule7_pressure = StringProperty('---')
    schedule8_pressure = StringProperty('---')

    time_state = StringProperty('Starting up the system')

    def __init__(self, **kwargs):
        super(Display, self).__init__(**kwargs)
        #print(kwargs)
        self.txt = 170
        print ("Started up the Display with control_args:", g.control_args)

        localtime = time.asctime(time.localtime(time.time()))
        print ("Display:",localtime)

    def schedule_system(self, interval):
        self.interval = interval
        print ("Scheduling the system to execute every", self.interval,"seconds")
        Clock.schedule_interval(partial(self.run_system, (g.control_args, g.user_args, g.pressure_parameters,\
            g.schedule_finished, g.start_time, g.elapsed_time, g.current_counter, g.imported_schedule,\
            g.Global_cnt, g.past_states, g.decision, g.airctrl, g.schedule, g.toggle) ), self.interval/refresh_period )

    def run_system(self, args, dt, *largs):
        #print ("run_system args:", args)

        # self.control_args, self.user_args, self.pressure_parameters, self.schedule_finished, self.start_time,\
        # self.elapsed_time, self.current_counter, self.imported_schedule, self.Global_cnt, self.past_states,\
        # self.decision, self.airctrl, self.schedule, self.toggle = args

        self.control_args, self.user_args, self.pressure_parameters, self.elapsed_time, self.start_time, \
        self.schedule_finished, self.current_counter, self.imported_schedule, self.Global_cnt, self.past_states,\
        self.decision, self.airctrl, self.schedule, self.toggle =\
            g.control_args, g.user_args, g.pressure_parameters, g.elapsed_time, g.start_time, \
            g.schedule_finished, g.current_counter, g.imported_schedule, g.Global_cnt,g.past_states,\
            g.decision, g.airctrl, g.schedule, g.toggle

        #print ("Current gGlobalcnt=", g.Global_cnt, "with selfGlobalcnt=", self.Global_cnt)
        # Not particularly necessary; mostly for debugging purposes
        self.Global_cnt += 1
        #print ("Incrementing selfGlobalCnt to", self.Global_cnt)


        # Keep a state history
        returned_state = self.airctrl.FSM.GetCurState()
        # pop out the highest-index entry from the state history
        self.past_states.popleft()
        # Add the newest state value to the lowest-index entry of the state history
        self.past_states.append(returned_state)

        old_elapsed_time = self.elapsed_time
        self.elapsed_time = time.time() - self.start_time

        # Pain schedule requires a one-second tick, created at the point where the integer truncation
        # of system time seconds ticks over to the next integer value (e.g. 3.99999992 becomes 4.0000245)

        if math.floor(self.elapsed_time) != math.floor(old_elapsed_time):
            self.second_tickover = True
            #localtime = time.asctime(time.localtime(time.time()))
            #print ("Second tick at", localtime)
        else:
            self.second_tickover = False

        # Read the current pressure value
        self.control_args = Read_Cuff_Pressure(self.control_args, self.past_states)

        self.current_pressure = str(g.control_args['PRESSURE'])
        self.new_pressure = str(g.user_args['override_pressure'])

        # Dynamic conditional update of display values and colours, such as graying out of inactive button text
        self.schedule1_pressure, self.ids.schedule1.color, self.schedule2_pressure, self.ids.schedule2.color,\
        self.schedule3_pressure, self.ids.schedule3.color, self.schedule4_pressure, self.ids.schedule4.color,\
        self.schedule5_pressure, self.ids.schedule5.color, self.schedule6_pressure, self.ids.schedule6.color,\
        self.schedule7_pressure, self.ids.schedule7.color, self.schedule8_pressure, self.ids.schedule8.color,\
        self.ids.go.color, self.ids.stop.color, self.ids.pain.color, self.ids.nopain.color, self.ids.enter.color,\
        self.time_state =\
            kivy_color_adjustment().grey_out(current_counter=self.current_counter, control_args=self.control_args,\
                                             user_args=self.user_args, pressure_parameters=self.pressure_parameters,\
                                             second_tickover=self.second_tickover, airctrl=self.airctrl)

        # Poll for user input and update the GUI based on the control arguments
        # Then update the user signals: {'GO','STOP','ABORT','override_pressure','OVERRIDE'} appropriately
        try:
            #old_control_args = control_args.copy()
            # Update or override the control signals: {'PAIN','STARTED','SCHEDULE_INDEX','PAUSE'}
            # Execute the asynchronous part of the state machine that implements the control decisions
            # with the newly-updated control signals and newly-sampled pressure value
            # Update 'PAUSE', 'STARTED', PAINH, PAINL, PAINVALUE, as appropriate

            self.user_args, self.control_args, self.current_counter, self.pressure_parameters,\
            self.schedule_finished, self.toggle =\
                self.decision.respond_to_user_inputs(self.current_counter, self.imported_schedule, self.control_args,\
                                                     self.user_args, self.pressure_parameters, self.second_tickover,
                                                     self.schedule_finished, self.airctrl,
                                                     self.schedule, self.toggle)
            if (self.schedule_finished == 1):
                # At the end of the pain schedule, turn off pain and keep venting the cuff in IDLE state
                self.control_args['PAIN'] = 0

            # Execute the state machine
            self.airctrl.FSM.Execute(self.control_args)

        except KeyboardInterrupt:
            print("\nDone")

        #print ("selfGlobalcnt=", self.Global_cnt, "and gGlobalcnt=", g.Global_cnt)

        g.control_args, g.user_args, g.pressure_parameters, g.elapsed_time, g.start_time,\
        g.schedule_finished, g.current_counter, g.imported_schedule, g.Global_cnt, g.past_states,\
        g.decision, g.airctrl, g.schedule, g.toggle =\
            self.control_args, self.user_args, self.pressure_parameters, self.elapsed_time, self.start_time,\
            self.schedule_finished, self.current_counter, self.imported_schedule, self.Global_cnt, self.past_states,\
            self.decision, self.airctrl, self.schedule, self.toggle

        # return(self.control_args, self.user_args, self.pressure_parameters, self.elapsed_time, self.start_time,
        #        self.schedule_finished, self.current_counter, self.imported_schedule, self.Global_cnt, self.past_states,
        #        self.decision, self.airctrl, self.schedule, self.toggle)

    def count(self, *varargs):
        pass
        #self.start = datetime.now()
        #Clock.schedule_interval(self.on_timeout, 1)

    def on_timeout(self, *args):
        d = datetime.now() - self.start
        self.ids.schedule1.text = datetime.utcfromtimestamp(d.total_seconds()).strftime("%S")

    def abort_ack_function(self):
        self.ids.abort.text = ""

    def abort_function(self):
        print ("Requesting an Abort ...")
        g.user_args['ABORT'] = 1
        self.ids.abort.text = "RELEASE/\nRESET"

    def enter_ack_function(self):
        self.ids.enter.text = ""
        #g.pressure_parameters['PAINVALUE'] = g.user_args['override_pressure']

    def enter_function(self):
        self.ids.enter.text = "ENTER"
        g.user_args['OVERRIDE'] = 1
        #g.pressure_parameters['PAINVALUE'] = g.user_args['override_pressure']

    def go_ack_function(self):
        self.ids.go.text = ""

    def go_function(self):
        g.user_args['GO'] = 1
        print ("Requesting start of a schedule")
        self.ids.go.text = "GO"  # changes go to clicked when clicked

    def stop_ack_function(self):
        self.ids.stop.text = ""

    def stop_function(self):
        g.user_args['STOP'] = 1
        print ("Requesting the Stopping/pausing of a schedule")
        self.ids.stop.text = "STOP"

    def new_pressure_down(self):
        g.user_args['override_pressure'] -= 1
        print ("Decreasing pressure to", g.user_args['override_pressure'])

    def new_pressure_up(self):
        g.user_args['override_pressure'] += 1
        print ("Increasing pressure to", g.user_args['override_pressure'])

class DisplayApp(App):  # defines app and returns display
    def build(self):
        disp = Display()
        disp.schedule_system(refresh_period)

        # result=0
        # localtime = time.asctime(time.localtime(time.time()))
        # Clock.schedule_interval(partial(disp.do_something, {'time':localtime, 'result':result} ), 1.0/60.0)
        return disp

    def setup_system(self, control_args, user_args, pressure_parameters, schedule_finished, start_time, elapsed_time,
                     current_counter, imported_schedule, Global_cnt, past_states, decision, airctrl, schedule, toggle):
        self.control_args = control_args
        self.user_args = user_args
        self.pressure_parameters = pressure_parameters
        self.schedule_finished = schedule_finished
        self.start_time = start_time
        self.elapsed_time = elapsed_time
        self.current_counter = current_counter
        self.imported_schedule = imported_schedule
        self.Global_cnt = Global_cnt
        self.past_states = past_states
        self.decision = decision
        self.airctrl = airctrl
        self.schedule = schedule
        self.toggle = toggle

        print (self.pressure_parameters)

        # Create a schedule for the administration of pain and set up the indices and pressure parameters
        self.current_counter,self.imported_schedule,self.Global_cnt,self.schedule_finished,self.pressure_parameters = \
            schedule.setup_pain_schedule(self.control_args, self.pressure_parameters)

        painl = int(self.pressure_parameters['PAINVALUE']) - int(self.pressure_parameters['PAINTOLERANCE'])
        painh = int(self.pressure_parameters['PAINVALUE']) + int(self.pressure_parameters['PAINTOLERANCE'])
        # Initial PAUSE state is not active, and there is no running schedule.
        # PAIN mode is disabled and all user inputs default to OFF or 0
        self.control_args = {'SCHEDULE_INDEX': 0, 'PAIN': 0, 'STARTED': 0, 'PAUSE': 0,
                        'PAINH': painh, 'PAINL': painl, 'PRESSURE': 0,
                        'PATM': self.pressure_parameters['PATM'], 'PMAX': self.pressure_parameters['PMAX']}
        self.user_args = {'GO': 0, 'STOP': 0, 'ABORT': 0, 'UP': 0, 'DOWN': 0,
                     'override_pressure': self.pressure_parameters['PAINVALUE'], 'OVERRIDE': 0}

        # Create the system state machine that implements the pain control decision and times the relay opening/closing
        # Vent the cuff first
        airctrl.FSM.SetState("ISOLATE_VENT")
        airctrl.Execute(control_args)

        # Initialize the timers
        self.start_time = time.time()
        time.process_time()

        g.control_args, g.user_args, g.pressure_parameters, g.elapsed_time, g.start_time,\
        g.schedule_finished, g.current_counter, g.imported_schedule, g.Global_cnt, g.past_states,\
        g.decision, g.airctrl, g.schedule, g.toggle =\
            self.control_args, self.user_args, self.pressure_parameters, self.elapsed_time, self.start_time,\
            self.schedule_finished, self.current_counter, self.imported_schedule, self.Global_cnt, self.past_states,\
            self.decision, self.airctrl, self.schedule, self.toggle

        print ("System set up")

        return(self.control_args, self.user_args, self.pressure_parameters,
               self.elapsed_time, self.start_time, self.schedule_finished,
               self.current_counter, self.imported_schedule, self.Global_cnt, self.past_states,
               self.decision, self.airctrl, self.schedule, self.toggle)


if __name__ == '__main__':
    gui = DisplayApp()
    print("gui: ", gui)

    # Initialize the system global variables.... maybe there is a better way to do this without globals
    g.control_args, g.user_args, g.pressure_parameters, g.schedule_finished, g.start_time, \
    g.elapsed_time, g.current_counter, g.imported_schedule, g.Global_cnt, g.past_states, \
    g.decision, g.airctrl, g.schedule, \
    g.toggle = gui.setup_system(g.control_args, g.user_args, g.pressure_parameters, \
                                 g.schedule_finished, g.start_time, g.elapsed_time, \
                                 g.current_counter, g.imported_schedule, g.Global_cnt, \
                                 g.past_states, g.decision, g.airctrl, g.schedule, \
                                 g.toggle)
    gui.run()