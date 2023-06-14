from pixellib.instance import instance_segmentation
from typing import Dict, Any, Union, Tuple
from numpy import ndarray

from singleton import SingletonMeta


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

    def check_persons_in_zone(self, zone: Any) -> Tuple[bool, int]:
        return self._get_persons_number() > 0, self._get_persons_number()

    def _get_persons_number(self) -> int:
        return len(self._last_result[0]["scores"])
