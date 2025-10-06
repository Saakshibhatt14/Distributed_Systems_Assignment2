@echo off
REM Performance Testing Script for Banking System
REM Tests both Layered and Microservice architectures

echo ==========================================
echo Banking System Performance Testing
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    exit /b 1
)

REM Install requirements
echo Installing requirements...
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo Warning: requirements.txt not found, installing basic dependencies...
    pip install aiohttp
)
echo.

REM Set equal request counts for both architectures
set REQUESTS_PER_TEST=2500
set HIGHLOAD_REQUESTS=10000

REM Test Layered Architecture
echo 1. Testing Layered Architecture
echo ================================
echo Testing layered architecture...
echo API URL: http://localhost:3001
echo REQUESTS_PER_TEST: %REQUESTS_PER_TEST%
echo HIGHLOAD_REQUESTS: %HIGHLOAD_REQUESTS%
echo.

REM Check if Layered API is running
curl -s "http://localhost:3001/health" >nul 2>&1
if errorlevel 1 (
    echo Error: Layered API is not running at http://localhost:3001
    echo Please start the system with: docker-compose up
    exit /b 1
)

REM Run Layered performance test
python load_test.py --architecture layered --url http://localhost:3001 --output layered_performance_results.json --requests-per-test %REQUESTS_PER_TEST% --highload-requests %HIGHLOAD_REQUESTS%

if errorlevel 1 (
    echo [ERROR] Layered test failed
    exit /b 1
) else (
    echo [SUCCESS] Layered test completed successfully
)
echo.

REM Test Microservice Architecture  
echo 2. Testing Microservice Architecture
echo =====================================
echo Testing microservice architecture...
echo API URL: http://localhost:3000
echo REQUESTS_PER_TEST: %REQUESTS_PER_TEST%
echo HIGHLOAD_REQUESTS: %HIGHLOAD_REQUESTS%
echo.

REM Check if Microservice API is running
curl -s "http://localhost:3000/health" >nul 2>&1
if errorlevel 1 (
    echo Error: Microservice API is not running at http://localhost:3000
    echo Please start the system with: docker-compose up
    exit /b 1
)

REM Run Microservice performance test
python load_test.py --architecture microservice --url http://localhost:3000 --output microservice_performance_results.json --requests-per-test %REQUESTS_PER_TEST% --highload-requests %HIGHLOAD_REQUESTS%

if errorlevel 1 (
    echo [ERROR] Microservice test failed
    exit /b 1
) else (
    echo [SUCCESS] Microservice test completed successfully
)
echo.

REM Compare results
echo 3. Comparing Results
echo ====================
if exist "layered_layered_performance_results.json" if exist "microservice_microservice_performance_results.json" (
    python compare_results.py --layered layered_layered_performance_results.json --microservice microservice_microservice_performance_results.json
    echo [SUCCESS] Comparison completed successfully
) else (
    echo [ERROR] Cannot compare results - one or both test files are missing
    exit /b 1
)

echo.
echo ==========================================
echo Performance testing completed!
echo ==========================================