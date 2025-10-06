from fastapi import FastAPI, HTTPException
import httpx
import uvicorn
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Banking Business Logic", version="1.0.0")

# Data access service URL
DATA_ACCESS_URL = "http://data-access:8001"

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

@app.get("/")
async def root():
    return {"message": "Banking Business Logic Service", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "business-logic"}

# Account management
@app.post("/accounts", response_model=AccountResponse)
async def create_account(account: AccountCreate):
    # Validate business rules
    if account.initial_balance < 0:
        raise HTTPException(status_code=400, detail="Initial balance cannot be negative")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{DATA_ACCESS_URL}/accounts", json=account.dict())
            if response.status_code == 201:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Data access service unavailable")

@app.get("/accounts/{account_id}", response_model=AccountResponse)
async def get_account(account_id: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{DATA_ACCESS_URL}/accounts/{account_id}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                raise HTTPException(status_code=404, detail="Account not found")
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Data access service unavailable")

@app.get("/accounts")
async def list_accounts():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{DATA_ACCESS_URL}/accounts")
            return response.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Data access service unavailable")

# Transaction processing
@app.post("/transactions/transfer")
async def transfer_money(transfer: TransferRequest):
    # Business logic validation
    if transfer.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    if transfer.from_account_id == transfer.to_account_id:
        raise HTTPException(status_code=400, detail="Cannot transfer to the same account")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{DATA_ACCESS_URL}/transactions/transfer", json=transfer.dict())
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Data access service unavailable")

@app.post("/transactions/deposit")
async def deposit_money(transaction: TransactionRequest):
    # Business logic validation
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{DATA_ACCESS_URL}/transactions/deposit", json=transaction.dict())
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Data access service unavailable")

@app.post("/transactions/withdraw")
async def withdraw_money(transaction: TransactionRequest):
    # Business logic validation
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{DATA_ACCESS_URL}/transactions/withdraw", json=transaction.dict())
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Data access service unavailable")

@app.get("/transactions/{account_id}")
async def get_transactions(account_id: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{DATA_ACCESS_URL}/transactions/{account_id}")
            return response.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Data access service unavailable")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

