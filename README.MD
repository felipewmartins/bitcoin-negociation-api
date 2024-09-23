# Bitcoin Negociation API

Este projeto utiliza Spark e Kafka para realizar o processamento de dados em tempo real e em lote de arquivos `.json` sobre negociações de Bitcoin. O resultado final é salvo em arquivos `.parquet`, que podem ser visualizados através de um dashboard interativo utilizando Streamlit.

## Pré-requisitos

- Docker e Docker Compose instalados

## Como executar o projeto

### 1. Inicializar a infraestrutura

Para compilar e executar o projeto com 3 workers do Spark, utilize o seguinte comando:

```bash
docker compose -f docker-compose.yml up --scale spark-worker=3
```

Este comando inicia todos os contêineres necessários (Kafka, Spark master, Spark workers) e escala os workers do Spark para 3.

### 2. Iniciar o produtor Kafka
Após os contêineres estarem no ar, acesse o terminal de um dos contêineres:

```bash
docker exec -it <hash_container> bash
```

No terminal do contêiner, execute o seguinte comando para iniciar o produtor Kafka que enviará os dados para o tópico:
 ```bash
 python bitcoin-negociation-api/bitcoin-negociation-api/start_producer.py
 ```

### 3. Iniciar o pipeline de streaming
Em outra sessão de terminal, acesse o mesmo contêiner (ou outro) e execute o pipeline de streaming do Spark, que lê os dados do Kafka e grava em .parquet:
```bash
python bitcoin-negociation-api/bitcoin-negociation-api/start_pipeline_writer.py
```

### 4. Executar o pipeline em batch
Em uma terceira sessão de terminal, execute o pipeline batch do Spark, que lê os arquivos .json e os transforma em .parquet:

```bash
python bitcoin-negociation-api/bitcoin-negociation-api/start_pipeline_batch.py
```

### 5. Visualizar o dashboard
Após a execução dos pipelines, saia do contêiner e, no diretório do projeto, execute o seguinte comando para iniciar o dashboard usando Streamlit:

```bash
streamlit run graph.py
````

O Streamlit irá ler os arquivos .parquet gerados na pasta data/output e exibir o dashboard interativo no seguinte endereço:

http://localhost:8501