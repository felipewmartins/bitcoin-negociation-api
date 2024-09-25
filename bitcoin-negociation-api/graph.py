import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time

# Função para carregar arquivos parquet
def load_parquet_files(path):
    all_files = os.listdir(path)
    df_list = []
    for file in all_files:
        if file.endswith(".parquet"):
            df = pd.read_parquet(os.path.join(path, file))
            df_list.append(df)
    if df_list:
        return pd.concat(df_list, ignore_index=True)
    else:
        return pd.DataFrame()  # Retorna DataFrame vazio se não houver arquivos

# Função para agregar os dados
def aggregate_data(df):
    aggregated_df = df.groupby("name")["average_last"].mean().reset_index()
    return aggregated_df

# Função para criar o gráfico
def create_plot(df):
    fig = px.bar(df, x="name", y="average_last", title="Média de Preço por Exchange (BTC)")
    return fig

st.title("Dashboard de Negociações de Bitcoin")

parquet_directory = "../data/output"

refresh_interval = 5

while True:
    data = load_parquet_files(parquet_directory)
    
    if not data.empty:
        st.write("Dados Carregados:")
        st.dataframe(data)

        aggregated_data = aggregate_data(data)
        st.write("Média de Preço por Exchange:")
        st.dataframe(aggregated_data)

        fig = create_plot(aggregated_data)
        st.plotly_chart(fig)

    else:
        st.write("Nenhum arquivo Parquet encontrado no diretório.")

    time.sleep(refresh_interval)

    st.rerun()