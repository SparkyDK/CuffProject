#:kivy 1.10.1
import kivy
kivy.require('1.10.1') # replace with your current kivy version !

#import kivy
#print("KIVY version is", kivy.__version__)

from kivy.app import App

from kivy.uix.label import Label

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.properties import ObjectProperty


from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ListProperty

class MovableRect(Widget):
    color = ListProperty([1, 0, 1, 0.5])

class HelloWorldApp(App):

    def build(self):
        pass
       #return Label(text='Hello world')

