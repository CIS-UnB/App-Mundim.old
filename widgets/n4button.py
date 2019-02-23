#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ListProperty, BooleanProperty
from widgets.n4label import N4Label
from kivy.uix.behaviors import ButtonBehavior
Builder.load_string('''
<N4Button>
    canvas.before:
        Color:
            rgba: app.colors['red_test'] if root.debug else [0, 0, 0, 0]
        Rectangle:
            size: self.size
            pos: self.pos
    style: 'body'
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
