from interfaces.i_spark_writer import ISparkWriter
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, FloatType, ArrayType
import os

class SparkWriterService(ISparkWriter):
    
    def __init__(self, kafka_servers, topic, json_dir) -> None:
        self.kafka_servers = kafka_servers
        self.topic = topic
        self.json_dir = json_dir
        
        # Cria uma sessão Spark
        self.spark = SparkSession.builder \
            .appName("SparkWriterJob") \
            .config("spark.executor.cores", "4") \
            .config("spark.cores.max", "4") \
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
        print(f'Kafka DF carregado==>{kafka_df}')
        schema = StructType([
            StructField("pair", StringType(), True),
            StructField("last", FloatType(), True),
            StructField("volume24h", FloatType(), True),
            StructField("var24h", FloatType(), True),
            StructField("time", StringType(), True),
            StructField("exchanges", ArrayType(StructType([
                StructField("code", StringType(), True),
                StructField("name", StringType(), True),
                StructField("volume24h", FloatType(), True),
                StructField("last", FloatType(), True)
            ])))
        ])
        # Converte os dados do Kafka de bytes para string
        kafka_df = kafka_df.selectExpr("CAST(value AS STRING)")
        
        parsed_df = kafka_df.withColumn("data", from_json(col("value"), schema)).select("data.*")

        return parsed_df
        
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