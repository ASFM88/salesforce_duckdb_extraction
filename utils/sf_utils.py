import re
from simple_salesforce import Salesforce

def consultar_completo(sf, soql):
    """Realiza a consulta completa com paginação na API do Salesforce."""
    resultado = sf.query(soql)
    registros = resultado['records']
    while not resultado['done']:
        resultado = sf.query_more(resultado['nextRecordsUrl'], True)
        registros.extend(resultado['records'])
    return registros

def extrair_nome_objeto(soql):
    """Extrai o nome do objeto Salesforce a partir de uma string SOQL."""
    tokens = soql.upper().split("FROM")
    if len(tokens) > 1:
        return tokens[1].strip().split()[0]
    return None