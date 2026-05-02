
"""
bronze_to_silver.py
Lê as tabelas RAW do Snowflake, limpa e padroniza,
e salva no schema STAGING (Silver).
"""

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, lower, to_date, when, round as spark_round
from dotenv import load_dotenv

load_dotenv()

SNOWFLAKE_OPTIONS = {
    "sfURL":       f"{os.getenv('SNOWFLAKE_ACCOUNT')}.snowflakecomputing.com",
    "sfUser":      os.getenv("SNOWFLAKE_USER"),
    "sfPassword":  os.getenv("SNOWFLAKE_PASSWORD"),
    "sfDatabase":  os.getenv("SNOWFLAKE_DATABASE"),
    "sfWarehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "sfRole":      os.getenv("SNOWFLAKE_ROLE"),
}

def get_spark():
    return (SparkSession.builder
        .appName("bronze_to_silver")
        .config("spark.jars.packages",
                "net.snowflake:snowflake-jdbc:3.13.30,"
                "net.snowflake:spark-snowflake_2.12:2.12.0-spark_3.4")
        .getOrCreate())

def read_table(spark, schema, table):
    return (spark.read.format("net.snowflake.spark.snowflake")
        .options(**SNOWFLAKE_OPTIONS)
        .option("sfSchema", schema)
        .option("dbtable", table)
        .load())

def write_table(df, schema, table):
    (df.write.format("net.snowflake.spark.snowflake")
        .options(**SNOWFLAKE_OPTIONS)
        .option("sfSchema", schema)
        .option("dbtable", table)
        .mode("overwrite")
        .save())

def clean_products(spark):
    df = read_table(spark, "RAW", "RAW_PRODUCTS")
    clean = (df
        .dropDuplicates(["ID"])
        .dropna(subset=["ID", "TITLE", "PRICE"])
        .withColumn("TITLE",    trim(col("TITLE")))
        .withColumn("CATEGORY", lower(trim(col("CATEGORY"))))
        .withColumn("PRICE",    spark_round(col("PRICE"), 2))
        .filter(col("PRICE") > 0)
    )
    write_table(clean, "STAGING", "STG_PRODUCTS")
    print(f"✅ STG_PRODUCTS: {clean.count()} linhas")

def clean_users(spark):
    df = read_table(spark, "RAW", "RAW_USERS")
    clean = (df
        .dropDuplicates(["ID"])
        .dropna(subset=["ID", "EMAIL"])
        .withColumn("EMAIL",     lower(trim(col("EMAIL"))))
        .withColumn("FIRSTNAME", trim(col("FIRSTNAME")))
        .withColumn("LASTNAME",  trim(col("LASTNAME")))
    )
    write_table(clean, "STAGING", "STG_USERS")
    print(f"✅ STG_USERS: {clean.count()} linhas")

def clean_orders(spark):
    df = read_table(spark, "RAW", "RAW_ORDERS")
    clean = (df
        .dropDuplicates(["ORDER_ID"])
        .dropna(subset=["ORDER_ID", "USER_ID", "PRODUCT_ID"])
        .withColumn("CATEGORY",   lower(trim(col("CATEGORY"))))
        .withColumn("STATUS",     lower(trim(col("STATUS"))))
        .withColumn("ORDER_DATE", to_date(col("ORDER_DATE")))
        .withColumn("TOTAL_PRICE", spark_round(col("TOTAL_PRICE"), 2))
        .filter(col("TOTAL_PRICE") > 0)
    )
    write_table(clean, "STAGING", "STG_ORDERS")
    print(f"✅ STG_ORDERS: {clean.count()} linhas")

if __name__ == "__main__":
    spark = get_spark()
    print("🔄 Iniciando Bronze → Silver...")
    clean_products(spark)
    clean_users(spark)
    clean_orders(spark)
    spark.stop()
    print("✅ Silver concluído!")