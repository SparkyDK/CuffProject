from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')

from app.GUI.GUI_main import DisplayApp

gui = DisplayApp()
gui.run()

