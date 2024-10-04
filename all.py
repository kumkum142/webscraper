from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# Function to scrape Amazon
def scrape_amazon(driver, category):
    url = f"https://www.amazon.in/s?k={category}"
    driver.get(url)
    time.sleep(10)  # Increase wait time for page load

    # Collecting item names and prices
    item_names = driver.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")
    item_prices = driver.find_elements(By.XPATH, "//span[@class='a-price-whole']")

    # Check if any data was found
    if not item_names or not item_prices:
        print("No data found on Amazon. Check if the XPATH is correct or if the page is loading properly.")
        return []
    
    # Debug: Print the number of items found
    print(f"Collected {len(item_names)} item names and {len(item_prices)} prices.")
    
    # Check if lengths match
    if len(item_names) != len(item_prices):
        print(f"Warning: Mismatch in number of item names ({len(item_names)}) and prices ({len(item_prices)})")

    return [(name.text, price.text) for name, price in zip(item_names, item_prices)]

# Function to scrape LinkedIn
def scrape_linkedin(driver):
    # LinkedIn login credentials
    email = "kumkumsijeriya@gmail.com"  # Replace with your LinkedIn email
    password = "kumkumsijeriya@gmail23"  # Replace with your LinkedIn password

    # Navigate to LinkedIn login page
    driver.get("https://www.linkedin.com/login")
    time.sleep(10)

    # Locate the email and password fields and enter your credentials
    driver.find_element(By.ID, "username").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Wait for the homepage to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Search')]"))
    )

    # Navigate to Web Development jobs
    driver.get("https://www.linkedin.com/jobs/search/?keywords=web%20development")
    time.sleep(10)

    # Collecting job titles, company names, and locations
    job_titles = driver.find_elements(By.XPATH, "//h3[contains(@class, 'base-search-card__title')]")
    company_names = driver.find_elements(By.XPATH, "//h4[contains(@class, 'base-search-card__subtitle')]")
    locations = driver.find_elements(By.XPATH, "//span[contains(@class, 'job-search-card__location')]")

    # Check if any data was found
    if not job_titles or not company_names or not locations:
        print("No data found on LinkedIn. Check if the XPATH is correct or if the page is loading properly.")
        return []

    return [(title.text, company.text, location.text) for title, company, location in zip(job_titles, company_names, locations)]

# Function to scrape Google
def scrape_google(driver, category):
    search_terms = {
        "study material": ["study material site:edu", "study material site:gov", "study material site:org"],
        "gaming": ["gaming site:reddit.com", "gaming news site:ign.com", "gaming reviews site:gamespot.com"]
    }
    
    if category not in search_terms:
        print(f"No search terms available for category: {category}")
        return []

    results = []
    
    for term in search_terms[category]:
        driver.get(f"https://www.google.com/search?q={term}")
        time.sleep(5)  # Allow the page to load
        
        # Collecting titles and URLs
        titles = driver.find_elements(By.XPATH, "//h3")
        urls = driver.find_elements(By.XPATH, "//div[@class='yuRUbf']/a")
        
        for title, url in zip(titles, urls):
            results.append((title.text, url.get_attribute('href')))
    
    if not results:
        print("No data found on Google. Check if the XPATH is correct or if the page is loading properly.")
    return results

# Main function to handle user selection
def main():
    # Set up the Chrome driver with options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode for no GUI
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # User selects a website to scrape
    print("Choose a website to scrape:")
    print("1. Amazon")
    print("2. LinkedIn")
    print("3. Google")
    choice = input("Enter your choice (1 for Amazon, 2 for LinkedIn, 3 for Google): ")

    if choice == "1":
        print("Choose Amazon category to scrape:")
        print("1. iPhone")
        print("2. Phone")
        print("3. Custom Category")
        category_choice = input("Enter your choice (1, 2, or 3): ")
        
        if category_choice == "1":
            category = "iphone"
        elif category_choice == "2":
            category = "phone"
        elif category_choice == "3":
            category = input("Enter your custom category: ")
        else:
            print("Invalid choice, defaulting to 'phone'.")
            category = "phone"
        
        results = scrape_amazon(driver)
        
        if results:
            # Saving data in CSV format
            with open(f'amazon_{category}_data.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Item Name', 'Price'])
                for name, price in results:
                    writer.writerow([name, price])
            print(f"Scraping completed! Data saved to 'amazon_{category}_data.csv'")
        else:
            print("No data to save.")
    
    elif choice == "2":
        results = scrape_linkedin(driver)
        
        if results:
            # Saving data in CSV format
            with open('linkedin_web_development_jobs.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Job Title', 'Company Name', 'Location'])
                for title, company, location in results:
                    writer.writerow([title, company, location])
            print("Scraping completed! Data saved to 'linkedin_web_development_jobs.csv'")
        else:
            print("No data to save.")

    elif choice == "3":
        print("Choose Google category to scrape:")
        print("1. Study Material")
        print("2. Gaming")
        category_choice = input("Enter your choice (1 for Study Material, 2 for Gaming): ")
        
        if category_choice == "1":
            category = "study material"
        elif category_choice == "2":
            category = "gaming"
        else:
            print("Invalid choice!")
            driver.quit()
            return

        results = scrape_google(driver, category)
        
        if results:
            # Saving data in CSV format
            with open(f'google_{category.replace(" ", "_")}_data.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Title', 'URL'])
                for title, url in results:
                    writer.writerow([title, url])
            print(f"Scraping completed! Data saved to 'google_{category.replace(' ', '_')}_data.csv'")
        else:
            print("No data to save.")

    else:
        print("Invalid choice!")

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    main()





# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# import csv

# # Function to scrape Amazon
# def scrape_amazon(driver, category):
#     url = f"https://www.amazon.in/s?k={category}"
#     driver.get(url)

#     try:
#         # Wait for the item names to load
#         WebDriverWait(driver, 30).until(
#             EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'a-text-normal')]"))
#         )
        
#         # Use XPaths for item names and prices
#         item_names = driver.find_elements(By.XPATH, "//span[contains(@class, 'a-text-normal')]")
#         item_prices = driver.find_elements(By.XPATH, "//span[@class='a-price-whole' or @class='a-offscreen']")

#         # Check if data is found
#         if not item_names or not item_prices:
#             print("No data found on Amazon. Check if the XPATH is correct or if the page is loading properly.")
#             return []
        
#         # Print item names and prices
#         return [(name.text, price.text) for name, price in zip(item_names, item_prices)]

#     except Exception as e:
#         print(f"Error while scraping Amazon: {e}")
#         return []

# # Function to scrape Google
# def scrape_google(driver, query):
#     url = f"https://www.google.com/search?q={query}"
#     driver.get(url)

#     try:
#         # Wait for the search results to load
#         WebDriverWait(driver, 30).until(
#             EC.presence_of_element_located((By.XPATH, "//h3[contains(@class, 'LC20lb')]"))
#         )

#         # Scrape search result titles and URLs
#         result_titles = driver.find_elements(By.XPATH, "//h3[contains(@class, 'LC20lb')]")
#         result_links = driver.find_elements(By.XPATH, "//div[@class='yuRUbf']/a")

#         # Check if data is found
#         if not result_titles or not result_links:
#             print("No data found on Google. Check if the XPATH is correct or if the page is loading properly.")
#             return []

#         return [(title.text, link.get_attribute('href')) for title, link in zip(result_titles, result_links)]

#     except Exception as e:
#         print(f"Error while scraping Google: {e}")
#         return []

# # Function to scrape LinkedIn
# def scrape_linkedin(driver, job_title):
#     url = f"https://www.linkedin.com/jobs/search/?keywords={job_title}"
#     driver.get(url)

#     try:
#         # Wait for job postings to load
#         WebDriverWait(driver, 30).until(
#             EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'result-card__full-card-link')]"))
#         )

#         # Scrape job titles and company names
#         job_titles = driver.find_elements(By.XPATH, "//h3[contains(@class, 'result-card__title')]")
#         company_names = driver.find_elements(By.XPATH, "//h4[contains(@class, 'result-card__subtitle')]")

#         # Check if data is found
#         if not job_titles or not company_names:
#             print("No data found on LinkedIn. Check if the XPATH is correct or if the page is loading properly.")
#             return []

#         return [(job.text, company.text) for job, company in zip(job_titles, company_names)]

#     except Exception as e:
#         print(f"Error while scraping LinkedIn: {e}")
#         return []

# # Main function to handle user input and call specific scraping functions
# def main():
#     # Set up the Chrome driver (turn off headless mode for debugging)
#     options = webdriver.ChromeOptions()
#     # Comment out the headless mode for debugging
#     # options.add_argument("--headless")  # Run in headless mode (no GUI)
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
#     # User selects a website to scrape
#     print("Choose a website to scrape:")
#     print("1. Amazon")
#     print("2. Google")
#     print("3. LinkedIn")
#     choice = input("Enter your choice (1, 2, or 3): ")
    
#     if choice == "1":  # Scrape Amazon
#         print("Choose Amazon category to scrape:")
#         print("1. iPhone")
#         print("2. Phone")
#         print("3. Custom Category")
#         category_choice = input("Enter your choice (1, 2, or 3): ")

#         if category_choice == "1":
#             category = "iphone"
#         elif category_choice == "2":
#             category = "phone"
#         elif category_choice == "3":
#             category = input("Enter your custom category: ")
#         else:
#             print("Invalid choice, defaulting to 'phone'.")
#             category = "phone"
        
#         results = scrape_amazon(driver, category)
        
#         if results:
#             # Save to CSV
#             with open(f'amazon_{category}_data.csv', 'w', newline='', encoding='utf-8') as file:
#                 writer = csv.writer(file)
#                 writer.writerow(['Item Name', 'Price'])
#                 for name, price in results:
#                     writer.writerow([name, price])
#             print(f"Scraping completed! Data saved to 'amazon_{category}_data.csv'")
#         else:
#             print("No data to save.")

#     elif choice == "2":  # Scrape Google
#         query = input("Enter your search query for Google: ")
#         results = scrape_google(driver, query)

#         if results:
#             # Save to CSV
#             with open(f'google_{query}_data.csv', 'w', newline='', encoding='utf-8') as file:
#                 writer = csv.writer(file)
#                 writer.writerow(['Result Title', 'URL'])
#                 for title, url in results:
#                     writer.writerow([title, url])
#             print(f"Scraping completed! Data saved to 'google_{query}_data.csv'")
#         else:
#             print("No data to save.")

#     elif choice == "3":  # Scrape LinkedIn
#         job_title = input("Enter the job title for LinkedIn search: ")
#         results = scrape_linkedin(driver, job_title)

#         if results:
#             # Save to CSV
#             with open(f'linkedin_{job_title}_data.csv', 'w', newline='', encoding='utf-8') as file:
#                 writer = csv.writer(file)
#                 writer.writerow(['Job Title', 'Company Name'])
#                 for job, company in results:
#                     writer.writerow([job, company])
#             print(f"Scraping completed! Data saved to 'linkedin_{job_title}_data.csv'")
#         else:
#             print("No data to save.")

#     else:
#         print("Invalid choice!")

#     driver.quit()

# if __name__ == "__main__":
#     main()


# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# import csv
# import os

# # Function to scrape Amazon
# def scrape_amazon(driver, category):
#     url = f"https://www.amazon.in/s?k={category}"
#     driver.get(url)
#     time.sleep(10)  # Increase wait time for page load

#     item_names = driver.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")
#     item_prices = driver.find_elements(By.XPATH, "//span[@class='a-price-whole']")

#     if not item_names or not item_prices:
#         print("No data found on Amazon. Check if the XPATH is correct or if the page is loading properly.")
#         return []

#     return [(name.text, price.text) for name, price in zip(item_names, item_prices)]

# # Function to scrape Google (basic search results)
# def scrape_google(driver, query):
#     url = f"https://www.google.com/search?q={query}"
#     driver.get(url)
#     time.sleep(10)  # Increase wait time for page load

#     item_names = driver.find_elements(By.XPATH, "//h3")
#     item_links = driver.find_elements(By.XPATH, "//a[@href]")

#     if not item_names:
#         print("No data found on Google. Check if the XPATH is correct or if the page is loading properly.")
#         return []

#     return [(name.text, link.get_attribute('href')) for name, link in zip(item_names, item_links)]

# # Function to scrape LinkedIn
# def scrape_linkedin(driver, job_title):
#     url = f"https://www.linkedin.com/jobs/search/?keywords={job_title}"
#     driver.get(url)
#     time.sleep(10)  # Increase wait time for page load

#     job_titles = driver.find_elements(By.XPATH, "//h3[@class='base-search-card__title']")
#     companies = driver.find_elements(By.XPATH, "//h4[@class='base-search-card__subtitle']")

#     if not job_titles or not companies:
#         print("No data found on LinkedIn. Check if the XPATH is correct or if the page is loading properly.")
#         return []

#     return [(job.text, company.text) for job, company in zip(job_titles, companies)]

# # Main function to handle user selection
# def main():
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")  # Run in headless mode for no GUI
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#     # User selects a website to scrape
#     print("Choose a website to scrape:")
#     print("1. Amazon")
#     print("2. Google")
#     print("3. LinkedIn")
#     choice = input("Enter your choice (1, 2, or 3): ")

#     if choice == "1":
#         print("Choose Amazon category to scrape:")
#         print("1. iPhone")
#         print("2. Phone")
#         category_choice = input("Enter your choice (1 or 2): ")
        
#         if category_choice == "1":
#             category = "iphone"
#         elif category_choice == "2":
#             category = "phone"
#         else:
#             print("Invalid choice, defaulting to 'phone'.")
#             category = "phone"
        
#         results = scrape_amazon(driver, category)
#         if results:
#             try:
#                 file_path = os.path.join(os.getcwd(), f'amazon_{category}_data.csv')
#                 with open(file_path, 'w', newline='', encoding='utf-8') as file:
#                     writer = csv.writer(file)
#                     writer.writerow(['Item Name', 'Price'])
#                     for name, price in results:
#                         writer.writerow([name, price])
#                 print(f"Scraping completed! Data saved to '{file_path}'")
#             except Exception as e:
#                 print(f"Error saving CSV: {e}")
#         else:
#             print("No data to save.")
    
#     elif choice == "2":
#         query = input("Enter the search query for Google: ")
#         results = scrape_google(driver, query)
#         if results:
#             try:
#                 file_path = os.path.join(os.getcwd(), f'google_search_results.csv')
#                 with open(file_path, 'w', newline='', encoding='utf-8') as file:
#                     writer = csv.writer(file)
#                     writer.writerow(['Result Title', 'Link'])
#                     for title, link in results:
#                         writer.writerow([title, link])
#                 print(f"Scraping completed! Data saved to '{file_path}'")
#             except Exception as e:
#                 print(f"Error saving CSV: {e}")
#         else:
#             print("No data to save.")

#     elif choice == "3":
#         job_title = input("Enter the job title to search on LinkedIn: ")
#         results = scrape_linkedin(driver, job_title)
#         if results:
#             try:
#                 file_path = os.path.join(os.getcwd(), f'linkedin_job_results.csv')
#                 with open(file_path, 'w', newline='', encoding='utf-8') as file:
#                     writer = csv.writer(file)
#                     writer.writerow(['Job Title', 'Company'])
#                     for job, company in results:
#                         writer.writerow([job, company])
#                 print(f"Scraping completed! Data saved to '{file_path}'")
#             except Exception as e:
#                 print(f"Error saving CSV: {e}")
#         else:
#             print("No data to save.")
    
#     else:
#         print("Invalid choice!")

#     # Close the browser
#     driver.quit()

# if __name__ == "__main__":
#     main()
