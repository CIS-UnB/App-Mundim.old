#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True

from kivy.app import App
from kivy.base import EventLoop
from kivy.properties import DictProperty

from root import MundimRoot
from utils import hex_to_rgb

from kivy.utils import platform
from kivy.config import Config
if platform == 'linux' or platform == 'win':
    Config.set('graphics', 'width', '480')
    Config.set('graphics', 'height', '986')

class Mundim(App):
    queue = []
    colors = DictProperty({
        'black': hex_to_rgb('000000'),
        'white': hex_to_rgb('FFFFFF'),
        'off_white': hex_to_rgb('F3F3F3'),
        'blue_1': hex_to_rgb('73B9E8'),
        'green_1': hex_to_rgb('73E89A'),
        'debug': hex_to_rgb('FF0000')[:3] + [0.1],
    })

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            if len(self.queue) > 0:
                self.back()
        return True

    def build(self):
        self.root = MundimRoot()
        self.root.app = self
        return self.root

Mundim().run()
