from interfaces.i_spark_batch import ISparkBatch
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, avg
import os
import glob
import time

class SparkBatchService(ISparkBatch):
    
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        
        self.spark = SparkSession.builder \
            .appName("SparkBatchServiceJob") \
            .config("spark.ui.port", "4050") \
            .config("spark.cores.max", "4") \
            .getOrCreate()
        
    
    def process(self):
        print(f"Lendo arquivos JSON da pasta '{self.input_dir}'...")

        # Excluir arquivos de metadados do Spark
        json_files = glob.glob(f"{self.input_dir}/*.json")
        if not json_files:
            print("Nenhum arquivo JSON encontrado para processamento.")
            return None

        # Lê os arquivos JSON do diretório de entrada
        df = self.spark.read.json(json_files)

        # Explode o array de exchanges para criar uma linha por exchange
        df_exploded = df.select(explode(col("exchanges")).alias("exchange"))

        # Agrupa por código de exchange e calcula a média do campo "average_last"
        df_grouped = df_exploded.groupBy("exchange.code", "exchange.name") \
                                .agg(avg(col("exchange.last")).alias("average_last"))
        
        self.spark.catalog.clearCache()

        return df_grouped
    
    def save(self, dataframe):
        print(f"Salvando arquivos Parquet na pasta '{self.output_dir}'...")

        # Salva os dados no formato Parquet
        dataframe.write \
            .mode("append") \
            .parquet(self.output_dir)

        # Remove apenas arquivos JSON da pasta de entrada
        print(f"Removendo arquivos JSON da pasta '{self.input_dir}'...")
        for json_file in glob.glob(f"{self.input_dir}/*.json"):
            os.remove(json_file)
        print(f"Arquivos JSON removidos da pasta '{self.input_dir}'.")
        
    def run(self):
        while True:
            df_grouped = self.process()
            self.save(df_grouped)

            time.sleep(65)