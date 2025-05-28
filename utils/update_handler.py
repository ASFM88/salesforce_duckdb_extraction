#%%
import duckdb
from datetime import datetime
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

def atualiza_incremental(conexao, nome_tabela, df_novo):
    """
    Atualiza a tabela existente com base em Id e LastModifiedDate.
    Insere novos registros, atualiza os alterados, e salva históricos.

    Parâmetros:
    - conexao: conexão ativa com o DuckDB.
    - nome_tabela: nome da tabela principal (ex: 'account').
    - df_novo: DataFrame com os dados extraídos do Salesforce.
    """
    # Converte string para datetime padrão
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_novo["data_inclusao_bd"] = now_str

    # Garante que a tabela base existe
    try:
        df_antigo = conexao.execute(f"SELECT * FROM {nome_tabela}").df()
    except:
        print(f"⚠️ Tabela '{nome_tabela}' não encontrada, criando pela primeira vez.")
        df_novo.to_sql(nome_tabela, conexao, index=False)
        return

    # JOIN por Id
    df_merge = df_novo.merge(df_antigo[["Id", "LastModifiedDate"]], on="Id", how="left", suffixes=("", "_antigo"))

    # INSERIR NOVOS
    df_insert = df_merge[df_merge["LastModifiedDate_antigo"].isna()]
    if not df_insert.empty:
        print(f"➕ Inserindo {len(df_insert)} novos registros...")
        df_insert[df_novo.columns].to_sql(nome_tabela, conexao, if_exists='append', index=False)

    # ATUALIZAR MODIFICADOS
    df_update = df_merge[
        df_merge["LastModifiedDate_antigo"].notna() &
        (df_merge["LastModifiedDate"] > df_merge["LastModifiedDate_antigo"])
    ]
    if not df_update.empty:
        print(f"♻️ Atualizando {len(df_update)} registros modificados...")

        # Salva os registros antigos no histórico
        id_lista = tuple(df_update["Id"])
        historico = conexao.execute(
            f"SELECT * FROM {nome_tabela} WHERE Id IN {id_lista}"
        ).df()
        historico["data_inclusao_bd"] = now_str
        historico.to_sql(f"{nome_tabela}_hist_update", conexao, if_exists="append", index=False)

        # Apaga os registros antigos
        conexao.execute(f"DELETE FROM {nome_tabela} WHERE Id IN {id_lista}")

        # Insere os registros novos (com update aplicado)
        df_update[df_novo.columns].to_sql(nome_tabela, conexao, if_exists='append', index=False)

#%%