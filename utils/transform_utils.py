import pandas as pd

# Mantém as colunas indicadas no dicionário de Campos por Tabela
def manter_colunas(df: pd.DataFrame, colunas_desejadas: list[str]) -> pd.DataFrame:
    """
    Retorna um DataFrame apenas com as colunas especificadas.
    Ignora colunas não existentes.

    """
    colunas_existentes = [col for col in colunas_desejadas if col in df.columns]
    return df[colunas_existentes]

def padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza os nomes das colunas para:
    - minúsculas
    - sem espaços
    - com caracteres especiais removidos
    """
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^\w_]", "", regex=True)
    )
    return df