import requests as req
from kafka import KafkaProducer
import json
from interfaces.i_producer_api import IProducerApi

class ProducerService(IProducerApi):
    def __init__(self, kafka_servers, topic, api_url, interval=60) -> None:
        self.kafka_servers = kafka_servers
        self.topic = topic
        self.api_url = api_url
        self.interval = interval

        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serializar mensagens em JSON
        )
        
    def fetch_api(self):
        
        try:
            response = req.get(self.api_url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'Erro na requisição: {response.status_code}')
                return None
        except Exception as e:
            print(f'Erro ao acessar a api: {e}')
            return None
    
    def produce(self, data):
        try:
            self.producer.send(self.topic, value=data)
            print(f"Dados enviados ao Kafka: {data}")
        except Exception as e:
            print(f"Erro ao enviar dados para o Kafka: {e}")