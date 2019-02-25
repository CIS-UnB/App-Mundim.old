#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.relativelayout import RelativeLayout
Builder.load_string('''
<Patient>
    canvas.before:
        Color:
            rgba: app.colors['debug'] if root.debug else [0, 0, 0, 0]
        Rectangle:
            size: self.size
            pos: self.pos
    size_hint: None, None
    size: dp(300), dp(50)
    N4Image:
        source: './assets/img/separator.png'
        size_hint_x: 1
        height: 1
        y: root.height - 1
    N4Image:
        source: './assets/img/separator.png'
        size_hint_x: 1
        height: 1
        y: 0
    N4Image:
        id: diagnostic_img
        source: './assets/img/diagnostic_sent.png' if root.diagnostic != '' else \
            './assets/img/diagnostic_unsent.png'
        center_y: root.center_y
        x: dp(11)
    N4Label:
        text: root.name
        pos: dp(45), root.height / 2.0 - self.height / 2.0
    N4Label:
        text: root.date_of_creation
        pos: root.width - self.width - dp(11), root.height / 2.0 - self.height / 2.0
''')

class Patient(RelativeLayout):
    debug = BooleanProperty(False)
    name = StringProperty('')
    age = StringProperty('')
    surname = StringProperty('')
    diagnostic = StringProperty('')
    date_of_creation = StringProperty('')
    def __init__(self, **kw):
        super(Patient, self).__init__(**kw)
