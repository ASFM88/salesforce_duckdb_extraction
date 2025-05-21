import os
os.environ["REQUESTS_CA_BUNDLE"] = ""  # Ignora verificação SSL (em redes com proxy)

from simple_salesforce import Salesforce
import pandas as pd
import keyring  # type: ignore
import duckdb

# Autenticação com Salesforce
username = keyring.get_password("salesforce", "SF_USER")
password = keyring.get_password("salesforce", "SF_PASS")
token = keyring.get_password("salesforce", "SF_TOKEN")
sf = Salesforce(username=username, password=password, security_token=token)

# Objetos que você deseja extrair completamente
objetos = {
    "raw_account": "Account",
    "raw_contact": "Contact",
    "raw_order": "Order"
}

# Conexão com o banco RAW do DuckDB
os.makedirs("db", exist_ok=True)
conn = duckdb.connect("db/raw_salesforce.duckdb")

# Loop de exportação
for nome_tabela, objeto_sf in objetos.items():
    try:
        # Recupera todos os campos via describe
        descricao = getattr(sf, objeto_sf).describe()
        campos = [f["name"] for f in descricao["fields"]]
        soql = "SELECT " + ", ".join(campos) + f" FROM {objeto_sf}"

        # Paginação da consulta
        resultado = sf.query(soql)
        registros = resultado["records"]
        while not resultado["done"]:
            resultado = sf.query_more(resultado["nextRecordsUrl"], True)
            registros.extend(resultado["records"])

        # Transforma em DataFrame e trata para compatibilidade com DuckDB
        df = pd.DataFrame(registros).drop(columns="attributes", errors="ignore")
        df = df.fillna("")      # Substitui todos os nulos por string vazia
        df = df.astype(str)     # Converte todas as colunas para string

        # Criação da tabela RAW no DuckDB
        conn.execute(f'DROP TABLE IF EXISTS "{nome_tabela}"')
        conn.execute(f'CREATE TABLE "{nome_tabela}" AS SELECT * FROM df')

        print(f"✅ {nome_tabela}: {len(df)} registros salvos com todos os campos.")
    
    except Exception as e:
        print(f"❌ Erro ao processar {objeto_sf} → {e}")

conn.close()
print("✅ Script executado com sucesso.")
