import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from service.producer_service import ProducerService
from service.spark_writer_service import SparkWriterService
from service.spark_batch_service import SparkBatchService
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,org.apache.kafka:kafka-clients:2.1.1 pyspark-shell'



def main():
    topic = "cotacao"
    kafka_servers = os.getenv('KAFKA_SERVERS', 'kafka:9092')
    base_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../data/input")
    )
    print('Entrando no writer')
    writer = SparkWriterService(kafka_servers, topic, base_path)
        
    
    writer.run()    
    
if __name__ == '__main__':
    main()