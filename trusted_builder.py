#%%
import duckdb
import sqlite3
import os
from utils import transform_utils as tu

STAGE_DB = "db/stage_salesforce.duckdb"
TRUSTED_DB = "db/trusted_salesforce.duckdb"

TABELAS = [
    "recordtype", "user", "account", "contact", "cultura", "endereco", "cidade",
    "order", "orderitem", "vendedores", "tabela_de_comissao", "tipo_negociacao",
    "unidade", "vencimento_pedido", "pagamento", "product2", "pricebook2",
    "top", "previsao_entrega_produto", "clientefinalentrega", "frete"
]

CAMPOS_POR_TABELA = {
    "recordtype": ["id", "name", "sobjecttype", "developername"],
    "user": ["id", "name", "email", "profileid", "username", "isactive"],
    "account": ["id", "name", "grupo_cliente__c", "tipo__c", "cnpj__c"],
    "contact": ["id", "lastname", "email", "accountid", "phone"],
    "cultura": ["id", "name", "cliente__c", "cultura__c"],
    "endereco": ["id", "name", "conta__c", "cidade__c", "cep__c", "principal__c"],
    "cidade": ["id", "name", "estado__c", "codigoibge__c"],
    "order": ["id", "status", "accountid", "effective_date", "recordtypeid"],
    "orderitem": ["id", "orderid", "product2id", "quantity", "unitprice"],
    "vendedores": ["id", "name", "usuario__c", "unidade__c"],
    "tabela_de_comissao": ["id", "name", "percentual__c", "ativo__c"],
    "tipo_negociacao": ["id", "name", "descricao__c", "ativo__c"],
    "unidade": ["id", "name", "regional__c"],
    "vencimento_pedido": ["id", "pedido__c", "datavencimento__c"],
    "pagamento": ["id", "pedido__c", "formapagamento__c", "valorpagamento__c"],
    "product2": ["id", "name", "familia__c", "ativo", "codigo__c"],
    "pricebook2": ["id", "name", "isactive"],
    "top": ["id", "pedido__c", "data_entrega__c"],
    "previsao_entrega_produto": ["id", "orderitem__c", "data_prevista__c"],
    "clientefinalentrega": ["id", "pedido__c", "nome_cliente_final__c"],
    "frete": ["id", "pedido__c", "transportadora__c", "valor__c"]
}

con_stage = duckdb.connect(STAGE_DB)
con_trusted = duckdb.connect(TRUSTED_DB)

for tabela in TABELAS:
    print(f"🔄 Processando tabela: {tabela}")
    try:
        nome_stage = f"stage_{tabela}"
        df = con_stage.execute(f"SELECT * FROM {nome_stage}").df()

        df = tu.padronizar_colunas(df)

        # Apenas mantém as colunas necessárias, sem aplicar outras transformações ainda
        colunas_desejadas = CAMPOS_POR_TABELA.get(tabela)
        if colunas_desejadas:
            df = tu.manter_colunas(df, colunas_desejadas)

        con_trusted.execute(f'CREATE OR REPLACE TABLE "{tabela}" AS SELECT * FROM df')
        print(f"✅ Tabela '{tabela}' salva na camada trusted.\n")

    except Exception as e:
        print(f"❌ Erro ao processar '{tabela}': {e}\n")

con_stage.close()

# Caminho do novo banco SQLite
SQLITE_STAGE_PATH = "db/stage_salesforce.sqlite"

# Remove o SQLite anterior (opcional: sobrescrever)
if os.path.exists(SQLITE_STAGE_PATH):
    os.remove(SQLITE_STAGE_PATH)

# Conexão com SQLite
sqlite_conn = sqlite3.connect(SQLITE_STAGE_PATH)

print("\n🟠 Salvando dados da camada STAGE também no SQLite...")
for tabela in TABELAS:
    try:
        nome_trusted = tabela
        df = con_trusted.execute(f'SELECT * FROM "{nome_trusted}"').df()
        df.to_sql(tabela, sqlite_conn, index=False)
        print(f"✅ Tabela '{tabela}' salva no SQLite.")
    except Exception as e:
        print(f"❌ Erro ao salvar '{tabela}' no SQLite: {e}")

sqlite_conn.close()
con_trusted.close()
#%%
