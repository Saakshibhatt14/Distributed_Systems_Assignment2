# Microservice Architecture - Banking System

This is the microservice architecture implementation of the banking transaction system using gRPC communication.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Routing   │  │   Auth      │  │   Rate      │        │
│  │   Service   │  │   Service   │  │  Limiting   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              │ gRPC
┌─────────────────────────────────────────────────────────────┐
│                    Microservices                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Account   │  │Transaction  │  │  Validation │        │
│  │  Service    │  │  Service    │  │   Service   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              │ gRPC
┌─────────────────────────────────────────────────────────────┐
│                    Database Service                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Account DB  │  │Transaction  │  │  Validation │        │
│  │(SQLite)     │  │     DB      │  │     DB      │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## Node Distribution

- **Node 1**: API Gateway (Port 3000)
- **Node 2**: Account Service (Port 5001)
- **Node 3**: Transaction Service (Port 5002)
- **Node 4**: Validation Service (Port 5003)
- **Node 5**: Database Service (Port 5432)

## Services

### 1. API Gateway (Node 1)
- **Technology**: FastAPI + gRPC
- **Port**: 3000
- **Purpose**: Entry point for all API requests
- **Features**: Request routing, gRPC client management, HTTP to gRPC conversion

### 2. Account Service (Node 2)
- **Technology**: gRPC Server
- **Port**: 5001
- **Purpose**: Account management operations
- **Features**: Create, read, update accounts

### 3. Transaction Service (Node 3)
- **Technology**: gRPC Server
- **Port**: 5002
- **Purpose**: Transaction processing
- **Features**: Transfer, deposit, withdraw, transaction history

### 4. Validation Service (Node 4)
- **Technology**: gRPC Server
- **Port**: 5003
- **Purpose**: Business rule validation
- **Features**: Account validation, transaction validation, amount validation

### 5. Database Service (Node 5)
- **Technology**: FastAPI + SQLite
- **Port**: 5432
- **Purpose**: Data persistence
- **Features**: Database initialization, health checks

## Communication Model

- **Protocol**: gRPC
- **Data Format**: Protocol Buffers
- **Request Flow**: API Gateway → Microservices → Database Service

## gRPC Services

### Account Service
```protobuf
service AccountService {
    rpc CreateAccount(CreateAccountRequest) returns (CreateAccountResponse);
    rpc GetAccount(GetAccountRequest) returns (GetAccountResponse);
    rpc ListAccounts(ListAccountsRequest) returns (ListAccountsResponse);
    rpc UpdateAccount(UpdateAccountRequest) returns (UpdateAccountResponse);
}
```

### Transaction Service
```protobuf
service TransactionService {
    rpc TransferMoney(TransferRequest) returns (TransferResponse);
    rpc DepositMoney(DepositRequest) returns (DepositResponse);
    rpc WithdrawMoney(WithdrawRequest) returns (WithdrawResponse);
    rpc GetTransactions(GetTransactionsRequest) returns (GetTransactionsResponse);
}
```

### Validation Service
```protobuf
service ValidationService {
    rpc ValidateAccount(ValidateAccountRequest) returns (ValidateAccountResponse);
    rpc ValidateTransaction(ValidateTransactionRequest) returns (ValidateTransactionResponse);
    rpc ValidateAmount(ValidateAmountRequest) returns (ValidateAmountResponse);
}
```

## Getting Started

### Prerequisites
- Docker
- Docker Compose

### Running the System

1. **Start all services:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   - API Gateway: http://localhost:3000
   - Account Service: localhost:5001 (gRPC)
   - Transaction Service: localhost:5002 (gRPC)
   - Validation Service: localhost:5003 (gRPC)
   - Database Service: http://localhost:5432

3. **Test the system:**
   - Use the same web UI from the layered architecture
   - Or test with curl/Postman using the API Gateway endpoints

### API Endpoints (via API Gateway)

#### Account Management
- `POST /accounts` - Create account
- `GET /accounts/{id}` - Get account details
- `GET /accounts` - List all accounts

#### Transaction Management
- `POST /transactions/transfer` - Transfer money
- `POST /transactions/deposit` - Deposit money
- `POST /transactions/withdraw` - Withdraw money
- `GET /transactions/{account_id}` - Get transaction history

## Functional Requirements

✅ **FR1: Account Management**
- Create Account
- View Account
- List Accounts

✅ **FR2: Basic Transactions**
- Transfer Money
- Deposit Money
- Withdraw Money
- View Transactions

✅ **FR3: Balance Operations**
- Check Balance
- Validate Funds
- Update Balance

✅ **FR4: Basic Validation**
- Amount Validation
- Account Validation
- Simple Logging

✅ **FR5: System Operations**
- Health Check
- Basic Logging
- Data Persistence

## Development

### Project Structure
```
Microservice/
├── api-gateway/        # API Gateway service
├── account-service/    # Account microservice
├── transaction-service/ # Transaction microservice
├── validation-service/ # Validation microservice
├── database-service/   # Database service
├── banking.proto      # gRPC protocol definition
└── docker-compose.yml
```

### gRPC Code Generation
The proto file is automatically compiled to Python code in each service's Dockerfile:
```bash
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. banking.proto
```

### Adding New Features
1. Update the proto file if needed
2. Regenerate gRPC code
3. Update the appropriate microservice
4. Update the API Gateway if needed
5. Test with Docker Compose

## Monitoring

### Health Checks
- All services expose `/health` endpoints
- Check service status: `curl http://localhost:<port>/health`

### Logs
- View logs: `docker-compose logs <service-name>`
- Follow logs: `docker-compose logs -f <service-name>`

## Performance Characteristics

### Strengths
- **Scalability**: Each service can be scaled independently
- **Technology Diversity**: Different services can use different technologies
- **Fault Isolation**: Failure in one service doesn't affect others
- **Team Independence**: Different teams can work on different services
- **Deployment**: Independent deployment of services

### Weaknesses
- **Complexity**: More complex than monolithic systems
- **Network Latency**: Inter-service communication overhead
- **Data Consistency**: Distributed data management challenges
- **Debugging**: Harder to debug across service boundaries
- **Testing**: More complex integration testing

### Use Cases
- Large, complex applications
- Teams with distributed systems experience
- Applications requiring independent scaling
- Multi-tenant systems
- Systems with diverse technology requirements

## gRPC vs HTTP Comparison

### gRPC Advantages
- **Performance**: Binary protocol, faster than JSON
- **Type Safety**: Strong typing with Protocol Buffers
- **Streaming**: Built-in support for streaming
- **Code Generation**: Automatic client/server code generation
- **HTTP/2**: Built on HTTP/2 for better performance

### gRPC Disadvantages
- **Browser Support**: Limited browser support (requires gRPC-Web)
- **Learning Curve**: More complex than REST
- **Debugging**: Harder to debug than HTTP
- **Caching**: Less cacheable than HTTP
- **Firewall**: Some firewalls may block gRPC traffic

