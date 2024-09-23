from abc import ABC, abstractmethod
from kafka import KafkaProducer

class IProducerApi(ABC):
    
    @abstractmethod
    def fetch_api(self):
        pass

    @abstractmethod
    def produce(self, data):
        pass

    def run(self):
        pass