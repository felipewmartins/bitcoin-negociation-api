from interfaces.i_spark_writer import ISparkWriter
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
import os

class SparkWriterService(ISparkWriter):
    
    def __init__(self, kafka_servers, topic, json_dir) -> None:
        self.kafka_servers = kafka_servers
        self.topic = topic
        self.json_dir = json_dir
        
        # Cria uma sessão Spark
        self.spark = SparkSession.builder \
            .appName("SparkWriterJob") \
            .getOrCreate()
        
    def process(self):
        print(f'Processando dados do tópido {self.topic}')
        
        kafka_df = self.spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.kafka_servers) \
            .option("subscribe", self.topic) \
            .option("startingOffsets", "earliest") \
            .load()

        # Converte os dados do Kafka de bytes para string
        kafka_df = kafka_df.selectExpr("CAST(value AS STRING)")
        
    def save(self, dataframe):
        print(f"Salvando dados no diretório '{self.json_dir}'...")

        query = dataframe.writeStream \
            .format("json") \
            .option("path", self.json_dir) \
            .option("checkpointLocation", os.path.join(self.json_dir, "checkpoint")) \
            .outputMode("append") \
            .start()

        query.awaitTermination()
        
    def run(self):
        parsed_df = self.process()
        self.save(parsed_df)