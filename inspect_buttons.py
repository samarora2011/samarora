from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://phptravels.net/tours")

# Wait for page to load
time.sleep(5)  # Simple wait

# Find all buttons
buttons = driver.find_elements(By.TAG_NAME, "button")
print(f"Total buttons found: {len(buttons)}")

for i, button in enumerate(buttons):
    print(f"\nButton {i+1}:")
    print(f"  Text: '{button.text}'")
    print(f"  Tag: {button.tag_name}")
    print(f"  Type: {button.get_attribute('type')}")
    print(f"  Class: {button.get_attribute('class')}")
    attrs = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', button)
    print(f"  All attributes: {attrs}")
    if 'click' in str(attrs).lower():
        print("  *** HAS CLICK ***")

driver.quit()