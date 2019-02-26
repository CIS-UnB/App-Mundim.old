#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string('''
#:import Patient widgets.patient.Patient
<HomeScreen>
    canvas:
        Color:
            rgba: app.colors['off_white']
        Rectangle:
            size: self.size
            pos: 0, 0
    HomeScreenTopBar:
        id: top_bar
        pos: 0, root.height - self.height
    N4Image:
        id: exams_label
        source: './assets/img/patient_exam_label.png'
        center_x: self.parent.center_x
        y: top_bar.y - self.height - dp(6)
    ScreenManager:
        id: screen_manager
        size_hint: 1, None
        height: exams_label.y - dp(6)
        Screen:
            id: todos_screen
            name: 'todos_screen'
            on_pre_enter:
                top_bar.ids.todos_btn.style = 'mont-body-selected'
                top_bar.ids.sem_prognostico_btn.style = 'mont-body'
            N4Label:
                text: 'Sem pacientes adicionados.' if app.patients_ammount == 0 else \
                    ('Carregando pacientes...' if app.patients_ammount == -1 else '')
                y: self.parent.height - self.height - dp(10)
                center_x: self.parent.center_x
            RecycleView:
                size_hint: None, None
                size: dp(300), self.parent.height - dp(6)
                viewclass: 'Patient'
                data: app.patients
                center_x: self.parent.center_x
                RecycleGridLayout:
                    cols: 1
                    size_hint: 1, None
                    height: self.minimum_height
                    spacing: -1

        Screen:
            id: sem_prognostico_screen
            name: 'sem_prognostico_screen'
            on_pre_enter:
                top_bar.ids.sem_prognostico_btn.style = 'mont-body-selected'
                top_bar.ids.todos_btn.style = 'mont-body'
            N4Label:
                text: 'Todos os pacientes já foram diagnosticados.' if app.no_prognostic_patients_ammount == 0 else \
                    ('Carregando pacientes...' if app.patients_ammount == -1 else '')
                y: self.parent.height - self.height - dp(10)
                center_x: self.parent.center_x
            RecycleView:
                size_hint: None, None
                size: dp(300), self.parent.height - dp(6)
                viewclass: 'Patient'
                data: app.no_prognostic_patients
                center_x: self.parent.center_x
                RecycleGridLayout:
                    cols: 1
                    size_hint: 1, None
                    height: self.minimum_height
                    spacing: -1
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
    height: int(dp(72))
    N4Label:
        id: title
        style: 'mont-title'
        text: 'Pacientes'
        pos: dp(32), dp(50)
    N4Image:
        source: './assets/img/separator_2.png'
        size_hint_x: 1
        height: 1
    RippledN4Button:
        id: todos_btn
        text: 'Todos'
        style: 'mont-body-selected'
        size_hint_x: 0.5
        height: dp(33.5)
        halign: 'left'
        padding_x: dp(32)
        on_press:
            app.root.change_screen('todos_screen', \
                direction='right', \
                transition='slide', \
                queue_enabled=False, \
                screen_manager=app.root.ids.home_screen.ids.screen_manager)
    RippledN4Button:
        id: sem_prognostico_btn
        text: 'Sem Prognóstico'
        style: 'mont-body'
        size_hint_x: 0.5
        height: dp(33.5)
        halign: 'center'
        pos: todos_btn.width, 0
        on_press:
            app.root.change_screen('sem_prognostico_screen', \
                transition='slide', \
                queue_enabled=False, \
                screen_manager=app.root.ids.home_screen.ids.screen_manager)
    RippledImageButton:
        ripple_rad_default: 0
        x: root.width - self.width
        center_y: title.center_y
        source: './assets/img/dots.png'
''')

class HomeScreen(Screen):
    def __init__(self, **kw):
        super(HomeScreen, self).__init__(**kw)
