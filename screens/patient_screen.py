#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from server_manager import execute_query
Builder.load_string('''
<PatientScreen>
    canvas:
        Color:
            rgba: app.colors['off_white']
        Rectangle:
            size: self.size
            pos: 0, 0
    PatientScreenTopBar:
        id: top_bar
        pos: 0, root.height - self.height

    N4TextInput:
        id: chart_id_txt
        hint_text: 'ID'
        edit_size: 'large'
        pos: int(dp(30)), int(top_bar.y - self.height - dp(10))
        on_text:
            root.chart_id = self.text
    N4TextInput:
        id: diagnostico_txt
        hint_text: 'DIAGNOSTICO'
        edit_size: 'large'
        pos: chart_id_txt.x, int(chart_id_txt.y - self.height - dp(5))
        on_text:
            root.initial_diagnostic = self.text
    N4Image:
        source: './assets/img/separator_2.png'
        height: 1
        center_x: self.parent.center_x
        y: int(diagnostico_txt.y - self.height - dp(10))
    N4ImageButton:
        source: './assets/img/save_data_btn.png'
        on_press:
            root.save_edited_patient()
            app.root.undo()

<PatientScreenTopBar@RelativeLayout>
    canvas:
        Color:
            rgba: app.colors['white']
        Rectangle:
            size: self.size
            pos: 0, 0
    size_hint: 1, None
    height: int(dp(47))
    N4ImageButton:
        source: './assets/img/back_btn.png'
        center_y: title.center_y
        on_press:
            app.root.undo()
    N4Label:
        id: title
        style: 'mont-title'
        text: 'Paciente: ' + root.parent.chart_id
        pos: dp(55), root.height/2.0 - self.height/2.0
    RippledImageButton:
        ripple_rad_default: 0
        x: root.width - self.width
        center_y: title.center_y
        source: './assets/img/dots.png'
    N4Image:
        source: './assets/img/separator_2.png'
        size_hint_x: 1
        height: 1

''')

class PatientScreen(Screen):
    chart_id = StringProperty('')
    age = StringProperty('')
    initial_diagnostic = StringProperty('')
    id = StringProperty('') # database id
    def __init__(self, **kw):
        super(PatientScreen, self).__init__(**kw)

    def save_edited_patient(self):
        app = App.get_running_app()
        patients = app.patients[:]

        for index, patient in enumerate(patients):
            print patients[index]['id'] == self.id
            if patients[index]['id'] == self.id:
                patients[index]['chart_id'] = self.chart_id
                patients[index]['age'] = self.age
                patients[index]['initial_diagnostic'] = self.diagnostic
        app.patients = []
        app.patients = patients

        execute_query(u" \
            UPDATE patients SET \
            chart_id = '{}', \
            age = '{}', \
            initial_diagnostic = '{}' \
            WHERE id = '{}'; \
            ".format(self.chart_id, self.age, self.initial_diagnostic, self.id), threaded=True)
