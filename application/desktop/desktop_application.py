from application.base import BaseApplication
from .kivy_application import PersonDetectionApp
from core import NoneCamera, Camera, get_cameras_list, NoneModel, Model


class DesktopApplication(BaseApplication):
    def __init__(self, debug: bool = False) -> None:
        super().__init__(debug)
        if self._debug:
            self._model = NoneModel()
            self._cameras = [NoneCamera(self._model), NoneCamera(self._model), NoneCamera(self._model)]
        else:
            self._model = Model('mask_rcnn_coco.h5', person=True)
            self._cameras = [Camera(camera_port, str(i), self._model)
                             for i, camera_port in enumerate(get_cameras_list())]

        self.__app = PersonDetectionApp(self._cameras)

    def _prepare(self) -> None:
        for camera in self._cameras:
            camera.start()

    def _app_cycle(self) -> None:
        self.__app.run()

    def _free_resources(self) -> None:
        for camera in self._cameras:
            camera.stop()
