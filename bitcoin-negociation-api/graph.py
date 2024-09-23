import streamlit as st
import pandas as pd
import plotly.express as px
import os

def load_parquet_files(path):
    all_files = os.listdir(path)
    print(all_files)
    df_list = []
    for file in all_files:
        if file.endswith(".parquet"):
            df = pd.read_parquet(os.path.join(path, file))
            df_list.append(df)
    return pd.concat(df_list, ignore_index=True)

def aggregate_data(df):
    aggregated_df = df.groupby("name")["average_last"].mean().reset_index()  # Média do valor 'last' por exchange
    return aggregated_df

def create_plot(df):
    fig = px.bar(df, x="name", y="average_last", title="Média de Preço por Exchange (BTC)")
    return fig

st.title("Dashboard de Negociações de Bitcoin")

parquet_directory = "../../data/output"  # Ajuste o caminho conforme necessário

data = load_parquet_files(parquet_directory)

st.write("Dados Carregados:")
st.dataframe(data)

# Agregar os dados e mostrar gráfico
aggregated_data = aggregate_data(data)
st.write("Média de Preço por Exchange:")
st.dataframe(aggregated_data)

fig = create_plot(aggregated_data)
st.plotly_chart(fig)