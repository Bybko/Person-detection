from cv2 import VideoCapture, imshow, destroyAllWindows
from typing import Any, Dict, List
import time
import datetime
from abc import abstractmethod, ABC
import numpy as np

from .model import BaseModel, NoneModel
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
    def create_zone(self, zone: Zone) -> None: ...

    @abstractmethod
    def proceed_frame(self) -> Any: ...

    @abstractmethod
    def get_info(self) -> Dict[str, Any]: ...


class NoneCamera(BaseCamera):
    def __init__(self, model: BaseModel = NoneModel()) -> None:
        super().__init__('None', model)
        self._zones = [Zone("None", 0, 0, 0, 0)]

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def create_zone(self, zone: Zone) -> None:
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
    def __init__(self, port: int, name: str, model: BaseModel) -> None:
        super().__init__(name, model)
        self._camera = VideoCapture(port)
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

    def create_zone(self, zone: Zone) -> None:
        self._zones.append(zone)

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


def get_cameras_list(max_non_working_ports: int = 6) -> List[int]:
    non_working_ports = []
    dev_port = 0
    working_ports = []

    while len(non_working_ports) < max_non_working_ports:
        camera = VideoCapture(dev_port)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
        else:
            is_reading, _ = camera.read()
            if is_reading:
                working_ports.append(dev_port)
            else:
                non_working_ports.append(dev_port)
        dev_port += 1

    return working_ports
