import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from service.producer_service import ProducerService
from service.spark_writer_service import SparkWriterService
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,org.apache.kafka:kafka-clients:2.1.1 pyspark-shell'



def main():
    api_url = 'https://cointradermonitor.com/api/pbb/v1/ticker?exchanges=true'
    topic = "cotacao"
    kafka_servers = os.getenv('KAFKA_SERVERS', 'kafka:9092')
    base_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../data/input")
    )
    print('Entrando no producer')
    producer = ProducerService(kafka_servers, topic, api_url)
    writer = SparkWriterService(kafka_servers, topic, base_path)
    data = producer.fetch_api()  # Consome dados da API
    print(data)
    if data is not None:
        producer.produce(data)
    
    writer.run()    
    
if __name__ == '__main__':
    main()