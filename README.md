# Distributed Banking Transaction System

A comprehensive distributed systems project implementing two distinct architectures (Layered and Microservice) for a banking transaction system, with performance comparison and evaluation.

## 🏗️ Project Overview

This project demonstrates the implementation and comparison of two different distributed system architectures:

1. **Layered Architecture** - HTTP REST API communication
2. **Microservice Architecture** - gRPC communication

Both architectures implement the same banking functionality but with different design patterns and communication models.

## 📁 Project Structure

```
DS_new/
├── Layered/                    # Layered Architecture Implementation
│   ├── web-ui/                 # Web Interface (Node 1)
│   ├── api-gateway/            # API Gateway (Node 1)
│   ├── business-logic/         # Business Logic Service (Node 2)
│   ├── data-access/            # Data Access Layer (Node 3)
│   ├── database/               # Database Service (Node 4)
│   ├── cache/                  # Cache Service (Node 5)
│   ├── docker-compose.yml      # Container orchestration
│   └── README.md               # Architecture documentation
├── Microservice/               # Microservice Architecture Implementation
│   ├── api-gateway/            # API Gateway (Node 1)
│   ├── account-service/        # Account Microservice (Node 2)
│   ├── transaction-service/     # Transaction Microservice (Node 3)
│   ├── validation-service/     # Validation Microservice (Node 4)
│   ├── database-service/       # Database Service (Node 5)
│   ├── banking.proto          # gRPC Protocol Definition
│   ├── docker-compose.yml     # Container orchestration
│   └── README.md              # Architecture documentation
├── Performance_testing/        # Performance Testing Suite
│   ├── load_test.py           # Main performance testing script
│   ├── compare_results.py     # Results comparison tool
│   ├── visualize_results.py   # Visualization generation
│   ├── run_tests.bat          # Windows automation script
│   ├── run_tests.sh           # Linux/Mac automation script
│   ├── requirements.txt       # Python dependencies
│   └── README.md              # Testing documentation
├── blueprint.md               # Project blueprint and requirements
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites
- **Docker** and **Docker Compose**
- **Python 3.7+** (for performance testing)
- **Git** (for version control)

### 1. Clone the Repository
```bash
git clone https://github.com/Saakshibhatt14/Distributed_Systems_Assignment2.git 
cd DS_new
```

### 2. Run Layered Architecture
```bash
cd Layered
docker-compose up --build
```
- **Web UI**: http://localhost:3100
- **API Gateway**: http://localhost:3001

### 3. Run Microservice Architecture
```bash
cd Microservice
docker-compose up --build
```
- **API Gateway**: http://localhost:3000
- **Services**: gRPC on ports 5001-5003

### 4. Run Performance Tests
```bash
cd "Performance_testing"
.\run_tests.bat  # Windows
# or
./run_tests.sh   # Linux/Mac
```

## 🧪 Functional Requirements

### FR1: Account Management
- **Create Account**: Simple account creation with basic info
- **View Account**: Get account balance and details
- **List Accounts**: View all accounts in the system

### FR2: Basic Transactions
- **Transfer Money**: Simple transfer between two accounts
- **Deposit Money**: Add money to an account
- **Withdraw Money**: Remove money from an account
- **View Transactions**: See transaction history for an account

### FR3: Balance Operations
- **Check Balance**: Get current account balance
- **Validate Funds**: Check if account has sufficient funds
- **Update Balance**: Simple balance updates

### FR4: Basic Validation
- **Amount Validation**: Ensure positive amounts
- **Account Validation**: Check if accounts exist
- **Simple Logging**: Basic transaction logging

### FR5: System Operations
- **Health Check**: Simple system health monitoring
- **Basic Logging**: Simple transaction logs
- **Data Persistence**: Basic data storage

## 🏛️ System Architectures

### 2.1 Layered Architecture
**Communication Model**: HTTP REST API

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Web UI    │  │  Mobile App │  │   API Docs  │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │ HTTP
┌─────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │Transaction  │  │   Account   │  │  Validation │          │
│  │  Service    │  │  Service    │  │   Service   │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │ HTTP
┌─────────────────────────────────────────────────────────────┐
│                    Data Access Layer                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Account   │  │Transaction  │  │    Audit    │          │
│  │ Repository  │  │ Repository  │  │ Repository  │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Database Layer                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │ PostgreSQL  │  │   Redis     │  │   MongoDB   │          │
│  │ (Accounts)  │  │  (Cache)    │  │  (Audit)    │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

**Node Distribution (Layered Architecture)**:
- **Node 1**: Web UI + API Gateway (Port 3100)
- **Node 2**: Business Logic Services (Port 8000)
- **Node 3**: Data Access Layer (Port 8001)
- **Node 4**: Database (SQLite/PostgreSQL) (Port 55432)
- **Node 5**: Cache & Logs (Redis) (Port 6379)

### 2.2 Microservice Architecture
**Communication Model**: gRPC

```
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Routing   │  │   Auth      │  │   Rate      │          │
│  │   Service   │  │   Service   │  │  Limiting   │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │ gRPC
┌─────────────────────────────────────────────────────────────┐
│                    Microservices                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Account   │  │Transaction  │  │  Notification│         │
│  │  Service    │  │  Service    │  │   Service   │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  Validation │  │   Audit     │  │   Fraud     │          │
│  │  Service    │  │  Service    │  │  Detection  │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │ gRPC
┌─────────────────────────────────────────────────────────────┐
│                    Service Databases                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │ Account DB  │  │Transaction  │  │  Audit DB   │          │
│  │(PostgreSQL) │  │     DB      │  │  (MongoDB)  │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

**Node Distribution (Microservice Architecture)**:
- **Node 1**: API Gateway (Port 3000)
- **Node 2**: Account Service (Port 5001)
- **Node 3**: Transaction Service (Port 5002)
- **Node 4**: Validation Service (Port 5003)
- **Node 5**: Database Service (Port 5432)

## 🔧 Technical Implementation

### Technology Stack
- **Backend**: Python (FastAPI)
- **Frontend**: HTML/JavaScript
- **Database**: SQLite (for simplicity)
- **Containerization**: Docker + Docker Compose
- **Communication**: HTTP REST API vs gRPC

### Simple Infrastructure
- **Containerization**: Docker + Docker Compose (local only)
- **Database**: SQLite (file-based) or PostgreSQL (single instance)
- **Cache**: Redis (optional, for learning)
- **Logging**: Simple file logging or console output

## 📊 Performance Testing

### Test Scenarios
1. **Account Creation**: 5 concurrent users, 2500 requests
2. **Account Retrieval**: 10 concurrent users, 2500 requests
3. **Money Transfer**: 5 concurrent users, 2500 requests
4. **Money Deposit**: 5 concurrent users, 2500 requests
5. **High Load Test**: 20 concurrent users, 10000 requests

### Metrics Measured
- **Throughput**: Requests per second
- **Latency**: Response time (average, 95th percentile)
- **Success Rate**: Percentage of successful requests
- **Resource Utilization**: CPU, memory usage

### Running Tests
```bash
# Automated testing (Windows)
.\run_tests.bat

# Automated testing (Linux/Mac)
./run_tests.sh

# Individual architecture testing
python load_test.py --architecture layered --url http://localhost:3001
python load_test.py --architecture microservice --url http://localhost:3000

# Generate visualizations
python visualize_results.py --layered layered_results.json --microservice microservice_results.json --comparison comparison_report.json
```

## 🎯 Project Requirements Fulfilled

✅ **5+ Functional Requirements**: All implemented
✅ **2 System Architectures**: Layered and Microservice
✅ **Different Communication Models**: HTTP vs gRPC
✅ **5+ Nodes**: Both architectures use 5 nodes
✅ **Containerization**: Docker containers for all services
✅ **Performance Evaluation**: Comprehensive testing suite
✅ **AI Tools**: Used for code generation and assistance
✅ **Git**: Version control throughout development

## 📈 Performance Results Summary

### Key Findings:
- **Microservice Architecture** generally outperforms Layered in most scenarios:
  - Account Creation: 152.2 vs 50.8 RPS (3x faster)
  - Account Retrieval: 168.6 vs 53.3 RPS (3.2x faster)
  - High Load Test: 168.4 vs 54.5 RPS (3.1x faster)
- **Exception**: Money Transfer where Layered performs better (50.7 vs 21.9 RPS)
- **Both architectures achieve 100% success rates**
- **Microservice wins in 4 out of 5 test categories**

### Recommendations:
1. **For High-Throughput Applications**: Choose Microservice Architecture
2. **For Money Transfer Operations**: Layered Architecture may be more suitable
3. **For Mixed Workloads**: Microservice Architecture provides better overall performance
4. **Both architectures are equally reliable** (100% success rates)

## 🛠️ Development Workflow

### Phase 1: Basic Setup (Week 1)
- Set up local development environment
- Create basic Docker containers
- Implement simple layered architecture
- Basic account and transaction functionality

### Phase 2: Microservice Version (Week 2)
- Implement microservice architecture
- Add gRPC communication
- Basic service-to-service communication
- Simple load testing

### Phase 3: Testing & Comparison (Week 3)
- Simple performance testing
- Compare both architectures
- Basic documentation
- Prepare demo

## 🔍 Monitoring and Debugging

### Health Checks
All services expose `/health` endpoints:
```bash
curl http://localhost:3000/health  # Microservice
curl http://localhost:3001/health  # Layered
```

### Logs
View service logs:
```bash
docker-compose logs <service-name>
docker-compose logs -f <service-name>  # Follow logs
```

### Container Status
```bash
docker-compose ps
```

## 📚 Documentation

- **`blueprint.md`**: Complete project blueprint and requirements
- **`Layered/README.md`**: Layered architecture documentation
- **`Microservice/README.md`**: Microservice architecture documentation
- **`Performance_testing/README.md`**: Performance testing guide

## 🎓 Learning Outcomes

After completing this project, you will understand:
- **Distributed Systems**: Architecture patterns and trade-offs
- **Communication Models**: HTTP vs gRPC differences
- **Containerization**: Docker and orchestration
- **Performance Testing**: Load testing and metrics
- **System Design**: Scalability and reliability considerations

## 🚀 Next Steps

1. **Run both architectures** and test functionality
2. **Execute performance tests** and analyze results
3. **Compare architectures** and understand trade-offs
4. **Experiment with modifications** to see impact
5. **Document findings** and recommendations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational purposes and demonstrates distributed systems concepts.

---

**Happy Learning! 🎉**


This project provides hands-on experience with distributed systems, helping you understand the practical implications of architectural decisions in real-world applications.
