# Performance Testing - Banking System

This directory contains performance testing tools for comparing the Layered and Microservice architectures of the banking system.

## Overview

The performance testing suite includes:
- **Load Testing**: Concurrent user simulation
- **Performance Metrics**: Response time, throughput, success rate
- **Comparison Tools**: Side-by-side architecture comparison
- **Automated Testing**: Scripts for both architectures

## Test Scenarios

### 1. Account Creation Test
- **Purpose**: Test account creation performance
- **Concurrency**: 5 concurrent users
- **Duration**: 30 seconds
- **Metrics**: Response time, success rate, throughput

### 2. Account Retrieval Test
- **Purpose**: Test account lookup performance
- **Concurrency**: 10 concurrent users
- **Duration**: 30 seconds
- **Metrics**: Response time, success rate, throughput

### 3. Money Transfer Test
- **Purpose**: Test transaction processing performance
- **Concurrency**: 5 concurrent users
- **Duration**: 30 seconds
- **Metrics**: Response time, success rate, throughput

### 4. Money Deposit Test
- **Purpose**: Test deposit operation performance
- **Concurrency**: 5 concurrent users
- **Duration**: 30 seconds
- **Metrics**: Response time, success rate, throughput

### 5. High Load Test
- **Purpose**: Test system under high load
- **Concurrency**: 20 concurrent users
- **Duration**: 60 seconds
- **Metrics**: Response time, success rate, throughput

## Files

### Core Testing Files
- **`load_test.py`**: Main performance testing script
- **`compare_results.py`**: Results comparison and analysis
- **`requirements.txt`**: Python dependencies

### Automation Scripts
- **`run_tests.sh`**: Linux/Mac automation script
- **`run_tests.bat`**: Windows automation script

## Usage

### Prerequisites
1. **Python 3.7+** installed
2. **Both architectures running**:
   - Layered: `cd Layered && docker-compose up`
   - Microservice: `cd Microservice && docker-compose up`

### Manual Testing

#### Test Layered Architecture
```bash
python load_test.py --architecture layered --url http://localhost:3001 --output layered_results.json
```

#### Test Microservice Architecture
```bash
python load_test.py --architecture microservice --url http://localhost:3000 --output microservice_results.json
```

#### Compare Results
```bash
python compare_results.py --layered layered_results.json --microservice microservice_results.json
```

### Automated Testing

#### Windows
```cmd
run_tests.bat
```

#### Linux/Mac
```bash
./run_tests.sh
```

## Performance Metrics

### Key Metrics Measured
1. **Total Requests**: Total number of requests sent
2. **Success Rate**: Percentage of successful requests
3. **Requests per Second**: Throughput measurement
4. **Response Time**: Average response time in milliseconds
5. **95th Percentile**: 95th percentile response time
6. **Min/Max Response Time**: Range of response times

### Expected Results

#### Layered Architecture
- **Strengths**: 
  - Lower network overhead
  - Simpler request flow
  - Better for simple operations
- **Expected Performance**:
  - Higher throughput for simple operations
  - Lower response times
  - Better resource utilization

#### Microservice Architecture
- **Strengths**:
  - Better scalability
  - Independent service scaling
  - Technology diversity
- **Expected Performance**:
  - Higher overhead due to gRPC
  - Better for complex operations
  - More resilient to failures

## Test Results Analysis

### Performance Comparison Table
The comparison tool generates a detailed table showing:
- Side-by-side metrics for each test
- Performance differences between architectures
- Success rate comparisons
- Throughput analysis

### Summary Analysis
- **Overall Performance**: Average metrics across all tests
- **Winner Analysis**: Which architecture performs better for each metric
- **Trade-off Analysis**: Architectural strengths and weaknesses

## Customization

### Modifying Test Parameters
Edit `load_test.py` to change:
- **Concurrency levels**: Number of concurrent users
- **Test duration**: How long each test runs
- **Test scenarios**: Add new test types
- **Request patterns**: Modify request data

### Adding New Tests
1. Create new test function in `load_test.py`
2. Add test to `run_comprehensive_test()`
3. Update comparison logic in `compare_results.py`

## Troubleshooting

### Common Issues

#### API Not Running
```
Error: Cannot connect to API
```
**Solution**: Start the banking system with `docker-compose up`

#### Port Conflicts
```
Error: Port already in use
```
**Solution**: Check if other services are using the ports (3000, 3001, 5001-5003, 5432)

#### Python Dependencies
```
Error: Module not found
```
**Solution**: Install requirements with `pip install -r requirements.txt`

### Debug Mode
Add `--debug` flag to see detailed request/response information:
```bash
python load_test.py --architecture layered --url http://localhost:3001 --debug
```

## Results Interpretation

### Good Performance Indicators
- **Success Rate**: > 95%
- **Response Time**: < 200ms average
- **Throughput**: > 10 requests/second
- **Consistency**: Low variance in response times

### Performance Issues
- **High Error Rate**: > 5% failures
- **Slow Response**: > 1000ms average
- **Low Throughput**: < 5 requests/second
- **High Variance**: Inconsistent performance

### Architecture Recommendations

#### Choose Layered Architecture When:
- Simple business logic
- Small to medium team
- Limited distributed systems experience
- Performance is critical
- Low latency requirements

#### Choose Microservice Architecture When:
- Complex business logic
- Large development team
- Need independent scaling
- Technology diversity required
- Long-term scalability needed

## Advanced Testing

### Stress Testing
Modify concurrency and duration for stress testing:
```python
await self.run_concurrent_test(
    "Stress Test",
    self.get_account,
    "1",
    concurrency=50,  # High concurrency
    duration=300     # 5 minutes
)
```

### Endurance Testing
Run tests for extended periods to check for memory leaks and performance degradation.

### Load Testing
Gradually increase load to find the breaking point of each architecture.

## Contributing

### Adding New Metrics
1. Modify the test functions to collect new metrics
2. Update the results structure
3. Add comparison logic in `compare_results.py`

### Improving Test Accuracy
- Add more realistic test data
- Implement proper error handling
- Add retry logic for failed requests
- Implement proper cleanup between tests

## Future Enhancements

### Planned Features
- **Database Performance**: Test database operations separately
- **Memory Usage**: Monitor memory consumption during tests
- **Network Analysis**: Analyze network traffic patterns
- **Scalability Testing**: Test with multiple service instances
- **Real-time Monitoring**: Live performance dashboards

### Integration with CI/CD
- Automated performance testing in CI pipeline
- Performance regression detection
- Automated reporting and alerts
