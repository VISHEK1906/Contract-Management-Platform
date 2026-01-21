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
    # Connect without DB to perform administrative tasks
    db = MySQLdb.connect(user=DB_USER, passwd=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = db.cursor()
    
    print(f"Forcing clean reset of database: {DB_NAME}")
    cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
    cursor.execute(f"CREATE DATABASE {DB_NAME}")
    
    db.select_db(DB_NAME)
    
    print("Creating django_migrations table manually (MySQL 5.5 campatibility)...")
    # Django < 5 uses this structure. 
    # Note: Modern Django might use slightly different structure but this usually works for initial bootstrap.
    cursor.execute("""
        CREATE TABLE django_migrations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            app VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            applied DATETIME NOT NULL
        ) ENGINE=InnoDB;
    """)
    
    print("Database reset successful.")
    db.close()

except Exception as e:
    print(f"Error: {e}")
    exit(1)
