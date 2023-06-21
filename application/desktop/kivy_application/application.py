from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from cv2 import flip
from typing import List

from core import BaseCamera, NoneCamera


class KivyCamera(Image):
    def __init__(self, camera: BaseCamera, **kwargs) -> None:
        super(KivyCamera, self).__init__(**kwargs)
        self.camera = camera
        self.size_hint = (1, 1)
        self.fit_mode = 'contain'
        Clock.schedule_interval(self.update, 1.0 / 20)

    def update(self, dt) -> None:
        frame = self.camera.proceed_frame()

        buf1 = flip(frame, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        self.texture = image_texture


class MainCamera(Image):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.camera: KivyCamera = KivyCamera(NoneCamera())
        Clock.schedule_interval(self.update, 1.0 / 30)

    def set_camera(self, camera: KivyCamera) -> None:
        if self.camera.parent is not None:
            self.camera.parent.parent.parent.line_color = MDApp.get_running_app().theme_cls.text_color
        self.camera = camera
        self.camera.parent.parent.parent.line_color = MDApp.get_running_app().theme_cls.primary_color

    def update(self, dt) -> None:
        self.texture = self.camera.texture
        MDApp.get_running_app().update_metrics(self.camera.camera)


class PersonDetectionApp(MDApp):
    kv_directory = './application/desktop/kivy_application/kv'

    def __init__(self, cameras: List[BaseCamera], **kwargs) -> None:
        super(PersonDetectionApp, self).__init__(**kwargs)

        self.cameras = cameras

        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.accent_palette = 'Red'
        self.theme_cls.accent_hue = '900'
        self.theme_cls.material_style = 'M3'

    def build(self):
        for camera in self.cameras:
            kivy_camera = KivyCamera(
                camera=camera,
                size_hint=(1, 0.9)
            )
            self.root.ids.cameras_list.add_widget(
                MDCard(
                    MDFlatButton(
                        MDBoxLayout(
                            kivy_camera,
                            MDLabel(
                                size_hint_y=0.1,
                                text=camera.name,
                                halign='center'
                            ),
                            orientation='vertical'
                        ),
                        size_hint=(1, 1),
                        on_press=lambda callback: self.set_main_camera(kivy_camera)
                    ),
                    line_color=self.theme_cls.text_color,
                    line_width=2,
                    size_hint=(1, None),
                    height=200
                )
            )

    def set_main_camera(self, camera: KivyCamera) -> None:
        self.root.ids.main_camera.set_camera(camera)

    def update_metrics(self, camera: BaseCamera) -> None:
        info = camera.get_info()
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
