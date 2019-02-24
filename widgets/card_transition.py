from kivy.uix.screenmanager import SlideTransition, Screen
from kivy.properties import OptionProperty
from kivy.graphics import Color, Rectangle, Canvas
from kivy.animation import AnimationTransition

class CardTransition(SlideTransition):
    mode = OptionProperty('push', options=['pop', 'push'])
    duration = 0.7
    
    def on_pause(self):
        return True    

    def on_resume(self):
        pass

    def start(self, manager):
        '''(internal) Starts the transition. This is automatically
        called by the :class:`ScreenManager`.
        '''
        self.manager = manager
        if hasattr(manager, 'c'):
            manager.canvas.remove(manager.c)

        manager.c = Canvas()
        with manager.c:
            opacity= 0
            Color(0, 0, 0, 0.6)
            Rectangle(size=manager.size, pos=manager.pos)
        super(CardTransition, self).start(manager)
        mode = self.mode
        a = self.screen_in
        b = self.screen_out
        # ensure that the correct widget is "on top"
        if mode == 'push':
            manager.canvas.remove(a.canvas)
            manager.canvas.add(manager.c)
            manager.canvas.add(a.canvas)
        elif mode == 'pop':
            manager.canvas.remove(b.canvas)
            manager.canvas.add(manager.c)
            manager.canvas.add(b.canvas)

    def on_progress(self, progression):
        a = self.screen_in
        b = self.screen_out
        manager = self.manager
        x, y = manager.pos
        width, height = manager.size
        direction = self.direction
        mode = self.mode
        al = AnimationTransition.out_cubic
        progression = al(progression)

        self.screen_in.opacity = 1
        if mode == 'push':
            manager.c.opacity = progression
            if direction == 'left':
                b.pos =  x - progression * width / 7.0, y 
                a.pos = x + width * (1 - progression), y
            elif direction == 'right':
                b.pos =  x + progression * width / 7.0, y 
                a.pos = x - width * (1 - progression), y
            elif direction == 'down':
                a.pos = x, y + height * (1 - progression)
            elif direction == 'up':
                a.pos = x, y - height * (1 - progression)
        elif mode == 'pop':
            a.pos = x, y
            if direction == 'left':
                b.pos = x - width * progression, y
            elif direction == 'right':
                b.pos = x + width * progression, y
            elif direction == 'down':
                b.pos = x, y - height * progression
            elif direction == 'up':
                b.pos = x, y + height * progression

        a.canvas.ask_update()
        b.canvas.ask_update()