import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from service.spark_batch_service import SparkBatchService



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