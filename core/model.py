from pixellib.instance import instance_segmentation
from typing import Dict, Any, Union, Tuple, List
from numpy import ndarray

from singleton import SingletonMeta


Box = Tuple[Any, Any, Any, Any]


class Model(metaclass=SingletonMeta):
    def __init__(self, model_path: str, infer_speed: str = 'rapid', **target_classes: bool) -> None:
        self._model_path = model_path
        self._segment_camera = instance_segmentation(infer_speed)
        self._segment_camera.load_model(self._model_path)
        self._target_class = self._segment_camera.select_target_classes(**target_classes)
        self._last_result: Tuple[Union[Dict[str, ndarray], Dict[str, ndarray]], Any] = ()

    def proceed_frame(self, frame: Any) -> None:
        self._last_result = self._segment_camera.segmentFrame(frame, show_bboxes=True,
                                                              segment_target_classes=self._target_class)
        print(self._last_result[0]['rois'])

    def check_persons_in_zone(self, zone: Any) -> Tuple[bool, int]:
        boxes = self._get_persons_boxes()
        count = 0
        for box in boxes:
            if self._check_x_overlap(zone, box) and self._check_y_overlap(zone, box):
                count += 1
        return count > 0, count

    def _get_persons_boxes(self) -> List[Box]:
        boxes = []
        for box in self._last_result[0]['rois']:
            boxes.append((box[1], box[0], box[3], box[2]))
        return boxes

    def _check_x_overlap(self, box1: Box, box2: Box) -> bool:
        return box1[2] >= box2[0] and box2[2] >= box1[0]

    def _check_y_overlap(self, box1: Box, box2: Box) -> bool:
        return box1[3] >= box2[1] and box2[3] >= box1[1]
