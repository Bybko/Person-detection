from cv2 import VideoCapture, imshow, waitKey, destroyAllWindows, rectangle
from typing import Any

from singleton import SingletonMeta
from .model import Model


class Zone:
    def __init__(self, x1: int, y1: int, x2:int, y2:int, model: Any) -> None:
        self.startX = x1
        self.startY = y1
        self.endX = x2
        self.endY = y2
        self._model = model
        self.person_frames = 0

    def draw_rectangle(self, frame: Any) -> None:
        rectangle(frame, (self.startX, self.startY), (self.endX, self.endY), (0, 255, 0), 2)

    def check_zone(self) -> None:
        if self._model.check_persons_in_zone((self.startX, self.startY, self.endX, self.endY))[0]:
            self.person_frames += 1

    def filling_time(self, total_frames: int) -> None:
        print(f"Процент времени, когда зона была заполнена: {self.person_frames / total_frames * 100}%")


class Camera(metaclass=SingletonMeta):
    def __init__(self, model: Model) -> None:
        self._model = model
        self._camera = VideoCapture(0)
        self._total_frames = 0
        self._person_frames = 0
        #cringe out here
        self.zones = [Zone(100, 100, 300, 300, self._model), Zone(350, 100, 550, 300, self._model)]
        #cringe over

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
            zone.check_zone()

        return frame

    def _show_frame(self, frame: Any) -> None:
        imshow('Video', frame)

    def _check_exit(self) -> bool:
        return waitKey(1) == ord('q')
