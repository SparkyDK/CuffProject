from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
#kivy.require("1.10.1")

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App

from datetime import datetime
from app.System.pressure_measurement.pressure_sampling import Read_Cuff_Pressure
from app.System.pain_schedule.pain_schedule import pain_schedule
from app.System.FSM.setup_FSM_states import Setup_FSM_States
from app.System.FSM.control_decisions import ControlDecisions

from tests.test_files.keyboard_test import keyboard_testing

import collections

from app.constants.CONSTANTS import HISTORY_LENGTH

import math
import time

class Display(FloatLayout):  # intro <display> and tells actions/functions
    def __init__(self, **kwargs):
        super(Display, self).__init__(**kwargs)
        print(kwargs)
        self.txt = 170
        print ("Started up the Display")

        time.sleep(10)

        # control_args = {}           # SCHEDULE_INDEX','PAIN','STARTED','PAUSE','PAINH','PAINL','PRESSURE','PATM','PMAX'
        # user_args = {}              # 'GO','STOP','ABORT','UP','DOWN','override_pressure','OVERRIDE'
        # pressure_parameters = {}    # 'PAINTOLERANCE', 'PAINVALUE', 'PATM', 'PMAX'
        # imported_schedule = []      # MAX_NUM_SCHEDULES tuples of: {NIL|PAIN, seconds_value}
        # schedule_finished = 0       # boolean to indicate pain schedule is complete
        #
        # past_states = collections.deque([None]*HISTORY_LENGTH)            # queue history of past few states
        # start_time = None           # initial system starting time for program
        # elapsed_time = 0            # program execution time
        #
        # Global_cnt=0                # Counter to keep track of number of loops in the while(true): construct
        # toggle = 0                  # used for keyboard-based debugging
        # current_counter=0           # keeps track of seconds count for current phase of pain schedule
        #
        # decision = ControlDecisions()
        # airctrl = Setup_FSM_States()    # state machine to control relays
        # schedule = pain_schedule()      # manages the NIL/PAIN schedule
        #
        # # Initialize the system
        # control_args, user_args, pressure_parameters, schedule_finished, start_time, elapsed_time, \
        # current_counter, imported_schedule, Global_cnt, past_states, decision, airctrl, schedule, toggle = \
        #     self.setup_system(control_args, user_args, pressure_parameters, schedule_finished, start_time,
        #                       elapsed_time, current_counter, imported_schedule, Global_cnt, past_states,
        #                       decision, airctrl, schedule, toggle)
        # #while (True):
        # if (True==True):
        #     # Run the system forever
        #     control_args, user_args, pressure_parameters, schedule_finished, start_time, elapsed_time, \
        #     current_counter, imported_schedule, Global_cnt, past_states, decision, airctrl, schedule, toggle = \
        #         self.run_system(control_args, user_args, pressure_parameters, schedule_finished, start_time,
        #                         elapsed_time, current_counter, imported_schedule, Global_cnt, past_states,
        #                         decision, airctrl, schedule, toggle)

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

        return(self.control_args, self.user_args, self.pressure_parameters,
               self.elapsed_time, self.start_time, self.schedule_finished,
               self.current_counter, self.imported_schedule, self.Global_cnt, self.past_states,
               self.decision, self.airctrl, self.schedule, self.toggle)

    def run_system(self, control_args, user_args, pressure_parameters, schedule_finished, start_time, elapsed_time,
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


        # Not particularly necessary; mostly for debugging purposes
        self.Global_cnt += 1

        # Keep a state history
        returned_state = airctrl.FSM.GetCurState()
        # pop out the highest-index entry from the state history
        self.past_states.popleft()
        # Add the newest state value to the lowest-index entry of the state history
        self.past_states.append(returned_state)

        #localtime = time.asctime(time.localtime(time.time()))
        old_elapsed_time = self.elapsed_time
        self.elapsed_time = time.time() - start_time

        # Pain schedule requires a one-second tick, created at the point where the integer truncation
        # of system time seconds ticks over to the next integer value (e.g. 3.99999992 becomes 4.0000245)
        if math.floor(self.elapsed_time) != math.floor(old_elapsed_time):
            second_tickover = True
        else:
            second_tickover = False

        # Read the current pressure value
        self.control_args = Read_Cuff_Pressure(self.control_args, self.past_states)

        # Poll for user input and update the GUI based on the control arguments
        # Then update the user signals: {'GO','STOP','ABORT','override_pressure','OVERRIDE'} appropriately

        try:
            old_control_args = control_args.copy()
            # Update or override the control signals: {'PAIN','STARTED','SCHEDULE_INDEX','PAUSE'}
            # Execute the asynchronous part of the state machine that implements the control decisions
            # with the newly-updated control signals and newly-sampled pressure value
            # Update 'PAUSE', 'STARTED', PAINH, PAINL, PAINVALUE, as appropriate


            self.control_args, self.current_counter, self.pressure_parameters, self.schedule_finished, self.toggle = \
                self.decision.respond_to_user_inputs(self.current_counter, self.imported_schedule, self.control_args,
                                                     self.user_args, self.pressure_parameters, second_tickover,
                                                     self.schedule_finished, self.airctrl,
                                                     self.schedule, toggle)
            if (self.schedule_finished == True):
                # At the end of the pain schedule, turn off pain and keep venting the cuff in IDLE state
                control_args['PAIN'] = 0

            # Execute the state machine
            airctrl.FSM.Execute(control_args)

        except KeyboardInterrupt:
            print("\nDone")

        return(self.control_args, self.user_args, self.pressure_parameters, self.elapsed_time, self.start_time,
               self.schedule_finished, self.current_counter, self.imported_schedule, self.Global_cnt, self.past_states,
               self.decision, self.airctrl, self.schedule, self.toggle)

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
        pass

class DisplayApp(App):  # defines app and returns display
    disp = Display()

    def build(self):
        return Display()