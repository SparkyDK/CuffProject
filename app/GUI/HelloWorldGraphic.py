#:kivy 1.10.1
import kivy
kivy.require('1.10.1') # replace with your current kivy version !

#import kivy
#print("KIVY version is", kivy.__version__)

from kivy.app import App
from kivy.uix.label import Label

class HelloWorld(App):

    def build(self):
        return Label(text='Hello world')

