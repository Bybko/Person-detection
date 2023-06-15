from cv2 import rectangle
from typing import Any


class Box:
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.startX = x1
        self.startY = y1
        self.endX = x2
        self.endY = y2


class Zone(Box):
    def __init__(self, name: str, x1: int, y1: int, x2: int, y2: int) -> None:
        super().__init__(x1, y1, x2, y2)
        self.name = name
        self.person_frames = 0
        self.one_person_frames = 0
        self.two_person_frames = 0
        self.more_person_frames = 0

    def draw_rectangle(self, frame: Any) -> None:
        rectangle(frame, (self.startX, self.startY), (self.endX, self.endY), (0, 255, 0), 2)

    def add_person_frames(self, count: int) -> None:
        if count <= 0:
            return

        self.person_frames += 1
        if count == 1:
            self.one_person_frames += 1
        elif count == 2:
            self.two_person_frames += 1
        else:
            self.more_person_frames += 1

    def filling_time(self, total_frames: int) -> None:
        print(f"Зона {self.name}: ")
        print(f"Процент времени, когда зона была заполнена: {self.person_frames / total_frames * 100}%")
        print(f"Процент времени, когда в зоне был один человек:  {self.one_person_frames / total_frames * 100}%")
        print(f"Процент времени, когда в зоне было два человека:  {self.two_person_frames / total_frames * 100}%")
        print(f"Процент времени, когда в зоне было 2+ человек:  {self.more_person_frames / total_frames * 100}%")
