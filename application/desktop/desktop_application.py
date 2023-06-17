from application.base import BaseApplication
from .kivy_application import PersonDetectionApp
from core import NoneCamera, Camera, NoneModel, Model


class DesktopApplication(BaseApplication):
    def __init__(self, debug: bool = False) -> None:
        super().__init__(debug)
        # TODO: change camera with camera list
        if self._debug:
            self._model = NoneModel()
            self._camera = NoneCamera(self._model)
        else:
            self._model = Model('mask_rcnn_coco.h5', person=True)
            self._camera = Camera('1', self._model)

        self.__app = PersonDetectionApp(self._camera)

    def _prepare(self) -> None:
        self._camera.start()

    def _app_cycle(self) -> None:
        self.__app.run()

    def _free_resources(self) -> None:
        self._camera.stop()
