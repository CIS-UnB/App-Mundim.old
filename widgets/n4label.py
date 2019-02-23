#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import StringProperty
Builder.load_string('''
<N4Label>
    canvas.before:
        Color:
            rgba: app.colors['red_test'] if root.debug else [0, 0, 0, 0]
        Rectangle:
            size: self.size
            pos: self.pos
    size_hint: None, None
    size: self.texture_size if self.opacity > 0 else (0, 0)
    style: 'title'
    font: './assets/fonts/' + root.font_name
    color: app.colors['white'] if root.enabled else app.colors['grey_5']
    canvas:
        Color:
            rgba: 0, 0, 0, 0
        Rectangle:
            size: self.size
            pos: self.pos
''')

class N4Label(Label):
    debug = BooleanProperty(False)
    style = StringProperty('body')
    font_name = StringProperty('Montserrat-Regular.ttf')

    styles = {
        'mont-title':{
            'font_name': 'Montserrat-Regular.ttf',
            'font_size': 55,
        },
        'mont-body-selected':{
            'font_name': 'Montserrat-SemiBold.ttf',
            'font_size': 45,
        },
        'mont-body':{
            'font_name': 'Montserrat-Regular.ttf',
            'font_size': 45,
        },
    }

    def __init__(self, **kw):
        super(N4Label, self).__init__(**kw)
        self.on_style(None, self.style)

    def on_style(self, instance, style):
        for attr in self.styles[style]:
            setattr(self, attr, self.styles[style][attr])
