# Import the necessary libraries
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
import concurrent.futures

# Start the timer to measure execution time
start_time = time.time()

# Set the URL and paths for geckodriver and Firefox binary
url = "http://www.league321.com/"
geckodriver_path = r'C:\Users\filip\Desktop\gecko\geckodriver.exe'
firefox_binary_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'

# Configure Firefox options
options = Options()
options.binary_location = firefox_binary_path
options.set_preference("webdriver.gecko.driver", geckodriver_path)

# Initialize the Firefox webdriver
driver = webdriver.Firefox(options=options)

# Open the URL in the Firefox webdriver and wait for 30 seconds
driver.get(url)
time.sleep(5)

# Extract the links using JavaScript execution in the browser
links = driver.execute_script("""
    var elements = Array.from(document.getElementsByTagName('a'));
    var filteredLinks = elements
        .filter(function(a) {
            var href = a.getAttribute('href');
            return href && href.startsWith('http://www.league321.com/');
        })
        .map(function(a) {
            return a.getAttribute('href');
        });
    return filteredLinks;
""")

# Filter the links based on specific criteria
filtered_links = [link for link in links if '-football' in link and link.endswith('-football.html')]

# Function to process each link
def process_link(link):
    retries = 5  # Number of retries in case of failure
    for i in range(retries):
        try:
            driver.get(link)
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.wsite-content-title > font > span')))
            header = driver.execute_script("""
                var headerElement = document.querySelector('h2.wsite-content-title > font > span');
                return headerElement ? headerElement.textContent.trim() : 'NA';
            """)
            if header != 'NA':
                break  # If a valid header is obtained, exit the loop
        except:
            pass
        time.sleep(5)  # Wait for 5 seconds before retrying
    else:
        header = 'NA'  # Set header to 'NA' if all retries fail
    return {'header': header}

# Use ThreadPoolExecutor to process the links concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(process_link, filtered_links)

# Wait for 5 seconds and then quit the Firefox webdriver
time.sleep(5)
driver.quit()

# Calculate the execution time
end_time = time.time()
execution_time = end_time - start_time
print("Execution Time: {:.2f} seconds".format(execution_time))

# Save the filtered links to a CSV file
f = pd.DataFrame(filtered_links)
output_path_f = r'C:\Users\filip\Desktop\WS project\selenium\selenium_links_output.csv'
f.to_csv(output_path_f, index=False)
print(f)

# Save the results (headers) to a CSV file
d = pd.DataFrame(results)
output_path_d = r'C:\Users\filip\Desktop\WS project\selenium\selenium_output.csv'
d.to_csv(output_path_d, index=False)
print(d)
