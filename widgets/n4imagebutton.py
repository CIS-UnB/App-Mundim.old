#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from widgets.n4image import N4Image
from kivy.uix.behaviors import ButtonBehavior

Builder.load_string('''
<N4ImageButton>
    canvas.before:
        Color:
            rgba: app.colors['debug'] if root.debug else [0, 0, 0, 0]
        Rectangle:
            size: self.size
            pos: self.pos
''')

class N4ImageButton(ButtonBehavior, N4Image):
    debug = BooleanProperty(False)
    def __init__(self, **kw):
        super(N4ImageButton, self).__init__(**kw)
