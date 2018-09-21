from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
#kivy.require("1.10.1")

from functools import partial

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.properties import NumericProperty

from app.GUI import g
from app.constants.CONSTANTS import refresh_period
from app.GUI.kivy_color_management import kivy_color_adjustment

from datetime import datetime
from app.System.pressure_measurement.pressure_sampling import Read_Cuff_Pressure

import math
import time

class Display(Screen):  # intro <display> and tells actions/functions
    # Pressure values (current value from sensor and adjustable pain value)
    current_pressure = StringProperty('---')
    new_pressure = StringProperty('---')

    # Schedule values
    phase1 = StringProperty('---')
    phase2 = StringProperty('---')
    phase3 = StringProperty('---')
    phase4 = StringProperty('---')
    phase5 = StringProperty('---')
    phase6 = StringProperty('---')
    phase7 = StringProperty('---')
    phase8 = StringProperty('---')

    time_state = StringProperty('Starting up the system')

    def __init__(self, **kwargs):
        super(Display, self).__init__(**kwargs)
        #print(kwargs)
        print ("Display: Started up the Display with control_args:", g.control_args, "and self=", self)

        #localtime = time.asctime(time.localtime(time.time()))
        #print ("Display:",localtime)

    def build(self):
        pass
        print ("Ran Display instance with self", self)

    def init_system(self):
        # Initialize the system global variables.... maybe there is a better way to do this without globals
        g.control_args, g.user_args, g.pressure_parameters, g.schedule_finished, g.start_time, \
        g.elapsed_time, g.current_counter, g.imported_schedule, g.Global_cnt, g.past_states, \
        g.decision, g.airctrl, g.schedule, \
        g.toggle = self.setup_system(g.control_args, g.user_args, g.pressure_parameters, \
                                    g.schedule_finished, g.start_time, g.elapsed_time, \
                                    g.current_counter, g.imported_schedule, g.Global_cnt, \
                                    g.past_states, g.decision, g.airctrl, g.schedule, \
                                    g.toggle)

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

    def schedule_system(self):
        self.interval = refresh_period
        if (g.already_running == False):
            print ("Scheduling the system to execute every", self.interval,"seconds")
            g.already_running = True
            Clock.schedule_interval(partial(self.run_system, (g.control_args, g.user_args, g.pressure_parameters,\
                g.schedule_finished, g.start_time, g.elapsed_time, g.current_counter, g.imported_schedule,\
                g.Global_cnt, g.past_states, g.decision, g.airctrl, g.schedule, g.toggle, g.already_running) ),\
                self.interval/refresh_period )

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
        self.phase1, self.ids.phase1.color, self.phase2, self.ids.phase2.color,\
        self.phase3, self.ids.phase3.color, self.phase4, self.ids.phase4.color,\
        self.phase5, self.ids.phase5.color, self.phase6, self.ids.phase6.color,\
        self.phase7, self.ids.phase7.color, self.phase8, self.ids.phase8.color,\
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

    def switch_function(self):
        self.ids.select.text = "ENTER"
        g.user_args['OVERRIDE'] = 1
        #g.pressure_parameters['PAINVALUE'] = g.user_args['override_pressure']

    def run_schedule_screen(self, args, *largs):
        #sched.current = 'schedule'
        print ("Run schedule_screen with self=", self, "and screen manager=", self.screen_manager)

    def run_display_screen(self, args, *largs):
        print ("Run display_screen with self=", self, "and screen manager=", self.screen_manager)
        #sched.current = 'display'
        pass

    # disp = Display()
    # sched = Schedule()
    #
    # Clock.schedule_once(self.run_schedule_screen, 2) # clock callback for the first screen
    # Clock.schedule_once(self.run_display_screen, 8) # clock callback for the second screen
    #
    # sched = Schedule()
    # sched.
    # return sched

class Schedule(Screen):
    s1_phase1= StringProperty('---')
    s1_phase2= StringProperty('---')
    s1_phase3= StringProperty('---')
    s1_phase4= StringProperty('---')
    s1_phase5= StringProperty('---')
    s1_phase6= StringProperty('---')
    s1_phase7= StringProperty('---')
    s1_phase8= StringProperty('---')
    s2_phase1= StringProperty('---')
    s2_phase2= StringProperty('---')
    s2_phase3= StringProperty('---')
    s2_phase4= StringProperty('---')
    s2_phase5= StringProperty('---')
    s2_phase6= StringProperty('---')
    s2_phase7= StringProperty('---')
    s2_phase8= StringProperty('---')
    s3_phase1= StringProperty('---')
    s3_phase2= StringProperty('---')
    s3_phase3= StringProperty('---')
    s3_phase4= StringProperty('---')
    s3_phase5= StringProperty('---')
    s3_phase6= StringProperty('---')
    s3_phase7= StringProperty('---')
    s3_phase8= StringProperty('---')

    def __init__(self, **kwargs):
        super(Schedule, self).__init__(**kwargs)
        localtime = time.asctime(time.localtime(time.time()))
        print ("Schedule (init): Started up Schedule Display at:", localtime, "self=", self)
        #Clock.schedule_once(self.run_schedule, 2) # clock callback for the first screen

    def build(self):
        pass
        localtime = time.asctime(time.localtime(time.time()))
        print ("Schedule (build): Started up Schedule Display at:", localtime, "self=", self)
        #Clock.schedule_once(self.run_schedule, 8) # clock callback for the second screen

    def sel_schedule(self, schedule_selection):
        self.schedule_selection = schedule_selection
        print("Selected schedule:", self.schedule_selection)

    def schedule_system(self, interval):
        self.interval = interval
        #print ("Scheduling the scheduling system to execute every", self.interval,"seconds")
        #lock.schedule_interval(partial(self.run_system, (g.imported_schedule) ), self.interval/refresh_period )

    def run_schedule(self, args, dt, *largs):
        self.imported_schedule = g.imported_schedule
        print ("Schedule.run_schedule with self=", self)

    def new_pressure_up(self):
        print ("Schedule: Pressure up")
        pass

    def new_pressure_down(self):
        print ("Schedule: Pressure down")
        pass

    def switch(self):
        print ("Schedule: Switch")
        pass

# class DisplayApp(App):  # defines app and returns display
#     pass
#     print ("DisplayApp class created")
#     def build(self):
#         print("DisplayApp instance run")
#         self.disp = Display()
#         self.disp.schedule_system(refresh_period)
#         return self.disp
#
#     def setup_system(self, control_args, user_args, pressure_parameters, schedule_finished, start_time, elapsed_time,
#                      current_counter, imported_schedule, Global_cnt, past_states, decision, airctrl, schedule, toggle):
#         self.control_args = control_args
#         self.user_args = user_args
#         self.pressure_parameters = pressure_parameters
#         self.schedule_finished = schedule_finished
#         self.start_time = start_time
#         self.elapsed_time = elapsed_time
#         self.current_counter = current_counter
#         self.imported_schedule = imported_schedule
#         self.Global_cnt = Global_cnt
#         self.past_states = past_states
#         self.decision = decision
#         self.airctrl = airctrl
#         self.schedule = schedule
#         self.toggle = toggle
#
#         print (self.pressure_parameters)
#
#         # Create a schedule for the administration of pain and set up the indices and pressure parameters
#         self.current_counter,self.imported_schedule,self.Global_cnt,self.schedule_finished,self.pressure_parameters = \
#             schedule.setup_pain_schedule(self.control_args, self.pressure_parameters)
#
#         painl = int(self.pressure_parameters['PAINVALUE']) - int(self.pressure_parameters['PAINTOLERANCE'])
#         painh = int(self.pressure_parameters['PAINVALUE']) + int(self.pressure_parameters['PAINTOLERANCE'])
#         # Initial PAUSE state is not active, and there is no running schedule.
#         # PAIN mode is disabled and all user inputs default to OFF or 0
#         self.control_args = {'SCHEDULE_INDEX': 0, 'PAIN': 0, 'STARTED': 0, 'PAUSE': 0,
#                         'PAINH': painh, 'PAINL': painl, 'PRESSURE': 0,
#                         'PATM': self.pressure_parameters['PATM'], 'PMAX': self.pressure_parameters['PMAX']}
#         self.user_args = {'GO': 0, 'STOP': 0, 'ABORT': 0, 'UP': 0, 'DOWN': 0,
#                      'override_pressure': self.pressure_parameters['PAINVALUE'], 'OVERRIDE': 0}
#
#         # Create the system state machine that implements the pain control decision and times the relay opening/closing
#         # Vent the cuff first
#         airctrl.FSM.SetState("ISOLATE_VENT")
#         airctrl.Execute(control_args)
#
#         # Initialize the timers
#         self.start_time = time.time()
#         time.process_time()
#
#         g.control_args, g.user_args, g.pressure_parameters, g.elapsed_time, g.start_time,\
#         g.schedule_finished, g.current_counter, g.imported_schedule, g.Global_cnt, g.past_states,\
#         g.decision, g.airctrl, g.schedule, g.toggle =\
#             self.control_args, self.user_args, self.pressure_parameters, self.elapsed_time, self.start_time,\
#             self.schedule_finished, self.current_counter, self.imported_schedule, self.Global_cnt, self.past_states,\
#             self.decision, self.airctrl, self.schedule, self.toggle
#
#         print ("System set up")
#
#         return(self.control_args, self.user_args, self.pressure_parameters,
#                self.elapsed_time, self.start_time, self.schedule_finished,
#                self.current_counter, self.imported_schedule, self.Global_cnt, self.past_states,
#                self.decision, self.airctrl, self.schedule, self.toggle)

class ScreenManagement(ScreenManager):
    pass
    print("Instance of Screen Manager created")
    def build(self):
        print ("Running the instance of ScreenManager")
        #gui = DisplayApp()
        # print("gui: ", gui)

        # Initialize the system global variables.... maybe there is a better way to do this without globals
        #g.control_args, g.user_args, g.pressure_parameters, g.schedule_finished, g.start_time, \
        #g.elapsed_time, g.current_counter, g.imported_schedule, g.Global_cnt, g.past_states, \
        #g.decision, g.airctrl, g.schedule, \
        #g.toggle = gui.setup_system(g.control_args, g.user_args, g.pressure_parameters, \
        #                            g.schedule_finished, g.start_time, g.elapsed_time, \
        #                            g.current_counter, g.imported_schedule, g.Global_cnt, \
        #                            g.past_states, g.decision, g.airctrl, g.schedule, \
        #                            g.toggle)
        #gui.run()

class ScreenManagementApp(App):
    screen_manager = None
    def build(self):
        # initalise the screen manager, add screens and game widget to game screen then return it
        self.screen_manager = ScreenManagement()
        self.schedule_widget = self.screen_manager.add_widget(Schedule(name='schedule'))
        self.display_widget = self.screen_manager.add_widget(Display(name='display'))
        print ("Adding widgets for schedule:",self.schedule_widget," and display", self.display_widget," in self=", self)
        print ("Screen_manager instance=", self.screen_manager)
        #print ("Screen_manager instance.display_widget=", self.screen_manager.display)

        disp = Display()

        return self.screen_manager

if __name__ == '__main__':

    #sched = ScheduleApp()
    #sched.switch_to(name='schedule')
    #sched.run()

    #exit(0)
    sm = ScreenManagementApp()
    print ("Instantiated the screen manager with sm=", sm)
    sm.run()

    #gui = DisplayApp()
    #print("gui: ", gui)

    # Initialize the system global variables.... maybe there is a better way to do this without globals
    #g.control_args, g.user_args, g.pressure_parameters, g.schedule_finished, g.start_time, \
    #g.elapsed_time, g.current_counter, g.imported_schedule, g.Global_cnt, g.past_states, \
    #g.decision, g.airctrl, g.schedule, \
    #g.toggle = gui.setup_system(g.control_args, g.user_args, g.pressure_parameters, \
    #                             g.schedule_finished, g.start_time, g.elapsed_time, \
    #                             g.current_counter, g.imported_schedule, g.Global_cnt, \
    #                             g.past_states, g.decision, g.airctrl, g.schedule, \
    #                             g.toggle)
    #gui.run()

