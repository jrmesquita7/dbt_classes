# imports

import yfinance as yf
import pandas as pd
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


def buscar_dados_commodities(simbolo, periodo='1y', intervalo='1d'):
    ticker = yf.Ticker(simbolo)
    dados = ticker.history(period=periodo, interval=intervalo)[['Close']]
    dados['simbolo'] = simbolo
    return dados

def buscar_todos_s_dados():
    todos_dados = []
    for simbolo in commodities:
        dados = buscar_dados_commodities(simbolo)
        todos_dados.append(dados)

    return pd.concat(todos_dados)

def salvar_dados_no_banco(df, schema='public'):
    df.to_sql(name='commodities', con=engine, schema=schema, if_exists='replace', index=True, index_label='Date')

if __name__ == '__main__':
    dados_concatenados = buscar_todos_s_dados()
    print(dados_concatenados)
    salvar_dados_no_banco(dados_concatenados, schema='public')

