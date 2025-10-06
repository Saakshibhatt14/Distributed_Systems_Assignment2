# Layered Architecture - Banking System

This is the layered architecture implementation of the banking transaction system using HTTP REST API communication.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Web UI    │  │  API Gateway│  │   Nginx     │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              │ HTTP
┌─────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │Transaction  │  │   Account   │  │  Validation │        │
│  │  Service    │  │  Service    │  │   Service   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              │ HTTP
┌─────────────────────────────────────────────────────────────┐
│                    Data Access Layer                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Account   │  │Transaction  │  │    Cache    │        │
│  │ Repository  │  │ Repository  │  │ Repository  │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Database Layer                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ SQLite      │  │   Cache     │  │   Logs      │        │
│  │ (Accounts)  │  │  (Redis)    │  │  (Files)    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## Node Distribution

- **Node 1**: Web UI + API Gateway (Port 3000, 3001)
- **Node 2**: Business Logic Services (Port 8000)
- **Node 3**: Data Access Layer (Port 8001)
- **Node 4**: Database (Port 5432)
- **Node 5**: Cache (Port 6379)

## Services

### 1. Web UI (Node 1)
- **Technology**: HTML/JavaScript + Nginx
- **Port**: 3000
- **Purpose**: User interface for banking operations
- **Features**: Account management, transaction processing

### 2. API Gateway (Node 1)
- **Technology**: FastAPI
- **Port**: 3001
- **Purpose**: Entry point for all API requests
- **Features**: Request routing, CORS handling

### 3. Business Logic (Node 2)
- **Technology**: FastAPI
- **Port**: 8000
- **Purpose**: Business rules and validation
- **Features**: Account validation, transaction processing logic

### 4. Data Access (Node 3)
- **Technology**: FastAPI
- **Port**: 8001
- **Purpose**: Data persistence and retrieval
- **Features**: CRUD operations, transaction logging

### 5. Database (Node 4)
- **Technology**: SQLite
- **Port**: 5432
- **Purpose**: Data storage
- **Features**: Account and transaction storage

### 6. Cache (Node 5)
- **Technology**: Redis (simplified)
- **Port**: 6379
- **Purpose**: Caching and session management
- **Features**: Key-value storage

## Communication Model

- **Protocol**: HTTP REST API
- **Data Format**: JSON
- **Request Flow**: Web UI → API Gateway → Business Logic → Data Access → Database

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
   - Web UI: http://localhost:3000
   - API Gateway: http://localhost:3001
   - Business Logic: http://localhost:8000
   - Data Access: http://localhost:8001
   - Database: http://localhost:5432
   - Cache: http://localhost:6379

3. **Test the system:**
   - Open http://localhost:3000 in your browser
   - Create accounts and perform transactions

### API Endpoints

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
Layered/
├── web-ui/           # Web interface
├── api-gateway/      # API gateway service
├── business-logic/   # Business logic service
├── data-access/      # Data access service
├── database/         # Database service
├── cache/           # Cache service
└── docker-compose.yml
```

### Adding New Features
1. Update the appropriate service
2. Modify the API gateway if needed
3. Update the web UI
4. Test with Docker Compose

## Monitoring

### Health Checks
- All services expose `/health` endpoints
- Check service status: `curl http://localhost:<port>/health`

### Logs
- View logs: `docker-compose logs <service-name>`
- Follow logs: `docker-compose logs -f <service-name>`

## Performance Characteristics

### Strengths
- **Simplicity**: Easy to understand and maintain
- **Monolithic**: All business logic in one place
- **Consistent**: Single database, single transaction model
- **Fast**: Direct database access

### Weaknesses
- **Scalability**: Hard to scale individual components
- **Coupling**: Tight coupling between layers
- **Deployment**: Single deployment unit
- **Technology**: Limited technology diversity

### Use Cases
- Small to medium applications
- Teams with limited distributed systems experience
- Applications with simple business logic
- Rapid prototyping and development
