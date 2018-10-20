from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
#kivy.require("1.10.1")

import commands, pigpio

import sys
sys.path.append("/home/pi/CuffProject")

from app.System.FSM.relay_control import set_relay
from app.GUI.airtank import air_tank

from functools import partial

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.lang import Builder

from app.GUI import g
from app.constants.CONSTANTS import refresh_period
from app.GUI.kivy_color_management import kivy_color_adjustment
from app.GUI.kivy_schedule_update import kivy_schedule_update
from app.GUI.logger import get_logger

from app.constants.CONSTANTS import airtank_stub

from datetime import datetime
from app.System.pressure_measurement.pressure_sampling import Read_Cuff_Pressure

import math
import time

class Display(Screen):  # intro <display> and tells actions/functions
    # Pressure values (current value from sensor and adjustable pain value)
    current_pressure = StringProperty('---')
    new_pressure = StringProperty('---')

    # Schedule values
    phase1 = StringProperty('---'); phase2 = StringProperty('---'); phase3 = StringProperty('---')
    phase4 = StringProperty('---'); phase5 = StringProperty('---'); phase6 = StringProperty('---')
    phase7 = StringProperty('---'); phase8 = StringProperty('---')

    time_state = StringProperty('Starting up the system')

    def __init__(self, **kwargs):
        super(Display, self).__init__(**kwargs)
        self.init_system()
        print ("Display: Started up the Display with control_args:", g.control_args, "and self=", self)

    def build(self):
        pass

    def init_system(self):
        # Initialize the system global variables.... maybe there is a better way to do this without globals
        if (g.already_running == False):
            print ("Initializing system")
            g.control_args, g.user_args, g.pressure_parameters, g.schedule_finished, g.start_time,\
            g.elapsed_time, g.current_counter, g.all_schedules, g.imported_schedule, g.Global_cnt, g.past_states,\
            g.decision, g.airctrl, g.schedule, g.adc,\
            g.toggle, g.schedule_selected, g.schedule_changed, g.already_running =\
                self.setup_system(g.control_args, g.user_args, g.pressure_parameters,\
                                  g.schedule_finished, g.start_time, g.elapsed_time,
                                  g.current_counter, g.all_schedules, g.imported_schedule, g.Global_cnt,\
                                  g.past_states, g.decision, g.airctrl, g.schedule, g.adc,\
                                  g.toggle, g.schedule_selected, g.schedule_changed, g.already_running)

    def setup_system(self, control_args, user_args, pressure_parameters, schedule_finished, start_time, elapsed_time,
                     current_counter, all_schedules, imported_schedule, Global_cnt, past_states, decision, airctrl,
                     schedule, adc, toggle, schedule_selected, schedule_changed, already_running):
        self.control_args = control_args
        self.user_args = user_args
        self.pressure_parameters = pressure_parameters
        self.schedule_finished = schedule_finished
        self.start_time = start_time
        self.elapsed_time = elapsed_time
        self.current_counter = current_counter
        self.all_schedules = all_schedules
        self.imported_schedule = imported_schedule
        self.Global_cnt = Global_cnt
        self.past_states = past_states
        self.decision = decision
        self.airctrl = airctrl
        self.schedule = schedule
        self.adc = adc
        self.toggle = toggle
        self.schedule_selected = schedule_selected
        self.schedule_changed = schedule_changed
        self.already_running = already_running

        # Create a schedule for the administration of pain and set up the indices and pressure parameters
        self.current_counter, self.all_schedules, self.imported_schedule,\
        self.Global_cnt, self.schedule_finished, self.pressure_parameters, self.schedule_selected = \
            schedule.setup_pain_schedule(self.control_args, self.pressure_parameters, self.schedule_selected)
        self.schedule_changed = False

        print ("Setting up system with schedule ", self.schedule_selected)

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

        g.control_args, g.user_args, g.pressure_parameters, g.elapsed_time, g.start_time, g.schedule_finished,\
        g.current_counter, g.all_schedules, g.imported_schedule, g.Global_cnt, g.past_states, g.decision,\
        g.airctrl, g.schedule, g.adc, g.toggle, g.schedule_selected, g.schedule_changed, g.already_running =\
            self.control_args, self.user_args, self.pressure_parameters, self.elapsed_time, self.start_time,\
            self.schedule_finished, self.current_counter, self.all_schedules, self.imported_schedule, self.Global_cnt,\
            self.past_states, self.decision, self.airctrl, self.schedule, self.adc, self.toggle, \
            self.schedule_selected, self.schedule_changed, self.already_running

        return(self.control_args, self.user_args, self.pressure_parameters,
               self.elapsed_time, self.start_time, self.schedule_finished,
               self.current_counter, self.all_schedules, self.imported_schedule, self.Global_cnt, self.past_states,
               self.decision, self.airctrl, self.schedule, self.adc, self.toggle, self.schedule_selected,
               self.schedule_changed, self.already_running)

    def schedule_system(self):
        self.interval = refresh_period
        if (g.already_running == False):
            print ("Scheduling the system to execute every", self.interval,"seconds")
            g.already_running = True
            g.my_logger = get_logger("Pressure log")

            event = Clock.schedule_interval(partial(self.run_system, (g.control_args, g.user_args,\
                                                                      g.pressure_parameters,\
                g.schedule_finished, g.start_time, g.elapsed_time, g.current_counter, g.all_schedules,
                g.imported_schedule, g.Global_cnt, g.past_states, g.decision, g.airctrl, g.schedule, g.adc, g.toggle,\
                g.already_running, g.schedule_selected, g.schedule_changed) ), self.interval )
            #print("EVENT: scheduled run_system with event=", event)
            #Clock.schedule_once(partial(self.run_system, (g.control_args, g.user_args, g.pressure_parameters,\
            #    g.schedule_finished, g.start_time, g.elapsed_time, g.current_counter, g.all_schedules,
            #    g.imported_schedule, g.Global_cnt, g.past_states, g.decision, g.airctrl, g.schedule, g.toggle,\
            #    g.already_running, g.schedule_selected, g.schedule_changed) ) )

    def run_system(self, args, dt, *largs):
        #time_locally = time.asctime(time.localtime(time.time()))
        #print ("dt:", dt, " and localtime=", time_locally)

        self.control_args, self.user_args, self.pressure_parameters, self.elapsed_time, self.start_time, \
        self.schedule_finished, self.current_counter, self.all_schedules, self.imported_schedule,\
        self.Global_cnt, self.past_states, self.already_running,\
        self.decision, self.airctrl, self.schedule, self.adc, self.toggle, self.schedule_selected,\
        self.schedule_changed, self.state_machine_ran =\
            g.control_args, g.user_args, g.pressure_parameters, g.elapsed_time, g.start_time,\
            g.schedule_finished, g.current_counter, g.all_schedules, g.imported_schedule,\
            g.Global_cnt, g.past_states, g.already_running, g.decision, g.airctrl, g.schedule, g.adc,\
            g.toggle, g.schedule_selected, g.schedule_changed, g.state_machine_ran

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
        #print ("State history:", self.past_states)

        self.old_elapsed_time = self.elapsed_time
        #self.elapsed_time = time.time() - self.start_time
        self.elapsed_time = time.time()

        # Pain schedule requires a one-second tick, created at the point where the integer truncation
        # of system time seconds ticks over to the next integer value (e.g. 3.99999992 becomes 4.0000245)
        if math.floor(self.elapsed_time) != math.floor(self.old_elapsed_time):
            self.second_tickover = True
            #print ("***** Second tick at", localtime)
        else:
            self.second_tickover = False

        # Check to make sure that we are running the old schedule.  If not, set up the new one
        if (self.schedule_changed == True):
            print ("Schedule change detected, now set to: ", g.schedule_selected)
            self.schedule_changed = False
            g.control_args, g.user_args, g.pressure_parameters, g.schedule_finished, g.start_time, g.elapsed_time,\
            g.current_counter, g.all_schedules, g.imported_schedule, g.Global_cnt, g.past_states, g.decision,\
            g.airctrl, g.schedule, g.adc, g.toggle, g.schedule_selected, g.schedule_changed, g.already_running =\
                self.setup_system(g.control_args, g.user_args, g.pressure_parameters,\
                                  g.schedule_finished, g.start_time, g.elapsed_time,\
                                  g.current_counter, g.all_schedules, g.imported_schedule, g.Global_cnt,\
                                  g.past_states, g.decision, g.airctrl, g.schedule, g.adc,\
                                  g.toggle, g.schedule_selected, g.schedule_changed, g.already_running)

        # Read the current pressure value
        self.control_args, self.digital_pressure_value, raw_average =\
            Read_Cuff_Pressure(self.adc, self.control_args, self.past_states)
        if (airtank_stub == True):
            air_tank()

        if (self.second_tickover):
            #localtime = time.asctime(time.localtime(time.time()))
            debug_msg = str("Pressure: " + self.current_pressure) + " (" + str(self.digital_pressure_value) +\
                        ";" + str(raw_average) + ")"
            g.my_logger.debug(debug_msg)

        # Micro logging
        #debug_msg = str(self.current_pressure) + " (" + str(self.digital_pressure_value) + ")"
        #g.my_logger.debug(debug_msg)

        # Fix up display of pressure values to be relative to atmospheric pressure, rather than being absolute
        if ( (g.control_args['PRESSURE'] - g.pressure_parameters['PATM']) < 0):
            self.current_pressure = str(0)
        else:
            self.current_pressure = str( g.control_args['PRESSURE'] - g.pressure_parameters['PATM'] )
        self.new_pressure = str( g.user_args['override_pressure'] - g.pressure_parameters['PATM'] )

        # Dynamic conditional update of display values and colours, such as graying out of inactive button text
        self.phase1, self.ids.phase1.color, self.phase2, self.ids.phase2.color,\
        self.phase3, self.ids.phase3.color, self.phase4, self.ids.phase4.color,\
        self.phase5, self.ids.phase5.color, self.phase6, self.ids.phase6.color,\
        self.phase7, self.ids.phase7.color, self.phase8, self.ids.phase8.color,\
        self.ids.go.color, self.ids.stop.color, self.ids.pain.color, self.ids.nopain.color,\
        self.ids.enter.color, self.ids.newpressure.color,\
        self.time_state =\
            kivy_color_adjustment().grey_out(current_counter=self.current_counter, control_args=self.control_args,\
                                             user_args=self.user_args, pressure_parameters=self.pressure_parameters,\
                                             second_tickover=self.second_tickover, airctrl=self.airctrl)

        # Poll for user input and update the GUI based on the control arguments
        # Then update the user signals: {'GO','STOP','ABORT','override_pressure','OVERRIDE'} appropriately
        try:
            # Update or override the control signals: {'PAIN','STARTED','SCHEDULE_INDEX','PAUSE'}
            # Execute the asynchronous part of the state machine that implements the control decisions
            # with the newly-updated control signals and newly-sampled pressure value
            # Update 'PAUSE', 'STARTED', PAINH, PAINL, PAINVALUE, as appropriate
            self.user_args, self.control_args, self.current_counter, self.pressure_parameters,\
            self.schedule_finished, self.toggle, self.schedule_selected, self.state_machine_ran =\
                self.decision.respond_to_user_inputs(self.current_counter, self.all_schedules, self.imported_schedule,\
                                                     self.control_args,\
                                                     self.user_args, self.pressure_parameters, self.second_tickover,\
                                                     self.schedule_finished, self.airctrl,\
                                                     self.schedule, self.adc, self.toggle, self.schedule_selected,\
                                                     self.state_machine_ran)
            if (self.schedule_finished == 1):
                # At the end of the pain schedule, turn off pain and keep venting the cuff in IDLE state
                self.control_args['PAIN'] = 0

            # Execute the state machine
            self.airctrl.FSM.Execute(self.control_args)
            self.state_machine_ran = True

        except KeyboardInterrupt:
            g.adc.pi.spi_close(g.adc.spi_id)
            print("\nDone")
            # Enclose more than this in try/except block

        g.control_args, g.user_args, g.pressure_parameters, g.elapsed_time, g.start_time, g.schedule_finished,\
        g.current_counter, g.all_schedules, g.imported_schedule, g.Global_cnt, g.past_states, g.already_running,\
        g.decision, g.airctrl, g.schedule, g.adc, g.toggle, g.schedule_selected, g.schedule_changed,\
        g.state_machine_ran =\
            self.control_args, self.user_args, self.pressure_parameters, self.elapsed_time, self.start_time,\
            self.schedule_finished, self.current_counter, self.all_schedules, self.imported_schedule, self.Global_cnt,\
            self.past_states, self.already_running, self.decision,\
            self.airctrl, self.schedule, self.adc, self.toggle, self.schedule_selected, self.schedule_changed,\
            self.state_machine_ran

    def on_timeout(self, *args):
        d = datetime.now() - self.start
        self.ids.schedule1.text = datetime.utcfromtimestamp(d.total_seconds()).strftime("%S")

    def abort_ack_function(self):
        self.ids.abort.text = ""

    def abort_function(self):
        print ("Requesting an Abort ...")
        g.user_args['ABORT'] = 1
        self.ids.abort.text = "RELEASE\n  RESET"

    def enter_ack_function(self):
        self.ids.enter.text = ""

    def enter_function(self):
        self.ids.enter.text = "ENTER"
        g.user_args['OVERRIDE'] = 1

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
        #set_relay(s1="open", s2="open", s3="open")

    def new_pressure_up(self):
        g.user_args['override_pressure'] += 1
        print ("Increasing pressure to", g.user_args['override_pressure'])
        #set_relay(s1="closed", s2="closed", s3="closed")

    def switch_function(self):
        self.ids.select.text = "ENTER"
        g.user_args['OVERRIDE'] = 1

    def run_schedule_screen(self, args, *largs):
        print ("Run schedule_screen with self=", self, "and screen manager=", self.screen_manager)

    def run_display_screen(self, args, *largs):
        print ("Run display_screen with self=", self, "and screen manager=", self.screen_manager)

class Schedule(Screen):
    s1_p1= "-"; s1_p2= "-"; s1_p3= "-"; s1_p4= "-"; s1_p5= "-"; s1_p6= "-"; s1_p7= "-"; s1_p8= "-"
    s2_p1= "-"; s2_p2= "-"; s2_p3= "-"; s2_p4= "-"; s2_p5= "-"; s2_p6= "-"; s2_p7= "-"; s2_p8= "-"
    s3_p1= "-"; s3_p2= "-"; s3_p3= "-"; s3_p4= "-"; s3_p5= "-"; s3_p6= "-"; s3_p7= "-"; s3_p8= "-"
    s4_p1= "-"; s4_p2= "-"; s4_p3= "-"; s4_p4= "-"; s4_p5= "-"; s4_p6= "-"; s4_p7= "-"; s4_p8= "-"
    exit_program_text=""
    def __init__(self, **kwargs):
        super(Schedule, self).__init__(**kwargs)
        localtime = time.asctime(time.localtime(time.time()))

    def build(self):
        localtime = time.asctime(time.localtime(time.time()))
        print ("Schedule (build): Started up Schedule Display at:", localtime, "self=", self)
        #Clock.schedule_once(self.run_schedule, 8) # clock callback for the second screen

    def exit_program(self):
        g.adc.pi.spi_close(g.adc.spi_id)
        exit(0)

    def sel_schedule(self, schedule_selection):
        self.schedule_selection = schedule_selection
        self.selected_schedule = int(self.schedule_selection)
        if (g.schedule_selected != self.selected_schedule):
            g.schedule_selected = self.selected_schedule
            g.schedule_changed = True
        print("Changed the selected schedule to schedule ", g.schedule_selected)

    def schedule_system(self, interval):
        self.interval = interval

    def run_schedule(self, args, dt, *largs):
        self.imported_schedule = g.imported_schedule
        print ("Schedule.run_schedule with self=", self)

    def update_schedule_event(self):
        print ("update_schedule_event")
        Clock.schedule_once(partial(self.update_schedule,))

    def update_schedule(self):
        # Fill in the schedule values for the pain schedule page
        self.ids.s1_p1.text, self.ids.s1_p2.text, self.ids.s1_p3.text, self.ids.s1_p4.text,\
        self.ids.s1_p5.text, self.ids.s1_p6.text, self.ids.s1_p7.text, self.ids.s1_p8.text,\
        self.ids.s2_p1.text, self.ids.s2_p2.text, self.ids.s2_p3.text, self.ids.s2_p4.text,\
        self.ids.s2_p5.text, self.ids.s2_p6.text, self.ids.s2_p7.text, self.ids.s2_p8.text,\
        self.ids.s3_p1.text, self.ids.s3_p2.text, self.ids.s3_p3.text, self.ids.s3_p4.text,\
        self.ids.s3_p5.text, self.ids.s3_p6.text, self.ids.s3_p7.text, self.ids.s3_p8.text,\
        self.ids.s4_p1.text, self.ids.s4_p2.text, self.ids.s4_p3.text, self.ids.s4_p4.text,\
        self.ids.s4_p5.text, self.ids.s4_p6.text, self.ids.s4_p7.text, self.ids.s4_p8.text =\
            kivy_schedule_update().schedule_update(all_schedules=g.all_schedules)

    def new_pressure_up(self):
        print ("Schedule: Pressure up")

    def new_pressure_down(self):
        print ("Schedule: Pressure down")

    def switch(self):
        print ("Schedule: Switch")

class ScreenManagement(ScreenManager):
    def build(self):
        print ("Running the instance of ScreenManager with self=", self)
        return self

graphics = Builder.load_file('ScreenManagement.kv')
#class ScreenManagementApp(App):
class Pressure_Control(App):
    screen_manager = None
    def build(self):
        # initalise the screen manager, add screens and game widget to game screen then return it

        # see if it is running already
        status, process = commands.getstatusoutput('sudo pidof pigpiod')
        if (status):  # it wasn't running, so start it
            print ("pigpiod was not running")
            commands.getstatusoutput('sudo pigpiod')  # try to  start it
            time.sleep(0.5)
            # check it again
            status, process = commands.getstatusoutput('sudo pidof pigpiod')

        if (not status):  # if it was started successfully (or was already running)...
            pigpiod_process = process
            print ("pigpiod is running, process ID is {} ",format(pigpiod_process) )

            try:
                self.pi = pigpio.pi()  # local GPIO only
                self.logger.info("pigpio's pi instantiated")
            except Exception as e:
                start_pigpiod_exception = str(e)
                print ("problem instantiating pi: {}",format(start_pigpiod_exception) )
        else:
            print ("start pigpiod was unsuccessful.")

        self.screen_manager = ScreenManagement()
        self.schedule_widget = self.screen_manager.add_widget(Schedule(name='schedule'))
        self.display_widget = self.screen_manager.add_widget(Display(name='display'))
        self.screen_manager.current = 'display'

        print ("graphics:", graphics)
        #return graphics
        #self.screen_manager.display_widget.init_system()
        return self.screen_manager

if __name__ == '__main__':
    sm = Pressure_Control()
    sm.run()
