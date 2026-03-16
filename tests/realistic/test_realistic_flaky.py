import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_network_flaky():
    """Flaky due to network timing - passes ~70% of the time"""
    # Simulates API call with variable response time
    start = time.time()
    time.sleep(random.uniform(0.05, 0.15))  # Variable delay
    duration = time.time() - start
    
    # Sometimes this assertion fails due to timing
    assert duration < 0.12, f"API call took {duration}s, expected < 0.12s"


def test_cache_state_flaky():
    """Flaky due to shared state - passes ~60% of the time"""
    # Simulates checking cache that may or may not exist
    cache = {}
    
    # Sometimes populate cache, sometimes don't
    if random.random() > 0.4:
        cache['user_id'] = 12345
    
    # This fails when cache isn't populated
    assert 'user_id' in cache, "Cache should contain user_id"


def test_pagination_flaky():
    """Flaky due to race condition in data loading - passes ~75% of the time"""
    # Simulates paginated results with race condition
    items = []
    
    # Simulate async data loading
    for i in range(10):
        if random.random() > 0.25:  # 75% chance each item loads
            items.append(i)
    
    # Expects all 10 items, but sometimes fewer load
    assert len(items) == 10, f"Expected 10 items, got {len(items)}"


def test_selenium_element_timing():
    """Flaky Selenium test - passes ~65% of the time"""
    # This test is intentionally flaky due to timing
    # In real world, element might not be ready
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("https://example.com")
        
        # Short wait that sometimes isn't enough
        time.sleep(random.uniform(0.1, 0.5))
        
        # This fails if page hasn't fully loaded
        h1 = driver.find_element(By.TAG_NAME, "h1")
        assert h1.text != "", "H1 should have text"
        
    except Exception as e:
        driver.quit()
        raise e
    finally:
        driver.quit()


def test_file_write_race():
    """Flaky due to file system operations - passes ~80% of the time"""
    import tempfile
    import os
    
    # Create temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_path = temp_file.name
    temp_file.close()
    
    try:
        # Write to file
        with open(temp_path, 'w') as f:
            f.write("test data")
        
        # Race condition: sometimes file isn't immediately readable
        if random.random() > 0.2:  # 80% success
            with open(temp_path, 'r') as f:
                data = f.read()
            assert data == "test data"
        else:
            # Simulate file not ready
            raise IOError("File not ready")
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_login_timeout_flaky():
    """Flaky authentication test - passes ~70% of the time"""
    # Simulates login with timeout
    login_time = random.uniform(0.5, 2.0)
    time.sleep(login_time)
    
    # Fails if login takes too long
    assert login_time < 1.5, f"Login took {login_time}s, maximum is 1.5s"


def test_stable_math_operations():
    """Stable test - always passes"""
    result = 2 + 2
    assert result == 4


def test_stable_string_concatenation():
    """Stable test - always passes"""
    text = "Hello" + " " + "World"
    assert text == "Hello World"