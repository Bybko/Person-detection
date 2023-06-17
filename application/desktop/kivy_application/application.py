from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from cv2 import flip

from core import BaseCamera


class KivyCamera(Image):
    def __init__(self, **kwargs) -> None:
        super(KivyCamera, self).__init__(**kwargs)
        self.camera = MDApp.get_running_app().camera
        Clock.schedule_interval(self.update, 1.0 / 20)

    def update(self, dt) -> None:
        frame = self.camera.proceed_frame()

        buf1 = flip(frame, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        self.texture = image_texture
        MDApp.get_running_app().update_metrics()


class PersonDetectionApp(MDApp):
    kv_directory = './application/desktop/kivy_application/kv'

    def __init__(self, camera: BaseCamera, **kwargs) -> None:
        super(PersonDetectionApp, self).__init__(**kwargs)

        self.camera = camera

        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.accent_palette = 'Red'
        self.theme_cls.accent_hue = '900'

    def update_metrics(self) -> None:
        info = self.camera.get_info()
        self.root.ids.metrics.clear_widgets()
        self.root.ids.camera_name.text = f'Camera: {info["name"]}'
        self.root.ids.total_time.text = f'Total time: {info["total_time"]}'

        for name, zone in info['zones'].items():
            self.root.ids.metrics.add_widget(MDLabel(text=f'{name}'))
            self.root.ids.metrics.add_widget(MDLabel(text=f'{zone["person_time"]}'))
            self.root.ids.metrics.add_widget(MDLabel(text=f'{zone["person_time_percent"]}%'))
            self.root.ids.metrics.add_widget(MDLabel(text=f'{zone["num_of_intervals"]}'))
            self.root.ids.metrics.add_widget(MDLabel(text=f'{zone["avg_of_intervals"]}'))
            self.root.ids.metrics.add_widget(MDLabel(text=f'{zone["persons_avg"]}'))
