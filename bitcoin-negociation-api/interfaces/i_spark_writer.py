from abc import ABC, abstractmethod
from pyspark.sql import DataFrame

class ISparkWriter(ABC):
    
    @abstractmethod
    def process(self):
        pass;
    
    @abstractmethod
    def save(self, dataframe: DataFrame):
        pass;
    
    @abstractmethod
    def process(self):
        pass;
    
    @abstractmethod
    def run(self):
        pass;