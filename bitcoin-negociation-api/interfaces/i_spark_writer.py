from abc import ABC, abstractmethod

class ISparkWriter(ABC):
    
    @abstractmethod
    def process(self):
        pass;
    
    @abstractmethod
    def save(self, dataframe):
        pass;
    
    @abstractmethod
    def process(self):
        pass;
    
    @abstractmethod
    def run(self):
        pass;