#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string('''
<NewPatientScreen>
    canvas:
        Color:
            rgba: app.colors['off_white']
        Rectangle:
            size: self.size
            pos: 0, 0
    NewPatientScreenTopBar:
        id: top_bar
        pos: 0, root.height - self.height
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
            Overlay:
                size_hint: 1, 1
            N4ImageButton:
                source: './assets/img/take_photo_btn.png'
                center_x: self.parent.center_x
                y: dp(25)
        Screen:
            id: outros_dados_screen
            name: 'outros_dados_screen'
            on_pre_enter:
                top_bar.ids.amostragem_btn.style = 'mont-body'
                top_bar.ids.outros_dados_btn.style = 'mont-body-selected'
            N4ImageButton:
                debug: True
                source: './assets/img/send_data_btn.png'
            N4TextInput:
                id: nome_txt
                hint_text: 'NOME'
                edit_size: 'medium'
                pos: int(dp(30)), int(self.parent.height - self.height - dp(10))
            N4TextInput:
                id: idade_txt
                hint_text: 'IDADE'
                edit_size: 'small'
                pos: nome_txt.x + nome_txt.width + int(dp(5)), nome_txt.y
            N4TextInput:
                id: sobrenome_txt
                hint_text: 'SOBRENOME'
                edit_size: 'large'
                pos: nome_txt.x, int(nome_txt.y - self.height - dp(5))
            N4TextInput:
                id: diagnostico_txt
                hint_text: 'DIAGNOSTICO'
                edit_size: 'large'
                pos: nome_txt.x, int(sobrenome_txt.y - self.height - dp(5))
            N4Image:
                source: './assets/img/separator_2.png'
                height: 1
                center_x: self.parent.center_x
                y: int(diagnostico_txt.y - self.height - dp(10))


<Overlay@RelativeLayout>
    Widget:
        canvas:
            Color:
                rgba: [0, 0, 0, 0.5]
            Rectangle:
                size: self.size
                pos: self.pos
        size_hint: None, None
        size: (root.width - 200) / 2, 200
        pos: 0, (root.height - 200) / 2 + 100
    Widget:
        canvas:
            Color:
                rgba: [0, 0, 0, 0.5]
            Rectangle:
                size: self.size
                pos: self.pos
        size_hint: 1, None
        height: (root.height - 200) / 2
        y: (root.height - 200) / 2 + 300
    Widget:
        canvas:
            Color:
                rgba: [0, 0, 0, 0.5]
            Rectangle:
                size: self.size
                pos: self.pos
        size_hint: None, None
        size: (root.width - 200) / 2, 200
        pos: (root.width - 200) / 2 + 201, (root.height - 200) / 2 + 100
    Widget:
        canvas:
            Color:
                rgba: [0, 0, 0, 0.5]
            Rectangle:
                size: self.size
                pos: self.pos
        size_hint: 1, None
        height: (root.height - 200) / 2 + 100


    Widget:
        canvas:
            Color:
                rgba: [1, 1, 1, 1]
            Rectangle:
                size: self.size
                pos: self.pos
        size_hint: None, 1
        width: 1
        x: int((root.width - 200) / 2 + 200)
    Widget:
        canvas:
            Color:
                rgba: [1, 1, 1, 1]
            Rectangle:
                size: self.size
                pos: self.pos
        size_hint: 1, None
        height: 1
        y: int((root.height - 200) / 2 + 200) + 100
    Widget:
        canvas:
            Color:
                rgba: [1, 1, 1, 1]
            Rectangle:
                size: self.size
                pos: self.pos
        size_hint: None, 1
        width: 1
        x: int((root.width - 200) / 2)
    Widget:
        canvas:
            Color:
                rgba: [1, 1, 1, 1]
            Rectangle:
                size: self.size
                pos: self.pos
        size_hint: 1, None
        height: 1
        y: int((root.height - 200) / 2) + 100

<NewPatientScreenTopBar@RelativeLayout>
    canvas:
        Color:
            rgba: app.colors['white']
        Rectangle:
            size: self.size
            pos: 0, 0
    size_hint: 1, None
    height: dp(82.5)
    N4Label:
        style: 'mont-title'
        text: 'Novo Paciente'
        pos: dp(55), dp(50)
    N4ImageButton:
        source: './assets/img/back_btn.png'
        pos: 0, root.height - self.height
        on_press:
            app.root.undo()
    N4Button:
        id: amostragem_btn
        text: 'Amostragem'
        style: 'mont-body-selected'
        size_hint_x: 0.5
        height: dp(33.5)
        halign: 'left'
        x: dp(10)
        padding_x: dp(45)
        on_press:
            app.root.change_screen('amostragem_screen', direction='right', transition='slide', screen_manager=app.root.ids.new_patient_screen.ids.screen_manager)

    N4Button:
        id: outros_dados_btn
        text: 'Outros Dados'
        style: 'mont-body'
        size_hint_x: 0.5
        height: dp(33.5)
        halign: 'center'
        pos: amostragem_btn.width, 0
        on_press:
            app.root.change_screen('outros_dados_screen', transition='slide', screen_manager=app.root.ids.new_patient_screen.ids.screen_manager)
    N4Image:
        source: './assets/img/separator.png'
        height: 1
''')

class NewPatientScreen(Screen):
    def __init__(self, **kw):
        super(NewPatientScreen, self).__init__(**kw)
