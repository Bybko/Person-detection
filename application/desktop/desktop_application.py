from application.base import BaseApplication
from .kivy_application import PersonDetectionApp
from core import Camera, Model


class DesktopApplication(BaseApplication):
    def __init__(self) -> None:
        super().__init__()
        self._model = Model('mask_rcnn_coco.h5', person=True)
        # TODO: change camera with camera list
        self._camera = Camera(self._model)
        self.__app = PersonDetectionApp(self._camera)

    def _prepare(self) -> None:
        self._camera.start()

    def _app_cycle(self) -> None:
        self.__app.run()

    def _free_resources(self) -> None:
        self._camera.stop()
