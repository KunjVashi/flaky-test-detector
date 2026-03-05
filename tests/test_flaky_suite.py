# tests/test_flaky_suite.py

# Import statements - bringing in tools we need
import time      # For adding delays/waits
import random    # For generating random numbers

# ==============================================
# STABLE TESTS (Always pass - for comparison)
# ==============================================

def test_stable_always_passes():
    """
    This test will NEVER fail
    It's testing basic math which is deterministic (always same result)
    """
    result = 10 + 5
    assert result == 15
    print("✅ Stable test passed!")


def test_stable_string():
    """Another stable test - strings behave predictably"""
    word = "testing"
    assert word.upper() == "TESTING"
    assert len(word) == 7
    print("✅ Stable string test passed!")


# ==============================================
# FLAKY TEST #1: Random Failure
# ==============================================

def test_flaky_random():
    """
    FLAKY REASON: Uses random numbers
    
    How it works:
    - random.random() gives a number between 0.0 and 1.0
    - If number > 0.5, test passes
    - If number <= 0.5, test fails
    - So it fails about 50% of the time!
    """
    random_number = random.random()  # Get random number
    
    print(f"Random number generated: {random_number}")
    
    # This assertion will fail about half the time
    assert random_number > 0.5, f"Failed! Number was {random_number}"


# ==============================================
# FLAKY TEST #2: Timing Issue (Very Common!)
# ==============================================

def test_flaky_timing():
    """
    FLAKY REASON: Simulates a timing/race condition
    
    Real-world example:
    - You click a button on a website
    - Button takes random time to respond (network, server load)
    - Sometimes button loads in time, sometimes doesn't
    """
    
    # Simulate something loading (like a webpage)
    load_time = random.uniform(0.05, 0.15)  # Random time between 50-150ms
    time.sleep(load_time)  # Wait for that amount of time
    
    # Let's say our test expects it to load in under 100ms
    max_allowed_time = 0.1  # 100 milliseconds
    
    print(f"Load time: {load_time:.3f}s, Max allowed: {max_allowed_time}s")
    
    # If load_time > 0.1, this fails
    assert load_time <= max_allowed_time, f"Too slow! Took {load_time:.3f}s"


# ==============================================
# FLAKY TEST #3: External Dependency Simulation
# ==============================================

def test_flaky_external_api():
    """
    FLAKY REASON: Simulates an unreliable external API/service
    
    Real-world example:
    - Your test calls a payment API
    - API is sometimes slow/down
    - Test fails when API is unavailable
    """
    
    # Simulate API call success rate (70% success, 30% failure)
    api_available = random.random() > 0.3  # 70% chance of True
    
    if api_available:
        print("✅ API responded successfully")
    else:
        print("❌ API timeout/unavailable")
    
    # Test fails 30% of the time when API is "down"
    assert api_available, "External API call failed!"


# ==============================================
# FLAKY TEST #4: Slightly Flaky (Rare failure)
# ==============================================

def test_slightly_flaky():
    """
    FLAKY REASON: Fails only 10% of the time
    
    This simulates a test that USUALLY works but occasionally fails
    These are the hardest to catch because they seem "mostly reliable"
    """
    
    # Only fails 10% of the time
    random_value = random.random()
    
    print(f"Value: {random_value:.3f} (fails if <= 0.1)")
    
    assert random_value > 0.1, f"Rare failure occurred! Value was {random_value:.3f}"


# ==============================================
# FLAKY TEST #5: Very Flaky (Fails often)
# ==============================================

def test_very_flaky():
    """
    FLAKY REASON: Fails 70% of the time!
    
    This simulates a really broken test
    """
    
    # Fails 70% of the time (only passes 30%)
    success = random.random() > 0.7
    
    print(f"Success rate: 30%, This run: {'PASS' if success else 'FAIL'}")
    
    assert success, "Test failed (happens 70% of the time)"


# ==============================================
# FLAKY TEST #6: Race Condition Simulation
# ==============================================

def test_flaky_race_condition():
    """
    FLAKY REASON: Simulates race condition
    
    Real-world example:
    - Two operations happen simultaneously
    - Order matters but isn't guaranteed
    - Sometimes operation A finishes first, sometimes B
    """
    
    # Simulate two tasks with random completion times
    task_a_time = random.uniform(0.01, 0.05)
    task_b_time = random.uniform(0.01, 0.05)
    
    print(f"Task A: {task_a_time:.3f}s, Task B: {task_b_time:.3f}s")
    
    # Test expects Task A to finish first, but it's random!
    assert task_a_time < task_b_time, "Race condition: Task B finished first!"