from kivy.app import App
# kivy.require("1.8.0")
from kivy.base import runTouchApp
from kivy.lang import Builder

from kivy.uix.image import Image

from kivy.uix.widget import Widget

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ListProperty
from kivy.core.window import Window

from kivy.properties import StringProperty

from functools import partial

import time
from kivy.clock import Clock
from datetime import datetime

state = 0


class Display(FloatLayout):  # intro <display> and tells actions/functions
    def __init__(self, **kwargs):
        super(Display, self).__init__(**kwargs)
        self.txt = 170

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

    def newpressure_function(self, event):
        self.event = event
        if (self.event == "up"):
            self.ids.newpressure.text = "up"
            self.txt += 1
        if (self.event == "down"):
            self.ids.newpressure.text = "down"
            self.txt -= 1
        self.ids.newpressure.text = "%d" % self.txt
        print(self.txt)


class DisplayApp(App):  # defines app and returns display
    def build(self):
        return Display()


if __name__ == "__main__":
    DisplayApp().run()
