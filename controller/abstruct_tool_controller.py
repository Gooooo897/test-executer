from abc import ABC, abstractmethod

class AbstructToolController(ABC):
    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass