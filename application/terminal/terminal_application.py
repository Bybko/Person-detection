from cv2 import waitKey
from typing import Dict, Any

from application.base import BaseApplication
from core import NoneModel, Model, NoneCamera, Camera


class TerminalApplication(BaseApplication):
    def __init__(self, debug: bool = False) -> None:
        super().__init__(debug)
        if self._debug:
            self._model = NoneModel()
            self._camera = NoneCamera(self._model)
        else:
            self._model = Model('mask_rcnn_coco.h5', person=True)
            # TODO: change camera with camera list
            self._camera = Camera('1', self._model)

    def _prepare(self) -> None:
        self._camera.start()

    def _app_cycle(self) -> None:
        while True:
            frame = self._camera.proceed_frame()
            self._camera.show_frame(frame)
            self._print_info(self._camera.get_info())

            if self._check_exit():
                break

    def _free_resources(self) -> None:
        self._camera.stop()

    def _print_info(self, info: Dict[str, Any]) -> None:
        print('\033[H\033[J', end='')
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
