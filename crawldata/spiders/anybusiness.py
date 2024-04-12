import scrapy
from random import randint
import re
class Anybusiness_Spider(scrapy.Spider):
    name = "anybusiness"
    baseUrl = "https://www.anybusiness.com.au"
    start_url = "https://www.anybusiness.com.au/search"
    '''
        `start_urls` is a list of URLs that the spider will start crawling from. Each URL in the list
        corresponds to a search page on the website `www.anybusiness.com.au` with a specific `state_id`
        parameter. The spider will send a request to each URL in the list and call the `pagination`
        function to extract links to individual business listings on each search page.
    '''
    start_urls = [
        "https://www.anybusiness.com.au/search?search[state_id]=23",
        "https://www.anybusiness.com.au/search?search[state_id]=21",
        "https://www.anybusiness.com.au/search?search[state_id]=20",
        "https://www.anybusiness.com.au/search?search[state_id]=19",
        "https://www.anybusiness.com.au/search?search[state_id]=18",
        "https://www.anybusiness.com.au/search?search[state_id]=24",
        "https://www.anybusiness.com.au/search?search[state_id]=17",
        "https://www.anybusiness.com.au/search?search[state_id]=22",
        ]
    
    # `custom_settings` is a dictionary that contains custom settings for the Scrapy spider.
    custom_settings = {
        'ROTATING_PROXY_LIST_PATH': 'proxies.txt',
        'ROTATING_PROXY_PAGE_RETRY_TIMES': 200,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 32,
        'CONCURRENT_REQUESTS_PER_IP':1,
        'DOWNLOADER_MIDDLEWARES': {
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
        }
    }
    '''
        `user_agents` is a list of user agent strings that the spider will use to identify itself to the
        server. The `headers` dictionary in the spider contains a randomly selected user agent string
        from this list to prevent the server from detecting that the requests are coming from a spider
        and potentially blocking them.
    '''
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/100.0.100.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/604.1 Edg/100.0.100.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edge/18.19042',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edge/18.19042',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/65.0.3467.48',
            'Mozilla/5.0 (X11; CrOS x86_64 10066.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        ]
    '''
        `headers` is a dictionary that contains two key-value pairs. The first key `'accept'` specifies
        the types of responses that the spider is willing to accept from the server. The second key
        `'user-agent'` specifies the user agent string that the spider will use to identify itself to
        the server. The value of `'user-agent'` is randomly selected from a list of user agent strings
        stored in the `user_agents` list using the `randint()` function from the `random` module. This
        is done to prevent the server from detecting that the requests are coming from a spider and
        potentially blocking them.
    '''
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': user_agents[randint(0,len(user_agents)-1)],
        }
    def start_requests(self):
        """
        This function sends a request to the start URL and calls the pagination function with the
        response and headers as arguments.
        """
        for url in self.start_urls:
            yield scrapy.Request(url,callback=self.pagination,headers=self.headers)

    def pagination(self,response):
        """
        This function extracts links from a webpage, sends requests to each link, and recursively calls
        itself to navigate to the next page if available.
        
        :param response: The response parameter is the HTTP response received after sending a request to
        a website using Scrapy. It contains the HTML content of the webpage and other metadata such as
        headers, status code, etc
        """
        links = response.xpath('//div[@class="uk-card uk-card-default uk-margin"]/div/a/@href').extract()
        for link in links:
            new_link = self.baseUrl+link
            yield scrapy.Request(new_link, callback=self.information,headers=self.headers,dont_filter=True)
        print(f'Search URL: {response.url} :Links:{len(links)} ')
        next_url = response.xpath('//a[text()="Next ›"]/@href').get()
        if next_url:
            new_next = self.baseUrl+next_url
            yield scrapy.Request(new_next, callback=self.pagination,headers=self.headers)
    def information(self,response):
        """
        This function extracts information from a website's response and returns a dictionary of
        relevant data.
        
        :param response: The response parameter is the HTTP response object returned by the website
        after making a request to a specific URL. It contains the HTML content of the webpage which can
        be parsed using a web scraping tool like Scrapy
        """

        address, category = self.extract_address_categories(response.url)
        if address == "NA":
            add_type2 = response.xpath('//div[@itemprop="name"]/div/text()').get(default='NA').strip().split('|')[-1].strip()
            if add_type2.strip() !="":
                address = add_type2.strip()

        if address != "NA":
            item = {}
            sellerName = response.xpath('//div[@itemprop="seller"]//a[contains(@href,"/business-broker/")]/text()').get(default='NA').strip()
            if sellerName == "NA":
                sellerName = response.xpath("//div[h4/text() = 'Vendor details']/div/div[contains(div, 'Name:')]/div[2]/text()").get(default='NA').strip()
            item['Listing URL'] = response.url
            item['Listing Id'] = response.xpath('//div[@itemprop="serialNumber"]/text()').get(default='NA').strip()
            item['Listing Type'] = response.xpath('//div[@itemprop="name"]/div/text()').get(default='NA').strip().split('|')[0].strip()
            item['Listing Title'] = response.xpath('//div[@itemprop="name"]/h1/text()').get(default='NA').replace('\n','').strip()
            item['Listing Price'] = response.xpath('//div[@itemprop="price"]/text()').get(default='NA').strip().replace('\n','')
            item['Listing Categories'] = category
            item['Listing Location'] = address
            item['Seller Organization'] = response.xpath('//div[@itemprop="seller"]//a/div/text()').get(default='NA').strip()
            item['Seller Personal Name'] = sellerName
    
            yield item



    def extract_address_categories(self,url):
        # Extract address from the URL
        address_match = re.search(r"/([a-z\-]+-\d+)-", url)
        if address_match:
            address = address_match.group(1).replace("-", ",")
        else:
            address = "NA"

        # Extract categories from the URL
        categories_match = re.search(r"\d+-(.*)-\d+", url)
        if categories_match:
            categories = categories_match.group(1).replace("-", ",")
            categories = self.remove_duplicates(categories)
        else:
            categories_match = re.search(r"/listings/(.*)-\d+", url)
            if categories_match:
                categories = categories_match.group(1).replace("-", ",")
                categories = self.remove_duplicates(categories)
            else:
                categories = "NA"

        return address, categories

    def remove_duplicates(self,categories):
        unique_categories = []
        category_list = categories.split(',')
        for category in category_list:
            category = category.strip()
            if category not in unique_categories:
                unique_categories.append(category)
        return ', '.join(unique_categories)
