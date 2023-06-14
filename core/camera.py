from cv2 import VideoCapture, imshow, waitKey, destroyAllWindows, rectangle
from typing import Any

from singleton import SingletonMeta
from .model import Model


class Camera(metaclass=SingletonMeta):
    def __init__(self, model: Model) -> None:
        self._model = model
        self._camera = VideoCapture(0)
        self._total_frames = 0
        self._person_frames = 0

    def start(self) -> None:
        self._total_frames = 0
        self._person_frames = 0
        self._cycle()
        self._camera.release()
        destroyAllWindows()
        print(f"Процент времени, когда зона была заполнена: {self._person_frames / self._total_frames * 100}%")

    def _cycle(self) -> None:
        while True:
            frame = self._proceed_frame()
            rectangle(frame, (200, 100), (500, 400), (0, 255, 0), 2)
            self._show_frame(frame)
            if self._check_exit():
                break

    def _proceed_frame(self) -> Any:
        success, frame = self._camera.read()

        if not success:
            raise ConnectionError('Cannot connect to camera.')

        self._model.proceed_frame(frame)
        self._total_frames += 1
        if self._model.check_persons_in_zone((200, 100, 500, 400))[0]:
            self._person_frames += 1

        return frame

    def _show_frame(self, frame: Any) -> None:
        imshow('Video', frame)

    def _check_exit(self) -> bool:
        return waitKey(1) == ord('q')
