from cv2 import VideoCapture, imshow, destroyAllWindows
from typing import Any, Dict
import time
import datetime
from abc import abstractmethod, ABC
import numpy as np

from .model import BaseModel
from .zone import Zone


class BaseCamera(ABC):
    def __init__(self, name: str, model: BaseModel) -> None:
        self.name = name
        self._model = model

    def show_frame(self, frame: Any) -> None:
        imshow('Video', frame)

    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...

    @abstractmethod
    def proceed_frame(self) -> Any: ...

    @abstractmethod
    def get_info(self) -> Dict[str, Any]: ...


class NoneCamera(BaseCamera):
    def __init__(self, model: BaseModel) -> None:
        super().__init__('None', model)
        self._zones = [Zone("None", 0, 0, 0, 0)]

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def proceed_frame(self) -> Any:
        return np.zeros((480, 640, 3), dtype=np.uint8)

    def get_info(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'total_time': str(datetime.timedelta(seconds=int(0))),
            'zones': {zone.name: zone.get_time_info(0) for zone in self._zones}
        }


class Camera(BaseCamera):
    def __init__(self, name: str, model: BaseModel) -> None:
        super().__init__(name, model)
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

    def get_info(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'total_time': str(datetime.timedelta(seconds=int(self._total_time))),
            'zones': {zone.name: zone.get_time_info(self._total_time) for zone in self._zones}
        }

    def show_frame(self, frame: Any) -> None:
        imshow('Video', frame)
