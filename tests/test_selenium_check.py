# tests/test_selenium_check.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_selenium_works():
    """Quick test to verify Selenium is working"""
    
    # Set up Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    # Open Google
    driver.get("https://www.google.com")
    
    # Check if we got to Google
    assert "Google" in driver.title
    
    print("✅ Selenium is working! Browser opened successfully!")
    
    # Close browser
    driver.quit()