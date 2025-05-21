# %%
import pandas as pd
import keyring # type: ignore
import duckdb # type: ignore
import sqlite3 # type: ignore
from simple_salesforce import Salesforce
from db_utils import salvar_em_duckdb, salvar_em_sqlite

# Recupera do cofre de senhas
username = keyring.get_password("salesforce", "SF_USER")
password = keyring.get_password("salesforce", "SF_PASS")
token = keyring.get_password("salesforce", "SF_TOKEN")

# Conecta o Salesforce
sf = Salesforce(username=username,
                password=password,
                security_token=token)

# Função auxiliar para paginação
def consultar_completo(query):
    resultado = sf.query(query)
    registros = resultado['records']
    while not resultado['done']:
        resultado = sf.query_more(resultado['nextRecordsUrl'], True)
        registros.extend(resultado['records'])
    return registros

# Consulta Account 
records_account = consultar_completo("SELECT Id, Name FROM Account")
df_account = pd.DataFrame(records_account).drop(columns='attributes')
salvar_em_duckdb(df_account, tabela="sf_account")
print(f"✅ Account: {len(df_account)} registros salvos.")

# Consulta Order
records_order = consultar_completo("SELECT Id, OrderNumber FROM Order")
df_order = pd.DataFrame(records_order).drop(columns='attributes')
salvar_em_duckdb(df_order, tabela="sf_order")
print(f"✅ Contact: {len(df_order)} registros salvos.")

# Salva nos bancos Account
salvar_em_duckdb(df_account, tabela="sf_account")
salvar_em_sqlite(df_account, tabela="sf_account")
print(f"✅ Account: {len(df_account)} registros salvos em DuckDB e SQLite.")

# Salva nos bancos Order
salvar_em_duckdb(df_order, tabela="sf_order")
salvar_em_sqlite(df_order, tabela="sf_order")
print(f"✅ Contact: {len(df_order)} registros salvos em DuckDB e SQLite.")

# Salvar em CSV
df_account.to_csv("teste_account_salesforce.csv", index=False)


# Conectando e listando as tabelas criadas DuckDB
conn = duckdb.connect("db/dados_salesforce.duckdb")
tables = conn.execute("SHOW TABLES").fetchall()
print("Tabelas existentes:", tables)

# Excluindo tabela DuckDB
conn.execute("DROP TABLE IF EXISTS account")
tables = conn.execute("SHOW TABLES").fetchall()
print("Tabelas existentes:", tables)

# Verifica a estrutura da tabela DuckDB
conn.execute("DESCRIBE sf_order").fetchdf()
conn.execute("DESCRIBE sf_account").fetchdf()

# Consulta as tabelas DuckDB
consulta_order = conn.execute("SELECT * FROM sf_order where Id = '8014y000002rFK2AAM' limit 10").fetchdf()
print(consulta_order)

# Encerrar conexão ativa com banco DuckDB
conn.close()

# Conecta ao banco SQLite
conn = sqlite3.connect("db/dados_salesforce.db")

# Consulta as tabelas existentes
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()

# Mostra o nome das tabelas
print("Tabelas encontradas:")
for t in tabelas:
    print("-", t[0])

# Consulta ao banco SQLite
consulta_order = pd.read_sql_query(
    "SELECT * FROM sf_order LIMIT 10",
    conn
)

# Exibe o resultado
print(consulta_order)

# Encerrar conexão ativa com banco SQLite
conn.close()


# %%
