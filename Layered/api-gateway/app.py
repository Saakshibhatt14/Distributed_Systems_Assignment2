from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn

app = FastAPI(title="Banking API Gateway", version="1.0.0")

# CORS middleware for web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Business logic service URL
BUSINESS_LOGIC_URL = "http://business-logic:8000"

@app.get("/")
async def root():
    return {"message": "Banking API Gateway", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "api-gateway"}

# Account endpoints
@app.post("/accounts")
async def create_account(account_data: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{BUSINESS_LOGIC_URL}/accounts", json=account_data)
            return response.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Business logic service unavailable")

@app.get("/accounts/{account_id}")
async def get_account(account_id: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BUSINESS_LOGIC_URL}/accounts/{account_id}")
            return response.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Business logic service unavailable")

@app.get("/accounts")
async def list_accounts():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BUSINESS_LOGIC_URL}/accounts")
            return response.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Business logic service unavailable")

# Transaction endpoints
@app.post("/transactions/transfer")
async def transfer_money(transaction_data: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{BUSINESS_LOGIC_URL}/transactions/transfer", json=transaction_data)
            return response.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Business logic service unavailable")

@app.post("/transactions/deposit")
async def deposit_money(transaction_data: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{BUSINESS_LOGIC_URL}/transactions/deposit", json=transaction_data)
            return response.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Business logic service unavailable")

@app.post("/transactions/withdraw")
async def withdraw_money(transaction_data: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{BUSINESS_LOGIC_URL}/transactions/withdraw", json=transaction_data)
            return response.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Business logic service unavailable")

@app.get("/transactions/{account_id}")
async def get_transactions(account_id: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BUSINESS_LOGIC_URL}/transactions/{account_id}")
            return response.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Business logic service unavailable")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)

