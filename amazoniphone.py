# pip install requests
# pip install bs4
# pip install html5lib

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# Setting up ChromeDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode for no GUI

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Amazon URL for iPhones (you can update this with any specific search)
url = "https://www.amazon.in/s?k=iphone"
driver.get(url)

# Give the page time to load
time.sleep(3)

# Collecting iPhone names and prices
iphone_names = driver.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")
iphone_prices = driver.find_elements(By.XPATH, "//span[@class='a-price-whole']")

# Saving data in CSV format
with open('iphone_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['iPhone Name', 'Price (INR)'])
    
    for name, price in zip(iphone_names, iphone_prices):
        writer.writerow([name.text, price.text])

# Close the browser
driver.quit()

print("Scraping completed! Data saved to 'iphone_data.csv'")

