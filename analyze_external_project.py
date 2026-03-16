#!/usr/bin/env python3
"""
Flaky Test Analyzer for External Projects
Analyzes any pytest-based project for flaky tests
"""

import subprocess
import sys
import os
from pathlib import Path
from src.tracker import TestResultTracker
from src.analyzer import FlakyTestAnalyzer
import argparse
from datetime import datetime

def analyze_project(test_directory, num_runs=50, output_file=None):
    """Analyze an external project for flaky tests."""
    
    # Validate test directory
    test_path = Path(test_directory)
    if not test_path.exists():
        print(f"❌ Error: Directory '{test_directory}' does not exist!")
        return
    
    # Find test files
    test_files = list(test_path.glob('**/test_*.py'))
    if not test_files:
        print(f"❌ Error: No test files found in '{test_directory}'!")
        return
    
    print("=" * 80)
    print("🔍 FLAKY TEST ANALYZER - EXTERNAL PROJECT MODE")
    print("=" * 80)
    print(f"\n📂 Target Directory: {test_directory}")
    print(f"📝 Test Files Found: {len(test_files)}")
    print(f"🔄 Runs per Test: {num_runs}")
    print(f"\n⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "=" * 80)
    
    # Initialize tracker with unique DB for this project
    project_name = Path(test_directory).name
    db_path = f"database/{project_name}_results.db"
    tracker = TestResultTracker(db_path=db_path)
    tracker.clear_database()
    
    # Initialize analyzer
    analyzer = FlakyTestAnalyzer(test_directory=str(test_path))
    
    print(f"\n🚀 Running tests {num_runs} times...")
    print("⏳ This may take several minutes...\n")
    
    # Run tests multiple times
    for i in range(1, num_runs + 1):
        print(f"Run {i}/{num_runs}...", end='\r')
        
        # Run pytest on the test directory
        result = subprocess.run(
            ['pytest', str(test_path), '-v', '--tb=no', '-q'],
            capture_output=True,
            text=True,
            cwd=test_path.parent  # Run from parent directory
        )
        
        # Parse results
        for line in result.stdout.split('\n'):
            if 'PASSED' in line or 'FAILED' in line:
                # Try to extract test name
                if '::' in line:
                    parts = line.split('::')
                    if len(parts) >= 2:
                        test_name = parts[-1].split()[0]
                        result_status = 'PASSED' if 'PASSED' in line else 'FAILED'
                        
                        tracker.add_result(
                            test_name=test_name,
                            result=result_status,
                            duration=0.1,
                            error_message=None if result_status == 'PASSED' else 'Failed'
                        )
    
    print(f"\n✅ Completed {num_runs} runs!")
    
    # Generate summary
    summary = tracker.get_summary()
    
    # Generate report
    report_lines = []
    report_lines.append("\n" + "=" * 80)
    report_lines.append("📊 FLAKINESS DETECTION REPORT")
    report_lines.append("=" * 80)
    report_lines.append(f"\nProject: {project_name}")
    report_lines.append(f"Test Directory: {test_directory}")
    report_lines.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"Runs per Test: {num_runs}")
    report_lines.append(f"\nTotal Unique Tests: {len(summary)}")
    
    # Count flaky tests
    flaky_tests = [t for t in summary if t['flake_rate'] > 0]
    stable_tests = [t for t in summary if t['flake_rate'] == 0]
    
    report_lines.append(f"Flaky Tests: {len(flaky_tests)}")
    report_lines.append(f"Stable Tests: {len(stable_tests)}")
    
    if flaky_tests:
        flakiness_percentage = (len(flaky_tests) / len(summary)) * 100
        report_lines.append(f"Flakiness Rate: {flakiness_percentage:.2f}%")
    
    report_lines.append("\n" + "=" * 80)
    report_lines.append("🔍 DETAILED RESULTS")
    report_lines.append("=" * 80)
    
    # Show only flaky tests with root causes
    if flaky_tests:
        for test in flaky_tests:
            test_name = test['test_name']
            flake_rate = test['flake_rate']
            classification = test['classification']
            
            report_lines.append(f"\n{classification}")
            report_lines.append(f"Test: {test_name}")
            report_lines.append(f"Flake Rate: {flake_rate}%")
            
            # Try to find root causes
            # Find which file contains this test
            test_file = None
            for tf in test_files:
                with open(tf, 'r') as f:
                    if f'def {test_name}' in f.read():
                        test_file = tf
                        break
            
            if test_file:
                root_causes = analyzer.get_test_root_causes(test_name, str(test_file))
                
                if root_causes:
                    report_lines.append(f"\n🔍 ROOT CAUSE ANALYSIS:")
                    report_lines.append(f"File: {test_file.relative_to(test_path.parent)}")
                    
                    # Group by category
                    timing = [r for r in root_causes if r['category'] == 'timing_issues']
                    race = [r for r in root_causes if r['category'] == 'race_conditions']
                    external = [r for r in root_causes if r['category'] == 'external_dependencies']
                    state = [r for r in root_causes if r['category'] == 'shared_state']
                    resource = [r for r in root_causes if r['category'] == 'resource_issues']
                    
                    if timing:
                        report_lines.append(f"  ⏱️  TIMING ISSUES:")
                        for issue in timing:
                            report_lines.append(f"    Line {issue['line']}: {issue['pattern']}")
                            report_lines.append(f"    💡 {issue['suggestion']}")
                    
                    if race:
                        report_lines.append(f"  🏁 RACE CONDITIONS:")
                        for issue in race:
                            report_lines.append(f"    Line {issue['line']}: {issue['pattern']}")
                            report_lines.append(f"    💡 {issue['suggestion']}")
                    
                    if external:
                        report_lines.append(f"  🌐 EXTERNAL DEPENDENCIES:")
                        for issue in external:
                            report_lines.append(f"    Line {issue['line']}: {issue['pattern']}")
                            report_lines.append(f"    💡 {issue['suggestion']}")
                    
                    if state:
                        report_lines.append(f"  💾 SHARED STATE:")
                        for issue in state:
                            report_lines.append(f"    Line {issue['line']}: {issue['pattern']}")
                            report_lines.append(f"    💡 {issue['suggestion']}")
                    
                    if resource:
                        report_lines.append(f"  📦 RESOURCE ISSUES:")
                        for issue in resource:
                            report_lines.append(f"    Line {issue['line']}: {issue['pattern']}")
                            report_lines.append(f"    💡 {issue['suggestion']}")
                else:
                    report_lines.append(f"\n✅ No obvious code patterns - may be environmental")
            
            report_lines.append("\n" + "-" * 80)
    else:
        report_lines.append("\n🎉 No flaky tests detected! All tests are stable!")
    
    # Priority action items
    if flaky_tests:
        report_lines.append("\n" + "=" * 80)
        report_lines.append("🎯 PRIORITY ACTION ITEMS")
        report_lines.append("=" * 80)
        report_lines.append(f"\n📌 Fix these {len(flaky_tests)} flaky tests in order of severity:\n")
        
        for i, test in enumerate(flaky_tests, 1):
            severity = "🔴 URGENT" if test['flake_rate'] > 60 else "🟠 HIGH" if test['flake_rate'] > 40 else "🟡 MEDIUM" if test['flake_rate'] > 10 else "⚠️  LOW"
            report_lines.append(f"{i}. {severity} - {test['test_name']} ({test['flake_rate']}%)")
    
    report_lines.append("\n" + "=" * 80)
    
    # Print to console
    report_text = '\n'.join(report_lines)
    print(report_text)
    
    # Save to file
    if output_file:
        with open(output_file, 'w') as f:
            f.write(report_text)
        print(f"\n💾 Report saved to: {output_file}")
    
    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze external projects for flaky tests')
    parser.add_argument('test_dir', help='Directory containing test files')
    parser.add_argument('--runs', type=int, default=50, help='Number of times to run each test (default: 50)')
    parser.add_argument('--output', help='Output file for report (optional)')
    
    args = parser.parse_args()
    
    analyze_project(args.test_dir, args.runs, args.output)