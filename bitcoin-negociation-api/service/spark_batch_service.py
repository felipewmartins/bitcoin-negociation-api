from interfaces.i_spark_batch import ISparkBatch
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, avg
import os
import shutil

class SparkBatchService(ISparkBatch):
    
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        
        self.spark = SparkSession.builder \
            .appName("SparkBatchServiceJob") \
            .getOrCreate()
        
    
    def process(self):
        print(f"Lendo arquivos JSON da pasta '{self.input_dir}'...")

        # Lê os arquivos JSON do diretório de entrada
        df = self.spark.read.json(self.input_dir)

        # Explode o array de exchanges para criar uma linha por exchange
        df_exploded = df.select(explode(col("exchanges")).alias("exchange"))

        # Agrupa por código de exchange e calcula a média do campo "last"
        df_grouped = df_exploded.groupBy("exchange.code", "exchange.name") \
                                .agg(avg(col("exchange.last")).alias("average_last"))
        return df_grouped
    
    def save(self, dataframe):
        print(f"Salvando arquivos Parquet na pasta '{self.output_dir}'...")

        # Salva os dados no formato Parquet
        dataframe.write \
            .mode("overwrite") \
            .parquet(self.output_dir)

        # Remove os arquivos JSON da pasta de entrada
        print(f"Removendo arquivos JSON da pasta '{self.input_dir}'...")
        shutil.rmtree(self.input_dir)
        os.makedirs(self.input_dir, exist_ok=True)