import subprocess
import time
from src.tracker import TestResultTracker

# Initialize tracker
tracker = TestResultTracker()

# Clear previous results
print("🧹 Clearing previous results...")
tracker.clear_database()

# Number of runs
NUM_RUNS = 100

print(f"\n🚀 Running flaky test suite {NUM_RUNS} times...")
print("This will take a few minutes...\n")

# Run tests multiple times
for i in range(1, NUM_RUNS + 1):
    print(f"Run {i}/{NUM_RUNS}...", end='\r')
    
    # Run pytest and capture results
    result = subprocess.run(
        ['pytest', 'tests/test_flaky_suite.py', '-v', '--tb=short'],
        capture_output=True,
        text=True
    )
    
    # Parse output and store results
    for line in result.stdout.split('\n'):
        if 'PASSED' in line or 'FAILED' in line:
            # Extract test name and result
            parts = line.split('::')
            if len(parts) >= 2:
                test_name = parts[1].split()[0]
                result_status = 'PASSED' if 'PASSED' in line else 'FAILED'
                
                # Store in database
                tracker.add_result(
                    test_name=test_name,
                    result=result_status,
                    duration=0.1,  # We'll improve this later
                    error_message=None if result_status == 'PASSED' else 'Test failed'
                )

print(f"\n✅ Completed {NUM_RUNS} runs!\n")

# Generate summary report
print("=" * 60)
print("📊 FLAKINESS DETECTION REPORT")
print("=" * 60)

summary = tracker.get_summary()

for test in summary:
    print(f"\n{test['classification']}")
    print(f"Test: {test['test_name']}")
    print(f"Flake Rate: {test['flake_rate']}%")

print("\n" + "=" * 60)