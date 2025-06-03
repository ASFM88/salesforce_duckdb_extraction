#%%

import duckdb
from datetime import datetime
from utils.transform_utils import alinhar_colunas  # Adicione esse import
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

        # Após carregar df_antigo com sucesso
        colunas_antigas = set(df_antigo.columns)
        colunas_novas = set(df_novo.columns)

        colunas_adicionadas = colunas_novas - colunas_antigas
        colunas_removidas = colunas_antigas - colunas_novas

        if colunas_adicionadas:
            print(f"➕ Novas colunas detectadas em '{nome_tabela}': {sorted(colunas_adicionadas)}")
        if colunas_removidas:
            print(f"❌ Colunas removidas em '{nome_tabela}': {sorted(colunas_removidas)}")
        if not colunas_adicionadas and not colunas_removidas:
            print(f"✅ Estrutura da tabela '{nome_tabela}' permanece inalterada.")

        # Alinha colunas do novo DF com o antigo
        df_novo = alinhar_colunas(df_novo, df_antigo)

        # 🚨 Valida se número de colunas é o mesmo
        if set(df_novo.columns) != set(df_antigo.columns):
            print(f"⚠️ Estrutura de colunas diferente em '{nome_tabela}'. Recriando tabela.")
            conexao.execute(f"DROP TABLE IF EXISTS {nome_tabela}")
            conexao.register("df_temp", df_novo)
            conexao.execute(f'CREATE TABLE {nome_tabela} AS SELECT * FROM df_temp')
            conexao.unregister("df_temp")
            return
        
    except Exception as e:
        print(f"⚠️ Tabela '{nome_tabela}' não encontrada. Criando do zero. Detalhes: {e}")
        conexao.register("df_temp", df_novo)
        conexao.execute(f'CREATE TABLE {nome_tabela} AS SELECT * FROM df_temp')
        conexao.unregister("df_temp")
        return

    # JOIN por Id
    df_merge = df_novo.merge(df_antigo[["Id", "LastModifiedDate"]], on="Id", how="left", suffixes=("", "_antigo"))

    # INSERIR NOVOS
    df_insert = df_merge[df_merge["LastModifiedDate_antigo"].isna()]
    if not df_insert.empty:
        print(f"➕ Inserindo {len(df_insert)} novos registros...")
        conexao.register("df_insert", df_insert[df_novo.columns])
        conexao.execute(f'INSERT INTO {nome_tabela} SELECT * FROM df_insert')
        conexao.unregister("df_insert")

    # ATUALIZAR MODIFICADOS
    df_update = df_merge[
        df_merge["LastModifiedDate_antigo"].notna() &
        (df_merge["LastModifiedDate"] > df_merge["LastModifiedDate_antigo"])
    ]
    if not df_update.empty:
        print(f"♻️ Atualizando {len(df_update)} registros modificados...")

        id_lista = tuple(df_update["Id"])
        historico = conexao.execute(f"SELECT * FROM {nome_tabela} WHERE Id IN {id_lista}").df()
        historico["data_inclusao_bd"] = now_str

        # Alinha backup com df_novo
        historico = alinhar_colunas(historico, df_novo)

        conexao.register("df_hist", historico)

        # Garante que a tabela _hist_update existe e tem a estrutura compatível
        try:
            df_hist_existente = conexao.execute(f"SELECT * FROM {nome_tabela}_hist_update LIMIT 1").df()
            historico = alinhar_colunas(historico, df_hist_existente)
            tabela_hist_existe = True
        except:
            print(f"⚠️ Tabela '{nome_tabela}_hist_update' não encontrada. Será criada.")
            tabela_hist_existe = False

        # Cria a estrutura com um nome temporário e depois insere
        if not tabela_hist_existe:
            conexao.register("df_hist_temp", historico)
            conexao.execute(f'CREATE TABLE {nome_tabela}_hist_update AS SELECT * FROM df_hist_temp WHERE 1=0')
            conexao.unregister("df_hist_temp")

        # Alinha novamente (defensivo)
        cols_hist = conexao.execute(f"SELECT * FROM {nome_tabela}_hist_update LIMIT 1").df().columns.tolist()
        historico = historico.reindex(columns=cols_hist, fill_value="")

    # Agora registra e insere com nome compatível
        conexao.register("df_hist", historico)
        conexao.execute(f'INSERT INTO {nome_tabela}_hist_update SELECT * FROM df_hist')
        conexao.unregister("df_hist")

        conexao.execute(f"DELETE FROM {nome_tabela} WHERE Id IN {id_lista}")
        conexao.register("df_update", df_update[df_novo.columns])
        conexao.execute(f'INSERT INTO {nome_tabela} SELECT * FROM df_update')
        conexao.unregister("df_update")

#%%