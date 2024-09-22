import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from service.spark_batch_service import SparkBatchService
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,org.apache.kafka:kafka-clients:2.1.1 pyspark-shell'



def main():
    base_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../data/input")
    )
    
    output_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../data/output")
    )
    print('Entrando no producer')
    batch = SparkBatchService(base_path, output_path)
    
    batch.run()
if __name__ == '__main__':
    main()