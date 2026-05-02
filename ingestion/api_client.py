
"""
api_client.py
Responsável por:
  1. Buscar dados da Fake Store API
  2. Gerar dados sintéticos para volume (simulando pedidos reais)
  3. Salvar os dados brutos no Snowflake (schema RAW)
"""

import os
import json
import requests
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import random
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

fake = Faker("pt_BR")
BASE_URL = os.getenv("FAKESTORE_BASE_URL", "https://fakestoreapi.com")

# ─── Conexão Snowflake ────────────────────────────────────────────────────────

def get_snowflake_conn():
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        role=os.getenv("SNOWFLAKE_ROLE"),
    )

# ─── Fetch da API ─────────────────────────────────────────────────────────────

def fetch_products():
    r = requests.get(f"{BASE_URL}/products", timeout=10)
    r.raise_for_status()
    return r.json()

def fetch_users():
    r = requests.get(f"{BASE_URL}/users", timeout=10)
    r.raise_for_status()
    return r.json()

def fetch_carts():
    r = requests.get(f"{BASE_URL}/carts", timeout=10)
    r.raise_for_status()
    return r.json()

# ─── Geração de dados sintéticos ─────────────────────────────────────────────

def generate_orders(products, users, n=500):
    """
    Simula n pedidos com base nos produtos e usuários reais da API.
    Isso dá volume suficiente para justificar o uso do Spark.
    """
    orders = []
    for i in range(n):
        product = random.choice(products)
        user    = random.choice(users)
        qty     = random.randint(1, 5)
        orders.append({
            "order_id":       i + 1,
            "user_id":        user["id"],
            "product_id":     product["id"],
            "product_title":  product["title"],
            "category":       product["category"],
            "unit_price":     product["price"],
            "quantity":       qty,
            "total_price":    round(product["price"] * qty, 2),
            "order_date":     (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
            "status":         random.choice(["completed", "pending", "cancelled", "refunded"]),
        })
    return orders

# ─── Carga no Snowflake ───────────────────────────────────────────────────────

def create_raw_tables(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS RAW.RAW_PRODUCTS (
            id            INT,
            title         STRING,
            price         FLOAT,
            category      STRING,
            description   STRING,
            rating_rate   FLOAT,
            rating_count  INT,
            loaded_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS RAW.RAW_USERS (
            id          INT,
            email       STRING,
            username    STRING,
            firstname   STRING,
            lastname    STRING,
            city        STRING,
            loaded_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS RAW.RAW_ORDERS (
            order_id      INT,
            user_id       INT,
            product_id    INT,
            product_title STRING,
            category      STRING,
            unit_price    FLOAT,
            quantity      INT,
            total_price   FLOAT,
            order_date    DATE,
            status        STRING,
            loaded_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.close()
    print("✅ Tabelas RAW criadas/verificadas.")

def load_products(conn, products):
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE RAW.RAW_PRODUCTS")
    for p in products:
        cur.execute("""
            INSERT INTO RAW.RAW_PRODUCTS
                (id, title, price, category, description, rating_rate, rating_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            p["id"], p["title"], p["price"], p["category"],
            p["description"], p["rating"]["rate"], p["rating"]["count"]
        ))
    cur.close()
    print(f"✅ {len(products)} produtos carregados em RAW.RAW_PRODUCTS")

def load_users(conn, users):
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE RAW.RAW_USERS")
    for u in users:
        cur.execute("""
            INSERT INTO RAW.RAW_USERS
                (id, email, username, firstname, lastname, city)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            u["id"], u["email"], u["username"],
            u["name"]["firstname"], u["name"]["lastname"],
            u["address"]["city"]
        ))
    cur.close()
    print(f"✅ {len(users)} usuários carregados em RAW.RAW_USERS")

def load_orders(conn, orders):
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE RAW.RAW_ORDERS")
    for o in orders:
        cur.execute("""
            INSERT INTO RAW.RAW_ORDERS
                (order_id, user_id, product_id, product_title, category,
                 unit_price, quantity, total_price, order_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            o["order_id"], o["user_id"], o["product_id"], o["product_title"],
            o["category"], o["unit_price"], o["quantity"],
            o["total_price"], o["order_date"], o["status"]
        ))
    cur.close()
    print(f"✅ {len(orders)} pedidos carregados em RAW.RAW_ORDERS")

# ─── Main ─────────────────────────────────────────────────────────────────────

def run():
    print("🔄 Iniciando ingestão...")

    # 1. Busca dados da API
    products = fetch_products()
    users    = fetch_users()
    carts    = fetch_carts()
    orders   = generate_orders(products, users, n=500)

    print(f"📦 Produtos: {len(products)} | Usuários: {len(users)} | Pedidos gerados: {len(orders)}")

    # 2. Conecta no Snowflake
    conn = get_snowflake_conn()

    # 3. Cria tabelas e carrega dados
    create_raw_tables(conn)
    load_products(conn, products)
    load_users(conn, users)
    load_orders(conn, orders)

    conn.close()
    print("✅ Ingestão concluída com sucesso!")

if __name__ == "__main__":
    run()