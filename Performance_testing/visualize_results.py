#!/usr/bin/env python3
"""
Performance Results Visualization
Creates comprehensive visualizations for banking system performance test results
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
import argparse
import sys

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class PerformanceVisualizer:
    def __init__(self, layered_file, microservice_file, comparison_file=None):
        self.layered_file = layered_file
        self.microservice_file = microservice_file
        self.comparison_file = comparison_file
        self.layered_data = None
        self.microservice_data = None
        self.comparison_data = None
    
    def load_data(self):
        """Load all performance data"""
        try:
            with open(self.layered_file, 'r') as f:
                self.layered_data = json.load(f)
            print(f"Loaded layered results from {self.layered_file}")
        except FileNotFoundError:
            print(f"Error: Layered results file {self.layered_file} not found")
            sys.exit(1)
        
        try:
            with open(self.microservice_file, 'r') as f:
                self.microservice_data = json.load(f)
            print(f"Loaded microservice results from {self.microservice_file}")
        except FileNotFoundError:
            print(f"Error: Microservice results file {self.microservice_file} not found")
            sys.exit(1)
        
        if self.comparison_file:
            try:
                with open(self.comparison_file, 'r') as f:
                    self.comparison_data = json.load(f)
                print(f"Loaded comparison data from {self.comparison_file}")
            except FileNotFoundError:
                print(f"Warning: Comparison file {self.comparison_file} not found")
    
    def create_throughput_comparison(self):
        """Create throughput comparison chart"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Extract test names and throughput data
        test_names = []
        layered_throughput = []
        microservice_throughput = []
        
        layered_tests = {test['test_name']: test for test in self.layered_data.get('tests', [])}
        microservice_tests = {test['test_name']: test for test in self.microservice_data.get('tests', [])}
        
        for test_name in sorted(set(layered_tests.keys()) | set(microservice_tests.keys())):
            if test_name in layered_tests and test_name in microservice_tests:
                test_names.append(test_name)
                layered_throughput.append(layered_tests[test_name].get('requests_per_second', 0))
                microservice_throughput.append(microservice_tests[test_name].get('requests_per_second', 0))
        
        x = np.arange(len(test_names))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, layered_throughput, width, label='Layered Architecture', alpha=0.8)
        bars2 = ax.bar(x + width/2, microservice_throughput, width, label='Microservice Architecture', alpha=0.8)
        
        ax.set_xlabel('Test Type')
        ax.set_ylabel('Requests per Second')
        ax.set_title('Throughput Comparison: Layered vs Microservice Architecture')
        ax.set_xticks(x)
        ax.set_xticklabels(test_names, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=8)
        
        for bar in bars2:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        plt.savefig('throughput_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_latency_comparison(self):
        """Create latency comparison chart"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Extract test names and latency data
        test_names = []
        layered_avg_latency = []
        microservice_avg_latency = []
        layered_p95_latency = []
        microservice_p95_latency = []
        
        layered_tests = {test['test_name']: test for test in self.layered_data.get('tests', [])}
        microservice_tests = {test['test_name']: test for test in self.microservice_data.get('tests', [])}
        
        for test_name in sorted(set(layered_tests.keys()) | set(microservice_tests.keys())):
            if test_name in layered_tests and test_name in microservice_tests:
                test_names.append(test_name)
                layered_avg_latency.append(layered_tests[test_name].get('avg_response_time', 0))
                microservice_avg_latency.append(microservice_tests[test_name].get('avg_response_time', 0))
                layered_p95_latency.append(layered_tests[test_name].get('p95_response_time', 0))
                microservice_p95_latency.append(microservice_tests[test_name].get('p95_response_time', 0))
        
        x = np.arange(len(test_names))
        width = 0.2
        
        bars1 = ax.bar(x - 1.5*width, layered_avg_latency, width, label='Layered (Avg)', alpha=0.8)
        bars2 = ax.bar(x - 0.5*width, microservice_avg_latency, width, label='Microservice (Avg)', alpha=0.8)
        bars3 = ax.bar(x + 0.5*width, layered_p95_latency, width, label='Layered (P95)', alpha=0.8)
        bars4 = ax.bar(x + 1.5*width, microservice_p95_latency, width, label='Microservice (P95)', alpha=0.8)
        
        ax.set_xlabel('Test Type')
        ax.set_ylabel('Response Time (ms)')
        ax.set_title('Latency Comparison: Layered vs Microservice Architecture')
        ax.set_xticks(x)
        ax.set_xticklabels(test_names, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('latency_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_success_rate_comparison(self):
        """Create success rate comparison chart"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        test_names = []
        layered_success = []
        microservice_success = []
        
        layered_tests = {test['test_name']: test for test in self.layered_data.get('tests', [])}
        microservice_tests = {test['test_name']: test for test in self.microservice_data.get('tests', [])}
        
        for test_name in sorted(set(layered_tests.keys()) | set(microservice_tests.keys())):
            if test_name in layered_tests and test_name in microservice_tests:
                test_names.append(test_name)
                layered_success.append(layered_tests[test_name].get('success_rate', 0))
                microservice_success.append(microservice_tests[test_name].get('success_rate', 0))
        
        x = np.arange(len(test_names))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, layered_success, width, label='Layered Architecture', alpha=0.8)
        bars2 = ax.bar(x + width/2, microservice_success, width, label='Microservice Architecture', alpha=0.8)
        
        ax.set_xlabel('Test Type')
        ax.set_ylabel('Success Rate (%)')
        ax.set_title('Success Rate Comparison: Layered vs Microservice Architecture')
        ax.set_xticks(x)
        ax.set_xticklabels(test_names, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 105)
        
        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}%',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=8)
        
        for bar in bars2:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}%',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        plt.savefig('success_rate_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_performance_radar_chart(self):
        """Create radar chart comparing overall performance"""
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # Normalize metrics for radar chart (0-1 scale)
        test_names = []
        layered_metrics = []
        microservice_metrics = []
        
        layered_tests = {test['test_name']: test for test in self.layered_data.get('tests', [])}
        microservice_tests = {test['test_name']: test for test in self.microservice_data.get('tests', [])}
        
        # Calculate normalized scores for each test
        for test_name in sorted(set(layered_tests.keys()) | set(microservice_tests.keys())):
            if test_name in layered_tests and test_name in microservice_tests:
                layered_test = layered_tests[test_name]
                microservice_test = microservice_tests[test_name]
                
                # Calculate composite score (throughput + success rate - normalized latency)
                layered_score = (
                    layered_test.get('requests_per_second', 0) / 200 +  # Normalize throughput
                    layered_test.get('success_rate', 0) / 100 +  # Success rate
                    (1000 - layered_test.get('avg_response_time', 0)) / 1000  # Inverted latency
                ) / 3
                
                microservice_score = (
                    microservice_test.get('requests_per_second', 0) / 200 +
                    microservice_test.get('success_rate', 0) / 100 +
                    (1000 - microservice_test.get('avg_response_time', 0)) / 1000
                ) / 3
                
                test_names.append(test_name)
                layered_metrics.append(layered_score)
                microservice_metrics.append(microservice_score)
        
        # Create radar chart
        angles = np.linspace(0, 2 * np.pi, len(test_names), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        layered_metrics += layered_metrics[:1]
        microservice_metrics += microservice_metrics[:1]
        
        ax.plot(angles, layered_metrics, 'o-', linewidth=2, label='Layered Architecture', color='blue')
        ax.fill(angles, layered_metrics, alpha=0.25, color='blue')
        ax.plot(angles, microservice_metrics, 'o-', linewidth=2, label='Microservice Architecture', color='red')
        ax.fill(angles, microservice_metrics, alpha=0.25, color='red')
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(test_names)
        ax.set_ylim(0, 1)
        ax.set_title('Overall Performance Radar Chart', size=16, pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        ax.grid(True)
        
        plt.tight_layout()
        plt.savefig('performance_radar.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_throughput_ratio_chart(self):
        """Create chart showing throughput ratios from comparison data"""
        if not self.comparison_data:
            print("No comparison data available for ratio chart")
            return
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        test_names = []
        throughput_ratios = []
        latency_ratios = []
        
        summary = self.comparison_data.get('summary', {})
        for test_name, data in summary.items():
            test_names.append(test_name)
            throughput_ratios.append(data.get('throughput_ratio', 1))
            latency_ratios.append(data.get('latency_ratio', 1))
        
        x = np.arange(len(test_names))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, throughput_ratios, width, label='Throughput Ratio (Microservice/Layered)', alpha=0.8)
        bars2 = ax.bar(x + width/2, latency_ratios, width, label='Latency Ratio (Microservice/Layered)', alpha=0.8)
        
        ax.set_xlabel('Test Type')
        ax.set_ylabel('Ratio')
        ax.set_title('Performance Ratios: Microservice vs Layered Architecture')
        ax.set_xticks(x)
        ax.set_xticklabels(test_names, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.axhline(y=1, color='black', linestyle='--', alpha=0.5, label='Equal Performance')
        
        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=8)
        
        for bar in bars2:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        plt.savefig('performance_ratios.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_comprehensive_dashboard(self):
        """Create a comprehensive dashboard with all visualizations"""
        fig = plt.figure(figsize=(20, 16))
        
        # Create a grid layout
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Throughput comparison (top left)
        ax1 = fig.add_subplot(gs[0, 0])
        self._plot_throughput_bars(ax1)
        
        # 2. Latency comparison (top middle)
        ax2 = fig.add_subplot(gs[0, 1])
        self._plot_latency_bars(ax2)
        
        # 3. Success rate comparison (top right)
        ax3 = fig.add_subplot(gs[0, 2])
        self._plot_success_rate_bars(ax3)
        
        # 4. Performance radar chart (middle row, spanning 2 columns)
        ax4 = fig.add_subplot(gs[1, :2], projection='polar')
        self._plot_radar_chart(ax4)
        
        # 5. Performance ratios (middle right)
        ax5 = fig.add_subplot(gs[1, 2])
        self._plot_ratios(ax5)
        
        # 6. Summary statistics (bottom row, spanning all columns)
        ax6 = fig.add_subplot(gs[2, :])
        self._plot_summary_table(ax6)
        
        plt.suptitle('Banking System Performance Analysis Dashboard', fontsize=20, y=0.98)
        plt.savefig('performance_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def _plot_throughput_bars(self, ax):
        """Helper method for throughput bars"""
        test_names = []
        layered_throughput = []
        microservice_throughput = []
        
        layered_tests = {test['test_name']: test for test in self.layered_data.get('tests', [])}
        microservice_tests = {test['test_name']: test for test in self.microservice_data.get('tests', [])}
        
        for test_name in sorted(set(layered_tests.keys()) | set(microservice_tests.keys())):
            if test_name in layered_tests and test_name in microservice_tests:
                test_names.append(test_name)
                layered_throughput.append(layered_tests[test_name].get('requests_per_second', 0))
                microservice_throughput.append(microservice_tests[test_name].get('requests_per_second', 0))
        
        x = np.arange(len(test_names))
        width = 0.35
        
        ax.bar(x - width/2, layered_throughput, width, label='Layered', alpha=0.8)
        ax.bar(x + width/2, microservice_throughput, width, label='Microservice', alpha=0.8)
        
        ax.set_title('Throughput Comparison')
        ax.set_ylabel('Requests/sec')
        ax.set_xticks(x)
        ax.set_xticklabels(test_names, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_latency_bars(self, ax):
        """Helper method for latency bars"""
        test_names = []
        layered_latency = []
        microservice_latency = []
        
        layered_tests = {test['test_name']: test for test in self.layered_data.get('tests', [])}
        microservice_tests = {test['test_name']: test for test in self.microservice_data.get('tests', [])}
        
        for test_name in sorted(set(layered_tests.keys()) | set(microservice_tests.keys())):
            if test_name in layered_tests and test_name in microservice_tests:
                test_names.append(test_name)
                layered_latency.append(layered_tests[test_name].get('avg_response_time', 0))
                microservice_latency.append(microservice_tests[test_name].get('avg_response_time', 0))
        
        x = np.arange(len(test_names))
        width = 0.35
        
        ax.bar(x - width/2, layered_latency, width, label='Layered', alpha=0.8)
        ax.bar(x + width/2, microservice_latency, width, label='Microservice', alpha=0.8)
        
        ax.set_title('Average Latency Comparison')
        ax.set_ylabel('Response Time (ms)')
        ax.set_xticks(x)
        ax.set_xticklabels(test_names, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_success_rate_bars(self, ax):
        """Helper method for success rate bars"""
        test_names = []
        layered_success = []
        microservice_success = []
        
        layered_tests = {test['test_name']: test for test in self.layered_data.get('tests', [])}
        microservice_tests = {test['test_name']: test for test in self.microservice_data.get('tests', [])}
        
        for test_name in sorted(set(layered_tests.keys()) | set(microservice_tests.keys())):
            if test_name in layered_tests and test_name in microservice_tests:
                test_names.append(test_name)
                layered_success.append(layered_tests[test_name].get('success_rate', 0))
                microservice_success.append(microservice_tests[test_name].get('success_rate', 0))
        
        x = np.arange(len(test_names))
        width = 0.35
        
        ax.bar(x - width/2, layered_success, width, label='Layered', alpha=0.8)
        ax.bar(x + width/2, microservice_success, width, label='Microservice', alpha=0.8)
        
        ax.set_title('Success Rate Comparison')
        ax.set_ylabel('Success Rate (%)')
        ax.set_xticks(x)
        ax.set_xticklabels(test_names, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 105)
    
    def _plot_radar_chart(self, ax):
        """Helper method for radar chart"""
        test_names = []
        layered_metrics = []
        microservice_metrics = []
        
        layered_tests = {test['test_name']: test for test in self.layered_data.get('tests', [])}
        microservice_tests = {test['test_name']: test for test in self.microservice_data.get('tests', [])}
        
        for test_name in sorted(set(layered_tests.keys()) | set(microservice_tests.keys())):
            if test_name in layered_tests and test_name in microservice_tests:
                layered_test = layered_tests[test_name]
                microservice_test = microservice_tests[test_name]
                
                layered_score = (
                    layered_test.get('requests_per_second', 0) / 200 +
                    layered_test.get('success_rate', 0) / 100 +
                    (1000 - layered_test.get('avg_response_time', 0)) / 1000
                ) / 3
                
                microservice_score = (
                    microservice_test.get('requests_per_second', 0) / 200 +
                    microservice_test.get('success_rate', 0) / 100 +
                    (1000 - microservice_test.get('avg_response_time', 0)) / 1000
                ) / 3
                
                test_names.append(test_name)
                layered_metrics.append(layered_score)
                microservice_metrics.append(microservice_score)
        
        angles = np.linspace(0, 2 * np.pi, len(test_names), endpoint=False).tolist()
        angles += angles[:1]
        
        layered_metrics += layered_metrics[:1]
        microservice_metrics += microservice_metrics[:1]
        
        ax.plot(angles, layered_metrics, 'o-', linewidth=2, label='Layered', color='blue')
        ax.fill(angles, layered_metrics, alpha=0.25, color='blue')
        ax.plot(angles, microservice_metrics, 'o-', linewidth=2, label='Microservice', color='red')
        ax.fill(angles, microservice_metrics, alpha=0.25, color='red')
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(test_names)
        ax.set_ylim(0, 1)
        ax.set_title('Performance Radar Chart')
        ax.legend()
        ax.grid(True)
    
    def _plot_ratios(self, ax):
        """Helper method for performance ratios"""
        if not self.comparison_data:
            ax.text(0.5, 0.5, 'No comparison data', ha='center', va='center', transform=ax.transAxes)
            return
        
        test_names = []
        throughput_ratios = []
        
        summary = self.comparison_data.get('summary', {})
        for test_name, data in summary.items():
            test_names.append(test_name)
            throughput_ratios.append(data.get('throughput_ratio', 1))
        
        x = np.arange(len(test_names))
        colors = ['green' if ratio > 1 else 'red' for ratio in throughput_ratios]
        
        bars = ax.bar(x, throughput_ratios, color=colors, alpha=0.7)
        ax.set_title('Throughput Ratios\n(Microservice/Layered)')
        ax.set_ylabel('Ratio')
        ax.set_xticks(x)
        ax.set_xticklabels(test_names, rotation=45, ha='right')
        ax.axhline(y=1, color='black', linestyle='--', alpha=0.5)
        ax.grid(True, alpha=0.3)
        
        for i, (bar, ratio) in enumerate(zip(bars, throughput_ratios)):
            ax.annotate(f'{ratio:.2f}',
                       xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=8)
    
    def _plot_summary_table(self, ax):
        """Helper method for summary table"""
        ax.axis('off')
        
        # Create summary data
        layered_tests = {test['test_name']: test for test in self.layered_data.get('tests', [])}
        microservice_tests = {test['test_name']: test for test in self.microservice_data.get('tests', [])}
        
        table_data = []
        for test_name in sorted(set(layered_tests.keys()) | set(microservice_tests.keys())):
            if test_name in layered_tests and test_name in microservice_tests:
                layered = layered_tests[test_name]
                microservice = microservice_tests[test_name]
                
                table_data.append([
                    test_name,
                    f"{layered.get('requests_per_second', 0):.1f}",
                    f"{microservice.get('requests_per_second', 0):.1f}",
                    f"{layered.get('avg_response_time', 0):.1f}",
                    f"{microservice.get('avg_response_time', 0):.1f}",
                    f"{layered.get('success_rate', 0):.1f}%",
                    f"{microservice.get('success_rate', 0):.1f}%"
                ])
        
        headers = ['Test', 'Layered RPS', 'Microservice RPS', 'Layered Latency (ms)', 'Microservice Latency (ms)', 'Layered Success %', 'Microservice Success %']
        
        table = ax.table(cellText=table_data, colLabels=headers, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1.2, 1.5)
        
        # Style the table
        for i in range(len(headers)):
            table[(0, i)].set_facecolor('#40466e')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        ax.set_title('Performance Summary Table', fontsize=14, pad=20)

def main():
    parser = argparse.ArgumentParser(description='Visualize Banking System Performance Results')
    parser.add_argument('--layered', required=True, help='Layered architecture results file')
    parser.add_argument('--microservice', required=True, help='Microservice architecture results file')
    parser.add_argument('--comparison', help='Comparison report file')
    parser.add_argument('--dashboard', action='store_true', help='Create comprehensive dashboard')
    
    args = parser.parse_args()
    
    print("Banking System Performance Visualization")
    print("=" * 50)
    
    visualizer = PerformanceVisualizer(args.layered, args.microservice, args.comparison)
    visualizer.load_data()
    
    if args.dashboard:
        print("Creating comprehensive dashboard...")
        visualizer.create_comprehensive_dashboard()
    else:
        print("Creating individual visualizations...")
        visualizer.create_throughput_comparison()
        visualizer.create_latency_comparison()
        visualizer.create_success_rate_comparison()
        visualizer.create_performance_radar_chart()
        
        if args.comparison:
            visualizer.create_throughput_ratio_chart()
    
    print("\nVisualization completed! Check the generated PNG files.")

if __name__ == "__main__":
    main()
