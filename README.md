## 🔍 Consulta de Dados no Salesforce com Python

Este repositório contém um script em Python desenvolvido para consultar registros diretamente da API do Salesforce utilizando a biblioteca `simple-salesforce`.

📌 Objetivo

Automatizar a extração de dados do Salesforce (ex: contas, contatos, pedidos etc.), estruturando as informações em um `DataFrame` e exportando para CSV, possibilitando análises locais ou integração com outras ferramentas.

⚙️ Tecnologias Utilizadas

- Python 3.12+
- [simple-salesforce](https://pypi.org/project/simple-salesforce/)
- requests
- pandas
- keyring (armazenamento seguro de credenciais)
- VSCode (com suporte a Python Interactive / Jupyter)

## 🔐 Segurança

As credenciais de acesso à API do Salesforce são armazenadas localmente e de forma segura com a biblioteca `keyring`, evitando exposição de informações sensíveis no código ou em arquivos do repositório.

> O arquivo `senhas.py` usado para configuração inicial está listado no `.gitignore` e **não deve ser versionado**.

## 📥 Como usar

1. Clone este repositório:
   ```bash
   git clone https://github.com/ASFM88/teste_consulta_salesforce.git

2. # 🔍 Consulta de Dados no Salesforce com Python

Este repositório contém um script em Python desenvolvido para consultar registros diretamente da API do Salesforce utilizando a biblioteca `simple-salesforce`.

## 📌 Objetivo

Automatizar a extração de dados do Salesforce (ex: contas, contatos, pedidos etc.), estruturando as informações em um `DataFrame` e exportando para CSV, possibilitando análises locais ou integração com outras ferramentas.

## ⚙️ Tecnologias Utilizadas

- Python 3.12+
- [simple-salesforce](https://pypi.org/project/simple-salesforce/)
- requests
- pandas
- keyring (armazenamento seguro de credenciais)
- VSCode (com suporte a Python Interactive / Jupyter)

## 🔐 Segurança

As credenciais de acesso à API do Salesforce são armazenadas localmente e de forma segura com a biblioteca `keyring`, evitando exposição de informações sensíveis no código ou em arquivos do repositório.

> O arquivo `senhas.py` usado para configuração inicial está listado no `.gitignore` e **não deve ser versionado**.

## 📥 Como usar

1. Clone este repositório:
   ```bash
   git clone https://github.com/ASFM88/teste_consulta_salesforce.git

2. Instale as dependências:

import keyring
keyring.set_password("salesforce", "SF_USER", "seu_email@exemplo.com")
keyring.set_password("salesforce", "SF_PASS", "sua_senha")
keyring.set_password("salesforce", "SF_TOKEN", "seu_token_de_segurança")

3. Configure suas credenciais (uma vez só):

import keyring
keyring.set_password("salesforce", "SF_USER", "seu_email@exemplo.com")
keyring.set_password("salesforce", "SF_PASS", "sua_senha")
keyring.set_password("salesforce", "SF_TOKEN", "seu_token_de_segurança")

4. Execute o script principal:

python main.py

5. O resultado será exportado como accounts_salesforce.csv no diretório do projeto.

📁 Estrutura do projeto
.
├── main.py              # Script principal para consulta e exportação
├── .gitignore           # Arquivos ignorados no Git (ex: senhas.py, .csv)
├── README.md            # Este arquivo

📌 Observações
- O script realiza a paginação automática da API do Salesforce para contornar a limitação de 2.000 registros por consulta.
- A exportação em CSV é feita com base no DataFrame final.
- Compatível com execução em células # %% no VSCode para uso interativo.

🧪 Próximos passos (ideias)
- Permitir consulta dinâmica de diferentes objetos (ex: Contact, Opportunity).
- Exportação para banco de dados (SQLite, PostgreSQL).
- Interface para usuários não técnicos.
