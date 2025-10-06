#!/usr/bin/env python3
"""
Results Comparison Script for Banking System Performance Testing
Compares performance results between Layered and Microservice architectures
"""

import json
import argparse
import sys
from datetime import datetime

class ResultsComparator:
    def __init__(self, layered_file, microservice_file):
        self.layered_file = layered_file
        self.microservice_file = microservice_file
        self.layered_data = None
        self.microservice_data = None
    
    def load_results(self):
        """Load performance results from JSON files"""
        try:
            with open(self.layered_file, 'r') as f:
                self.layered_data = json.load(f)
            print(f"Loaded layered results from {self.layered_file}")
        except FileNotFoundError:
            print(f"Error: Layered results file {self.layered_file} not found")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {self.layered_file}: {e}")
            sys.exit(1)
        
        try:
            with open(self.microservice_file, 'r') as f:
                self.microservice_data = json.load(f)
            print(f"Loaded microservice results from {self.microservice_file}")
        except FileNotFoundError:
            print(f"Error: Microservice results file {self.microservice_file} not found")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {self.microservice_file}: {e}")
            sys.exit(1)
    
    def compare_test_results(self, test_name, layered_test, microservice_test):
        """Compare results for a specific test"""
        print(f"\n{test_name} Comparison:")
        print("=" * 50)
        
        # Extract metrics
        layered_metrics = {
            'total_requests': layered_test.get('total_requests', 0),
            'successful_requests': layered_test.get('successful_requests', 0),
            'failed_requests': layered_test.get('failed_requests', 0),
            'success_rate': layered_test.get('success_rate', 0),
            'requests_per_second': layered_test.get('requests_per_second', 0),
            'avg_response_time': layered_test.get('avg_response_time', 0),
            'min_response_time': layered_test.get('min_response_time', 0),
            'max_response_time': layered_test.get('max_response_time', 0),
            'p95_response_time': layered_test.get('p95_response_time', 0)
        }
        
        microservice_metrics = {
            'total_requests': microservice_test.get('total_requests', 0),
            'successful_requests': microservice_test.get('successful_requests', 0),
            'failed_requests': microservice_test.get('failed_requests', 0),
            'success_rate': microservice_test.get('success_rate', 0),
            'requests_per_second': microservice_test.get('requests_per_second', 0),
            'avg_response_time': microservice_test.get('avg_response_time', 0),
            'min_response_time': microservice_test.get('min_response_time', 0),
            'max_response_time': microservice_test.get('max_response_time', 0),
            'p95_response_time': microservice_test.get('p95_response_time', 0)
        }
        
        # Print comparison table
        print(f"{'Metric':<25} {'Layered':<15} {'Microservice':<15} {'Winner':<15}")
        print("-" * 70)
        
        metrics_to_compare = [
            ('Total Requests', 'total_requests', 'higher'),
            ('Successful Requests', 'successful_requests', 'higher'),
            ('Success Rate (%)', 'success_rate', 'higher'),
            ('Requests/sec', 'requests_per_second', 'higher'),
            ('Avg Response Time (ms)', 'avg_response_time', 'lower'),
            ('Min Response Time (ms)', 'min_response_time', 'lower'),
            ('Max Response Time (ms)', 'max_response_time', 'lower'),
            ('95th Percentile (ms)', 'p95_response_time', 'lower')
        ]
        
        winners = {'Layered': 0, 'Microservice': 0, 'Tie': 0}
        
        for metric_name, metric_key, better_direction in metrics_to_compare:
            layered_val = layered_metrics[metric_key]
            microservice_val = microservice_metrics[metric_key]
            
            if better_direction == 'higher':
                if layered_val > microservice_val:
                    winner = 'Layered'
                elif microservice_val > layered_val:
                    winner = 'Microservice'
                else:
                    winner = 'Tie'
            else:  # lower is better
                if layered_val < microservice_val:
                    winner = 'Layered'
                elif microservice_val < layered_val:
                    winner = 'Microservice'
                else:
                    winner = 'Tie'
            
            winners[winner] += 1
            
            print(f"{metric_name:<25} {layered_val:<15.2f} {microservice_val:<15.2f} {winner:<15}")
        
        # Overall winner for this test
        if winners['Layered'] > winners['Microservice']:
            test_winner = 'Layered Architecture'
        elif winners['Microservice'] > winners['Layered']:
            test_winner = 'Microservice Architecture'
        else:
            test_winner = 'Tie'
        
        print(f"\nTest Winner: {test_winner}")
        return test_winner
    
    def generate_summary_report(self):
        """Generate a comprehensive summary report"""
        print("\n" + "=" * 80)
        print("PERFORMANCE COMPARISON SUMMARY")
        print("=" * 80)
        
        print(f"\nTest Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Layered Architecture Results: {self.layered_file}")
        print(f"Microservice Architecture Results: {self.microservice_file}")
        
        # Get test names from both architectures
        layered_tests = {test['test_name']: test for test in self.layered_data.get('tests', [])}
        microservice_tests = {test['test_name']: test for test in self.microservice_data.get('tests', [])}
        
        all_test_names = set(layered_tests.keys()) | set(microservice_tests.keys())
        
        if not all_test_names:
            print("\nNo test results found in either file.")
            return
        
        test_winners = {}
        
        for test_name in sorted(all_test_names):
            if test_name in layered_tests and test_name in microservice_tests:
                winner = self.compare_test_results(test_name, layered_tests[test_name], microservice_tests[test_name])
                test_winners[test_name] = winner
            else:
                print(f"\n{test_name}:")
                print("=" * 50)
                if test_name in layered_tests:
                    print("Only Layered Architecture results available")
                else:
                    print("Only Microservice Architecture results available")
        
        # Overall winner
        print("\n" + "=" * 80)
        print("OVERALL PERFORMANCE WINNER")
        print("=" * 80)
        
        if test_winners:
            layered_wins = sum(1 for winner in test_winners.values() if winner == 'Layered Architecture')
            microservice_wins = sum(1 for winner in test_winners.values() if winner == 'Microservice Architecture')
            ties = sum(1 for winner in test_winners.values() if winner == 'Tie')
            
            print(f"Layered Architecture wins: {layered_wins}")
            print(f"Microservice Architecture wins: {microservice_wins}")
            print(f"Ties: {ties}")
            
            if layered_wins > microservice_wins:
                overall_winner = "Layered Architecture"
            elif microservice_wins > layered_wins:
                overall_winner = "Microservice Architecture"
            else:
                overall_winner = "Tie - Both architectures perform similarly"
            
            print(f"\nOverall Winner: {overall_winner}")
        else:
            print("No comparable test results found.")
    
    def save_comparison_report(self, output_file):
        """Save comparison report to file"""
        report = {
            'comparison_date': datetime.now().isoformat(),
            'layered_file': self.layered_file,
            'microservice_file': self.microservice_file,
            'summary': {}
        }
        
        # Generate summary statistics
        layered_tests = {test['test_name']: test for test in self.layered_data.get('tests', [])}
        microservice_tests = {test['test_name']: test for test in self.microservice_data.get('tests', [])}
        
        for test_name in set(layered_tests.keys()) | set(microservice_tests.keys()):
            if test_name in layered_tests and test_name in microservice_tests:
                layered_test = layered_tests[test_name]
                microservice_test = microservice_tests[test_name]
                
                # Calculate performance ratios
                throughput_ratio = microservice_test.get('requests_per_second', 0) / layered_test.get('requests_per_second', 1)
                latency_ratio = microservice_test.get('avg_response_time', 0) / layered_test.get('avg_response_time', 1)
                
                report['summary'][test_name] = {
                    'layered_throughput': layered_test.get('requests_per_second', 0),
                    'microservice_throughput': microservice_test.get('requests_per_second', 0),
                    'throughput_ratio': throughput_ratio,
                    'layered_latency': layered_test.get('avg_response_time', 0),
                    'microservice_latency': microservice_test.get('avg_response_time', 0),
                    'latency_ratio': latency_ratio
                }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\nComparison report saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Compare Banking System Performance Results')
    parser.add_argument('--layered', required=True, help='Layered architecture results file')
    parser.add_argument('--microservice', required=True, help='Microservice architecture results file')
    parser.add_argument('--output', default='comparison_report.json', help='Output file for comparison report')
    
    args = parser.parse_args()
    
    print("Banking System Performance Comparison")
    print("=" * 50)
    
    comparator = ResultsComparator(args.layered, args.microservice)
    comparator.load_results()
    comparator.generate_summary_report()
    comparator.save_comparison_report(args.output)
    
    print("\nComparison completed successfully!")

if __name__ == "__main__":
    main()