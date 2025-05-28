# -*- coding: utf-8 -*-
import duckdb
import os

TRUSTED_DB_PATH = "db/trusted_salesforce.duckdb"

# Dicionário com tabelas finais e suas queries
TABELAS_FINAIS = {
    "order_final": """
        SELECT 
            a.Id,
            a.numeropedido__c as OrderNumber,
            a.accountid,
            b.name as NomeCliente,
            b.raizdocumento__c as RaizDocumento,
            c.cnpjcpf__c as CNPJCPF,
            c.name as NomeEndereco,
            d.name as NomeVendedor,
            a.contratosubstituido__c as ContratoSubstituido,
            a.justificativa_margem__c as JustificativaMargem,
            a.motivosubstituicaocontrato__c as MotivoSubstituicaoContrato,
            a.parentid__c as ContratoMae,
            a.condicao_pagamento__c as CondicaoPagamento,
            a.observacaonfcontrato__c as ObservacaoNFContrato,
            a.status as StatusContrato,
            f.name as UnidadeFaturamento,
            f.RecordTypeName as RegistroUnidade,
            g.name as TipoVencimento,
            a.currencyisocode as OrderCurrency,
            a.taxa_dolar_do_catalogo__c as Cambio,
            a.data_de_negocia_o__c as DataNegociacao,
            a.effectivedate as DataInicioContrato,
            a.margemsugerida__c as MargemSugeridaUSD,
            a.margem_do_contrato_usd__c as MargemNegociadaUSD,
            a.desvio_da_margem_usd__c,
            a.volume_toneladas__c as QtdeNegociada,
            a.quantidade_faturada__c as QtdeFaturada,
            a.saldo_quantidade__c as SaldoContrato,
            a.valorpedido__c as ValorContrato,
            a.valor_faturado__c as ValorFaturado,
            a.saldo_financeiro__c as SaldoFinanceiro,
            a.valorpagopedido__c as ValorPagoContrato,
            a.saldo_de_pagamento__c as ValorReceber,
            h_vp.Name as VicePresidente,
            h_diretor.Name as Diretor,
            h_gerente.Name as Gerente,
            h_consultor.Name as Consultor,
            a.diretoria__c as VicePresidencia,
            a.gerencianacionalvenda__c as Diretoria,
            a.gerencia__c as Gerencia,
            a.territorio__c as Territorio,
            h_proprietario.name as ProprietarioContrato,
            a.data_inclusao_bd 
        FROM
            "order" a 
        LEFT JOIN account b ON a.accountid = b.id
        LEFT JOIN endereco c ON a.endereco__c = c.id
        LEFT JOIN vendedores d ON a.vendedores__c = d.id
        LEFT JOIN (
            SELECT a.*, b.name AS RecordTypeName 
            FROM unidade a 
            LEFT JOIN recordtype b ON a.recordtypeid = b.id
        ) f ON a.unidade_faturamento__c = f.id
        LEFT JOIN tipo_negociacao g ON a.tipo_de_negociacao__c = g.name
        LEFT JOIN "user" h_vp ON a.diretor__c = h_vp.id 
        LEFT JOIN "user" h_diretor ON a.gerentenacionalvenda__c = h_diretor.id
        LEFT JOIN "user" h_gerente ON a.gerente__c = h_gerente.id
        LEFT JOIN "user" h_consultor ON a.supervisor__c = h_consultor.id
        LEFT JOIN "user" h_proprietario ON a.ownerid = h_proprietario.id
    """
    # Futuras tabelas podem ser adicionadas aqui...
}

def construir_tabelas_finais(db_path=TRUSTED_DB_PATH):
    con = duckdb.connect(str(db_path))
    for nome_tabela, query in TABELAS_FINAIS.items():
        try:
            print(f"📦 Criando tabela final: {nome_tabela}")
            con.execute(f'CREATE OR REPLACE TABLE {nome_tabela} AS {query}')
            print(f"✅ {nome_tabela} criada com sucesso.\n")
        except Exception as e:
            print(f"❌ Erro ao criar '{nome_tabela}': {e}\n")
    con.close()

if __name__ == "__main__":
    construir_tabelas_finais()