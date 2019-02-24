#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, BooleanProperty
from widgets.n4label import N4Label
from kivy.metrics import dp
Builder.load_string('''
<N4TextInput>
    size_hint: None, None
    size: dp(290), dp(44)
    font_name: './assets/fonts/Montserrat-Regular.ttf' if self.text != '' else \
        './assets/fonts/Montserrat-Medium.ttf'
    font_size: dp(11) if self.text != '' else dp(9)
    use_bubble: False
    foreground_color: [0, 0, 0, 1]
    cursor_color: [0, 0, 0, 1]
    padding_x: dp(20)
    padding_y: dp(15)
''')

class N4TextInput(TextInput):
    debug = BooleanProperty(False)
    edit_size = StringProperty('large')

    def on_edit_size(self, instance, value):
        if value == 'large':
            self.background_active = './assets/img/text_input_large.png'
            self.background_normal = './assets/img/text_input_large.png'
            self.size = dp(290), dp(44)
        elif value == 'medium':
            self.background_active = './assets/img/text_input_medium.png'
            self.background_normal = './assets/img/text_input_medium.png'
            self.size = dp(189), dp(44)
        elif value == 'small':
            self.background_active = './assets/img/text_input_small.png'
            self.background_normal = './assets/img/text_input_small.png'
            self.size = dp(96), dp(44)

    def __init__(self, **kw):
        super(N4TextInput, self).__init__(**kw)
        self.on_edit_size(self, self.edit_size)
