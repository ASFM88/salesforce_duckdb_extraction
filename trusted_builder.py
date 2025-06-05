#%%
import duckdb
import sqlite3
import os
from utils import transform_utils as tu

STAGE_DB = "db/stage_salesforce.duckdb"
TRUSTED_DB = "db/trusted_salesforce.duckdb"

TABELAS = [
    "recordtype", "user", "account", "contact", "cultura", "culturacliente", "endereco", "cidade",
    "subregiao", "order", "orderitem", "vendedores", "tabela_de_comissao", "tipo_negociacao",
    "unidade", "vencimento_pedido", "pagamento", "product2", "pricebook2",
    "top", "previsao_entrega_produto", "clientefinalentrega", "frete", "territorio", "userterritorio"
]

CAMPOS_POR_TABELA = {
    "recordtype": ["id", "name", "description", "sobjecttype", "isactive", "data_inclusao_bd"],
    "user": ["id", "name", "isactive", "title", "companyname", "email", "phone", "mobilephone", 
             "address", "createdbyid", "lastmodifiedbyid", "data_inclusao_bd"],
    "account": ["id", "name", "raizdocumento__c", "creditoliberado__c", "valor_de_cr_dito_exposto__c", 
                "phone", "telefone_do_contato__c", "grupocliente__c", "segmenta_o__c", 
                "clientenegativado__c", "recordtypeid", "ownerid", "createdbyid", "lastmodifiedbyid", "data_inclusao_bd"],
    "contact": ["id", "name", "accountid", "cpf__c", "phone", "email", "departamento__c", "createdbyid", "lastmodifiedbyid", "data_inclusao_bd"],
    "cultura": ["id", "name", "cliente__c", "cultura__c", "hectare__c", 
                "dosagem__c", "potencial_de_consumo_ton__c", "createdbyid", "lastmodifiedbyid", "data_inclusao_bd"],
    "culturacliente": ["id", "name", "cliente__c", "cultura__c", "lastmodifiedbyid", "data_inclusao_bd"],
    "endereco": ["id", "conta__c", "name", "emailcontato__c", "emailparaenvionfe__c", 
                 "cnpjcpf__c", "inscricaoestadual__c", "statussuframa__c", "inscricaosuframa__c", 
                 "roteiroentrega__c", "logradouro__c", "numero__c", "cidade__c", "uf__c", "bairro__c", 
                 "cep__c", "complemento__c", "status__c", "tipoendereco__c", "codigosap__c", 
                 "statusintegracao__c", "createdbyid", "lastmodifiedbyid", "data_inclusao_bd"],
    "cidade": ["id", "name", "codigo_ibge__c", "uf__c", "estado__c", "pais__c", 
               "sigla_do_estado__c", "codigo_externo__c", "createdbyid", "lastmodifiedbyid", "data_inclusao_bd"],
    "subregiao": ["id", "name", "cidade__c", "status__c", "codigo_externo__c", "createdbyid", "lastmodifiedbyid", "data_inclusao_bd"],
    "order": ["id", "numeropedido__c", "ordemvenda__c", "accountid", "endereco__c", "vendedores__c", 
              "contratosubstituido__c", "justificativa_margem__c", "proposta__c", "versao__c", 
              "motivosubstituicaocontrato__c", "parentid__c", "condicao_pagamento__c", "observacaonfcontrato__c", 
              "status", "unidade_faturamento__c", "tipo_de_negociacao__c", "currencyisocode", 
              "taxa_dolar_do_catalogo__c", "data_de_negocia_o__c", "margemsugerida__c", 
              "margem_do_contrato_usd__c", "desvio_da_margem_usd__c", "volume_toneladas__c", 
              "quantidade_faturada__c", "saldo_quantidade__c", "valorpedido__c", "valor_faturado__c", 
              "saldo_financeiro__c", "valorpagopedido__c", "saldo_de_pagamento__c", "diretor__c", 
              "gerentenacionalvenda__c", "gerente__c", "supervisor__c", "diretoria__c", "gerencianacionalvenda__c", 
              "gerencia__c", "id_territorio__c", "territorio__c", "ownerid", "effectivedate", "createdbyid", "lastmodifiedbyid", "data_inclusao_bd"],
    "orderitem": ["id", "orderid", "cultura__c", "top__c", "frete__c", "status__c", "statusproduto__c", 
                  "ordemcompracliente__c", "seqordemcompracliente__c", "unidadefaturamento__c", "quantity", 
                  "quantidade_editada__c", "quantidade_faturada__c", "saldo_quantidade__c", "totalprice", 
                  "valor_editado__c", "valor_faturado__c", "saldo_financeiro__c", "precounitariosugerido__c", 
                  "margem_sugerida__c", "custo_unit__c", "unitprice", "valortotaljuros__c", "valor_impostos__c", 
                  "valorfretetotal__c", "valorbasecomissao__c", "valor_sugerido_total__c", 
                  "valor_unitario_de_desconto__c", "porcentagem_segmentacao__c", "margemsugerida__c", 
                  "margem_venda_usd__c", "desvio_da_margem__c", "product2id", "embalagem_produto__c", 
                  "especificacao_produto__c", "liner__c", "data_entrega_inicial__c", "data_entrega_final__c", 
                  "tipo_de_entrega__c", "unidade_de_producao__c", "tipo_de_comissao__c", 
                  "porcen_valor_negociado_comissao__c", "indicepagamentocomissao__c", 
                  "provisionamento_de_pagamento__c", "valor_negociado_comissao__c", "motivo_do_cancelamento__c", 
                  "contratosubstituto__c", "data_hora_cancelamento__c", "observacaocancelamento__c", 
                  "quantidade__c", "createdbyid", "lastmodifiedbyid", "data_inclusao_bd"],
    "vendedores": ["id", "name", "cnpjcpf__c", "tipo__c", "usuario__c", 
                   "unidade_de_negocio__c", "status__c", "telefone__c", 
                   "tabelacomissao__c", "email__c", "data_de_inicio__c", "data_de_fim__c", 
                   "codigo_externo__c", "createdbyid", "lastmodifiedbyid", "data_inclusao_bd"],
    "tabela_de_comissao": ["id", "name", "valor_de_desconto_de__c", "valor_de_desconto_ate__c", 
                           "porcentagem_de_comissao__c", "status__c", "tipotabela__c", 
                           "vendedores__c", "createdbyid", "lastmodifiedbyid", "data_inclusao_bd"],
    "tipo_negociacao": ["id", "name", "parcelas__c", "currencyisocode", "prazo__c", 
                        "totalprazo__c", "tipo__c", "status__c", "observacao__c", 
                        "codigo_externo__c", "recordtypeid", "createdbyid", "lastmodifiedbyid", "data_inclusao_bd"],
    "unidade": ["id", "name", "status__c", "nome_resumido__c", "tipo__c", "tipo_entrega__c", "tipo_unidade__c", 
                "currencyisocode", "raz_o_social__c", "cnpj__c", "inscricao_estadual__c", "cidade__c", 
                "endereco__c", "capacidade_diaria__c", "codigo_externo__c", "codigosap__c", "recordtypeid", 
                "createdbyid", "lastmodifiedbyid", "data_inclusao_bd"],
    "vencimento_pedido": ["id", "name", "pedido__c", "valor__c", "statuspagamento__c", "currencyisocode", 
                          "valor_pago__c", "saldodevedor__c", "status__c", "createdbyid", "lastmodifiedbyid", "data_inclusao_bd"],
    "pagamento": ["id", "name", "cliente__c", "tipo_vencimento__c", "data_hora_recebimento__c", 
                  "data_vinculo__c", "ptax_recebimento__c", "valor_adiantamento__c", "vencimento_pedido__c", 
                  "currencyisocode", "numero_unico_financeiro_adiantamento__c", "createdbyid", 
                  "pedido_de_venda__c", "lastmodifiedbyid", "data_inclusao_bd"],
    "product2": ["id", "name", "productcode", "embalagem__c", "codigo_externo__c", "codigoembsap__c", 
                 "tipo_de_produto__c", "isactive", "naturezafisica__c", "nomegrupo__c", "description", 
                 "premium__c", "recordtypeid", "createdbyid", "lastmodifiedbyid", "data_inclusao_bd"],
    "pricebook2": ["id", "name", "description", "unidade_de_faturamento__c", "vigor__c", 
                   "data_inicial_para_entrega__c", "data_final_para_entrega__c", 
                   "codigo_externo__c", "createdbyid", "lastmodifiedbyid", "data_inclusao_bd"],
    "proposta": ["id", "cliente__c", "grupocredito__c", "operacao__c", "vigencia__c", "datarevisao__c",
                 "isactive", "name", "aprovador_final__c", "dataaprovacao__c", "rating__c", "limite_aprovado__c",
                 "limite_liberado__c", "saldo_limite_aprovado__c", "saldodisponivel__c", "valorgarantido__c",
                 "limite_faturado__c", "limite_vencido__c", "exposto__c", "createdbyid", 
                 "lastmodifiedbyid", "data_inclusao_bd"],
    "top": ["id", "name", "status__c", "comentarios__c", "tipo_de_operacao__c", "frete__c", 
            "faturamento_antecipado__c", "produtos_revenda__c", "gera_financeiro__c", 
            "unidade_produtora__c", "cidade_entrega__c", "suframa__c", "createdbyid", "lastmodifiedbyid", "data_inclusao_bd"],
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
                                 "valormes23__c", "valormes24__c", "lastmodifiedbyid", "data_inclusao_bd"],
    "clientefinalentrega": ["id", "name", "previsaoentregaproduto__c", 
                            "produtocontrato__c", "conta__c", "endereco__c", 
                            "enderecofaturamento__c", "datainicialentrega__c", 
                            "datafinalentrega__c", "status__c", "dataexecucao__c", 
                            "volume_a_entregar__c", "saldo__c", "createdbyid", "data_inclusao_bd"],
    "frete": ["id", "name", "data_vigor__c", "datafinal__c", "cidade_origem__c", "cidade_destino__c", 
              "sub_regiao_destino__c", "valormes1__c", "valormes2__c", "valormes3__c", "valormes4__c", 
              "valormes5__c", "valormes6__c", "valormes7__c", "valormes8__c", "valormes9__c", "valormes10__c", 
              "valormes11__c", "valormes12__c", "valormes13__c", "valormes14__c", "valormes15__c", "valormes16__c", 
              "valormes17__c", "valormes18__c", "valormes19__c", "valormes20__c", "valormes21__c", "valormes22__c", 
              "valormes23__c", "valormes24__c", "createdbyid", "lastmodifiedbyid", "data_inclusao_bd"],
    "territorio": ["id", "name", "developername", "codigo_do_territorio__c", "createdbyid", "lastmodifiedbyid", "data_inclusao_bd"],
    "userterritorio": ["id", "userid", "territory2id", "lastmodifiedbyid", "data_inclusao_bd"]
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

#%%
