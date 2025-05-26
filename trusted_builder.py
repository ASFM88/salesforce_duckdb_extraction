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
    "product2": ["id", "name", "productcode", "embalagem__c", "codigo_externo__c", "codigoembsap__c", 
                 "tipo_de_produto__c", "isactive", "naturezafisica__c", "nomegrupo__c", "description", 
                 "premium__c", "recordtypeid", "createdbyid"],
    "pricebook2": ["id", "name", "description", "unidade_de_faturamento__c", "vigor__c", 
                   "data_inicial_para_entrega__c", "data_final_para_entrega__c", 
                   "codigo_externo__c", "createdbyid"],
    "top": ["id", "name", "status__c", "comentarios__c", "tipo_de_operacao__c", "frete__c", 
            "faturamento_antecipado__c", "produtos_revenda__c", "gera_financeiro__c", 
            "unidade_produtora__c", "cidade_entrega__c", "suframa__c", "createdbyid"],
    "previsao_entrega_produto": ["id", "name", "hedge__c", "valorhedge__c", "diashedge__c", 
                                 "condicao_pagamento__c", "ultimadatainseta__c", "jurosdiario__c", 
                                 "vencimento_financeiro__c", "jurosantecipacao__c", "prazocontratodias__c", 
                                 "valortotaljuros__c", "tabelafrete__c", "valor_frete__c", 
                                 "valor_frete_total__c", "percentagemicms__c", "valorimpostos__c", 
                                 "clientefaturamento__c", "endereçofaturamento__c", "unidade_faturamento__c", 
                                 "top__c", "quantidade__c", "quantidade_editada__c", "quantidade_faturada__c", 
                                 "saldo__c", "valor_total__c", "valoreditado__c", "valorfaturado__c", 
                                 "saldofinanceiro__c", "valorunitariosugerido__c", "margemsugerida__c", 
                                 "custolistapreco__c", "margemnegociada__c", "valorbasepreco__c", 
                                 "base_de_pre_o_unit_rio__c", "valorunitarionegociado__c", "produto_pedido__c", 
                                 "name", "data__c", "cadencia__c", "enderecoentrega__c", "cliente_final__c", 
                                 "cidade_de_entrega__c", "sub_regiao_de_entrega__c", "roteiro__c", "novo_roteiro__c", 
                                 "observacoes__c", "observacoes_internas__c", "createdbyid", "data_vigor__c", 
                                 "datainiciofrete__c", "datafinalfrete__c", "valormes1__c", "valormes2__c", 
                                 "valormes3__c", "valormes4__c", "valormes5__c", "valormes6__c", "valormes7__c", 
                                 "valormes8__c", "valormes9__c", "valormes10__c","valormes11__c", "valormes12__c", 
                                 "valormes13__c", "valormes14__c", "valormes15__c", "valormes16__c", "valormes17__c", 
                                 "valormes18__c", "valormes19__c", "valormes20__c", "valormes21__c", "valormes22__c",
                                 "valormes23__c", "valormes24__c", ],
    "clientefinalentrega": ["id", "name", "previsaoentregaproduto__c", 
                            "produtocontrato__c", "conta__c", "endereco__c", 
                            "enderecofaturamento__c", "datainicialentrega__c", 
                            "datafinalentrega__c", "status__c", "dataexecucao__c", 
                            "volume_a_entregar__c", "saldo__c", "createdbyid"],
    "frete": ["id", "name", "data_vigor__c", "datafinal__c", "cidade_origem__c", "cidade_destino__c", 
              "sub_regiao_destino__c", "valormes1__c", "valormes2__c", "valormes3__c", "valormes4__c", 
              "valormes5__c", "valormes6__c", "valormes7__c", "valormes8__c", "valormes9__c", "valormes10__c", 
              "valormes11__c", "valormes12__c", "valormes13__c", "valormes14__c", "valormes15__c", "valormes16__c", 
              "valormes17__c", "valormes18__c", "valormes19__c", "valormes20__c", "valormes21__c", "valormes22__c", 
              "valormes23__c", "valormes24__c", "createdbyid"]
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
SQLITE_TRUSTED_PATH = "db/trusted_salesforce.sqlite"

# Remove o SQLite anterior (opcional: sobrescrever)
if os.path.exists(SQLITE_TRUSTED_PATH):
    os.remove(SQLITE_TRUSTED_PATH)

# Conexão com SQLite
sqlite_conn = sqlite3.connect(SQLITE_TRUSTED_PATH)

print("\n🟠 Salvando dados da camada TRUSTED também no SQLite...")
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
