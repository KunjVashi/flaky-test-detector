import subprocess
from src.tracker import TestResultTracker
from src.analyzer import FlakyTestAnalyzer

print("=" * 80)
print("🚀 REALISTIC TEST ANALYSIS - 50 RUNS")
print("=" * 80)

# Initialize
tracker = TestResultTracker(db_path="database/realistic_results.db")
analyzer = FlakyTestAnalyzer(test_directory="tests/realistic")

# Clear previous
tracker.clear_database()

NUM_RUNS = 50

print(f"\n🔄 Running realistic test suite {NUM_RUNS} times...\n")

# Run tests
for i in range(1, NUM_RUNS + 1):
    print(f"Run {i}/{NUM_RUNS}...", end='\r')
    
    result = subprocess.run(
        ['pytest', 'tests/realistic/test_realistic_flaky.py', '-v', '--tb=short'],
        capture_output=True,
        text=True
    )
    
    # Parse results
    for line in result.stdout.split('\n'):
        if 'PASSED' in line or 'FAILED' in line:
            parts = line.split('::')
            if len(parts) >= 2:
                test_name = parts[1].split()[0]
                result_status = 'PASSED' if 'PASSED' in line else 'FAILED'
                
                tracker.add_result(
                    test_name=test_name,
                    result=result_status,
                    duration=0.1,
                    error_message=None if result_status == 'PASSED' else 'Test failed'
                )

print(f"\n✅ Completed {NUM_RUNS} runs!\n")

# Generate summary
summary = tracker.get_summary()

print("=" * 80)
print("📊 REALISTIC FLAKY TEST ANALYSIS RESULTS")
print("=" * 80)

for test in summary:
    test_name = test['test_name']
    flake_rate = test['flake_rate']
    classification = test['classification']
    
    print(f"\n{classification}")
    print(f"Test: {test_name}")
    print(f"Flake Rate: {flake_rate}%")
    
    # Get root causes
    root_causes = analyzer.get_test_root_causes(test_name, 'tests/realistic/test_realistic_flaky.py')
    
    if root_causes:
        print(f"\n🔍 ROOT CAUSE ANALYSIS:")
        
        timing = [r for r in root_causes if r['category'] == 'timing_issues']
        race = [r for r in root_causes if r['category'] == 'race_conditions']
        
        if timing:
            print(f"  ⏱️  TIMING ISSUES:")
            for issue in timing:
                print(f"    Line {issue['line']}: {issue['pattern']}")
                print(f"    💡 {issue['suggestion']}")
        
        if race:
            print(f"  🏁 RACE CONDITIONS:")
            for issue in race:
                print(f"    Line {issue['line']}: {issue['pattern']}")
                print(f"    💡 {issue['suggestion']}")
    else:
        print(f"\n✅ No obvious code patterns detected")
    
    print("\n" + "-" * 80)

# Save to file
with open('case_studies/realistic_flaky_report.txt', 'w') as f:
    f.write("REALISTIC FLAKY TEST ANALYSIS\n")
    f.write("=" * 80 + "\n\n")
    for test in summary:
        f.write(f"{test['classification']}\n")
        f.write(f"Test: {test['test_name']}\n")
        f.write(f"Flake Rate: {test['flake_rate']}%\n\n")

print("\n💾 Report saved to: case_studies/realistic_flaky_report.txt") 