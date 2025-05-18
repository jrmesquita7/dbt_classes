# Imports
import yfinance as yf
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import plotly.express as px
import plotly.graph_objects as go

# Load .env
load_dotenv()

# Database config
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_SCHEMA = os.getenv('DB_SCHEMA')

DB_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require'
engine = create_engine(DB_URL)

# Função para pegar os dados
def get_data():
    query = "SELECT * FROM public.commodities"
    df = pd.read_sql(query, con=engine)
    df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)  # Remove timezone
    return df

# Configuração da página
st.set_page_config(page_title="Commodities Dashboard", page_icon="💰", layout="wide")
st.title("📈 Commodities Dashboard")
st.write("Esse dashboard mostra os preços de commodities ao longo do tempo.")

# Dados
df = get_data()

# Filtros
symbols = df['simbolo'].unique()
selected_symbol = st.selectbox("Escolha o símbolo:", symbols)

df_filtered = df[df['simbolo'] == selected_symbol]
start_date = st.date_input("Data inicial", df_filtered['Date'].min().date())
end_date = st.date_input("Data final", df_filtered['Date'].max().date())

df_filtered = df_filtered[
    (df_filtered['Date'] >= pd.to_datetime(start_date)) &
    (df_filtered['Date'] <= pd.to_datetime(end_date))
]

# Métricas
st.subheader("📊 Métricas")
col1, col2, col3 = st.columns(3)
col1.metric("Preço Máximo", f"${df_filtered['Close'].max():.2f}")
col2.metric("Preço Mínimo", f"${df_filtered['Close'].min():.2f}")
col3.metric("Preço Médio", f"${df_filtered['Close'].mean():.2f}")

# Gráfico de Linha
st.subheader("📉 Evolução dos Preços (Linha)")
fig_line = px.line(df_filtered, x='Date', y='Close', title=f'Preço de fechamento - {selected_symbol}', markers=True)
fig_line.update_layout(xaxis_title="Data", yaxis_title="Preço", template="plotly_white")
st.plotly_chart(fig_line, use_container_width=True)

# Gráfico Candlestick (caso tenha colunas OHLC)
if {'Open', 'High', 'Low', 'Close'}.issubset(df_filtered.columns):
    st.subheader("📈 Gráfico Candlestick")
    fig_candle = go.Figure(data=[go.Candlestick(
        x=df_filtered['Date'],
        open=df_filtered['Open'],
        high=df_filtered['High'],
        low=df_filtered['Low'],
        close=df_filtered['Close']
    )])
    fig_candle.update_layout(
        title=f'Candlestick - {selected_symbol}',
        xaxis_title='Data',
        yaxis_title='Preço',
        template='plotly_white'
    )
    st.plotly_chart(fig_candle, use_container_width=True)

# Tabela final
st.subheader("📋 Tabela de dados")
st.dataframe(
    df_filtered.style
        .format({"Close": "{:.2f}"})
        .highlight_max("Close", color="lightgreen")
        .highlight_min("Close", color="lightcoral"),
    use_container_width=True
)
