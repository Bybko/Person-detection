from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from cv2 import flip

from core import Camera


class KivyCamera(Image):
    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.camera = MDApp.get_running_app().camera
        Clock.schedule_interval(self.update, 1.0 / 20)

    def update(self, dt):
        frame = self.camera.proceed_frame()

        buf1 = flip(frame, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        self.texture = image_texture


class PersonDetectionApp(MDApp):
    kv_directory = './application/desktop/kivy_application/kv'

    def __init__(self, camera: Camera, **kwargs) -> None:
        super(PersonDetectionApp, self).__init__(**kwargs)

        self.camera = camera

        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.accent_palette = 'Red'
        self.theme_cls.accent_hue = '900'
