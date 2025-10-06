import grpc
from concurrent import futures
import banking_pb2
import banking_pb2_grpc
import threading
import time

# In-memory storage for demo (in production, this would connect to account service)
accounts_db = {}

# Account service connection
ACCOUNT_SERVICE_URL = "account-service:5001"

def get_account_stub():
    channel = grpc.insecure_channel(ACCOUNT_SERVICE_URL)
    return banking_pb2_grpc.AccountServiceStub(channel)

def sync_accounts_from_service():
    """Sync account data from the account service"""
    try:
        account_stub = get_account_stub()
        request = banking_pb2.ListAccountsRequest()
        response = account_stub.ListAccounts(request)
        
        if response.success:
            for account in response.accounts:
                accounts_db[account.account_id] = {
                    "account_id": account.account_id,
                    "name": account.name,
                    "email": account.email,
                    "balance": account.balance,
                    "created_at": account.created_at
                }
            return True
    except Exception as e:
        print(f"Failed to sync accounts: {e}")
    return False

class ValidationService(banking_pb2_grpc.ValidationServiceServicer):
    
    def ValidateAccount(self, request, context):
        if request.account_id not in accounts_db:
            return banking_pb2.ValidateAccountResponse(
                is_valid=False,
                message="Account not found"
            )
        
        account = accounts_db[request.account_id]
        
        # Basic validation rules
        if not account.get("name"):
            return banking_pb2.ValidateAccountResponse(
                is_valid=False,
                message="Account name is required"
            )
        
        if not account.get("email"):
            return banking_pb2.ValidateAccountResponse(
                is_valid=False,
                message="Account email is required"
            )
        
        return banking_pb2.ValidateAccountResponse(
            is_valid=True,
            message="Account is valid"
        )
    
    def ValidateTransaction(self, request, context):
        # Sync accounts from account service first
        sync_accounts_from_service()
        
        # Check if both accounts exist
        if request.from_account_id not in accounts_db:
            return banking_pb2.ValidateTransactionResponse(
                is_valid=False,
                message="Source account not found"
            )
        
        if request.to_account_id not in accounts_db:
            return banking_pb2.ValidateTransactionResponse(
                is_valid=False,
                message="Destination account not found"
            )
        
        # Check if transferring to the same account
        if request.from_account_id == request.to_account_id:
            return banking_pb2.ValidateTransactionResponse(
                is_valid=False,
                message="Cannot transfer to the same account"
            )
        
        # Check sufficient funds
        if accounts_db[request.from_account_id]["balance"] < request.amount:
            return banking_pb2.ValidateTransactionResponse(
                is_valid=False,
                message="Insufficient funds"
            )
        
        return banking_pb2.ValidateTransactionResponse(
            is_valid=True,
            message="Transaction is valid"
        )
    
    def ValidateAmount(self, request, context):
        # Check if amount is positive
        if request.amount <= 0:
            return banking_pb2.ValidateAmountResponse(
                is_valid=False,
                message="Amount must be positive"
            )
        
        # Check if amount is within reasonable limits (demo: max $10,000)
        if request.amount > 10000:
            return banking_pb2.ValidateAmountResponse(
                is_valid=False,
                message="Amount exceeds maximum limit of $10,000"
            )
        
        return banking_pb2.ValidateAmountResponse(
            is_valid=True,
            message="Amount is valid"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    banking_pb2_grpc.add_ValidationServiceServicer_to_server(ValidationService(), server)
    server.add_insecure_port('[::]:5003')
    server.start()
    print("Validation Service started on port 5003")
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()

