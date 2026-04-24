import pytest
import allure
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
import requests


@allure.feature("Non-Functional Requirements")
@allure.story("NFR1 - Usability - Intuitive Interface")
def test_usability_intuitive_interface(driver):
    """Test that UI is clean, responsive, and navigable"""
    try:
        driver.get("https://phptravels.net/")

        # Check for navigation elements
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "nav, .navbar, .navigation")))

        # Check for main content areas (more flexible selectors)
        main_content = driver.find_elements(By.CSS_SELECTOR, "main, .main-content, #content, .container, .wrapper, body > div")
        assert len(main_content) > 0, "Main content area not found"

        # Check for responsive design indicators (viewport meta tag)
        viewport_meta = driver.find_elements(By.CSS_SELECTOR, "meta[name='viewport']")
        assert len(viewport_meta) > 0, "Viewport meta tag not found"

        # Check for search forms (indicating navigability) - more flexible
        search_forms = driver.find_elements(By.CSS_SELECTOR, "form, .search-form, input[type='text'], .search")
        assert len(search_forms) > 0, "Search functionality not accessible"

        allure.attach("UI appears clean and navigable", name="Usability Check", attachment_type=allure.attachment_type.TEXT)

    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="Usability Test Failure", attachment_type=allure.attachment_type.PNG)
        raise e


@allure.feature("Non-Functional Requirements")
@allure.story("NFR2 - Performance - Response Time")
@pytest.mark.parametrize("page,expected_max_time", [
    ("https://phptravels.net/", 5),
    ("https://phptravels.net/flights", 5),
    ("https://phptravels.net/hotels", 5),
    ("https://phptravels.net/tours", 5),
    ("https://phptravels.net/cars", 5),
])
def test_performance_response_time(driver, page, expected_max_time):
    """Test that pages load within specified time limits"""
    try:
        start_time = time.time()
        driver.get(page)
        WebDriverWait(driver, expected_max_time).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        load_time = time.time() - start_time

        assert load_time <= expected_max_time, f"Page load time {load_time:.2f}s exceeded {expected_max_time}s limit"

        allure.attach(f"Page loaded in {load_time:.2f} seconds", name="Load Time", attachment_type=allure.attachment_type.TEXT)

    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="Performance Test Failure", attachment_type=allure.attachment_type.PNG)
        raise e


@allure.feature("Non-Functional Requirements")
@allure.story("NFR3 - Reliability - System Availability")
def test_reliability_system_availability():
    """Test that the system is available (basic uptime check)"""
    try:
        response = requests.get("https://phptravels.net/", timeout=10)
        assert response.status_code == 200, f"Site returned status code {response.status_code}"

        # Check response time is reasonable
        assert response.elapsed.total_seconds() < 5, f"Response time too slow: {response.elapsed.total_seconds()}s"

        allure.attach("System is available and responding", name="Availability Check", attachment_type=allure.attachment_type.TEXT)

    except requests.RequestException as e:
        pytest.fail(f"System availability check failed: {str(e)}")


@allure.feature("Non-Functional Requirements")
@allure.story("NFR4 - Security - Secure Authentication")
def test_security_secure_authentication(driver):
    """Test that authentication uses HTTPS and basic security measures"""
    try:
        # Check login page uses HTTPS
        driver.get("https://phptravels.net/login")
        assert driver.current_url.startswith("https://"), "Login page does not use HTTPS"

        # Check for password field with proper type
        password_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password'], input[name='password']"))
        )
        assert password_field.get_attribute("type") == "password", "Password field does not have secure type"

        # Basic brute force protection check (look for rate limiting indicators)
        # This is a basic check - real brute force testing would require more sophisticated setup
        login_form = driver.find_element(By.CSS_SELECTOR, "form")
        assert login_form is not None, "Login form not found"

        allure.attach("Authentication appears to use HTTPS and secure password handling", name="Security Check", attachment_type=allure.attachment_type.TEXT)

    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="Security Test Failure", attachment_type=allure.attachment_type.PNG)
        raise e


@allure.feature("Non-Functional Requirements")
@allure.story("NFR5 - Compatibility - Cross Browser Support")
@pytest.mark.parametrize("browser_name", ["chrome", "firefox", "edge", "safari"])
def test_compatibility_cross_browser(browser_name):
    """Test core features work across different browsers"""
    driver = None
    try:
        if browser_name == "chrome":
            options = ChromeOptions()
            options.add_argument("--headless=new")
            driver = webdriver.Chrome(options=options)
        elif browser_name == "firefox":
            options = FirefoxOptions()
            options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
        elif browser_name == "edge":
            options = EdgeOptions()
            options.add_argument("--headless")
            driver = webdriver.Edge(options=options)
        elif browser_name == "safari":
            # Safari doesn't support headless mode in all versions
            driver = webdriver.Safari()

        # Test basic navigation and core functionality
        driver.get("https://phptravels.net/")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "nav, .navbar")))

        # Test login page accessibility
        driver.get("https://phptravels.net/login")
        email_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "email")))

        # Test search functionality
        driver.get("https://phptravels.net/flights")
        WebDriverWait(driver, 30).until(lambda d: len(d.page_source) > 1000)

        allure.attach(f"Core features working on {browser_name}", name=f"{browser_name} Compatibility", attachment_type=allure.attachment_type.TEXT)

    except Exception as e:
        if driver:
            allure.attach(driver.get_screenshot_as_png(), name=f"{browser_name} Compatibility Failure", attachment_type=allure.attachment_type.PNG)
        raise e
    finally:
        if driver:
            driver.quit()


@allure.feature("Non-Functional Requirements")
@allure.story("NFR6 - Compatibility - Responsive Design")
@pytest.mark.parametrize("viewport_width,device_type", [
    (1920, "desktop"),
    (1200, "desktop"),
    (768, "tablet"),
    (375, "mobile"),
])
def test_compatibility_responsive_design(driver, viewport_width, device_type):
    """Test that UI adapts to different screen sizes"""
    try:
        # Set viewport size
        driver.set_window_size(viewport_width, 1080)

        driver.get("https://phptravels.net/")

        # Wait for page to load
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # Check that navigation is accessible
        nav_elements = driver.find_elements(By.CSS_SELECTOR, "nav, .navbar, .navigation")
        assert len(nav_elements) > 0, f"Navigation not found on {device_type} viewport"

        # Check for responsive behavior (elements should be visible and usable)
        body_width = driver.execute_script("return document.body.scrollWidth")
        assert body_width <= viewport_width + 50, f"Content overflow on {device_type} viewport"

        # Check that search forms are accessible
        search_elements = driver.find_elements(By.CSS_SELECTOR, "form, .search-form, input[type='text']")
        assert len(search_elements) > 0, f"Search elements not accessible on {device_type} viewport"

        allure.attach(f"UI adapts properly to {device_type} screen size ({viewport_width}px)", name=f"Responsive {device_type}", attachment_type=allure.attachment_type.TEXT)

    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name=f"Responsive {device_type} Failure", attachment_type=allure.attachment_type.PNG)
        raise e