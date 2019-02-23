#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout

Builder.load_string('''
<MundimRoot>
    id: main
    canvas:
        Color:
            rgba: app.colors['white']
        Rectangle:
            size: self.size
            pos: 0, 0
''')

class MundimRoot(RelativeLayout):
    def __init__(self, **kw):
        super(MundimRoot, self).__init__(**kw)
