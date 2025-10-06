from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import grpc
import banking_pb2
import banking_pb2_grpc
import uvicorn
from concurrent import futures
import threading

app = FastAPI(title="Banking Microservice API Gateway", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# gRPC channel configurations
ACCOUNT_SERVICE_URL = "account-service:5001"
TRANSACTION_SERVICE_URL = "transaction-service:5002"
VALIDATION_SERVICE_URL = "validation-service:5003"

# gRPC channel options
grpc_options = [
    ('grpc.keepalive_time_ms', 10000),
    ('grpc.keepalive_timeout_ms', 5000),
    ('grpc.keepalive_permit_without_calls', True),
    ('grpc.http2.max_pings_without_data', 0),
    ('grpc.http2.min_time_between_pings_ms', 10000),
    ('grpc.http2.min_ping_interval_without_data_ms', 300000)
]

def get_account_stub():
    channel = grpc.insecure_channel(ACCOUNT_SERVICE_URL, options=grpc_options)
    return banking_pb2_grpc.AccountServiceStub(channel)

def get_transaction_stub():
    channel = grpc.insecure_channel(TRANSACTION_SERVICE_URL, options=grpc_options)
    return banking_pb2_grpc.TransactionServiceStub(channel)

def get_validation_stub():
    channel = grpc.insecure_channel(VALIDATION_SERVICE_URL, options=grpc_options)
    return banking_pb2_grpc.ValidationServiceStub(channel)

@app.get("/")
async def root():
    return {"message": "Banking Microservice API Gateway", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "api-gateway"}

# Account endpoints
@app.post("/accounts")
async def create_account(account_data: dict):
    try:
        stub = get_account_stub()
        request = banking_pb2.CreateAccountRequest(
            name=account_data["name"],
            email=account_data["email"],
            initial_balance=account_data.get("initial_balance", 0.0)
        )
        response = stub.CreateAccount(request)
        
        if response.success:
            return {
                "id": response.account_id,
                "name": response.name,
                "email": response.email,
                "balance": response.balance,
                "created_at": response.created_at
            }
        else:
            raise HTTPException(status_code=400, detail=response.message)
    except grpc.RpcError as e:
        raise HTTPException(status_code=503, detail=f"Account service unavailable: {e.details()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/accounts/{account_id}")
async def get_account(account_id: str):
    try:
        stub = get_account_stub()
        request = banking_pb2.GetAccountRequest(account_id=account_id)
        response = stub.GetAccount(request)
        
        if response.success:
            return {
                "id": response.account_id,
                "name": response.name,
                "email": response.email,
                "balance": response.balance,
                "created_at": response.created_at
            }
        else:
            raise HTTPException(status_code=404, detail=response.message)
    except grpc.RpcError as e:
        raise HTTPException(status_code=503, detail=f"Account service unavailable: {e.details()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/accounts")
async def list_accounts():
    try:
        stub = get_account_stub()
        request = banking_pb2.ListAccountsRequest()
        response = stub.ListAccounts(request)
        
        if response.success:
            accounts = []
            for account in response.accounts:
                accounts.append({
                    "id": account.account_id,
                    "name": account.name,
                    "email": account.email,
                    "balance": account.balance,
                    "created_at": account.created_at
                })
            return accounts
        else:
            raise HTTPException(status_code=500, detail=response.message)
    except grpc.RpcError as e:
        raise HTTPException(status_code=503, detail=f"Account service unavailable: {e.details()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Transaction endpoints
@app.post("/transactions/transfer")
async def transfer_money(transaction_data: dict):
    try:
        # Validate transaction first
        validation_stub = get_validation_stub()
        validation_request = banking_pb2.ValidateTransactionRequest(
            from_account_id=transaction_data["from_account_id"],
            to_account_id=transaction_data["to_account_id"],
            amount=transaction_data["amount"]
        )
        validation_response = validation_stub.ValidateTransaction(validation_request)
        
        if not validation_response.is_valid:
            raise HTTPException(status_code=400, detail=validation_response.message)
        
        # Process transaction
        stub = get_transaction_stub()
        request = banking_pb2.TransferRequest(
            from_account_id=transaction_data["from_account_id"],
            to_account_id=transaction_data["to_account_id"],
            amount=transaction_data["amount"],
            description=transaction_data.get("description", "")
        )
        response = stub.TransferMoney(request)
        
        if response.success:
            return {
                "message": response.message,
                "transaction_id": response.transaction_id,
                "from_balance": response.from_balance,
                "to_balance": response.to_balance
            }
        else:
            raise HTTPException(status_code=400, detail=response.message)
    except grpc.RpcError as e:
        raise HTTPException(status_code=503, detail=f"Transaction service unavailable: {e.details()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transactions/deposit")
async def deposit_money(transaction_data: dict):
    try:
        # Validate amount
        validation_stub = get_validation_stub()
        validation_request = banking_pb2.ValidateAmountRequest(amount=transaction_data["amount"])
        validation_response = validation_stub.ValidateAmount(validation_request)
        
        if not validation_response.is_valid:
            raise HTTPException(status_code=400, detail=validation_response.message)
        
        # Process transaction
        stub = get_transaction_stub()
        request = banking_pb2.DepositRequest(
            account_id=transaction_data["account_id"],
            amount=transaction_data["amount"],
            description=transaction_data.get("description", "")
        )
        response = stub.DepositMoney(request)
        
        if response.success:
            return {
                "message": response.message,
                "transaction_id": response.transaction_id,
                "new_balance": response.new_balance
            }
        else:
            raise HTTPException(status_code=400, detail=response.message)
    except grpc.RpcError as e:
        raise HTTPException(status_code=503, detail=f"Transaction service unavailable: {e.details()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transactions/withdraw")
async def withdraw_money(transaction_data: dict):
    try:
        # Validate amount
        validation_stub = get_validation_stub()
        validation_request = banking_pb2.ValidateAmountRequest(amount=transaction_data["amount"])
        validation_response = validation_stub.ValidateAmount(validation_request)
        
        if not validation_response.is_valid:
            raise HTTPException(status_code=400, detail=validation_response.message)
        
        # Process transaction
        stub = get_transaction_stub()
        request = banking_pb2.WithdrawRequest(
            account_id=transaction_data["account_id"],
            amount=transaction_data["amount"],
            description=transaction_data.get("description", "")
        )
        response = stub.WithdrawMoney(request)
        
        if response.success:
            return {
                "message": response.message,
                "transaction_id": response.transaction_id,
                "new_balance": response.new_balance
            }
        else:
            raise HTTPException(status_code=400, detail=response.message)
    except grpc.RpcError as e:
        raise HTTPException(status_code=503, detail=f"Transaction service unavailable: {e.details()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/transactions/{account_id}")
async def get_transactions(account_id: str):
    try:
        stub = get_transaction_stub()
        request = banking_pb2.GetTransactionsRequest(account_id=account_id)
        response = stub.GetTransactions(request)
        
        if response.success:
            transactions = []
            for transaction in response.transactions:
                transactions.append({
                    "id": transaction.transaction_id,
                    "account_id": transaction.account_id,
                    "type": transaction.type,
                    "amount": transaction.amount,
                    "description": transaction.description,
                    "timestamp": transaction.timestamp
                })
            return transactions
        else:
            raise HTTPException(status_code=500, detail=response.message)
    except grpc.RpcError as e:
        raise HTTPException(status_code=503, detail=f"Transaction service unavailable: {e.details()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)

