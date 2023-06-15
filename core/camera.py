from cv2 import VideoCapture, imshow, waitKey, destroyAllWindows, rectangle
from typing import Any

from singleton import SingletonMeta
from .model import Model
from .zone import Zone


class Camera(metaclass=SingletonMeta):
    def __init__(self, model: Model) -> None:
        self._model = model
        self._camera = VideoCapture(0)
        self._total_frames = 0
        self._person_frames = 0
        # cringe out here
        self.zones = [Zone("FirstZone", 100, 100, 300, 300), Zone("SecondZone", 350, 100, 550, 300)]
        # cringe over

    def start(self) -> None:
        self._total_frames = 0
        self._person_frames = 0

        self._cycle()
        self._camera.release()
        destroyAllWindows()

        for zone in self.zones:
            zone.filling_time(self._total_frames)

    def _cycle(self) -> None:
        while True:
            frame = self._proceed_frame()

            self._show_frame(frame)
            if self._check_exit():
                break

    def _proceed_frame(self) -> Any:
        success, frame = self._camera.read()

        if not success:
            raise ConnectionError('Cannot connect to camera.')

        for zone in self.zones:
            zone.draw_rectangle(frame)

        self._model.proceed_frame(frame)
        self._total_frames += 1

        for zone in self.zones:
            self._model.check_persons_in_zone(zone)

        return frame

    def _show_frame(self, frame: Any) -> None:
        imshow('Video', frame)

    def _check_exit(self) -> bool:
        return waitKey(1) == ord('q')
