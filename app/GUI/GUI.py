from kivy.app import App
# kivy.require("1.8.0")
from kivy.base import runTouchApp
from kivy.lang import Builder

from kivy.uix.image import Image

from kivy.uix.widget import Widget

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.properties import ListProperty
from kivy.core.window import Window

from kivy.animation import Animation
from kivy.properties import StringProperty

from functools import partial

import random

from kivy.app import App

import time
from kivy.clock import Clock

from datetime import datetime

state = 0


class Display(FloatLayout):  # intro <display> and tells actions/functions
    def __init__(self, **kwargs):
        super(Display, self).__init__(**kwargs)
        print (kwargs)
        # self.txt = 170

    def update(self, current_counter, control_args, user_args):
        self.current_counter = current_counter
        self.control_args = control_args
        # current_counter = [] * max_num_schedules
        # control_args = {'SCHEDULE_INDEX': 0, 'PAIN': 0, 'STARTED': 0, 'PAUSE': 0, 'FORCE': 0}
        # user_args = {'GO': 0, 'STOP': 0, 'ABORT': 0, 'UP': 0, 'DOWN': 0
        #              'override_pressure': pressure_parameters['PAINVALUE'], 'OVERRIDE': 0}
        return(user_args)

    def count(self, *varargs):
        self.start = datetime.now()
        Clock.schedule_interval(self.on_timeout, 1)

    def on_timeout(self, *args):
        d = datetime.now() - self.start
        self.ids.schedule1.text = datetime.utcfromtimestamp(d.total_seconds()).strftime("%S")

    def abort_function(self):
        self.ids.abort.text = "Clicked"

    def enter_function(self):
        self.ids.enter.text = "Clicked"

    def go_function(self):
        self.ids.go.text = "Clicked"  # changes go to clicked when clicked

    def stop_function(self):
        self.ids.stop.text = "Clicked"

    def newpressureup(self):
        pass

    def newpressure_function(self, direction, desired_pressure):
        app = App.get_running_app()
        # self.direction = direction
        # self.desired_pressure = desired_pressure

        if (direction == "up"):
            app.desired_pressure += 1
        elif (direction == "down"):
            app.desired_pressure -= 1
        else:
            print ("Error! newpressure_function: We should not be here (expecting 'up' or 'down' only)")

        self.ids.newpressure.text = "%d" % app.desired_pressure
        print ("New desired pressure is now ", app.desired_pressure)


class DisplayApp(App):  # defines app and returns display

    #desired_pressure = Patm

    desired_pressure = 0
    ENTER = 0
    STOP = 0
    GO = 0
    ABORT = 0

    current_pressure = 0
    disp = Display()


def build(self):
    return DisplayApp.disp


#if __name__ == "__main__":
#    gui = DisplayApp()
#    gui.run()
# DisplayApp().run()