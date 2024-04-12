# Mark Project

## 1. commercialrealestate
This is a Python script that implements a web scraper using Scrapy framework. The spider is designed to extract information about real estate listings from the website https://www.commercialrealestate.com.au. It collects data such as listing ID, type, title, price, location, and seller information.

### Installation
To run this script, you need python (version>=3.7) installed along with scrapy. 
Download and install python using the link https://www.python.org/downloads/
To install scrapy use the following command in terminal:

```bash
pip install scrapy
```

### Execution
1. Download the Estate Spider script and save it in a directory.

2. Open a terminal or command prompt and navigate to the directory where the script is saved.

3. Run the spider using the following command:
```bash
scrapy crawl commercialrealestate -o ./datafolder/file_name.csv
```
Replace datafolder with the desired directory path where you want to save the extracted data. Also, change file_name.csv to the desired name for the output file.

4. To run it for an individuall category, give the category link in the command like this:
```bash
scrapy crawl commercialrealestate -o ./datafolder/category_name.csv -a name=https://www.commercialrealestate.com.au/business-for-sale/australia/accommodation-tourism/
```
Replace the link with the valid category link, along with the file name 'category_name.csv'

The spider will start scraping the website and save the extracted data in a CSV file.


### Customization and Maintenance
Modify the XPath expressions in the spider methods to extract the desired information from the website.
In case website changes its format. Update the Xpaths using the inspect tool in the browser


## 2. Anybusiness Spider
Scrapy spider called Anybusiness_Spider that is designed to scrape data from the website "https://www.anybusiness.com.au". The spider starts crawling from multiple search pages on the website, extracts links to individual business listings, and then navigates through the pagination to scrape information from each listing.

### Prerequisites
To run this script, make sure you have the following dependencies installed:
1. Scrapy
2. scrapy-rotating-proxies
3. proxies.txt file containing rotating proxies

### Installation
1. Install Scrapy using the following command:
```bash
pip install scrapy
```
2. Install Rotating proxy module using the following command:
```bash
pip install scrapy-rotating-proxies
```
3. Create a file named proxies.txt and add the proxies to be used by the spider.

### Usage
1. Open a terminal or command prompt.
2. Navigate to the directory where the script is located.
3. Run the spider using the following command:
```bash
scrapy crawl anybusiness -o ./datafolder/file_name.csv
```
Replace file_name.csv with the desired name of the output file.

### Custom Settings
The spider includes custom settings that can be modified as per your requirements. These settings are defined in the custom_settings dictionary within the spider class. The current custom settings are:

- ROTATING_PROXY_LIST_PATH: Path to the proxies.txt file containing rotating proxies.
- ROTATING_PROXY_PAGE_RETRY_TIMES: Maximum number of times to retry a request when using rotating proxies.
- CONCURRENT_REQUESTS_PER_DOMAIN: Maximum number of concurrent requests allowed for a single domain.
- CONCURRENT_REQUESTS_PER_IP: Maximum number of concurrent requests allowed for a single IP address.
- DOWNLOADER_MIDDLEWARES: Middleware settings for rotating proxies.



### Customization and Maintenance
Modify the XPath expressions in the spider methods to extract the desired information from the website.
In case website changes its format. Update the Xpaths using the inspect tool in the browser


## 3. Bsale Spider
This script contains a Scrapy spider called "Bsale_Spider" that is designed to scrape information from the website "https://bsale.com.au". The spider navigates through the website, extracts relevant data from each page, and stores it in a dictionary.

### Requirements
- Python 3.x
- Scrapy library

### Installation
Make sure you have Python 3.x installed on your system.
Install the Scrapy library by running the following command:

```bash
pip install scrapy
```
### Usage
1. Open a command prompt or terminal window.
2. Navigate to the directory where the script is saved.
3. Run the spider using the following command:
```bash
scrapy crawl bsale -o ./datafolder/file_name.csv
```
Replace file_name.csv with the desired filename for the output file. The scraped data will be saved in CSV format.

### Customization and Maintenance
Modify the XPath expressions in the spider methods to extract the desired information from the website.
In case website changes its format. Update the Xpaths using the inspect tool in the browser

## 4. Edenexchange Spider
This script implements a Scrapy spider (Edenexchange) that scrapes data from a website's API for retrieving listings. The spider sends a POST request to the API with pagination to retrieve the data. It extracts product IDs and their corresponding categories from the API response and sends a separate request for each ID to get more detailed information about each listing. The extracted information is then parsed and returned as a dictionary.

### Prerequisites
- Python 3.x
- Scrapy library

### Usage
1. Install the required dependencies by running the following command:
```bash
pip install scrapy
```
2. Execute the spider by running the following command:
```bash
scrapy crawl edenexchange -o ./datafolder/file_name.csv
```
Replace file_name.csv with the desired filename for the output file. The scraped data will be saved in CSV format.


## 5. Franchisedirect Spider
This script is a web scraping spider implemented using Scrapy framework. The spider is designed to extract information from the website "www.franchisedirect.com.au".

### Prerequisites
To run this script, you need to have the following dependencies installed:
- Scrapy
You can install Scrapy using the following command:
```bash
pip install scrapy
```

### Usage
To use this spider, follow these steps:

1. Navigate to an existing Scrapy project directory.

2. In the command line, navigate to the project directory.

3. Run the spider using the following command:
```bash
scrapy crawl franchisedirect -o ./datafolder/file_name.csv
```
Replace file_name.csv with the desired filename for the output file. The scraped data will be saved in CSV format.

### Customization and Maintenance
Modify the XPath expressions in the spider methods to extract the desired information from the website.
In case website changes its format. Update the Xpaths using the inspect tool in the browser

## 5. Businessforsale Spider
This script is a web scraping spider implemented using Scrapy framework. The spider is designed to extract information from the website "https://www.businessforsale.com.au/".

### Prerequisites
To run this script, you need to have the following dependencies installed:
- Scrapy
You can install Scrapy using the following command:
```bash
pip install scrapy
```

### Usage
To use this spider, follow these steps:

1. Navigate to an existing Scrapy project directory.

2. In the command line, navigate to the project directory.

3. Run the spider using the following command:
```bash
scrapy crawl businessforsale -o ./datafolder/businessforsale.csv
```
Replace file_name.csv with the desired filename for the output file. The scraped data will be saved in CSV format.

### Customization and Maintenance
Modify the XPath expressions in the spider methods to extract the desired information from the website.
In case website changes its format. Update the Xpaths using the inspect tool in the browser