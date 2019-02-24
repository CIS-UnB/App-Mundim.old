'''
Touch Ripple
============

.. versionadded:: 1.10.1

.. warning::
    This code is still experimental, and its API is subject to change in a
    future version.

This module contains `mixin <https://en.wikipedia.org/wiki/Mixin>`_ classes
to add a touch ripple visual effect known from `Google Material Design
<https://en.wikipedia.org/wiki/Material_Design>_` to widgets.

For an overview of behaviors, please refer to the :mod:`~kivy.uix.behaviors`
documentation.

The class :class:`~kivy.uix.behaviors.touchripple.RippleBehavior` provides
rendering the ripple animation.

The class :class:`~kivy.uix.behaviors.touchripple.RippleButtonBehavior`
basically provides the same functionality as
:class:`~kivy.uix.behaviors.button.ButtonBehavior` but rendering the ripple
animation instead of default press/release visualization.
'''
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Canvas, CanvasBase, Color, Ellipse, Rectangle, ScissorPush, ScissorPop
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, \
    ObjectProperty, StringProperty
from kivy.uix.relativelayout import RelativeLayout


__all__ = (
    'RippleBehavior',
    'RippleButtonBehavior'
)


class RippleBehavior(object):
    '''Touch ripple behavior.

    Supposed to be used as mixin on widget classes.

    Ripple behavior does not trigger automatically, concrete implementation
    needs to call :func:`ripple_show` respective :func:`ripple_fade` manually.

    Example
    -------

    Here we create a Label which renders the touch ripple animation on
    interaction::

        class RippleLabel(RippleBehavior, Label):

            def __init__(self, **kwargs):
                super(RippleLabel, self).__init__(**kwargs)

            def on_touch_down(self, touch):
                collide_point = self.collide_point(touch.x, touch.y)
                if collide_point:
                    touch.grab(self)
                    self.ripple_show(touch)
                    return True
                return False

            def on_touch_up(self, touch):
                if touch.grab_current is self:
                    touch.ungrab(self)
                    self.ripple_fade()
                    return True
                return False
    '''

    ripple_rad_default = NumericProperty(10)
    '''Default radius the animation starts from.

    :attr:`ripple_rad_default` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `10`.
    '''

    ripple_duration_in = NumericProperty(.5)
    '''Animation duration taken to show the overlay.

    :attr:`ripple_duration_in` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `0.5`.
    '''

    ripple_duration_out = NumericProperty(.2)
    '''Animation duration taken to fade the overlay.

    :attr:`ripple_duration_out` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `0.2`.
    '''

    ripple_fade_from_alpha = NumericProperty(.5)
    '''Alpha channel for ripple color the animation starts with.

    :attr:`ripple_fade_from_alpha` is a
    :class:`~kivy.properties.NumericProperty` and defaults to `0.5`.
    '''

    ripple_fade_to_alpha = NumericProperty(.8)
    '''Alpha channel for ripple color the animation targets to.

    :attr:`ripple_fade_to_alpha` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `0.8`.
    '''

    ripple_scale = NumericProperty(2.)
    '''Max scale of the animation overlay calculated from max(width/height) of
    the decorated widget.

    :attr:`ripple_scale` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `2.0`.
    '''

    ripple_func_in = StringProperty('out_quad')
    '''Animation callback for showing the overlay.

    :attr:`ripple_func_in` is a :class:`~kivy.properties.StringProperty`
    and defaults to `in_cubic`.
    '''

    ripple_func_out = StringProperty('out_quad')
    '''Animation callback for hiding the overlay.

    :attr:`ripple_func_out` is a :class:`~kivy.properties.StringProperty`
    and defaults to `out_quad`.
    '''

    ripple_rad = NumericProperty(10)
    ripple_pos = ListProperty([0, 0])
    ripple_color = ListProperty((1, 1, 1, 0.5))
    ripple_bg_color = ListProperty((0.85, 0.85, 0.85, .5))

    lower_ripple_completed = BooleanProperty(True)
    upper_ripple_completed = BooleanProperty(False)
    ciripple_bg_color_fixedular_ripple = NumericProperty(0)
    ripple_center = ListProperty([])
    circular_ripple = NumericProperty(0)
    def __init__(self, **kwargs):
        super(RippleBehavior, self).__init__(**kwargs)
        self.ripple_pane_bg = Canvas()
        self.canvas.add(self.ripple_pane_bg)
        self.bind(
            ripple_bg_color=self._ripple_set_bg_color,
        )
        self.ripple_rectangle = None
        self.ripple_bg_color_instruction = None

        self.ripple_pane = Canvas()
        self.canvas.add(self.ripple_pane)
        self.bind(
            ripple_color=self._ripple_set_color,
            ripple_pos=self._ripple_set_ellipse,
            ripple_rad=self._ripple_set_ellipse
        )
        self.ripple_ellipse = None
        self.ripple_col_instruction = None

        self.execution_index = 1

    def ripple_show(self, touch):
        '''Begin ripple animation on current widget.

        Expects touch event as argument.
        '''
        Animation.cancel_all(self, 'ripple_rad', 'ripple_bg_color', 'ripple_color')
        self.execution_index += 1
        self._ripple_reset_pane()
        x, y = self.to_window(*self.pos)

        ripple_bg_color_fixed = self.ripple_bg_color
        self.ripple_bg_color = [ripple_bg_color_fixed[0], ripple_bg_color_fixed[1], ripple_bg_color_fixed[2], self.ripple_fade_from_alpha]

        if not self.circular_ripple:
            with self.ripple_pane_bg.before:
                self.ripple_bg_color_instruction = Color(rgba=self.ripple_bg_color)
                self.ripple_rectangle = Rectangle(
                    size=self.size,
                    pos=self.pos,
                )

        width, height = self.size
        if isinstance(self, RelativeLayout):
            self.ripple_pos = ripple_pos = (touch.x - x, touch.y - y)
        else:
            self.ripple_pos = ripple_pos = (touch.x, touch.y)
        if self.circular_ripple:
            self.ripple_pos = ripple_pos = self.ripple_center if self.ripple_center else self.center
        rc = self.ripple_color
        ripple_rad = self.ripple_rad
        self.ripple_color = [rc[0], rc[1], rc[2], self.ripple_fade_from_alpha]
        with self.ripple_pane.before:
            if not self.circular_ripple:
                self.sp = ScissorPush(
                    x=int(round(x)),
                    y=int(round(y)),
                    width=int(round(width)),
                    height=int(round(height))
                )
            self.ripple_col_instruction = Color(rgba=self.ripple_color)
            self.ripple_ellipse = Ellipse(
                size=(ripple_rad, ripple_rad),
                pos=(
                        ripple_pos[0] - ripple_rad / 2.,
                        ripple_pos[1] - ripple_rad / 2.
                )
            )
            if not self.circular_ripple:
                ScissorPop()

        self.ripple_scale = self.circular_ripple if self.circular_ripple else self.ripple_scale
        anim = Animation(
            t=self.ripple_func_in,
            ripple_color=[rc[0], rc[1], rc[2], self.ripple_fade_to_alpha],
            ripple_bg_color=[ripple_bg_color_fixed[0], ripple_bg_color_fixed[1], ripple_bg_color_fixed[2], self.ripple_fade_to_alpha],
            duration=self.ripple_duration_in,
        )

        ripple_rad = max(width, height)/1.62 if not self.circular_ripple else max(width, height) * self.ripple_scale
        radii_animation = Animation(
            ripple_rad=ripple_rad,
            t='out_expo',
            duration=self.ripple_duration_in + self.ripple_duration_out,
        )
        radii_animation.start(self)
        anim.start(self)
        ei = self.execution_index
        fade = lambda s: self.ripple_fade(ei)

    def ripple_fade(self, index=0):
        '''Finish ripple animation on current widget.
        '''
        if self.execution_index != index and index > 0:
            return

        Animation.cancel_all(self, 'ripple_bg_color', 'ripple_color')
        ripple_bg_color_fixed = self.ripple_bg_color
        rc = self.ripple_color
        anim = Animation(
            ripple_color=[rc[0], rc[1], rc[2], 0.],
            ripple_bg_color=[ripple_bg_color_fixed[0], ripple_bg_color_fixed[1], ripple_bg_color_fixed[2], 0.],
            t=self.ripple_func_out,
            duration=self.ripple_duration_out,
        )
        anim.bind(on_complete=self._ripple_anim_complete)
        anim.start(self)

    def _ripple_set_ellipse(self, instance, value):
        ellipse = self.ripple_ellipse
        width, height = self.size
        if not ellipse:
            return
        x, y = self.to_window(*self.pos)
        if not self.circular_ripple:
            self.sp.x = x
            self.sp.y = y
        ripple_pos = self.ripple_pos
        ripple_rad = self.ripple_rad
        m = max(width, height)
        cr = self.circular_ripple**2
        if cr and (ripple_rad > m*cr):
            ripple_rad = m*cr
        ellipse.size = (ripple_rad, ripple_rad)
        ellipse.pos = (
            ripple_pos[0] - ripple_rad / 2.,
            ripple_pos[1] - ripple_rad / 2.
        )

    def _ripple_set_color(self, instance, value):
        if not self.ripple_col_instruction:
            return
        self.ripple_col_instruction.rgba = value
        if self.ripple_color[:3]+[0] == value:
            self.lower_ripple_completed = True
        elif self.ripple_color[:3]+[self.ripple_fade_to_alpha] == value:
            self.upper_ripple_completed = True
        else:
            self.upper_ripple_completed = False
            self.lower_ripple_completed = False


    def _ripple_set_bg_color(self, instance, value):
        if not self.ripple_bg_color_instruction:
            return
        self.ripple_bg_color_instruction.rgba = value
        if self.ripple_bg_color[:3]+[0] == value:
            self.lower_ripple_completed = True
        elif self.ripple_bg_color[:3]+[self.ripple_fade_to_alpha] == value:
            self.upper_ripple_completed = True
        else:
            self.upper_ripple_completed = False
            self.lower_ripple_completed = False


    def _ripple_anim_complete(self, anim, instance):
        self._ripple_reset_pane()

    def _ripple_reset_pane(self):
        self.ripple_rad = self.ripple_rad_default
        self.ripple_pane.before.clear()
        self.ripple_pane_bg.before.clear()


class RippleButtonBehavior(RippleBehavior):
    '''
    This `mixin <https://en.wikipedia.org/wiki/Mixin>`_ class provides
    a similar behavior to :class:`~kivy.uix.behaviors.button.ButtonBehavior`
    but provides touch ripple animation instead of button pressed/released as
    visual effect.

    :Events:
        `on_press`
            Fired when the button is pressed.
        `on_release`
            Fired when the button is released (i.e. the touch/click that
            pressed the button goes away).
    '''

    last_touch = ObjectProperty(None)
    '''Contains the last relevant touch received by the Button. This can
    be used in `on_press` or `on_release` in order to know which touch
    dispatched the event.

    :attr:`last_touch` is a :class:`~kivy.properties.ObjectProperty` and
    defaults to `None`.
    '''

    always_release = BooleanProperty(False)
    '''This determines whether or not the widget fires an `on_release` event if
    the touch_up is outside the widget.

    :attr:`always_release` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to `False`.
    '''

    def __init__(self, **kwargs):
        self.register_event_type('on_press')
        self.register_event_type('on_release')
        super(RippleButtonBehavior, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if super(RippleButtonBehavior, self).on_touch_down(touch):
            return True
        if touch.is_mouse_scrolling:
            return False
        if not self.collide_point(touch.x, touch.y):
            return False
        if self in touch.ud:
            return False
        touch.grab(self)
        touch.ud[self] = True
        self.last_touch = touch
        self.ripple_show(touch)
        self.dispatch('on_press')
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            return True
        if super(RippleButtonBehavior, self).on_touch_move(touch):
            return True
        return self in touch.ud

    def on_touch_up(self, touch):
        self.ripple_fade()
        if touch.grab_current is not self:
            return super(RippleButtonBehavior, self).on_touch_up(touch)
        assert(self in touch.ud)
        touch.ungrab(self)
        self.last_touch = touch
        if self.disabled:
            return
        if not self.always_release and not self.collide_point(*touch.pos):
            return
        # defer on_release until ripple_fade has completed
        def defer_release(dt):
            if self.collide_point(touch.x, touch.y):
                self.dispatch('on_release')
        Clock.schedule_once(defer_release, self.ripple_duration_out)
        return True

    def on_disabled(self, instance, value):
        # ensure ripple animation completes if disabled gets set to True
        if value:
            self.ripple_fade()
        return super(RippleButtonBehavior, self).on_disabled(
            instance, value)

    def on_press(self):
        pass

    def on_release(self):
        pass