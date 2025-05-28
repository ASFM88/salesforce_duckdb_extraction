import os
os.environ["REQUESTS_CA_BUNDLE"] = ""  # Ignora verificação SSL (em redes com proxy)

from simple_salesforce import Salesforce
from utils.update_handler import atualiza_incremental # type: ignore
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
    "raw_proposta": "Proposta_Credito__c",
    "raw_pricebook": "Pricebook2",
    "raw_top": "TOP__c",
    "raw_previsao_entrega": "Previsao_Entrega_Produto__c",
    "raw_cliente_final": "Clientefinalentrega__c",
    "raw_frete": "Frete__c"
}

# Conexão com o banco RAW do DuckDB
os.makedirs("db", exist_ok=True)
conn = duckdb.connect("db/raw_salesforce.duckdb")

# Loop de extração e atualização incremental
for nome_tabela, objeto_sf in objetos.items():
    try:
        print(f"\n🔄 Processando objeto '{objeto_sf}' → tabela '{nome_tabela}'")

        # Descreve os campos do objeto
        descricao = getattr(sf, objeto_sf).describe()
        campos = [f["name"] for f in descricao["fields"]]
        soql = "SELECT " + ", ".join(campos) + f" FROM {objeto_sf}"

        # Paginação
        resultado = sf.query(soql)
        registros = resultado["records"]
        while not resultado["done"]:
            resultado = sf.query_more(resultado["nextRecordsUrl"], True)
            registros.extend(resultado["records"])

        # Transforma em DataFrame
        df = pd.DataFrame(registros).drop(columns="attributes", errors="ignore")
        df = df.fillna("").astype(str)

        # Aplica atualização incremental
        atualiza_incremental(conn, nome_tabela, df)

    except Exception as e:
        print(f"❌ Erro ao processar {objeto_sf} → {e}")

conn.close()
print("\n✅ Script executado com sucesso.")
