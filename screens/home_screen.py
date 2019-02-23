#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string('''
<HomeScreen>
    canvas:
        Color:
            rgba: app.colors['off_white']
        Rectangle:
            size: self.size
            pos: 0, 0
    HomeScreenTopBar:
        pos: 0, root.height - self.height
    N4ImageButton:
        source: './assets/img/add_patient_btn.png'
        pos: root.width - self.width - dp(35), dp(25)
        on_press:
            app.root.change_screen('new_patient_screen')

<HomeScreenTopBar@RelativeLayout>
    canvas:
        Color:
            rgba: app.colors['white']
        Rectangle:
            size: self.size
            pos: 0, 0
    size_hint: 1, None
    height: int(dp(82.5))
    N4Label:
        style: 'mont-title'
        text: 'Pacientes'
        pos: dp(32), dp(50)
    N4Image:
        source: './assets/img/separator.png'
        height: 1
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
    N4ImageButton:
        pos: root.width - self.width, root.height - self.height
        source: './assets/img/dots.png'
''')

class HomeScreen(Screen):
    def __init__(self, **kw):
        super(HomeScreen, self).__init__(**kw)
