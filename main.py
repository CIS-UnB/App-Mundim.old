#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True

from kivy.app import App
from kivy.base import EventLoop
from kivy.properties import DictProperty

from widgets.n4textinput import N4TextInput
from widgets.n4label import N4Label
from widgets.n4button import N4Button
from widgets.n4image import N4Image
from widgets.n4imagebutton import N4ImageButton
from root import MundimRoot
from kivy.utils import platform
from utils import hex_to_rgb, set_statusbar_color

class Mundim(App):
    colors = DictProperty({
        'black': hex_to_rgb('000000'),
        'white': hex_to_rgb('FFFFFF'),
        'off_white': hex_to_rgb('F3F3F3'),
        'blue_1': hex_to_rgb('73B9E8'),
        'green_1': hex_to_rgb('73E89A'),
        'debug': hex_to_rgb('FF0000')[:3] + [0.1],
    })

    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)
        if platform == 'android':
            set_statusbar_color('#FFFFFF')

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.root.undo()
            return True

    def build(self):
        self.root = MundimRoot()
        self.root.app = self
        return self.root

Mundim().run()
