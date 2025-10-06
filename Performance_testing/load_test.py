#!/usr/bin/env python3
"""
Performance Testing Script for Banking System
Tests both Layered and Microservice architectures
"""

import asyncio
import aiohttp
import time
import statistics
import json
from datetime import datetime
import argparse
import sys
import copy
import uuid

class PerformanceTest:
    def __init__(self, base_url, architecture_name):
        self.base_url = base_url
        self.architecture_name = architecture_name
        self.results = {
            'architecture': architecture_name,
            'timestamp': datetime.now().isoformat(),
            'tests': []
        }
        # IDs for pre-created accounts used across tests
        self.primary_account_id = None
        self.secondary_account_id = None
    
    async def create_account(self, session, account_data):
        """Create a new account"""
        start_time = time.time()
        try:
            async with session.post(f"{self.base_url}/accounts", json=account_data) as response:
                end_time = time.time()
                response_time = (end_time - start_time) * 1000  # Convert to milliseconds
                
                if response.status == 201 or response.status == 200:
                    account_info = await response.json()
                    # Handle case where response might be wrapped in 'detail' field
                    if 'detail' in account_info:
                        try:
                            import json
                            account_info = json.loads(account_info['detail'])
                        except:
                            pass
                    
                    account_id = account_info.get('id')
                    if not account_id:
                        return {
                            'success': False,
                            'response_time': response_time,
                            'error': f"No account ID in response: {account_info}",
                            'status_code': response.status
                        }
                    
                    return {
                        'success': True,
                        'response_time': response_time,
                        'account_id': account_id,
                        'status_code': response.status
                    }
                else:
                    return {
                        'success': False,
                        'response_time': response_time,
                        'error': f"HTTP {response.status}",
                        'status_code': response.status
                    }
        except Exception as e:
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            return {
                'success': False,
                'response_time': response_time,
                'error': str(e),
                'status_code': 0
            }
    
    async def get_account(self, session, account_id):
        """Get account information"""
        start_time = time.time()
        try:
            async with session.get(f"{self.base_url}/accounts/{account_id}") as response:
                end_time = time.time()
                response_time = (end_time - start_time) * 1000
                
                if response.status == 200:
                    return {
                        'success': True,
                        'response_time': response_time,
                        'status_code': response.status
                    }
                else:
                    return {
                        'success': False,
                        'response_time': response_time,
                        'error': f"HTTP {response.status}",
                        'status_code': response.status
                    }
        except Exception as e:
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            return {
                'success': False,
                'response_time': response_time,
                'error': str(e),
                'status_code': 0
            }
    
    async def transfer_money(self, session, transfer_data):
        """Transfer money between accounts"""
        start_time = time.time()
        try:
            async with session.post(f"{self.base_url}/transactions/transfer", json=transfer_data) as response:
                end_time = time.time()
                response_time = (end_time - start_time) * 1000
                
                if response.status == 200:
                    return {
                        'success': True,
                        'response_time': response_time,
                        'status_code': response.status
                    }
                else:
                    return {
                        'success': False,
                        'response_time': response_time,
                        'error': f"HTTP {response.status}",
                        'status_code': response.status
                    }
        except Exception as e:
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            return {
                'success': False,
                'response_time': response_time,
                'error': str(e),
                'status_code': 0
            }
    
    async def deposit_money(self, session, deposit_data):
        """Deposit money to an account"""
        start_time = time.time()
        try:
            async with session.post(f"{self.base_url}/transactions/deposit", json=deposit_data) as response:
                end_time = time.time()
                response_time = (end_time - start_time) * 1000
                
                if response.status == 200:
                    return {
                        'success': True,
                        'response_time': response_time,
                        'status_code': response.status
                    }
                else:
                    return {
                        'success': False,
                        'response_time': response_time,
                        'error': f"HTTP {response.status}",
                        'status_code': response.status
                    }
        except Exception as e:
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            return {
                'success': False,
                'response_time': response_time,
                'error': str(e),
                'status_code': 0
            }
    
    async def run_concurrent_test(self, test_name, test_function, test_data, concurrency=10, duration=30, total_requests=None):
        """Run a concurrent test. If total_requests is provided, execute exactly that many requests; otherwise run for duration seconds."""
        mode_desc = f"{total_requests} total requests" if total_requests else f"{concurrency} concurrent users for {duration} seconds"
        print(f"Running {test_name} test: {mode_desc}")

        start_time = time.time()

        results = []
        failure_status_counts = {}

        async with aiohttp.ClientSession() as session:
            if total_requests:
                # Fixed-request mode using a bounded semaphore for concurrency
                semaphore = asyncio.Semaphore(concurrency)

                async def run_one(i: int):
                    nonlocal results
                    async with semaphore:
                        # Prepare payload per request
                        base_data = test_data[i % len(test_data)] if isinstance(test_data, list) else test_data
                        data = copy.deepcopy(base_data)
                        if test_function == self.create_account and isinstance(data, dict):
                            unique_suffix = f"{int(time.time()*1000)}-{i}-{uuid.uuid4().hex[:8]}"
                            if 'email' in data and isinstance(data['email'], str):
                                local, _, domain = data['email'].partition('@')
                                domain = domain or 'example.com'
                                data['email'] = f"{local}+{unique_suffix}@{domain}"
                            else:
                                data['email'] = f"test+{unique_suffix}@example.com"
                        try:
                            result = await test_function(session, data)
                            results.append(result)
                            if not result.get('success'):
                                code = result.get('status_code', 0)
                                failure_status_counts[code] = failure_status_counts.get(code, 0) + 1
                        except Exception as e:
                            results.append({'success': False, 'response_time': 0, 'error': str(e), 'status_code': 0})
                            failure_status_counts[0] = failure_status_counts.get(0, 0) + 1

                await asyncio.gather(*(run_one(i) for i in range(total_requests)))
            else:
                # Time-boxed mode (original behavior)
                end_time = start_time + duration
                tasks = []
                tasks_created = 0

                while time.time() < end_time:
                    for _ in range(concurrency):
                        base_data = test_data[len(tasks) % len(test_data)] if isinstance(test_data, list) else test_data
                        data = copy.deepcopy(base_data)
                        if test_function == self.create_account and isinstance(data, dict):
                            unique_suffix = f"{int(time.time()*1000)}-{tasks_created}-{uuid.uuid4().hex[:8]}"
                            if 'email' in data and isinstance(data['email'], str):
                                local, _, domain = data['email'].partition('@')
                                domain = domain or 'example.com'
                                data['email'] = f"{local}+{unique_suffix}@{domain}"
                            else:
                                data['email'] = f"test+{unique_suffix}@example.com"
                        task = asyncio.create_task(test_function(session, data))
                        tasks.append(task)
                        tasks_created += 1

                    if len(tasks) >= concurrency * 2:
                        completed_tasks = tasks[:concurrency]
                        tasks = tasks[concurrency:]
                        for task in completed_tasks:
                            try:
                                result = await task
                                results.append(result)
                                if not result.get('success'):
                                    code = result.get('status_code', 0)
                                    failure_status_counts[code] = failure_status_counts.get(code, 0) + 1
                            except Exception as e:
                                results.append({'success': False, 'response_time': 0, 'error': str(e), 'status_code': 0})
                                failure_status_counts[0] = failure_status_counts.get(0, 0) + 1

                for task in tasks:
                    try:
                        result = await task
                        results.append(result)
                        if not result.get('success'):
                            code = result.get('status_code', 0)
                            failure_status_counts[code] = failure_status_counts.get(code, 0) + 1
                    except Exception as e:
                        results.append({'success': False, 'response_time': 0, 'error': str(e), 'status_code': 0})
                        failure_status_counts[0] = failure_status_counts.get(0, 0) + 1
        
        # Calculate statistics
        successful_requests = [r for r in results if r['success']]
        failed_requests = [r for r in results if not r['success']]
        
        if successful_requests:
            response_times = [r['response_time'] for r in successful_requests]
            avg_response_time = statistics.mean(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            p95_response_time = statistics.quantiles(response_times, n=20)[18]  # 95th percentile
        else:
            avg_response_time = 0
            min_response_time = 0
            max_response_time = 0
            p95_response_time = 0
        
        total_requests_count = len(results)
        success_rate = len(successful_requests) / total_requests_count * 100 if total_requests_count > 0 else 0
        elapsed = max(time.time() - start_time, 1e-6)
        requests_per_second = total_requests_count / elapsed
        
        test_result = {
            'test_name': test_name,
            'duration': duration,
            'concurrency': concurrency,
            'total_requests': total_requests_count,
            'successful_requests': len(successful_requests),
            'failed_requests': len(failed_requests),
            'success_rate': success_rate,
            'requests_per_second': requests_per_second,
            'avg_response_time': avg_response_time,
            'min_response_time': min_response_time,
            'max_response_time': max_response_time,
            'p95_response_time': p95_response_time,
            'failure_status_code_counts': failure_status_counts
        }
        
        self.results['tests'].append(test_result)
        
        print(f"  Total Requests: {total_requests_count}")
        print(f"  Successful: {len(successful_requests)}")
        print(f"  Failed: {len(failed_requests)}")
        print(f"  Success Rate: {success_rate:.2f}%")
        print(f"  Requests/sec: {requests_per_second:.2f}")
        print(f"  Avg Response Time: {avg_response_time:.2f}ms")
        print(f"  Min Response Time: {min_response_time:.2f}ms")
        print(f"  Max Response Time: {max_response_time:.2f}ms")
        print(f"  95th Percentile: {p95_response_time:.2f}ms")
        print()
        
        return test_result
    
    async def setup_test_accounts(self):
        """Create two test accounts with sufficient balances and store their IDs."""
        print("Setting up test accounts...")
        async with aiohttp.ClientSession() as session:
            # Create primary account
            acc1_payload = {
                "name": "Perf Test User 1",
                "email": f"perf1+{int(time.time()*1000)}@example.com",
                "initial_balance": 10000.0
            }
            res1 = await self.create_account(session, acc1_payload)
            if not res1.get('success') or not res1.get('account_id'):
                raise RuntimeError(f"Failed to create primary account: {res1}")
            self.primary_account_id = str(res1.get('account_id'))

            # Create secondary account
            acc2_payload = {
                "name": "Perf Test User 2",
                "email": f"perf2+{int(time.time()*1000)}@example.com",
                "initial_balance": 10000.0
            }
            res2 = await self.create_account(session, acc2_payload)
            if not res2.get('success') or not res2.get('account_id'):
                raise RuntimeError(f"Failed to create secondary account: {res2}")
            self.secondary_account_id = str(res2.get('account_id'))

        print(f"Test accounts ready: primary={self.primary_account_id}, secondary={self.secondary_account_id}")

    async def run_comprehensive_test(self, requests_per_test: int | None = None, highload_requests: int | None = None):
        """Run comprehensive performance tests"""
        print(f"Starting performance tests for {self.architecture_name}")
        print("=" * 60)
        
        # Ensure we have two accounts to operate on
        await self.setup_test_accounts()

        # Test 1: Account Creation
        account_data = {
            "name": "Test User",
            "email": "test@example.com",
            "initial_balance": 1000.0
        }
        
        await self.run_concurrent_test(
            "Account Creation",
            self.create_account,
            account_data,
            concurrency=5,
            duration=30,
            total_requests=requests_per_test
        )
        
        # Test 2: Account Retrieval (use an existing created account)
        await self.run_concurrent_test(
            "Account Retrieval",
            self.get_account,
            self.primary_account_id,
            concurrency=10,
            duration=30,
            total_requests=requests_per_test
        )
        
        # Test 3: Money Transfer
        transfer_data = {
            "from_account_id": self.primary_account_id,
            "to_account_id": self.secondary_account_id,
            "amount": 100.0,
            "description": "Performance test transfer"
        }
        
        await self.run_concurrent_test(
            "Money Transfer",
            self.transfer_money,
            transfer_data,
            concurrency=5,
            duration=30,
            total_requests=requests_per_test
        )
        
        # Test 4: Money Deposit
        deposit_data = {
            "account_id": self.primary_account_id,
            "amount": 50.0,
            "description": "Performance test deposit"
        }
        
        await self.run_concurrent_test(
            "Money Deposit",
            self.deposit_money,
            deposit_data,
            concurrency=5,
            duration=30,
            total_requests=requests_per_test
        )
        
        # Test 5: High Load Test
        await self.run_concurrent_test(
            "High Load Test",
            self.get_account,
            self.primary_account_id,
            concurrency=20,
            duration=60,
            total_requests=highload_requests
        )
    
    def save_results(self, filename):
        """Save test results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Results saved to {filename}")

async def main():
    parser = argparse.ArgumentParser(description='Performance Testing for Banking System')
    parser.add_argument('--architecture', choices=['layered', 'microservice'], required=True,
                       help='Architecture to test')
    parser.add_argument('--url', default='http://localhost:3000',
                       help='Base URL for the API')
    parser.add_argument('--output', default='performance_results.json',
                       help='Output file for results')
    parser.add_argument('--requests-per-test', type=int, default=None,
                       help='If set, run exactly this many requests per test instead of time-based')
    parser.add_argument('--highload-requests', type=int, default=None,
                       help='If set, run exactly this many requests for the high load test')
    
    args = parser.parse_args()
    
    architecture_name = "Layered Architecture" if args.architecture == 'layered' else "Microservice Architecture"
    
    print(f"Testing {architecture_name}")
    print(f"API URL: {args.url}")
    print()
    
    # Check if API is accessible
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{args.url}/health") as response:
                if response.status != 200:
                    print(f"API health check failed: HTTP {response.status}")
                    sys.exit(1)
    except Exception as e:
        print(f"Cannot connect to API: {e}")
        print("Make sure the banking system is running with docker-compose up")
        sys.exit(1)
    
    # Run performance tests
    tester = PerformanceTest(args.url, architecture_name)
    await tester.run_comprehensive_test(
        requests_per_test=args.requests_per_test,
        highload_requests=args.highload_requests
    )
    
    # Save results
    output_file = f"{args.architecture}_{args.output}"
    tester.save_results(output_file)
    
    print("Performance testing completed!")

if __name__ == "__main__":
    asyncio.run(main())

