from abc import ABC, abstractmethod

class ISparkBatch(ABC):
    
    @abstractmethod
    def process(self):
        pass;
    
    @abstractmethod
    def save(self, dataframe):
        pass;
    
    @abstractmethod
    def run(self):
        pass;