from cv2 import VideoCapture, imshow, destroyAllWindows
from typing import Any
import time
import datetime


from singleton import SingletonMeta
from .model import Model
from .zone import Zone


class Camera(metaclass=SingletonMeta):
    def __init__(self, model: Model) -> None:
        self._model = model
        self._camera = VideoCapture(0)
        self._total_time = 0
        self._prev_frame_time = 0
        self._current_frame_time = 0
        # cringe out here
        self._zones = [Zone("FirstZone", 100, 100, 300, 300), Zone("SecondZone", 350, 100, 550, 300)]
        # cringe over

    def start(self) -> None:
        self._total_time = 0
        self._prev_frame_time = time.time()

    def stop(self) -> None:
        self._camera.release()
        destroyAllWindows()

    def proceed_frame(self) -> Any:
        success, frame = self._camera.read()

        if not success:
            raise ConnectionError('Cannot connect to camera.')

        for zone in self._zones:
            zone.draw_rectangle(frame)

        self._model.proceed_frame(frame)
        self._current_frame_time = time.time()
        self._total_time += self._current_frame_time - self._prev_frame_time

        for zone in self._zones:
            zone.add_person_frames(self._model.check_persons_in_zone(zone),
                                   self._current_frame_time - self._prev_frame_time)

        self._prev_frame_time = time.time()
        return frame

    def get_info(self) -> str:
        info = f'camera: 1\t time:{str(datetime.timedelta(seconds=int(self._total_time)))}\n'
        info += f'{"id": ^15}|{"time with person": ^20}|{"one person": ^20}|{"two person": ^20}|{"more person": ^20}\n'
        for zone in self._zones:
            zone_time = zone.get_time_info(self._total_time)
            info += f'{zone.name: ^15}|{zone_time["person_time"][0]:>9} {zone_time["person_time"][1]:>8}% |'\
                    f'{zone_time["one_person_time"][0]:>9} {zone_time["one_person_time"][1]:>8}% |'\
                    f'{zone_time["two_person_time"][0]:>9} {zone_time["two_person_time"][1]:>8}% |'\
                    f'{zone_time["more_person_time"][0]:>9} {zone_time["more_person_time"][1]:>8}%\n'
        return info

    def show_frame(self, frame: Any) -> None:
        imshow('Video', frame)
