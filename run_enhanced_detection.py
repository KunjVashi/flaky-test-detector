import subprocess
from src.tracker import TestResultTracker
from src.analyzer import FlakyTestAnalyzer

print("=" * 80)
print("🚀 ENHANCED FLAKY TEST DETECTION & ROOT CAUSE ANALYSIS")
print("=" * 80)

# Initialize tracker and analyzer
tracker = TestResultTracker()
analyzer = FlakyTestAnalyzer(test_directory="tests")

# Clear previous results
print("\n🧹 Clearing previous results...")
tracker.clear_database()

# Number of runs
NUM_RUNS = 100

print(f"\n🔄 Running flaky test suite {NUM_RUNS} times...")
print("This will take a few minutes...\n")

# Run tests multiple times
for i in range(1, NUM_RUNS + 1):
    print(f"Run {i}/{NUM_RUNS}...", end='\r')
    
    result = subprocess.run(
        ['pytest', 'tests/test_flaky_suite.py', '-v', '--tb=short'],
        capture_output=True,
        text=True
    )
    
    # Parse and store results
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

# Get flaky test summary
summary = tracker.get_summary()

# Generate enhanced analysis
print("\n" + "=" * 80)
print("📊 ENHANCED FLAKINESS DETECTION REPORT WITH ROOT CAUSE ANALYSIS")
print("=" * 80)

for test in summary:
    test_name = test['test_name']
    flake_rate = test['flake_rate']
    classification = test['classification']
    
    print(f"\n{classification}")
    print(f"Test: {test_name}")
    print(f"Flake Rate: {flake_rate}%")
    
    # Get root cause analysis
    root_causes = analyzer.get_test_root_causes(test_name, 'tests/test_flaky_suite.py')
    
    if root_causes:
        print(f"\n🔍 ROOT CAUSE ANALYSIS:")
        
        # Group by category
        timing = [r for r in root_causes if r['category'] == 'timing_issues']
        race = [r for r in root_causes if r['category'] == 'race_conditions']
        external = [r for r in root_causes if r['category'] == 'external_dependencies']
        state = [r for r in root_causes if r['category'] == 'shared_state']
        resource = [r for r in root_causes if r['category'] == 'resource_issues']
        
        if timing:
            print(f"  ⏱️  TIMING ISSUES DETECTED:")
            for issue in timing:
                print(f"    Line {issue['line']}: {issue['pattern']}")
                print(f"    💡 Fix: {issue['suggestion']}")
        
        if race:
            print(f"  🏁 RACE CONDITIONS DETECTED:")
            for issue in race:
                print(f"    Line {issue['line']}: {issue['pattern']}")
                print(f"    💡 Fix: {issue['suggestion']}")
        
        if external:
            print(f"  🌐 EXTERNAL DEPENDENCIES DETECTED:")
            for issue in external:
                print(f"    Line {issue['line']}: {issue['pattern']}")
                print(f"    💡 Fix: {issue['suggestion']}")
        
        if state:
            print(f"  💾 SHARED STATE DETECTED:")
            for issue in state:
                print(f"    Line {issue['line']}: {issue['pattern']}")
                print(f"    💡 Fix: {issue['suggestion']}")
        
        if resource:
            print(f"  📦 RESOURCE ISSUES DETECTED:")
            for issue in resource:
                print(f"    Line {issue['line']}: {issue['pattern']}")
                print(f"    💡 Fix: {issue['suggestion']}")
    else:
        print(f"\n✅ No obvious code patterns detected - may be environmental")
    
    print("\n" + "-" * 80)

print("\n" + "=" * 80)
print("🎯 PRIORITY ACTION ITEMS:")
print("=" * 80)

# Get only flaky tests (flake_rate > 0)
flaky_tests = [t for t in summary if t['flake_rate'] > 0]

if flaky_tests:
    print(f"\n📌 Fix these {len(flaky_tests)} flaky tests in order of severity:\n")
    
    for i, test in enumerate(flaky_tests, 1):
        severity = "🔴 URGENT" if test['flake_rate'] > 60 else "🟠 HIGH" if test['flake_rate'] > 40 else "🟡 MEDIUM"
        print(f"{i}. {severity} - {test['test_name']} ({test['flake_rate']}%)")
else:
    print("\n🎉 No flaky tests detected! All tests are stable!")

print("\n" + "=" * 80)