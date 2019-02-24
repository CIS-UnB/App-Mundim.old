#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from screens.home_screen import HomeScreen
Builder.load_string('''
<MundimRoot>
    id: main
    ScreenManager:
        id: screen_manager
        canvas:
            Color:
                rgba: app.colors['off_white']
            Rectangle:
                size: self.size
                pos: 0, 0
        HomeScreen:
            id: home_screen
            name: 'home_screen'

''')

class MundimRoot(RelativeLayout):
    def __init__(self, **kw):
        super(MundimRoot, self).__init__(**kw)
