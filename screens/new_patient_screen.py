#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from server_manager import execute_query
from kivy.metrics import dp
from kivy.properties import NumericProperty

Builder.load_string('''
<NewPatientScreen>
    canvas:
        Color:
            rgba: app.colors['off_white']
        Rectangle:
            size: self.size
            pos: 0, 0
    on_enter:
        camera_object.play = True
    on_leave:
        camera_object.play = False
    ScreenManager:
        id: screen_manager
        size_hint: 1, None
        height: top_bar.y - dp(6)
        Screen:
            id: amostragem_screen
            name: 'amostragem_screen'
            on_pre_enter:
                top_bar.ids.amostragem_btn.style = 'mont-body-selected'
                top_bar.ids.outros_dados_btn.style = 'mont-body'
            XCamera:
                id: camera_object
                size_hint: None, None
                resolution: 1, 1
                size: root.height * self.resolution[0]/self.resolution[1] * root.camera_zoom, root.height * root.camera_zoom
                keep_ratio: False
                allow_stretch: True
                canvas.before:
                    PushMatrix
                    Rotate:
                        angle: -90
                        origin: root.center
                canvas.after:
                    PopMatrix
                pos: (root.width - self.width)/2.0, (root.height - self.height)/2.0
            Overlay:
                size_hint: 1, 1
            RippledImageButton:
                source: './assets/img/take_photo_btn.png'
                center_x: self.parent.center_x
                y: dp(25)
                on_press: camera_object.shoot('temp.jpg')
        Screen:
            id: outros_dados_screen
            name: 'outros_dados_screen'
            on_pre_enter:
                top_bar.ids.amostragem_btn.style = 'mont-body'
                top_bar.ids.outros_dados_btn.style = 'mont-body-selected'
            Widget:
                size_hint: 1, 1
                canvas:
                    Color:
                        rgba: app.colors['off_white']
                    Rectangle:
                        size: self.size
                        pos: self.pos
            N4ImageButton:
                debug: True
                source: './assets/img/send_data_btn.png'
                on_press:
                    root.add_patient(chart_id_txt, diagnostico_txt)
                    app.root.change_screen('home_screen', \
                        direction='right', \
                        queue_enabled=False)

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
            N4Image:
                source: './assets/img/separator_2.png'
                height: 1
                center_x: self.parent.center_x
                y: int(diagnostico_txt.y - self.height - dp(10))
    NewPatientScreenTopBar:
        id: top_bar
        pos: 0, root.height - self.height


<Overlay@RelativeLayout>
    square_size: dp(150)
    y_offset: dp(50)
    Widget:
        canvas:
            Color:
                rgba: [0, 0, 0, 0.5]
            Rectangle:
                size: self.size
                pos: self.pos
        size_hint: None, None
        size: (root.width - root.square_size) / 2, root.square_size
        pos: 0, (root.height - root.square_size) / 2 + root.y_offset
    Widget:
        canvas:
            Color:
                rgba: [0, 0, 0, 0.5]
            Rectangle:
                size: self.size
                pos: self.pos
        size_hint: 1, None
        height: (root.height - root.square_size) / 2
        y: (root.height - root.square_size) / 2 + root.square_size + root.y_offset
    Widget:
        canvas:
            Color:
                rgba: [0, 0, 0, 0.5]
            Rectangle:
                size: self.size
                pos: self.pos
        size_hint: None, None
        size: (root.width - root.square_size) / 2, root.square_size
        pos: (root.width - root.square_size) / 2 + root.square_size + 1, (root.height - root.square_size) / 2 + root.y_offset
    Widget:
        canvas:
            Color:
                rgba: [0, 0, 0, 0.5]
            Rectangle:
                size: self.size
                pos: self.pos
        size_hint: 1, None
        height: (root.height - root.square_size) / 2 + root.y_offset


    Widget:
        canvas:
            Color:
                rgba: [1, 1, 1, 1]
            Rectangle:
                size: self.size
                pos: self.pos
        size_hint: None, 1
        width: 1
        x: int((root.width - root.square_size) / 2 + root.square_size)
    Widget:
        canvas:
            Color:
                rgba: [1, 1, 1, 1]
            Rectangle:
                size: self.size
                pos: self.pos
        size_hint: 1, None
        height: 1
        y: int((root.height - root.square_size) / 2 + root.square_size) + root.y_offset
    Widget:
        canvas:
            Color:
                rgba: [1, 1, 1, 1]
            Rectangle:
                size: self.size
                pos: self.pos
        size_hint: None, 1
        width: 1
        x: int((root.width - root.square_size) / 2)
    Widget:
        canvas:
            Color:
                rgba: [1, 1, 1, 1]
            Rectangle:
                size: self.size
                pos: self.pos
        size_hint: 1, None
        height: 1
        y: int((root.height - root.square_size) / 2) + root.y_offset

<NewPatientScreenTopBar@RelativeLayout>
    canvas:
        Color:
            rgba: app.colors['white']
        Rectangle:
            size: self.size
            pos: 0, 0
    size_hint: 1, None
    height: dp(72)
    N4Label:
        id: title
        style: 'mont-title'
        text: 'Novo Paciente'
        pos: dp(55), dp(50)
    N4ImageButton:
        source: './assets/img/back_btn.png'
        center_y: title.center_y
        on_press:
            app.root.undo()
            app.root.change_screen('amostragem_screen', \
                direction='right', \
                transition='slide', \
                queue_enabled=False, \
                screen_manager=app.root.ids.new_patient_screen.ids.screen_manager)
    RippledN4Button:
        id: amostragem_btn
        text: 'Amostragem'
        style: 'mont-body-selected'
        size_hint_x: 0.5
        height: dp(33.5)
        halign: 'left'
        x: dp(10)
        padding_x: dp(45)
        on_press:
            app.root.change_screen('amostragem_screen', \
                direction='right', \
                transition='slide', \
                queue_enabled=False, \
                screen_manager=app.root.ids.new_patient_screen.ids.screen_manager)
    RippledN4Button:
        id: outros_dados_btn
        text: 'Outros Dados'
        style: 'mont-body'
        size_hint_x: 0.5
        height: dp(33.5)
        halign: 'center'
        pos: amostragem_btn.width, 0
        on_press:
            app.root.change_screen('outros_dados_screen', \
                transition='slide', \
                queue_enabled=False, \
                screen_manager=app.root.ids.new_patient_screen.ids.screen_manager)
    N4Image:
        source: './assets/img/separator_2.png'
        size_hint_x: 1
        height: 1
''')

class NewPatientScreen(Screen):
    camera_zoom = NumericProperty(2)
    fixed_resolution = False
    def __init__(self, **kw):
        super(NewPatientScreen, self).__init__(**kw)

    def update_resolution(self):
        if not self.fixed_resolution:
            self.fixed_resolution = True
            self.ids.camera_object.resolution = (3840, 2160)

    def on_camera_click(self, *args):
        pass

    def add_patient(self, chart_id_txt, diagnostico_txt):
        execute_query("INSERT INTO patients (chart_id, initial_diagnostic) VALUES \
            ('" + chart_id_txt.text + "',\
            '" + diagnostico_txt.text + "')", threaded=True, debug=False)

        App.get_running_app().patients.append(
            {
                'chart_id': chart_id_txt.text,
                'age': '',
                'initial_diagnostic': diagnostico_txt.text,
                'size_hint': [None, None],
                'size': [dp(300), dp(50)],
            }
        )

        chart_id_txt.text = ''
        diagnostico_txt.text = ''
