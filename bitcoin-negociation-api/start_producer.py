from service.producer_service import ProducerService
import os

def main():
    api_url = 'https://cointradermonitor.com/api/pbb/v1/ticker?exchanges=true'
    topic = "cotacao"
    kafka_servers = os.getenv('KAFKA_SERVERS', 'kafka:9092')

    producer = ProducerService(kafka_servers, topic, api_url)
    producer.run()

if __name__ == '__main__':
    main()