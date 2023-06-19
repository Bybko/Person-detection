from cv2 import waitKey
from typing import Dict, Any

from application.base import BaseApplication
from core import NoneModel, Model, NoneCamera, Camera, get_cameras_list


class TerminalApplication(BaseApplication):
    def __init__(self, debug: bool = False) -> None:
        super().__init__(debug)
        if self._debug:
            self._model = NoneModel()
            self._cameras = [NoneCamera(self._model)]
        else:
            self._model = Model('mask_rcnn_coco.h5', person=True)
            # TODO: change camera with camera list
            self._cameras = [Camera(camera_port, str(i), self._model)
                             for i, camera_port in enumerate(get_cameras_list())]

    def _prepare(self) -> None:
        for camera in self._cameras:
            camera.start()

    def _app_cycle(self) -> None:
        while True:
            self._clear_terminal()
            for camera in self._cameras:
                frame = camera.proceed_frame()
                camera.show_frame(frame)
                self._print_info(camera.get_info())

            if self._check_exit():
                break

    def _free_resources(self) -> None:
        for camera in self._cameras:
            camera.stop()

    def _clear_terminal(self) -> None:
        print('\033[H\033[J', end='')

    def _print_info(self, info: Dict[str, Any]) -> None:
        print(f'Camera: {info["name"]}\t Time:{info["total_time"]}')
        print(f'{"Zone name":^15}|{"Occupation time":^20}|{"Intervals num & avg":^20}|{"Persons avg":^11}')
        for name, zone in info['zones'].items():
            print(f'{name:^15}|{zone["person_time"]:>9} {zone["person_time_percent"]:>8}% |', end='')
            print(f'{zone["num_of_intervals"]:>5} {zone["avg_of_intervals"]:>13} |', end='')
            print(f'{zone["persons_avg"]:^11}')

    def _check_exit(self) -> bool:
        return waitKey(1) == ord('q')

    def __del__(self) -> None:
        self.stop()
