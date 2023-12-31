from typing import List

from cv2 import flip
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from core import BaseCamera, NoneCamera, Zone
from .behaviors.resize import ResizableBehavior


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
        Clock.schedule_interval(self.update_camera, 1.0 / 60)
        Clock.schedule_interval(self.update_metrics, 1.0)

    def set_camera(self, camera: KivyCamera) -> None:
        if self.camera.parent is not None:
            self.camera.parent.parent.parent.line_color = MDApp.get_running_app().theme_cls.text_color
        self.camera = camera
        self.camera.parent.parent.parent.line_color = MDApp.get_running_app().theme_cls.primary_color
        self.add_zones()

    def add_zones(self):
        for zone in self.camera.camera.get_zones():
            self.add_widget(KivyZone(zone))

    def update_camera(self, dt) -> None:
        self.texture = self.camera.texture

    def update_metrics(self, dt) -> None:
        MDApp.get_running_app().update_metrics(self.camera.camera)

    def reposition_children(self) -> None:
        for child in self.children[:]:
            if isinstance(child, KivyZone):
                child.reposition()


class KivyZone(ResizableBehavior, Image):
    resizable_up = True
    resizable_down = True
    resizable_left = True
    resizable_right = True

    def __init__(self, zone: Zone, **kwargs):
        super().__init__(**kwargs)
        self._zone = zone
        self.size = (abs(self._zone.startX - self._zone.endX),
                     abs(self._zone.startY - self._zone.endY))
        self.size_hint = (None, None)
        self.opacity = 0.2

    def reposition(self):
        offset = ((self.parent.size[0] - self.parent.texture_size[0]) // 2,
                  (self.parent.size[1] - self.parent.texture_size[1]) // 2)
        self.pos = (self.parent.pos[0] + offset[0] + self._zone.startX,
                    self.parent.pos[1] + offset[1] + (self.parent.texture_size[1] - self._zone.endY))


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
                size_hint=(0.5, 0.9)
            )
            self.root.ids.cameras_list.add_widget(
                MDCard(
                    MDFlatButton(
                        MDBoxLayout(
                            kivy_camera,
                            MDLabel(
                                size_hint_y=0.1,
                                text=camera.name,
                                halign='center',
                            ),
                            orientation='vertical',
                        ),
                        size_hint=(1, 1),
                        on_press=self.set_main_camera,
                    ),
                    radius=[0, 0, 0, 0],
                    line_color=self.theme_cls.text_color,
                    line_width=2,
                    size_hint=(1, None),
                    height=200
                )
            )

    def set_main_camera(self, instance) -> None:
        camera_layout = self.root.ids.main_camera

        for child in camera_layout.children[:]:
            if isinstance(child, KivyZone):
                camera_layout.remove_widget(child)

        main_camera = instance.children[0].children[-1]
        camera_layout.set_camera(main_camera)

    def create_zone(self) -> None:
        self.root.ids.main_camera.create_new_zone()

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
