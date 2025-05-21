# 🔄 Consulta de Dados Salesforce com Armazenamento Local em Camadas

Este projeto realiza a extração de dados do Salesforce utilizando a biblioteca `simple_salesforce`, e armazena os dados localmente em **camadas** usando o banco de dados **DuckDB**. A estrutura segue boas práticas de arquitetura de dados para ambientes de ETL/ELT.

---

## 📁 Estrutura do Projeto

```
.
├── raw_builder.py          # Extrai dados brutos do Salesforce e salva em RAW (.duckdb)
├── main.py                 # (Futuro) Transformação e carregamento para camada TRUSTED
├── sf_utils.py             # Funções auxiliares de integração com Salesforce
├── db_utils.py             # Funções para salvar e carregar dados do DuckDB e SQLite
├── inspector.py            # Explora tabelas e dados salvos localmente
├── requirements.txt
├── README.md
└── db/
    ├── raw_salesforce.duckdb      # Camada RAW: dados brutos do Salesforce
    ├── (stage_salesforce.duckdb)  # (Futuro) Dados parcialmente tratados
    └── (trusted_salesforce.duckdb) # (Futuro) Dados prontos para análise
```

---

## 🚀 Como usar

### 1. Extração dos dados RAW (todos os campos disponíveis)

```bash
python raw_builder.py
```

- Conecta-se ao Salesforce via `keyring`
- Usa `describe()` para consultar todos os campos de cada objeto
- Salva os dados crus em `db/raw_salesforce.duckdb`

---

## 🔍 Visualizar os dados com `inspector.py`

```bash
python inspector.py
```

- Lista todas as tabelas do banco
- Mostra estrutura de colunas e amostras de registros
- Funciona tanto para DuckDB quanto para SQLite

---

## 📌 Próximos passos (em desenvolvimento)

- Criar `stage_utils.py` para tratamento de tipos, limpeza e enriquecimento
- Refatorar `main.py` para carregar dados tratados na camada TRUSTED
- Exportar versão final para SQLite (somente a camada TRUSTED)

---

## 🔐 Segurança

- As credenciais do Salesforce são armazenadas com `keyring`, fora do código-fonte.
- Arquivos `.db`, `.duckdb` e `.csv` são ignorados no `.gitignore`.

---

## 🙋‍♂️ Contribuições

Sinta-se à vontade para sugerir melhorias, organizar scripts em camadas, ou adaptar para outro CRM.