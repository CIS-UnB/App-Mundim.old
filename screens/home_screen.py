#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string('''
<HomeScreen>
    TopBar:
        pos: 0, root.height - self.height
    N4ImageButton:
        source: './assets/img/add_patient_btn.png'
        pos: root.width - self.width - dp(35), dp(25) 

<TopBar@RelativeLayout>
    canvas:
        Color:
            rgba: app.colors['white']
        Rectangle:
            size: self.size
            pos: 0, 0
    size_hint: 1, None
    height: dp(82.5)
    N4Label:
        text: 'Pacientes'
        pos: dp(32), dp(53)
    N4Image:
        source: './assets/img/separator.png'
    N4Button:
        id: todos_btn
        text: 'Todos'
        style: 'mont-body-selected'
        size_hint_x: 0.5
        height: dp(33.5)
        halign: 'left'
        padding_x: dp(32)
    N4Button:
        text: 'Sem Prognóstico'
        style: 'mont-body'
        size_hint_x: 0.5
        height: dp(33.5)
        halign: 'center'
        pos: todos_btn.width, 0
    N4Image:
        pos: root.width - self.width, root.height - self.height
        source: './assets/img/dots.png'
''')

class HomeScreen(Screen):
    def __init__(self, **kw):
        super(HomeScreen, self).__init__(**kw)
