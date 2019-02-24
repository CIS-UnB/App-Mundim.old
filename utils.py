import struct
def hex_to_rgb(rgb):
    return [item/255.0 for item in struct.unpack('BBB', rgb.decode('hex'))] + [1]

def set_statusbar_color(color):
    from android.runnable import run_on_ui_thread
    from jnius import autoclass
    Color = autoclass("android.graphics.Color")
    WindowManager = autoclass('android.view.WindowManager$LayoutParams')
    AndroidView = autoclass('android.view.View')
    AndroidPythonActivity = autoclass('org.kivy.android.PythonActivity')
    activity = AndroidPythonActivity.mActivity

    @run_on_ui_thread
    def _set_statusbar_color(color):
        window = activity.getWindow()
        view = AndroidPythonActivity.mActivity.getWindow().getDecorView()

        window.clearFlags(WindowManager.FLAG_TRANSLUCENT_STATUS)
        window.addFlags(WindowManager.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
        window.setStatusBarColor(Color.parseColor(color))
        view.setSystemUiVisibility(AndroidView.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR)

    _set_statusbar_color(color)
