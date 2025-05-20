# %%
from simple_salesforce import Salesforce
import pandas as pd
import keyring # type: ignore

# Recupera do cofre de senhas
username = keyring.get_password("salesforce", "SF_USER")
password = keyring.get_password("salesforce", "SF_PASS")
token = keyring.get_password("salesforce", "SF_TOKEN")

# Conecta o Salesforce
sf = Salesforce(username=username,
                password=password,
                security_token=token)

# Consulta Simples Account
query_result = sf.query("SELECT Id, Name FROM Account")

# Armazena todos os registros (inicialmente os 2 mil primeiros ou menos)
all_records = query_result['records']

# Continua buscando até que 'done' seja True
while not query_result['done']:
    query_result = sf.query_more(query_result['nextRecordsUrl'], True)
    all_records.extend(query_result['records'])

# Agora sobrescreve o query_result com tudo
query_result['records'] = all_records
query_result['totalSize'] = len(all_records)
query_result['done'] = True

# Exemplo: mostrar total
print(f"Total de registros completos: {query_result['totalSize']}")

# Conversão dos dados para DataFrame
df = pd.DataFrame(query_result['records']).drop(columns='attributes')

# Exibição como tabela
print(df)

# Salvar em CSV
df.to_csv("teste_account_salesforce.csv", index=False)
# %%
