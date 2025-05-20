# 🔍 Consulta de Dados no Salesforce com Python

Este repositório contém um script em Python desenvolvido para consultar registros diretamente da API do Salesforce utilizando a biblioteca `simple-salesforce`.

---

## 📌 Objetivo

Automatizar a extração de dados do Salesforce (ex: contas, contatos, pedidos etc.), estruturando as informações em um `DataFrame` e exportando para CSV, possibilitando análises locais ou integração com outras ferramentas.

---

## ⚙️ Tecnologias Utilizadas

- Python 3.12+
- [`simple-salesforce`](https://pypi.org/project/simple-salesforce/)
- `requests`
- `pandas`
- `keyring` (armazenamento seguro de credenciais)
- Visual Studio Code com suporte a Python Interactive (`# %%`)

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

### 5. Arquivo de saída:
- O resultado será salvo como `accounts_salesforce.csv` no diretório atual do projeto.

---

## 📁 Estrutura do Projeto

```
.
├── main.py              # Script principal para consulta e exportação
├── .gitignore           # Ignora CSVs, credenciais e arquivos temporários
├── README.md            # Este arquivo
└── requirements.txt     # Dependências do projeto
```

---

## 📌 Recursos Implementados

- 🔄 Paginação automática da API do Salesforce (sem limite de 2.000 registros).
- 💾 Exportação direta para CSV.
- 🔐 Armazenamento seguro de credenciais com `keyring`.
- 🧠 Uso interativo possível via VSCode com Python Preview ou Interactive Window.

---

## 🚀 Possíveis melhorias futuras

- Consulta dinâmica de diferentes objetos Salesforce.
- Exportação para banco de dados.
- Interface gráfica ou CLI para facilitar uso.

---

## 🙋‍♂️ Contribuições

Sugestões, melhorias e contribuições são bem-vindas. Basta abrir uma [issue](https://github.com/ASFM88/teste_consulta_salesforce/issues) ou enviar um pull request.

---