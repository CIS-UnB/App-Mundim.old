#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.camera import Camera
from screens.home_screen import HomeScreen
from screens.new_patient_screen import NewPatientScreen
from screens.patient_screen import PatientScreen
from widgets.card_transition import CardTransition
from kivy.clock import Clock
from kivy.properties import NumericProperty
from functools import partial
import time
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
        NewPatientScreen:
            id: new_patient_screen
            name: 'new_patient_screen'
        PatientScreen:
            id: patient_screen
            name: 'patient_screen'

''')

class MundimRoot(RelativeLayout):
    queue = []
    last_transition = 0
    def __init__(self, **kw):
        super(MundimRoot, self).__init__(**kw)

    def change_screen(self, target, delay=0, direction='left', transition='slide', queue_enabled=True, screen_manager=None):
        if not screen_manager:
            screen_manager = self.ids.screen_manager

        if delay > 0:
            Clock.schedule_once(
                lambda item: self.change_screen(
                    target,
                    direction=direction,
                    transition=transition,
                    queue_enabled=queue_enabled,
                    screen_manager=screen_manager,
                ), delay
            )
            return

        self.last_transition = time.time()
        if queue_enabled:
            new_direction = 'right' if direction == 'left' else 'left'
            self.add_to_queue(
                'Undo screen change. {} -> {}'.format(target, screen_manager.current),
                partial(
                    self.change_screen,
                    screen_manager.current,
                    direction=new_direction,
                    transition=transition,
                    queue_enabled=False,
                    screen_manager=screen_manager,
                )
            )

        screen_transition = CardTransition(direction=direction)
        if transition == 'slide':
            screen_transition = SlideTransition(direction=direction, duration=0.6)

        screen_manager.transition = screen_transition
        screen_manager.current = target

    def add_to_queue(self, description, function):
        descriptions = [item[0] for item in self.queue]
        if description not in descriptions:
            self.queue.append([description, function])

    def undo(self):
        if time.time() - self.last_transition < 0.7:
            return

        if len(self.queue) > 0:
            description, function = self.queue.pop()
            function()
