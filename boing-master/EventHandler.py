from abc import ABC, abstractmethod

class EventHandler(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def execute(self):
        pass