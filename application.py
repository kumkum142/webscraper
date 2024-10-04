from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# Function to scrape Amazon
def scrape_amazon(driver, category):
    # Amazon URL based on category
    url = f"https://www.amazon.in/s?k={category}"
    driver.get(url)
    
    time.sleep(5)  # Allow the page to load
    
    # Collecting item names and prices
    item_names = driver.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")
    item_prices = driver.find_elements(By.XPATH, "//span[@class='a-price-whole']")
    
    return [(name.text, price.text) for name, price in zip(item_names, item_prices)]

# Function to scrape Google
def scrape_google(driver, query):
    url = f"https://www.google.com/search?q={query}"
    driver.get(url)
    
    time.sleep(5)  # Allow the page to load
    
    # Collecting results
    result_titles = driver.find_elements(By.XPATH, "//h3")
    
    return [title.text for title in result_titles]

# Main function
def main():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # User selects a website to scrape
    choice = input("Choose website to scrape (1 for Amazon, 2 for Google): ")
    
    if choice == "1":
        category = input("Enter Amazon category (e.g., grocery, phone, dress, shoes): ")
        results = scrape_amazon(driver, category)
        
        # Saving data in CSV format
        with open(f'amazon_{category}_data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Item Name', 'Price'])
            for name, price in results:
                writer.writerow([name, price])
        
        print(f"Scraping completed! Data saved to 'amazon_{category}_data.csv'")
    
    elif choice == "2":
        query = input("Enter Google query (e.g., study materials): ")
        results = scrape_google(driver, query)
        
        # Saving data in CSV format
        with open(f'google_{query.replace(" ", "_")}_data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Result Title'])
            for title in results:
                writer.writerow([title])
        
        print(f"Scraping completed! Data saved to 'google_{query.replace(' ', '_')}_data.csv'")
    
    else:
        print("Invalid choice!")
    
    driver.quit()

if __name__ == "__main__":
    main()
