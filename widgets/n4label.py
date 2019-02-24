#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import StringProperty, BooleanProperty
from kivy.metrics import sp
Builder.load_string('''
<N4Label>
    canvas.before:
        Color:
            rgba: app.colors['debug'] if root.debug else [0, 0, 0, 0]
        Rectangle:
            size: self.size
            pos: self.pos
    size_hint: None, None
    size: self.texture_size if self.opacity > 0 else (0, 0)
    font: './assets/fonts/' + root.font_name
    color: app.colors['black']
    canvas:
        Color:
            rgba: 0, 0, 0, 0
        Rectangle:
            size: self.size
            pos: self.pos
''')

class N4Label(Label):
    debug = BooleanProperty(False)
    style = StringProperty('mont-body')
    font_name = StringProperty('Montserrat-Regular.ttf')

    styles = {
        'mont-title':{
            'font_name': 'Montserrat-Regular.ttf',
            'font_size': sp(13.75),
        },
        'mont-body-selected':{
            'font_name': 'Montserrat-SemiBold.ttf',
            'font_size': sp(11.25),
        },
        'mont-body':{
            'font_name': 'Montserrat-Regular.ttf',
            'font_size': sp(11.25),
        },
    }

    def __init__(self, **kw):
        super(N4Label, self).__init__(**kw)
        self.on_style(None, self.style)

    def on_style(self, instance, style):
        for attr in self.styles[style]:
            setattr(self, attr, self.styles[style][attr])
