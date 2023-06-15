from cv2 import waitKey

from application.base import BaseApplication
from core import Model, Camera


class TerminalApplication(BaseApplication):
    def __init__(self) -> None:
        super().__init__()
        self._model = Model('mask_rcnn_coco.h5', person=True)
        # TODO: change camera with camera list
        self._camera = Camera(self._model)

    def _prepare(self) -> None:
        self._camera.start()

    def _app_cycle(self) -> None:
        while True:
            frame = self._camera.proceed_frame()
            self._camera.show_frame(frame)
            print('\033[H\033[J', end='')
            print(self._camera.get_info())

            if self._check_exit():
                break

    def _free_resources(self) -> None:
        self._camera.stop()

    def _check_exit(self) -> bool:
        return waitKey(1) == ord('q')

    def __del__(self) -> None:
        self.stop()
