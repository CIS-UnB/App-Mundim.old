#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ListProperty, BooleanProperty
from widgets.n4label import N4Label
from kivy.uix.behaviors import ButtonBehavior
from widgets.ripplebehavior import RippleButtonBehavior
Builder.load_string('''
<N4Button>
    canvas.before:
        Color:
            rgba: app.colors['debug'] if root.debug else [0, 0, 0, 0]
        Rectangle:
            size: self.size
            pos: self.pos
    style: 'mont-body'
    size_hint: None, None
    valign: 'center'
    halign: 'center'
    size: (100, 100) if self.opacity > 0 else (0, 0)
    text_size: self.size
''')

class N4Button(ButtonBehavior, N4Label):
    debug = BooleanProperty(False)

    def __init__(self, **kw):
        super(N4Button, self).__init__(**kw)

    def on_press(self):
        if self.debug:
            print 'PRESSED', self.text


class RippledN4Button(RippleButtonBehavior, N4Button):
    ripple_rad_default = 50
    ripple_duration_in = 0.5
    ripple_duration_out = 0.5
    ripple_fade_from_alpha = 0.5
    ripple_scale = 2

    def __init__(self, **kwargs):
        self.bind(upper_ripple_completed=self.on_ripple_completed)
        super(RippledN4Button, self).__init__(**kwargs)
        self.register_event_type('on_press')

    def on_ripple_completed(self, instance, value):
        if not value:
            return

    def on_touch_down(self, touch):
        collide_point = self.collide_point(touch.x, touch.y)
        if collide_point:
            touch.grab(self)
            self.ripple_show(touch)

            return True
        return False

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.ripple_fade()
            if self.collide_point(touch.x, touch.y):
                self.dispatch('on_press')
            return True
        return False
