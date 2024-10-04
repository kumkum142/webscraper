# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# import csv

# # Setting up ChromeDriver
# options = webdriver.ChromeOptions()
# # Uncomment the next line to run in headless mode (no GUI)
# # options.add_argument("--headless")  

# # Initialize the Chrome driver
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# # LinkedIn login credentials
# email = "kumkumsijeriya@gmail.com"  # Replace with your LinkedIn email
# password = "kumkumsijeriya@gmail23"  # Replace with your LinkedIn password

# # Navigate to LinkedIn login page
# driver.get("https://www.linkedin.com/login")

# # Allow time for the login page to load
# time.sleep(5)

# # Locate the email and password fields and enter your credentials
# driver.find_element(By.ID, "kumkumsijeriya@gmail.com").send_keys(email)
# driver.find_element(By.ID, "kumkumsijeriya@gmail23").send_keys(password)
# driver.find_element(By.XPATH, "//button[@type='submit']").click()

# # After logging in, wait for the page to load
# time.sleep(10)

# # LinkedIn URL for Web Development jobs
# url = "https://www.linkedin.com/jobs/search/?keywords=web%20development"
# driver.get(url)

# # Allow the job listings page to load
# time.sleep(10)

# # Collecting job titles, company names, and locations
# job_titles = driver.find_elements(By.XPATH, "//h3[contains(@class, 'base-search-card__title')]")
# company_names = driver.find_elements(By.XPATH, "//h4[contains(@class, 'base-search-card__subtitle')]")
# locations = driver.find_elements(By.XPATH, "//span[contains(@class, 'job-search-card__location')]")

# # Saving data in CSV format
# with open('web_development_jobs.csv', 'w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Job Title', 'Company Name', 'Location'])

#     for title, company, location in zip(job_titles, company_names, locations):
#         writer.writerow([title.text, company.text, location.text])

# # Close the browser
# driver.quit()

# print("Scraping completed! Data saved to 'web_development_jobs.csv'")


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# Setting up ChromeDriver
options = webdriver.ChromeOptions()
# Uncomment the next line to run in headless mode (no GUI)
# options.add_argument("--headless")  

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# LinkedIn login credentials
email = "kumkumsijeriya@gmail.com"  # Replace with your LinkedIn email
password = "kumkumsijeriya@gmail23"  # Replace with your LinkedIn password

# Navigate to LinkedIn login page
driver.get("https://www.linkedin.com/login")

# Allow time for the login page to load
time.sleep(15)

# Locate the email and password fields and enter your credentials
driver.find_element(By.ID, "username").send_keys(email)  # Correct ID for email field
driver.find_element(By.ID, "password").send_keys(password)  # Correct ID for password field
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# After logging in, wait for the page to load
time.sleep(15)

# LinkedIn URL for Web Development jobs
url = "https://www.linkedin.com/jobs/search/?keywords=web%20development"
driver.get(url)

# Allow the job listings page to load
time.sleep(15)

# Collecting job titles, company names, and locations
job_titles = driver.find_elements(By.XPATH, "//h3[contains(@class, 'base-search-card__title')]")
company_names = driver.find_elements(By.XPATH, "//h4[contains(@class, 'base-search-card__subtitle')]")
locations = driver.find_elements(By.XPATH, "//span[contains(@class, 'job-search-card__location')]")

# Saving data in CSV format
with open('web_development_jobs.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Job Title', 'Company Name', 'Location'])

    for title, company, location in zip(job_titles, company_names, locations):
        writer.writerow([title.text, company.text, location.text])

# Close the browser
driver.quit()

print("Scraping completed! Data saved to 'web_development_jobs.csv'")
