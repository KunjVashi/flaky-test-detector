# tests/test_real_world_flaky.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pytest

# ==============================================
# SETUP: This runs before each test
# ==============================================

@pytest.fixture
def driver():
    """
    This fixture creates a browser for each test
    'yield' means: set up browser, run test, then clean up
    """
    # Create Chrome browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    # Maximize window (some tests fail on small windows!)
    driver.maximize_window()
    
    # Give the test access to the driver
    yield driver
    
    # After test finishes, close browser
    driver.quit()


# ==============================================
# REAL-WORLD FLAKY TEST #1: Dynamic Loading
# ==============================================

def test_flaky_dynamic_loading(driver):
    """
    REAL FLAKY SCENARIO: Element appears after a delay
    
    Real-world examples:
    - Loading spinners
    - Lazy-loaded content
    - Content that appears after API call
    """
    
    # Go to page with dynamic loading
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")
    print("📍 Opened dynamic loading page")
    
    # Click the Start button
    start_button = driver.find_element(By.CSS_SELECTOR, "#start button")
    start_button.click()
    print("🖱️  Clicked Start button")
    
    # BAD APPROACH: Fixed wait (FLAKY!)
    time.sleep(3)  # Wait 3 seconds
    
    # Try to find the text that appears
    try:
        result = driver.find_element(By.ID, "finish")
        print(f"✅ Found text: {result.text}")
        assert result.text == "Hello World!"
    except:
        print("❌ Element not found yet! (Test failed)")
        raise
    
    # WHY FLAKY: Sometimes loads in 2 seconds, sometimes 4 seconds
    # Our fixed 3-second wait isn't always enough!


# ==============================================
# REAL-WORLD FLAKY TEST #2: Button Click Timing
# ==============================================

def test_flaky_add_remove_elements(driver):
    """
    REAL FLAKY SCENARIO: Click button, check if element appears
    
    Real-world examples:
    - Add to cart button
    - Like/favorite buttons
    - Form submission
    """
    
    driver.get("https://the-internet.herokuapp.com/add_remove_elements/")
    print("📍 Opened add/remove elements page")
    
    # Click "Add Element" button
    add_button = driver.find_element(By.CSS_SELECTOR, "button[onclick='addElement()']")
    add_button.click()
    print("🖱️  Clicked Add Element button")
    
    # BAD APPROACH: Immediately check if button appeared (FLAKY!)
    time.sleep(0.1)  # Tiny wait - often not enough!
    
    try:
        delete_buttons = driver.find_elements(By.CLASS_NAME, "added-manually")
        print(f"Found {len(delete_buttons)} delete button(s)")
        assert len(delete_buttons) == 1, "Delete button should appear!"
    except:
        print("❌ Delete button didn't appear in time!")
        raise
    
    # WHY FLAKY: JavaScript execution time varies
    # Sometimes button appears instantly, sometimes takes 200ms


# ==============================================
# REAL-WORLD FLAKY TEST #3: Form Input with Validation
# ==============================================

def test_flaky_form_authentication(driver):
    """
    REAL FLAKY SCENARIO: Login form with network delay
    
    Real-world examples:
    - Login forms
    - Checkout forms
    - Any form with server validation
    """
    
    driver.get("https://the-internet.herokuapp.com/login")
    print("📍 Opened login page")
    
    # Fill in username
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys("tomsmith")
    
    # Fill in password
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("SuperSecretPassword!")
    
    # Click login button
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    print("🖱️  Clicked Login button")
    
    # BAD APPROACH: Immediately check for success message (FLAKY!)
    time.sleep(1)  # Wait 1 second
    
    try:
        success_message = driver.find_element(By.CLASS_NAME, "success")
        print(f"✅ Success! Message: {success_message.text}")
        assert "You logged into a secure area!" in success_message.text
    except:
        print("❌ Login didn't complete in time!")
        # Take screenshot for debugging
        driver.save_screenshot("login_failed.png")
        raise
    
    # WHY FLAKY: Network speed varies
    # Server response time varies
    # Page redirect time varies


# ==============================================
# REAL-WORLD FLAKY TEST #4: Dropdown Selection
# ==============================================

def test_flaky_dropdown(driver):
    """
    REAL FLAKY SCENARIO: Dropdown that loads options dynamically
    
    Real-world examples:
    - Country/state selectors
    - Dynamic filters
    - Cascading dropdowns
    """
    
    driver.get("https://the-internet.herokuapp.com/dropdown")
    print("📍 Opened dropdown page")
    
    # BAD APPROACH: Select immediately without checking if loaded
    time.sleep(0.5)  # Half-second wait
    
    try:
        dropdown = driver.find_element(By.ID, "dropdown")
        
        # Click to open dropdown
        dropdown.click()
        
        # Try to select Option 1
        option1 = driver.find_element(By.CSS_SELECTOR, "option[value='1']")
        option1.click()
        
        print("✅ Selected Option 1")
        
        # Verify selection
        selected_option = dropdown.find_element(By.CSS_SELECTOR, "option[selected]")
        assert selected_option.get_attribute("value") == "1"
        
    except:
        print("❌ Dropdown interaction failed!")
        raise
    
    # WHY FLAKY: Dropdown might not be fully rendered
    # Options might load with slight delay


# ==============================================
# STABLE TEST (For comparison)
# ==============================================

def test_stable_page_title(driver):
    """
    STABLE TEST: Just checks page title (fast, reliable)
    This should NEVER fail
    """
    
    driver.get("https://the-internet.herokuapp.com")
    print("📍 Opened homepage")
    
    # Simple assertion that always works
    assert "The Internet" in driver.title
    print("✅ Page title is correct!")


# ==============================================
# BONUS: Fixed version of flaky test
# ==============================================

def test_fixed_dynamic_loading(driver):
    """
    FIXED VERSION: Using explicit waits (NOT FLAKY!)
    
    This is how you SHOULD write tests
    """
    
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")
    print("📍 Opened dynamic loading page")
    
    # Click Start button
    start_button = driver.find_element(By.CSS_SELECTOR, "#start button")
    start_button.click()
    print("🖱️  Clicked Start button")
    
    # GOOD APPROACH: Explicit wait (wait UP TO 10 seconds)
    wait = WebDriverWait(driver, 10)
    result = wait.until(
        EC.visibility_of_element_located((By.ID, "finish"))
    )
    
    print(f"✅ Found text: {result.text}")
    assert result.text == "Hello World!"
    
    # WHY NOT FLAKY: Waits intelligently
    # Checks every 500ms if element is visible
    # Succeeds as soon as element appears (even if 1 second)
    # Fails only if element doesn't appear in 10 seconds

def test_measure_actual_load_time(driver):
    """
    Let's measure how long the dynamic page actually takes!
    This will tell us WHY our 3-second wait always fails.
    """
    import time
    
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")
    
    # Click start button
    start_button = driver.find_element(By.CSS_SELECTOR, "#start button")
    
    # Record time BEFORE clicking
    start_time = time.time()
    start_button.click()
    
    # Wait for element (up to 15 seconds)
    wait = WebDriverWait(driver, 15)
    result = wait.until(
        EC.visibility_of_element_located((By.ID, "finish"))
    )
    
    # Record time AFTER element appears
    end_time = time.time()
    
    # Calculate how long it took
    load_time = end_time - start_time
    
    print(f"\n⏱️  Actual load time: {load_time:.2f} seconds")
    print(f"📝 Element text: {result.text}")
    print(f"💡 Our flaky test only waits 3 seconds")
    print(f"💡 That's why it {'PASSES' if load_time <= 3 else 'FAILS'}!")
    
    # This test always passes (just measuring!)
    assert result.text == "Hello World!"