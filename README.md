# 🔄 Consulta de Dados Salesforce com Armazenamento Local em Camadas

Este projeto realiza a extração de dados do Salesforce utilizando a biblioteca `simple_salesforce`, e armazena os dados localmente em **camadas** usando o banco de dados **DuckDB** e **SQLite**. A estrutura segue boas práticas de arquitetura de dados para ambientes de ETL/ELT.

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Salesforce](https://img.shields.io/badge/Salesforce-API--v59-00A1E0)
![DuckDB](https://img.shields.io/badge/DuckDB-embedded-lightgrey)
![SQLite](https://img.shields.io/badge/SQLite-3.x-blue)


---

## 📁 Estrutura do Projeto

```
.
├── run_pipeline.py                 # Orquestra execução completa: RAW ➝ STAGE ➝ TRUSTED
├── raw_builder.py                  # Extrai dados brutos do Salesforce e salva em RAW (.duckdb)
├── stage_builder.py                # Transformação e carregamento para camada STAGE (tipagem e limpeza)
├── trusted_builder.py              # Transformação e carregamento para camada TRUSTED (modelagem final)
├── export_sqlite.py                # Exporta camadas para bancos SQLite
├── gitignore                       # Arquivos que devem ser ignorados.
├── requirements.txt
├── README.md
├── utils/
│   ├── transform_utils.py          # Funções auxiliares para tratamento
│   ├── sf_utils.py                 # Funções auxiliares de integração com Salesforce
│   └── db_utils.py                 # Funções para salvar e carregar dados do DuckDB e SQLite
│   └── update_handler.py           # Funções para atualização incremental do arquivo
├── tools/
│   └──inspector.py                 # Explora tabelas e dados salvos localmente
└── db/
    ├── raw_salesforce.duckdb       # Camada RAW: dados brutos extraídos
    ├── stage_salesforce.duckdb     # Camada STAGE: dados levemente tratados
    └── trusted_salesforce.duckdb   # Camada TRUSTED: dados prontos para análise

```

---

## 🚀 Como executar o pipeline completo

```bash
python run_pipeline.py
```

Este comando executa as três camadas em sequência:

1. `raw_builder.py`     → coleta dados do Salesforce  
2. `stage_builder.py`   → prepara os dados  
3. `trusted_builder.py` → aplica transformações finais
4. `export_sqlite.py`   → salva os bancos no SQLite

---

## 🛠️ Execução individual (opcional)

Você pode executar cada etapa separadamente, se desejar:

```bash
python raw_builder.py
python stage_builder.py
python trusted_builder.py
python export_sqlite.py
```

---

## 🔎 Inspecionar o banco de dados

```bash
python inspector.py
```

- Lista as tabelas presentes nas camadas RAW, STAGE e TRUSTED
- Mostra número de colunas e registros
- Ajuda a validar o pipeline e depurar inconsistências

---

## ✅ Transformações aplicadas

A camada de transformação utiliza funções localizadas em `utils/`, com destaque para os seguintes módulos:

- `transform_utils.py`  
  - `padronizar_colunas()` → converte nomes para minúsculas e snake_case
  - `manter_colunas()` → mantém apenas os campos relevantes por tabela

- `sf_utils.py`  
  - Funções auxiliares para autenticação e comunicação com a API do Salesforce

- `db_utils.py`  
  - Funções de leitura e escrita em DuckDB e SQLite, criação de pastas, e controle de arquivos

- `update_handler.py`  
  - Função `atualiza_incremental()` para atualização de registros com base em `Id` e `LastModifiedDate`
  - Criação da coluna `data_inclusao_bd`
  - Armazenamento de versões antigas dos registros alterados nas tabelas `*_hist_update`

---

## 🔐 Segurança

- As credenciais do Salesforce são armazenadas com `keyring`, fora do código-fonte.
- Arquivos `.db`, `.duckdb` e `.csv` devem ser ignorados via `.gitignore`.

---

📌 Próximos passos
- Criar coluna de comparação automática nos `_hist_update` para identificar os campos alterados
- Modularizar criação de relatórios e visualizações com base nos dados da camada TRUSTED
- Orquestrar o fluxo de execução (RAW ➝ STAGE ➝ TRUSTED) com agendamento diário utilizando ferramentas como **Apache Airflow** ou **crontab**
- Gerar monitoramento e logs para controle de falhas e validação do pipeline em produção

---

## 🙋‍♂️ Contribuições

Sinta-se à vontade para sugerir melhorias, modularizar mais ainda o projeto, ou adaptar para outras fontes (ex: HubSpot, SAP, Google Sheets).

---