import pymysql
import os

connection = pymysql.connect(
    host=os.getenv("DB_HOST") or "localhost",
    user=os.getenv("DB_USER") or "root",
    password=os.getenv("DB_PASSWORD") or "root"
)

with connection.cursor() as cursor:
    try:
        cursor.execute("SHOW DATABASES")
        databases = [row[0] for row in cursor.fetchall()]
        if (os.getenv("DB_NAME") or "evoting_flask_app_database") in databases:
            print("Database is already exist, skipping creating")
        else:
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {os.getenv("DB_NAME") or "evoting_flask_app_database"} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;')
            print("Database creation succeed")
    except pymysql.MySQLError as e:
        print("Database creation failed")

pymysql.install_as_MySQLdb()