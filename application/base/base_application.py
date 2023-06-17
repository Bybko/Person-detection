from abc import ABC, abstractmethod


class BaseApplication(ABC):
    def __init__(self, debug: bool) -> None:
        self._debug = debug

    def start(self) -> None:
        self._prepare()
        self._app_cycle()

    def stop(self) -> None:
        self._free_resources()

    @abstractmethod
    def _prepare(self) -> None: ...

    @abstractmethod
    def _app_cycle(self) -> None: ...

    @abstractmethod
    def _free_resources(self) -> None: ...
