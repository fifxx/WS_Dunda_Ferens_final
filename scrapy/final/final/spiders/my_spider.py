import scrapy # Importing the scrapy module
from bs4 import BeautifulSoup as BS # Importing BeautifulSoup class from bs4 for HTML parsing

class League321Spider(scrapy.Spider):
    name = 'league321'                             # Setting the name of the spider
    start_urls = ['http://www.league321.com/']     # List of URLs to start crawling from

    def parse(self, response):
        bs = BS(response.text, 'html.parser')              # Creating a BeautifulSoup object by parsing the HTML content of the response
        links = [tag['href'] for tag in bs.find_all('a', href=lambda href: href and href.startswith('http://www.league321.com/'))]  # Extracting all links that start with 'http://www.league321.com/' from the HTML content
        filtered_links = [link for link in links if '-football' in link and link.endswith('-football.html')]                        # Filtering the links to keep only those containing '-football' and ending with '-football.html'
        with open('scrapy_links.csv', 'w') as file: # Writing the filtered links to a CSV file named 'scrapy_links.csv'
            file.write('\n'.join(filtered_links))
        for link in filtered_links:
            yield response.follow(link, self.parse_link) # Following each filtered link and passing the response to the parse_link method

    def parse_link(self, response):
        bs = BS(response.text, 'html.parser')              # Creating a BeautifulSoup object by parsing the HTML content of the response
        try:
            header = bs.select_one('h2.wsite-content-title > font > span').text.strip() # Selecting the header element and extracting its text content
        except:
            header = 'NA'
        yield {'header': header} # Yielding a dictionary with the extracted header value
