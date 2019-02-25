#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from widgets.n4image import N4Image
from kivy.uix.behaviors import ButtonBehavior
from widgets.touchripple import TouchRippleButtonBehavior
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

    def on_press(self):
        if self.debug:
            print 'PRESSED', self.source

class RippledImageButton(TouchRippleButtonBehavior, N4Image):
    ripple_rad_default = 90
    ripple_duration_in = 0.5
    ripple_duration_out = 0.5
    ripple_fade_from_alpha = 0.5
    ripple_scale = 2
    circular_ripple = 2

    def __init__(self, **kwargs):
        self.bind(upper_ripple_completed=self.on_ripple_completed)
        super(RippledImageButton, self).__init__(**kwargs)
        self.ripple_color = [0.9, 0.9, 0.9, 1]

    def on_ripple_completed(self, instance, value):
        if not value:
            return
