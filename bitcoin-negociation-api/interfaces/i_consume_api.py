from abc import ABC, abstractmethod

class IConsumeApi(ABC):

    @abstractmethod
    def consume(self):
        pass