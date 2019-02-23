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
        'white': hex_to_rgb('FFFFFF'),
        'off_white': hex_to_rgb('fafafb'), # details color
        'grey_1': hex_to_rgb('2e323d'), # menu color
        'grey_2': hex_to_rgb('3b414c'), # topbar color
        'grey_3': hex_to_rgb('474e59'), # topestbar color
        'grey_4': hex_to_rgb('2E323D'),
        'grey_5': hex_to_rgb('62656e'), # disabled color
        'green_1': hex_to_rgb('48C136'),
        'red_1': hex_to_rgb('C61033'),
        'red_2': hex_to_rgb('E22727'),
        'red_3': hex_to_rgb('FF2424'),
        'red_test': hex_to_rgb('FF0000')[:3] + [0.1],
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
