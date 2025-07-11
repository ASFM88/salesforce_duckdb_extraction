# %%
import duckdb
import pandas as pd
import os

# Cria pasta de saída se não existir
os.makedirs("db", exist_ok=True)

# Conexões com os bancos RAW e STAGE
conn_raw = duckdb.connect("db/raw_salesforce.duckdb")
conn_stage = duckdb.connect("db/stage_salesforce.duckdb")

# Lista de tabelas RAW para processar
objetos_raw = {
    "raw_recordtype": "stage_recordtype",
    "raw_user": "stage_user",
    "raw_account": "stage_account",
    "raw_contact": "stage_contact",
    "raw_cultura": "stage_cultura",
    "raw_culturacliente": "stage_culturacliente",
    "raw_endereco": "stage_endereco",
    "raw_cidade": "stage_cidade",
    "raw_subregiao": "stage_subregiao",
    "raw_order": "stage_order",
    "raw_orderitem": "stage_orderitem",
    "raw_vendedores": "stage_vendedores",
    "raw_tipo_comissao": "stage_tabela_de_comissao",
    "raw_tipo_vencimento": "stage_tipo_negociacao",
    "raw_unidade": "stage_unidade",
    "raw_vencimento_contrato": "stage_vencimento_pedido",
    "raw_pagamento": "stage_pagamento",
    "raw_proposta": "stage_proposta",
    "raw_product": "stage_product2",
    "raw_pricebook": "stage_pricebook2",
    "raw_top": "stage_top",
    "raw_previsao_entrega": "stage_previsao_entrega_produto",
    "raw_cliente_final": "stage_clientefinalentrega",
    "raw_frete": "stage_frete",
    "raw_territorio": "stage_territorio",
    "raw_userterritorio": "stage_userterritorio",
    "raw_notafiscal": "stage_notafiscal",
    "raw_item_notafiscal": "stage_item_notafiscal"
}

# Loop de transformação básica
for tabela_raw, tabela_stage in objetos_raw.items():
    try:
        df = conn_raw.execute(f'SELECT * FROM "{tabela_raw}"').fetchdf()

        # Exemplo de transformação mínima (expandido depois na camada trusted)
        df = df.fillna("")  # ou ajustes de tipo, normalizações, etc

        # Salva na camada STAGE
        conn_stage.execute(f'DROP TABLE IF EXISTS "{tabela_stage}"')
        conn_stage.execute(f'CREATE TABLE "{tabela_stage}" AS SELECT * FROM df')

        print(f"✅ {tabela_stage}: {len(df)} registros transformados e salvos.")
    except Exception as e:
        print(f"❌ Erro ao processar {tabela_raw} → {e}")

# Fecha conexões
conn_raw.close()
conn_stage.close()

print("✅ Transformação para camada STAGE concluída.")

# %%
