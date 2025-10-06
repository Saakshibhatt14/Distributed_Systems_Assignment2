from fastapi import FastAPI, HTTPException
import httpx
import uvicorn
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import json
from datetime import datetime

app = FastAPI(title="Banking Data Access", version="1.0.0")

# Database service URL
DATABASE_URL = "http://database:5432"

# Pydantic models
class AccountCreate(BaseModel):
    name: str
    email: str
    initial_balance: float = 0.0

class AccountResponse(BaseModel):
    id: str
    name: str
    email: str
    balance: float
    created_at: str

class TransactionRequest(BaseModel):
    account_id: str
    amount: float
    description: Optional[str] = None

class TransferRequest(BaseModel):
    from_account_id: str
    to_account_id: str
    amount: float
    description: Optional[str] = None

# Simple in-memory storage for demo (in production, this would connect to database service)
accounts_db = {}
transactions_db = {}
account_counter = 1
transaction_counter = 1

@app.get("/")
async def root():
    return {"message": "Banking Data Access Service", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "data-access"}

# Account operations
@app.post("/accounts", response_model=AccountResponse)
async def create_account(account: AccountCreate):
    global account_counter
    
    account_id = str(account_counter)
    account_counter += 1
    
    new_account = {
        "id": account_id,
        "name": account.name,
        "email": account.email,
        "balance": account.initial_balance,
        "created_at": datetime.now().isoformat()
    }
    
    accounts_db[account_id] = new_account
    
    return AccountResponse(**new_account)

@app.get("/accounts/{account_id}", response_model=AccountResponse)
async def get_account(account_id: str):
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return AccountResponse(**accounts_db[account_id])

@app.get("/accounts")
async def list_accounts():
    return list(accounts_db.values())

# Transaction operations
@app.post("/transactions/transfer")
async def transfer_money(transfer: TransferRequest):
    global transaction_counter
    
    # Check if both accounts exist
    if transfer.from_account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Source account not found")
    
    if transfer.to_account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Destination account not found")
    
    # Check sufficient funds
    if accounts_db[transfer.from_account_id]["balance"] < transfer.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    # Perform transfer
    accounts_db[transfer.from_account_id]["balance"] -= transfer.amount
    accounts_db[transfer.to_account_id]["balance"] += transfer.amount
    
    # Record transactions
    transaction_id = str(transaction_counter)
    transaction_counter += 1
    
    timestamp = datetime.now().isoformat()
    
    # Debit transaction
    debit_transaction = {
        "id": transaction_id,
        "account_id": transfer.from_account_id,
        "type": "debit",
        "amount": transfer.amount,
        "description": f"Transfer to {transfer.to_account_id}",
        "timestamp": timestamp
    }
    
    # Credit transaction
    credit_transaction = {
        "id": str(transaction_counter),
        "account_id": transfer.to_account_id,
        "type": "credit",
        "amount": transfer.amount,
        "description": f"Transfer from {transfer.from_account_id}",
        "timestamp": timestamp
    }
    
    transaction_counter += 1
    
    transactions_db[transaction_id] = debit_transaction
    transactions_db[str(transaction_counter - 1)] = credit_transaction
    
    return {
        "message": "Transfer successful",
        "transaction_id": transaction_id,
        "from_balance": accounts_db[transfer.from_account_id]["balance"],
        "to_balance": accounts_db[transfer.to_account_id]["balance"]
    }

@app.post("/transactions/deposit")
async def deposit_money(transaction: TransactionRequest):
    global transaction_counter
    
    if transaction.account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Update balance
    accounts_db[transaction.account_id]["balance"] += transaction.amount
    
    # Record transaction
    transaction_id = str(transaction_counter)
    transaction_counter += 1
    
    new_transaction = {
        "id": transaction_id,
        "account_id": transaction.account_id,
        "type": "credit",
        "amount": transaction.amount,
        "description": transaction.description or "Deposit",
        "timestamp": datetime.now().isoformat()
    }
    
    transactions_db[transaction_id] = new_transaction
    
    return {
        "message": "Deposit successful",
        "transaction_id": transaction_id,
        "new_balance": accounts_db[transaction.account_id]["balance"]
    }

@app.post("/transactions/withdraw")
async def withdraw_money(transaction: TransactionRequest):
    global transaction_counter
    
    if transaction.account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Check sufficient funds
    if accounts_db[transaction.account_id]["balance"] < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    # Update balance
    accounts_db[transaction.account_id]["balance"] -= transaction.amount
    
    # Record transaction
    transaction_id = str(transaction_counter)
    transaction_counter += 1
    
    new_transaction = {
        "id": transaction_id,
        "account_id": transaction.account_id,
        "type": "debit",
        "amount": transaction.amount,
        "description": transaction.description or "Withdrawal",
        "timestamp": datetime.now().isoformat()
    }
    
    transactions_db[transaction_id] = new_transaction
    
    return {
        "message": "Withdrawal successful",
        "transaction_id": transaction_id,
        "new_balance": accounts_db[transaction.account_id]["balance"]
    }

@app.get("/transactions/{account_id}")
async def get_transactions(account_id: str):
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account_transactions = [
        transaction for transaction in transactions_db.values()
        if transaction["account_id"] == account_id
    ]
    
    return account_transactions

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

