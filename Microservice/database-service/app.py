from fastapi import FastAPI
import uvicorn
import sqlite3
import os

app = FastAPI(title="Banking Database Service", version="1.0.0")

# Database file path
DB_PATH = "/app/banking_microservice.db"

def init_database():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create accounts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            balance REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts (id)
        )
    ''')
    
    conn.commit()
    conn.close()

@app.get("/")
async def root():
    return {"message": "Banking Database Service", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "database"}

@app.get("/init")
async def initialize_database():
    """Initialize database tables"""
    try:
        init_database()
        return {"message": "Database initialized successfully"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Initialize database on startup
    init_database()
    uvicorn.run(app, host="0.0.0.0", port=5432)

