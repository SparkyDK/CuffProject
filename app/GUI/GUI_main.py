from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
#kivy.require("1.10.1")

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App

from datetime import datetime
from app.System.pressure_measurement.pressure_sampling import Read_Cuff_Pressure
from app.System.pain_schedule.pain_schedule import pain_schedule
from app.System.FSM.setup_FSM_states import Setup_FSM_States

from app.constants.CONSTANTS import DEBUG

import math
import time

state = 0

class Display(FloatLayout):  # intro <display> and tells actions/functions
    def __init__(self, **kwargs):
        super(Display, self).__init__(**kwargs)
        print(kwargs)
        self.txt = 170
        print ("Started up the Display")
        control_args = []
        user_args = []
        pressure_parameters = []
        imported_schedule = []
        schedule_finished = 0

        past_states = []
        start_time = None
        elapsed_time = 0

        Global_cnt=0
        toggle = 0
        current_counter=0

        airctrl = Setup_FSM_States()
        schedule = pain_schedule()

        control_args, user_args, pressure_parameters, schedule_finished, start_time, elapsed_time, \
        current_counter, imported_schedule, Global_cnt, past_states, airctrl, schedule, toggle = \
            self.setup_system(control_args, user_args, pressure_parameters, schedule_finished, start_time,
                              elapsed_time, current_counter, imported_schedule, Global_cnt, past_states,
                              airctrl, schedule, toggle)
        while (True):
            control_args, user_args, pressure_parameters, schedule_finished, start_time, elapsed_time, \
            current_counter, imported_schedule, Global_cnt, past_states, airctrl, schedule, toggle = \
                self.run_system(control_args, user_args, pressure_parameters, schedule_finished, start_time,
                                elapsed_time, current_counter, imported_schedule, Global_cnt, past_states,
                                airctrl, schedule, toggle)

    def setup_system(self, control_args, user_args, pressure_parameters, schedule_finished, start_time, elapsed_time,
                     current_counter, imported_schedule, Global_cnt, past_states, airctrl, schedule, toggle):
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
        self.airctrl = airctrl
        self.schedule = schedule
        self.toggle = toggle

        # Initial PAUSE state is not active, and there is no running schedule.
        # PAIN mode is disabled and all user inputs default to OFF or 0

        painl = int(self.pressure_parameters['PAINVALUE'] - self.pressure_parameters['PAINTOLERANCE'])
        painh = int(self.pressure_parameters['PAINVALUE'] + self.pressure_parameters['PAINTOLERANCE'])

        self.control_args = {'SCHEDULE_INDEX': 0, 'PAIN': 0, 'STARTED': 0, 'PAUSE': 0,
                        'PAINH': painh, 'PAINL': painl, 'PRESSURE': 0,
                        'PATM': self.pressure_parameters['PATM'], 'PMAX': self.pressure_parameters['PMAX']}
        self.user_args = {'GO': 0, 'STOP': 0, 'ABORT': 0, 'UP': 0, 'DOWN': 0,
                     'override_pressure': self.pressure_parameters['PAINVALUE'], 'OVERRIDE': 0}

        # Create a schedule for the administration of pain
        self.current_counter,self.imported_schedule,self.Global_cnt,self.schedule_finished,self.pressure_parameters = \
            schedule.setup_pain_schedule(self.control_args, self.pressure_parameters)

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
               self.airctrl, self.schedule, self.toggle)

    def run_system(self, control_args, user_args, pressure_parameters, schedule_finished, start_time, elapsed_time,
                     current_counter, imported_schedule, Global_cnt, past_states, airctrl, schedule, toggle):
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
        self.airctrl = airctrl
        self.schedule = schedule
        self.toggle = toggle


        Global_cnt += 1

        # Keep a state history
        returned_state = airctrl.FSM.GetCurState()
        # pop out the highest-index entry from the state history
        self.past_states.popleft()
        # Add the newest state value to the lowest-index entry of the state history
        self.past_states.append(returned_state)

        #localtime = time.asctime(time.localtime(time.time()))
        old_elapsed_time = elapsed_time
        elapsed_time = time.time() - start_time

        # Pain schedule requires a second tick, created as an integer truncation of system time seconds
        if math.floor(elapsed_time) != math.floor(old_elapsed_time):
            second_tickover = True
            # run the pain schedule to determine whether in NIL or PAIN state ... or finished
            schedule.execute_pain_schedule()

        else:
            second_tickover = False

        # Read pressure value from transducer via the ADC
        control_args = Read_Cuff_Pressure(control_args, past_states)

        # Poll for user input and update the GUI based on the control arguments
        # Then update the user signals: {'GO','STOP','ABORT','override_pressure','OVERRIDE'} appropriately
        old_user_args = user_args.copy()

        try:
            old_control_args = control_args.copy()
            # Update or override the control signals: {'PAIN','STARTED','SCHEDULE_INDEX','PAUSE'}
            # Execute the asynchronous part of the state machine that implements the control decisions
            # with the newly-updated control signals and newly-sampled pressure value
            # Update 'PAUSE', 'STARTED', PAINH, PAINL, PAINVALUE, as appropriate
            control_args, current_counter, pressure_parameters, schedule_finished, toggle = \
                airctrl.FSM.ControlDecisions(current_counter, imported_schedule, control_args, old_user_args,
                                             user_args,
                                             pressure_parameters, second_tickover, schedule_finished, toggle) \
                # Pain schedule is completed
            if (schedule_finished == True):
                # At the end of the pain schedule, hold the state machine in the vent state and turn off pain
                # Could send it back to IDLE (which would result in less wear and tear on the solenoids
                # and which might be a bit safer, in the case where the air tank solenoid fails)
                # What if there is some residual pressure in the cuff at the end of the experiment though? ...
                airctrl.FSM.SetState("VENT")
                control_args['PAIN'] = 0

            # Execute the state machine
            airctrl.FSM.Execute(control_args)

        except KeyboardInterrupt:
            print("\nDone")

        return(self.control_args, self.user_args, self.pressure_parameters,
               self.elapsed_time, self.start_time, self.schedule_finished,
               self.current_counter, self.imported_schedule, self.Global_cnt,
               self.past_states, self.airctrl, self.schedule, self.toggle)

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

class DisplayApp(App):  # defines app and returns display

    disp = Display()

    from kivy.config import Config
    Config.set('kivy', 'keyboard_mode', 'systemandmulti')

    def build(self):
        return Display()