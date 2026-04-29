from database import engine
from sqlalchemy import text

def test_connection():
    print("Connecting to PostgreSQL...")
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            row = result.fetchone()
            print("✅ Connection Successful!")
            print(f"Postgres Version: {row[0]}")
    except Exception as e:
        print("❌ Connection Failed!")
        print(f"Error Details: {e}")

if __name__ == "__main__":
    test_connection()