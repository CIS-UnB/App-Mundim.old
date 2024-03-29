#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.relativelayout import RelativeLayout
import datetime
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
        source: './assets/img/separator_2.png'
        size_hint_x: 1
        height: 1
        y: root.height - 1
    N4Image:
        source: './assets/img/separator_2.png'
        size_hint_x: 1
        height: 1
        y: 0
    N4Image:
        id: diagnostic_img
        source: './assets/img/diagnostic_sent.png' if root.initial_diagnostic != '' else \
            './assets/img/diagnostic_unsent.png'
        pos: dp(11), root.height / 2.0 - self.height / 2.0
    N4Label:
        text: root.chart_id
        pos: dp(45), root.height / 2.0 - self.height / 2.0
    N4Label:
        text: root.creation_hour
        pos: root.width - self.width - dp(20), root.height / 2.0 - self.height / 2.0
    N4Button:
        size_hint: 1, 1
        on_press:
            root.load_patient_screen()
''')

class Patient(RelativeLayout):
    debug = BooleanProperty(False)
    date_of_creation = StringProperty('')
    creation_hour = StringProperty('')

    # database info
    id = StringProperty('')
    chart_id = StringProperty('')
    age = StringProperty('')
    sex = StringProperty('')
    anatomic_area = StringProperty('')
    initial_diagnostic = StringProperty('')
    biopsy_diagnostic = StringProperty('')

    def __init__(self, **kw):
        super(Patient, self).__init__(**kw)
        if not self.date_of_creation:
            self.date_of_creation = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def load_patient_screen(self):
        app = App.get_running_app()
        patient_screen = app.root.ids.patient_screen
        patient_screen.id = self.id

        patient_screen.ids.chart_id_txt.text = self.chart_id
        patient_screen.ids.age_txt.text = self.age
        patient_screen.ids.sex_txt.text = self.sex
        patient_screen.ids.anatomic_area_txt.text = self.anatomic_area
        patient_screen.ids.initial_diagnostic_txt.text = self.initial_diagnostic
        patient_screen.ids.biopsy_diagnostic_txt.text = self.biopsy_diagnostic
        app.root.change_screen('patient_screen')

    def on_date_of_creation(self, instance, value):
        self.creation_hour = self.get_creation_hour()

    def get_creation_hour(self):
        return datetime.datetime.strptime(self.date_of_creation, '%Y-%m-%d %H:%M:%S').strftime('%d/%m, %H:%M')
