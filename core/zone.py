from cv2 import rectangle
from typing import Any
from datetime import timedelta
from typing import Tuple, Dict


class Box:
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.startX = x1
        self.startY = y1
        self.endX = x2
        self.endY = y2

    def draw_rectangle(self, frame: Any) -> None:
        rectangle(frame, (self.startX, self.startY), (self.endX, self.endY), (0, 255, 0), 2)


class Zone(Box):
    def __init__(self, name: str, x1: int, y1: int, x2: int, y2: int) -> None:
        super().__init__(x1, y1, x2, y2)
        self.name = name
        self.person_time = 0
        self.one_person_time = 0
        self.two_person_time = 0
        self.more_person_time = 0

    def add_person_frames(self, count: int, delta_time: float) -> None:
        if count <= 0:
            return

        self.person_time += delta_time
        if count == 1:
            self.one_person_time += delta_time
        elif count == 2:
            self.two_person_time += delta_time
        else:
            self.more_person_time += delta_time

    def get_time_info(self, total_time: int) -> Dict[str, str]:
        return {
            'person_time':
                (str(timedelta(seconds=int(self.person_time)))),
            'person_time_percen':
                (str(f'{self.person_time / total_time * 100: .1f}')),
            '':




                (str(timedelta(seconds=int(self.one_person_time))), f'{self.one_person_time / total_time * 100: .1f}'),
            'two_person_time':
                (str(timedelta(seconds=int(self.two_person_time))), f'{self.two_person_time / total_time * 100: .1f}'),
            'more_person_time':
                (str(timedelta(seconds=int(self.more_person_time))), f'{self.more_person_time / total_time * 100: .1f}')
        }
