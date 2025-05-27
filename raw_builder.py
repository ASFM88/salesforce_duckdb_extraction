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
    "raw_recordtype": "RecordType",
    "raw_user": "User",
    "raw_account": "Account",
    "raw_contact": "Contact",
    "raw_culturacliente": "Cultura_do_Cliente__c",
    "raw_cultura": "Cultura__c",
    "raw_endereco": "Endereco__c",
    "raw_cidade": "Cidade__c",
    "raw_subregiao": "Sub_regiao__c",
    "raw_order": "Order",
    "raw_orderitem": "OrderItem",
    "raw_vendedores": "Vendedores__c",
    "raw_tipo_comissao": "Tabela_de_comissao__c",
    "raw_tipo_vencimento": "Tipo_Negociacao__c",
    "raw_unidade": "Unidade__c",
    "raw_vencimento_contrato": "Vencimento_Pedido__c",
    "raw_pagamento": "Pagamento__c",
    "raw_product": "Product2",
    "raw_pricebook": "Pricebook2",
    "raw_top": "TOP__c",
    "raw_previsao_entrega": "Previsao_Entrega_Produto__c",
    "raw_cliente_final": "Clientefinalentrega__c",
    "raw_frete": "Frete__c"
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
