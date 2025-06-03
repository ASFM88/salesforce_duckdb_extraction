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

def alinhar_colunas(df_novo: pd.DataFrame, df_antigo: pd.DataFrame) -> pd.DataFrame:
    """
    Alinha o df_novo para ter a mesma estrutura de colunas que df_antigo,
    incluindo colunas extras ou faltantes, mantendo a ordem original.
    """
    colunas_antigas = set(df_antigo.columns)
    colunas_novas = set(df_novo.columns)

    # Adiciona colunas faltantes no df_antigo
    for coluna in colunas_novas - colunas_antigas:
        df_antigo[coluna] = None

    # Adiciona colunas removidas no df_novo
    for coluna in colunas_antigas - colunas_novas:
        df_novo[coluna] = None

    # Reordena df_novo para a mesma ordem do df_antigo
    df_novo = df_novo[df_antigo.columns]

    return df_novo