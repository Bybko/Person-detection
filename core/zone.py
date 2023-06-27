from datetime import timedelta
from typing import Any
from typing import Dict

from cv2 import rectangle


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
        self.intervals = 0
        self.__occupied = False
        self.persons_times = {}

    def add_person_frames(self, count: int, delta_time: float) -> None:
        if count <= 0:
            if self.__occupied:
                self.__occupied = False
            return

        if not self.__occupied:
            self.__occupied = True
            self.intervals += 1

        self.person_time += delta_time
        if count in self.persons_times:
            self.persons_times[count] += delta_time
        else:
            self.persons_times[count] = delta_time

    def get_time_info(self, total_time: int) -> Dict[str, str]:
        persons_avg = sum(persons * (self.persons_times[persons] / self.person_time) for persons in self.persons_times)
        return {
            'person_time': str(timedelta(seconds=int(self.person_time))),
            'person_time_percent': f'{0 if total_time == 0 else self.person_time / total_time * 100: .1f}',
            'num_of_intervals': str(self.intervals),
            'avg_of_intervals': str(timedelta(seconds=int(0 if self.intervals == 0 else
                                                          self.person_time / self.intervals))),
            'persons_avg': f'{persons_avg: .1f}'
        }
