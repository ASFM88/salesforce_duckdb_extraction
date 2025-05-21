# 🔄 Consulta de Dados Salesforce com Armazenamento Local em Camadas

Este projeto realiza a extração de dados do Salesforce utilizando a biblioteca `simple_salesforce`, e armazena os dados localmente em **camadas** usando o banco de dados **DuckDB**. A estrutura segue boas práticas de arquitetura de dados para ambientes de ETL/ELT.

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![DuckDB](https://img.shields.io/badge/DuckDB-embedded-lightgrey)
![Salesforce](https://img.shields.io/badge/Salesforce-API--v59-00A1E0)

---

## 📁 Estrutura do Projeto

```
.
├── raw_builder.py                  # Extrai dados brutos do Salesforce e salva em RAW (.duckdb)
├── main.py                         # Transformação e carregamento para camada STAGE (tipagem e limpeza)
├── trusted_builder.py              # Transformação e carregamento para camada TRUSTED (modelagem final)
├── gitignore                       # Arquivos que devem ser ignorados.
├── requirements.txt
├── README.md
├── utils/
│   ├── transform_utils.py          # Funções auxiliares para tratamento
│   ├── sf_utils.py                 # Funções auxiliares de integração com Salesforce
│   └── db_utils.py                 # Funções para salvar e carregar dados do DuckDB e SQLite
├── tools/
│   └──inspector.py                 # Explora tabelas e dados salvos localmente
├── db/
│   ├── raw_salesforce.duckdb       # Camada RAW: dados brutos extraídos
│   ├── stage_salesforce.duckdb     # Camada STAGE: dados levemente tratados
│   └── trusted_salesforce.duckdb   # Camada TRUSTED: dados prontos para análise

```

---

## 🚀 Como usar

### 1. Extrair dados do Salesforce → camada RAW

```bash
python raw_builder.py
```

- Usa `simple_salesforce` para autenticação e extração
- Salva objetos do Salesforce em `db/raw_salesforce.duckdb`

---

### 2. Gerar camada TRUSTED a partir da STAGE

```bash
python trusted_builder.py
```

- Lê as tabelas da `stage_salesforce.duckdb`
- Padroniza nomes de colunas (`snake_case`)
- Mantém apenas os campos relevantes por tabela
- Salva resultado final em `trusted_salesforce.duckdb`
- Escapa nomes reservados (ex: `order`) com aspas

---

### 3. Inspecionar as camadas e tabelas disponíveis

```bash
python inspector.py
```

- Lista as tabelas presentes nas camadas RAW, STAGE e TRUSTED
- Mostra quantidade de colunas e registros por tabela
- Ajuda a validar o pipeline e depurar inconsistências

---

## ✅ Transformações aplicadas

As transformações são aplicadas com suporte do módulo `utils/transform_utils.py`, contendo funções como:

- `padronizar_colunas()` → minúsculas, snake_case, remove caracteres especiais
- `manter_colunas()` → mantém apenas campos desejados por tabela (ignora faltantes)

---

## 🔐 Segurança

- As credenciais do Salesforce são armazenadas com `keyring`, fora do código-fonte.
- Arquivos `.db`, `.duckdb` e `.csv` devem ser ignorados via `.gitignore`.

---

📌 Próximos passos (em desenvolvimento)
- Criar backup do `stage_salesforce.duckdb` no SQLite.
- Adicionar novas funções para tratamento dos dados no módulo `utils/transform_utils.py`
- Inclusão atualização incremental do `raw_salesforce.duckdb`

---

## 🙋‍♂️ Contribuições

Sinta-se à vontade para sugerir melhorias, modularizar mais ainda o projeto, ou adaptar para outras fontes (ex: HubSpot, SAP, Google Sheets).

---