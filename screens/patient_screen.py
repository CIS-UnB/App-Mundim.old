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
        edit_size: 'small'
        pos: int(dp(30)), int(top_bar.y - self.height - dp(10))
        on_text:
            root.chart_id = self.text
    N4TextInput:
        id: age_txt
        hint_text: 'IDADE'
        edit_size: 'small'
        pos: chart_id_txt.x + chart_id_txt.width, chart_id_txt.y
        on_text:
            root.age = self.text
    N4TextInput:
        id: sex_txt
        hint_text: 'SEXO (M/F)'
        edit_size: 'small'
        pos: age_txt.x + age_txt.width, age_txt.y
        on_text:
            root.sex = self.text
    N4TextInput:
        id: anatomic_area_txt
        hint_text: 'AREA ANATOMICA'
        edit_size: 'large'
        pos: chart_id_txt.x, int(chart_id_txt.y - self.height - dp(5))
        on_text:
            root.anatomic_area = self.text
    N4TextInput:
        id: initial_diagnostic_txt
        hint_text: 'DIAGNOSTICO'
        edit_size: 'large'
        pos: anatomic_area_txt.x, int(anatomic_area_txt.y - self.height - dp(5))
        on_text:
            root.initial_diagnostic = self.text
    N4TextInput:
        id: biopsy_diagnostic_txt
        hint_text: 'BIOPSIA'
        edit_size: 'large'
        pos: initial_diagnostic_txt.x, int(initial_diagnostic_txt.y - self.height - dp(5))
        on_text:
            root.biopsy_diagnostic = self.text
    N4Image:
        source: './assets/img/separator_2.png'
        height: 1
        center_x: self.parent.center_x
        y: int(biopsy_diagnostic_txt.y - self.height - dp(10))
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
    # database info
    id = StringProperty('')
    chart_id = StringProperty('')
    age = StringProperty('')
    sex = StringProperty('')
    anatomic_area = StringProperty('')
    initial_diagnostic = StringProperty('')
    biopsy_diagnostic = StringProperty('')

    def __init__(self, **kw):
        super(PatientScreen, self).__init__(**kw)

    def save_edited_patient(self):
        app = App.get_running_app()
        patients = app.patients[:]

        for index, patient in enumerate(patients):
            if patients[index]['id'] == self.id:
                patients[index]['chart_id'] = self.chart_id
                patients[index]['age'] = self.age
                patients[index]['sex'] = self.sex
                patients[index]['anatomic_area'] = self.anatomic_area
                patients[index]['initial_diagnostic'] = self.initial_diagnostic
                patients[index]['biopsy_diagnostic'] = self.biopsy_diagnostic
        app.patients = []
        app.patients = patients

        execute_query(u" \
            UPDATE patients SET \
            chart_id = '{}', \
            age = '{}', \
            sex = '{}', \
            anatomic_area = '{}', \
            initial_diagnostic = '{}', \
            biopsy_diagnostic = '{}' \
            WHERE id = '{}'; \
            ".format(self.chart_id, self.age, self.sex, self.anatomic_area, self.initial_diagnostic, self.biopsy_diagnostic, self.id), debug=True)
