# 🔍 Consulta de Dados no Salesforce com Python

Este repositório contém um script em Python desenvolvido para consultar registros diretamente da API do Salesforce utilizando a biblioteca `simple-salesforce`.

---

## 📌 Objetivo

Automatizar a extração de dados do Salesforce (ex: contas, contatos, pedidos etc.), estruturando as informações em um `DataFrame` e exportando para CSV ou armazenando Banco DuckDB e SQLite, possibilitando análises locais ou integração com outras ferramentas.

---

## ⚙️ Tecnologias Utilizadas

- Python 3.12+
- [`simple-salesforce`](https://pypi.org/project/simple-salesforce/)
- `pandas` (manipulação de dados)
- `keyring` (armazenamento seguro de credenciais)
- `duckdb` (banco de dados local em arquivo único)
- `sqlite3` (banco de dados local em arquivo único)
- VSCode com Python Interactive / Preview (opcional)

---

## 🔐 Segurança das Credenciais

As credenciais de acesso à API do Salesforce são armazenadas com a biblioteca `keyring`, utilizando o cofre seguro do sistema operacional. Dessa forma:

- ❌ As credenciais **não ficam visíveis no código**
- ❌ Nenhum arquivo `.env` ou `.py` sensível é versionado
- ✅ Segurança adequada para uso pessoal e corporativo

> O arquivo `senhas.py` usado para cadastrar as credenciais está no `.gitignore` e **não deve ser enviado ao repositório.**

---

## ▶️ Como usar

### 1. Clone o repositório:
```bash
git clone https://github.com/ASFM88/teste_consulta_salesforce.git
cd teste_consulta_salesforce
```

### 2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### 3. Configure suas credenciais Salesforce:
Abra o Python interativamente ou crie um arquivo auxiliar com:

```python
import keyring

keyring.set_password("salesforce", "SF_USER", "seu_email@exemplo.com")
keyring.set_password("salesforce", "SF_PASS", "sua_senha")
keyring.set_password("salesforce", "SF_TOKEN", "seu_token_de_segurança")
```

### 4. Execute o script principal:
```bash
python main.py
```

### 5. Arquivo de saída CSV:
- O resultado será salvo como `teste_account_salesforce.csv` no diretório atual do projeto.

---

## 📁 Estrutura do Projeto

```
.
├── main.py              # Script principal de extração e gravação no banco
├── db_utils.py          # Função auxiliar para salvar DataFrame no DuckDB
├── sf_utils.py          # Funções auxiliares do Salesforce (SOQL, describe, paginação)
├── db/                  # Contém o banco local (dados_salesforce.duckdb)
├── .gitignore           # Arquivos ignorados no controle de versão
├── requirements.txt     # Bibliotecas necessárias
└── README.md            # Documentação do projeto
```

---

## 📌 Recursos Implementados

- 🔄 Paginação automática da API do Salesforce (sem limite de 2.000 registros).
- 💾 Exportação direta para CSV.
- 🔐 Armazenamento seguro de credenciais com `keyring`.
- 🧠 Uso interativo possível via VSCode com Python Preview ou Interactive Window.
- 🦆 Uso do DuckDB com múltiplas tabelas.
- 🧩 Uso do SQLite com múltiplas tabelas.
---

## 🔎 Sobre o banco DuckDB

- Armazenado como arquivo único (`.duckdb`)
- Portável entre máquinas
- SQL completo (joins, CTEs, filtros, etc.)
- O arquivo `.wal` (Write-Ahead Log) é criado temporariamente durante escritas e pode desaparecer após `conn.close()`

## 💾 Sobre o banco SQLite

- Armazenado como um único arquivo (`.db`)
- Altamente compatível com diversos sistemas e linguagens
- Ideal para aplicações locais e manipulação de dados leve a moderada
- Permite operações `CRUD` completas (`INSERT`, `UPDATE`, `DELETE`, `SELECT`)
- Pode ser acessado visualmente com ferramentas como [DB Browser for SQLite](https://sqlitebrowser.org)
- Não gera `.wal` por padrão, mas pode usar journal para controle de integridade em transações


## 🚀 Possíveis melhorias futuras

- Atualização incremental das tabelas DuckDB e SQLite.
- Automatização da atualização.

---

## 🙋‍♂️ Contribuições

Sugestões, melhorias e contribuições são bem-vindas. Basta abrir uma [issue](https://github.com/ASFM88/teste_consulta_salesforce/issues) ou enviar um pull request.

---