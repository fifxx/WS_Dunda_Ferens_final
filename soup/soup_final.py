# Libraries load
from urllib import request                 # Importing the request module from urllib for making HTTP requests
from bs4 import BeautifulSoup as BS        # Importing BeautifulSoup class from bs4 for HTML parsing
import pandas as pd                        # Importing pandas for data manipulation
import concurrent.futures                  # Importing concurrent.futures for parallel processing
import ssl                                 # Importing ssl for SSL context control
import time                                # Importing time for measuring execution time

ssl._create_default_https_context = ssl._create_unverified_context

# URL setup
url = 'http://www.league321.com/'          # The website URL to be scraped

start_time = time.time()                   # Start measuring execution time

# Links extraction
html = request.urlopen(url)                # Opening the URL and retrieving the HTML content
bs = BS(html.read(), 'html.parser')        # Creating a BeautifulSoup object by parsing the HTML content

links = [tag['href'] for tag in bs.find_all('a', href=lambda href: href and href.startswith('http://www.league321.com/'))] # Extracting all links that start with 'http://www.league321.com/' from the HTML content
filtered_links = [link for link in links if '-football' in link and link.endswith('-football.html')]                       # Filtering the links to keep only those containing '-football' and ending with '-football.html'

# Headers extraction
def process_link(link):
    try:
        html = request.urlopen(link)                                                # Opening the link and retrieving the HTML content
        bs = BS(html.read(), 'html.parser')                                         # Creating a BeautifulSoup object by parsing the HTML content
        header = bs.select_one('h2.wsite-content-title > font > span').text.strip() # Selecting the header element and extracting its text content   
    except:
        header = 'NA'
    return {'header': header}

# Parallel processing of links which is asynchronously executing the process_link function for each filtered link using multiple threads
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(process_link, filtered_links)

# Calculate extraction time
extraction_time = time.time() - start_time

# Print extraction time
print(f"Time: {extraction_time} seconds")

# Saving filtered links to CSV
f = pd.DataFrame(filtered_links)                                                # Creating a DataFrame from the filtered links
output_path_f = r'C:\Users\filip\Desktop\WS project\soup\soup_links_output.csv' # Specify the output file path for filtered links
f.to_csv(output_path_f, index=False)                                            # Saving the DataFrame to a CSV file
print(f)

# Saving headers to CSV
d = pd.DataFrame(results)                                                 # Creating a DataFrame from the results iterator
output_path_d = r'C:\Users\filip\Desktop\WS project\soup\soup_output.csv' # Specify the output file path for headers
d.to_csv(output_path_d, index=False)                                      # Saving the DataFrame to a CSV file
print(d)