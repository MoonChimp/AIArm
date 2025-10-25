from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Create Edge driver instance
driver = webdriver.Edge()

try:
    # Navigate to Google
    driver.get("https://www.google.com")
    
    # Wait for the search box to be present
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    
    # Enter search term
    search_box.send_keys("Mary Magdalene")
    search_box.send_keys(Keys.RETURN)
    
    # Keep the browser open for 10 seconds so you can see the results
    time.sleep(10)

finally:
    # Close the browser
    driver.quit()