import MySQLdb
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "cmp_db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))

print(f"Connecting to MySQL at {DB_HOST}:{DB_PORT} as {DB_USER}...")

try:
    # Connect without DB to create it
    db = MySQLdb.connect(user=DB_USER, passwd=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = db.cursor()
    
    print(f"Creating database {DB_NAME} if not exists...")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    
    db.select_db(DB_NAME)
    
    print("Creating django_migrations table manually...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS django_migrations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            app VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            applied DATETIME NOT NULL
        ) ENGINE=InnoDB;
    """)
    
    print("Success.")
    db.close()

except Exception as e:
    print(f"Error: {e}")
    exit(1)
