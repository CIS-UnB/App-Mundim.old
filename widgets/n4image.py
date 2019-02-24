#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import NumericProperty, BooleanProperty
from kivy.uix.image import Image
Builder.load_string('''
<N4Image>
    canvas.before:
        PushMatrix
        Color:
            rgba: app.colors['debug'] if root.debug else [0, 0, 0, 0]
        Rectangle:
            size: self.size
            pos: self.pos
        Rotate:
            angle: root.angle
            axis: 0, 0, 1
            origin: root.center
    canvas.after:
        PopMatrix
    canvas.before:


    allow_stretch: True
    keep_ratio: False
    size_hint: (None, None) if self.opacity > 0 else (0, 0)
    size: (dp(self.texture_size[0]/4), dp(self.texture_size[1]/4)) if self.opacity > 0 else (0, 0)

''')

class N4Image(Image):
    angle = NumericProperty(0)
    debug = BooleanProperty(False)
    def __init__(self, **kw):
        super(N4Image, self).__init__(**kw)
