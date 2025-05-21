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

# Dicionário com nome da tabela local e a respectiva consulta SOQL
objetos_soql = {
    "sf_account": "SELECT Id, Name FROM Account",
    "sf_contact": "SELECT Id, LastName, Email FROM Contact",
    "sf_order": "SELECT Id, Status, EffectiveDate FROM Order"
}

# Salvar em CSV
# df_account.to_csv("teste_account_salesforce.csv", index=False)

# Loop para consultar e salvar os dados de cada objeto
for tabela, soql in objetos_soql.items():
    print(f"🔍 Consultando {tabela}...")

    try:
        registros = consultar_completo(soql)
        df = pd.DataFrame(registros).drop(columns='attributes')
        
        # Salva em DuckDB e SQLite
        salvar_em_duckdb(df, tabela=tabela)
        salvar_em_sqlite(df, tabela=tabela)

        print(f"✅ {tabela}: {len(df)} registros salvos em DuckDB e SQLite.")
    
    except Exception as e:
        print(f"❌ Erro ao consultar {tabela}: {e}")


# Conectando e listando as tabelas criadas DuckDB
conn = duckdb.connect("db/dados_salesforce.duckdb")
tables = conn.execute("SHOW TABLES").fetchall()
print("Tabelas existentes:", tables)

# Excluindo tabela DuckDB
# conn.execute("DROP TABLE IF EXISTS account")
# tables = conn.execute("SHOW TABLES").fetchall()
# print("Tabelas existentes:", tables)

# Verifica a estrutura da tabela DuckDB
for tabela in tables:
    nome = tabela[0]
    print(f"📋 Estrutura da tabela: {nome}")
    estrutura = conn.execute(f'DESCRIBE "{nome}"').fetchdf()
    print(estrutura, "\n")

conn.close()

# # Consulta as tabelas DuckDB
# consulta_order = conn.execute("SELECT * FROM sf_order limit 10").fetchdf()
# print(consulta_order)

# Encerrar conexão ativa com banco DuckDB
# conn.close()

# Conecta ao banco SQLite
conn = sqlite3.connect("db/dados_salesforce.db")

# Consulta as tabelas existentes
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()

# Mostra o nome das tabelas SQLite
print("Tabelas encontradas:")
for t in tabelas:
    print("-", t[0])

# Verifica a estrutura da tabela SQLite
for tabela in tabelas:
    nome = tabela[0]
    print(f"📋 Estrutura da tabela: {nome}")
    
    # PRAGMA retorna a estrutura da tabela
    estrutura = pd.read_sql_query(f"PRAGMA table_info('{nome}')", conn)
    print(estrutura, "\n")

conn.close()

# Consulta ao banco SQLite
# consulta_order = pd.read_sql_query(
#     "SELECT * FROM sf_order LIMIT 10",
#     conn
# )

# Exibe o resultado
# print(consulta_order)

# Encerrar conexão ativa com banco SQLite
# conn.close()

print("✅ Script executado com sucesso.")
# %%
