#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True

from kivy.app import App
from kivy.base import EventLoop
from kivy.properties import DictProperty, ListProperty, NumericProperty

from widgets.n4textinput import N4TextInput
from widgets.n4label import N4Label
from widgets.n4button import N4Button, RippledN4Button
from widgets.n4image import N4Image
from widgets.n4imagebutton import N4ImageButton, RippledImageButton
from widgets.xcamera import XCamera
from root import MundimRoot

from kivy.utils import platform
from utils import hex_to_rgb, set_statusbar_color
from server_manager import load_query, execute_query
from threading import Thread
from kivy.clock import Clock
from kivy.metrics import dp

class Mundim(App):
    colors = DictProperty({
        'black': hex_to_rgb('000000'),
        'white': hex_to_rgb('FFFFFF'),
        'off_white': hex_to_rgb('F3F3F3'),
        'blue_1': hex_to_rgb('73B9E8'),
        'green_1': hex_to_rgb('73E89A'),
        'debug': hex_to_rgb('FF0000')[:3] + [0.1],
    })

    patients_ammount = NumericProperty(-1)
    patients = ListProperty([])

    no_prognostic_patients_ammount = NumericProperty(-1)
    no_prognostic_patients = ListProperty([])

    def load_patients(self, threaded=False, delay=0):
        def _load_patients():
            patients = load_query("SELECT * FROM patients")
            for patient in patients:
                patient['size_hint'] = [None, None]
                patient['size'] = dp(300), dp(50)

            self.patients = patients
            self.patients_ammount = len(self.patients)

        if delay:
            Clock.schedule_once(
                (lambda x: self.load_patients(threaded=threaded)), delay
            )
            return

        if threaded:
            Thread(target=_load_patients, args=[]).start()
        else:
            _load_patients()

    def on_patients(self, instance, value):
        no_prognostic_patients = []
        for patient in value:
            if patient['biopsy_diagnostic'] == '':
                no_prognostic_patients.append(patient)
        self.no_prognostic_patients = no_prognostic_patients
        self.no_prognostic_patients_ammount = len(self.no_prognostic_patients)

    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

        self.load_patients(threaded=True, delay=1)
        Clock.schedule_interval(lambda x: self.load_patients(threaded=True), 60)
        if platform == 'android':
            set_statusbar_color('#FFFFFF')

    @staticmethod
    def check_request_permission():
        if platform != "android":
            return
        from android.permissions import (
            Permission, request_permission, check_permission)
        permission = Permission.CAMERA
        if not check_permission(permission):
            request_permission(permission)

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.root.undo()
            return True

    def build(self):
        self.check_request_permission()

        self.root = MundimRoot()
        self.root.app = self
        return self.root

Mundim().run()
