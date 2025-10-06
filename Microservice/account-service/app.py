import grpc
from concurrent import futures
import banking_pb2
import banking_pb2_grpc
import threading
import time
from datetime import datetime
import uuid

# In-memory storage for demo (in production, this would connect to database service)
accounts_db = {}
account_counter = 1

class AccountService(banking_pb2_grpc.AccountServiceServicer):
    
    def CreateAccount(self, request, context):
        global account_counter
        
        account_id = str(account_counter)
        account_counter += 1
        
        # Check if email already exists
        for account in accounts_db.values():
            if account["email"] == request.email:
                return banking_pb2.CreateAccountResponse(
                    success=False,
                    message="Email already exists"
                )
        
        new_account = {
            "account_id": account_id,
            "name": request.name,
            "email": request.email,
            "balance": request.initial_balance,
            "created_at": datetime.now().isoformat()
        }
        
        accounts_db[account_id] = new_account
        
        return banking_pb2.CreateAccountResponse(
            account_id=account_id,
            name=request.name,
            email=request.email,
            balance=request.initial_balance,
            created_at=new_account["created_at"],
            success=True,
            message="Account created successfully"
        )
    
    def GetAccount(self, request, context):
        if request.account_id not in accounts_db:
            return banking_pb2.GetAccountResponse(
                success=False,
                message="Account not found"
            )
        
        account = accounts_db[request.account_id]
        return banking_pb2.GetAccountResponse(
            account_id=account["account_id"],
            name=account["name"],
            email=account["email"],
            balance=account["balance"],
            created_at=account["created_at"],
            success=True,
            message="Account retrieved successfully"
        )
    
    def ListAccounts(self, request, context):
        accounts = []
        for account in accounts_db.values():
            accounts.append(banking_pb2.Account(
                account_id=account["account_id"],
                name=account["name"],
                email=account["email"],
                balance=account["balance"],
                created_at=account["created_at"]
            ))
        
        return banking_pb2.ListAccountsResponse(
            accounts=accounts,
            success=True,
            message="Accounts retrieved successfully"
        )
    
    def UpdateAccount(self, request, context):
        if request.account_id not in accounts_db:
            return banking_pb2.UpdateAccountResponse(
                success=False,
                message="Account not found"
            )
        
        # Update account information
        if request.name:
            accounts_db[request.account_id]["name"] = request.name
        if request.email:
            accounts_db[request.account_id]["email"] = request.email
        if request.balance is not None:
            accounts_db[request.account_id]["balance"] = request.balance
        
        return banking_pb2.UpdateAccountResponse(
            success=True,
            message="Account updated successfully"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    banking_pb2_grpc.add_AccountServiceServicer_to_server(AccountService(), server)
    server.add_insecure_port('[::]:5001')
    server.start()
    print("Account Service started on port 5001")
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()

