# imports

import yfinance as yf
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# variaveis de ambiente 

commodities = ['CL=F', 'SI=F', 'GC=F']

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_SCHEMA = os.getenv('DB_SCHEMA')

DB_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require'


engine = create_engine(DB_URL)

def get_data():
    query = "SELECT * FROM public.cb_dm_commodities"

    df = pd.read_sql(query, con=engine)

    return df


st.set_page_config(
    page_title="Commodities Dashboard",
    page_icon="💰",
    layout="wide",
)

st.title("Commodities Dashboard")

st.write("""
    Esse dashboard mostra os preços de commodities ao longo do tempo.
""")

df = get_data()

st.dataframe(df)