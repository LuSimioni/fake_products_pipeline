# 🛒 E-Commerce Data Pipeline

Pipeline de dados end-to-end com dados de e-commerce público, construído para fins de aprendizado e portfólio pessoal.

## 🧰 Stack

| Camada | Tecnologia |
|---|---|
| Ingestão | Python + Fake Store API |
| Orquestração | Apache Airflow |
| Processamento | Apache Spark (PySpark) |
| Transformação | dbt Core |
| Data Warehouse | Snowflake |
| Containerização | Docker + Docker Compose |
| Versionamento | Git |
| IDE | VS Code |

---

## 🏗️ Arquitetura

```
[Fake Store API]
      │
      ▼
 (Airflow DAG)
      │
      ▼
[Bronze Layer — Raw]   ← dados brutos da API, sem transformação
      │
      ▼ PySpark
[Silver Layer — Clean] ← dados limpos, tipados e padronizados
      │
      ▼ dbt Core
[Gold Layer — Analytics] ← modelos analíticos prontos para consumo
      │
      ▼
[Snowflake Data Warehouse]
```

---

## 📁 Estrutura de Pastas

```
ecommerce-pipeline/
├── airflow/
│   ├── dags/
│   │   ├── ingest_dag.py          # DAG de ingestão da API
│   │   └── transform_dag.py       # DAG de transformação Spark + dbt
│   └── plugins/
├── spark/
│   └── jobs/
│       ├── bronze_to_silver.py    # Job PySpark Bronze → Silver
│       └── utils.py
├── dbt/
│   ├── models/
│   │   ├── staging/               # Modelos Silver → staging
│   │   └── marts/                 # Modelos Gold / analíticos
│   ├── dbt_project.yml
│   └── profiles.yml
├── ingestion/
│   └── api_client.py              # Client da Fake Store API
├── docker/
│   └── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Etapas do Projeto

### ✅ Etapa 1 — Setup do Ambiente
> _Preencha ao concluir esta etapa_

- [ ] Docker e Docker Compose instalados
- [ ] Conta Snowflake criada (trial gratuito)
- [ ] VS Code configurado com extensões (Python, dbt, Docker)
- [ ] Repositório Git inicializado
- [ ] Variáveis de ambiente configuradas (`.env`)

**O que eu fiz:**
```
# Adicione aqui suas anotações pessoais sobre esta etapa
```

---

### ⬜ Etapa 2 — Ingestão da Fake Store API
> _Preencha ao concluir esta etapa_

- [ ] Client Python criado (`ingestion/api_client.py`)
- [ ] Endpoints consumidos: `/products`, `/carts`, `/users`
- [ ] Dados salvos em JSON na camada Bronze (Snowflake Stage ou local)
- [ ] Geração de dados sintéticos para volume (simulação de pedidos)

**O que eu fiz:**
```
# Adicione aqui suas anotações pessoais sobre esta etapa
```

---

### ⬜ Etapa 3 — Orquestração com Airflow
> _Preencha ao concluir esta etapa_

- [ ] Airflow rodando via Docker Compose
- [ ] DAG `ingest_dag` criada e funcional
- [ ] DAG `transform_dag` criada e funcional
- [ ] Dependências entre tasks configuradas
- [ ] Agendamento definido (ex: diário)

**O que eu fiz:**
```
# Adicione aqui suas anotações pessoais sobre esta etapa
```

---

### ⬜ Etapa 4 — Processamento com PySpark (Bronze → Silver)
> _Preencha ao concluir esta etapa_

- [ ] Job PySpark `bronze_to_silver.py` criado
- [ ] Limpeza de dados: nulos, tipos, duplicatas
- [ ] Padronização de colunas (snake_case, datas ISO)
- [ ] Dados Silver carregados no Snowflake

**O que eu fiz:**
```
# Adicione aqui suas anotações pessoais sobre esta etapa
```

---

### ⬜ Etapa 5 — Transformação com dbt (Silver → Gold)
> _Preencha ao concluir esta etapa_

- [ ] dbt Core instalado e configurado
- [ ] `profiles.yml` apontando para Snowflake
- [ ] Modelos de staging criados
- [ ] Modelos analíticos (marts) criados:
  - [ ] `mart_sales` — vendas por período
  - [ ] `mart_products` — performance de produtos
  - [ ] `mart_customers` — comportamento de clientes
- [ ] `dbt run` e `dbt test` executados com sucesso

**O que eu fiz:**
```
# Adicione aqui suas anotações pessoais sobre esta etapa
```

---

### ⬜ Etapa 6 — Git e Boas Práticas
> _Preencha ao concluir esta etapa_

- [ ] `.gitignore` configurado (ignorar `.env`, credenciais, `__pycache__`)
- [ ] Commits organizados por etapa
- [ ] Branch strategy definida (ex: `main` + `dev`)
- [ ] README atualizado com prints ou resultados

**O que eu fiz:**
```
# Adicione aqui suas anotações pessoais sobre esta etapa
```

---

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz com base no `.env.example`:

```env
# Snowflake
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_DATABASE=ECOMMERCE_DB
SNOWFLAKE_SCHEMA=RAW
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_ROLE=SYSADMIN

# Airflow
AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW_UID=50000

# API
FAKESTORE_BASE_URL=https://fakestoreapi.com
```

---

## 📦 Como Rodar o Projeto

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/ecommerce-pipeline.git
cd ecommerce-pipeline

# 2. Configure o .env
cp .env.example .env
# edite o .env com suas credenciais

# 3. Suba os containers
docker-compose -f docker/docker-compose.yml up -d

# 4. Acesse o Airflow
# http://localhost:8080

# 5. Execute o dbt manualmente (opcional)
cd dbt
dbt run
dbt test
```

---

## 📊 Resultados / Prints

> _Adicione aqui prints do Airflow, Snowflake e outputs do dbt ao finalizar o projeto_

---

## 📚 Referências

- [Fake Store API](https://fakestoreapi.com/docs)
- [Apache Airflow Docs](https://airflow.apache.org/docs/)
- [dbt Core Docs](https://docs.getdbt.com/)
- [PySpark Docs](https://spark.apache.org/docs/latest/api/python/)
- [Snowflake Docs](https://docs.snowflake.com/)

---

## 👤 Autor

**Seu Nome**
[LinkedIn](#) | [GitHub](#)