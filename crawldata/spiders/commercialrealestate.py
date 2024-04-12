import scrapy
from random import randint

# Spider that extracts information from commercial real estate websites.
class Commercialrealestate_Spider(scrapy.Spider):
    name = "commercialrealestate"
    baseUrl = "https://www.commercialrealestate.com.au"
    start_url = "https://www.commercialrealestate.com.au/business-for-sale/"
    
    '''
        `download_delay` is a setting in Scrapy that specifies the amount of time (in seconds) that the
        spider should wait between making requests to the target website. In this case, it is set to 0.5
        seconds, which means that the spider will wait half a second between each request it makes to
        the website.
    '''
    download_delay = 0.5
    concurrent_request = 5
    
    ''' 
        `user_agents` is a list of user agent strings that will be used by the spider to mimic different
        web browsers and operating systems when making requests to the target website. The spider
        randomly selects a user agent string from this list for each request it makes to the website.
        This helps to prevent the website from detecting that the requests are being made by a spider
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
        `headers` is a dictionary that contains two key-value pairs. The first key-value pair specifies
        the `accept` header, which tells the server what type of response the client is willing to
        accept. The value of this key is a string that lists the different types of content that the
        client can accept, in order of preference. The second key-value pair specifies the `user-agent`
        header, which identifies the client making the request. The value of this key is a randomly
        selected user agent string from the `user_agents` list, which helps to prevent the website from
        detecting that the requests are being made by a spider and potentially blocking them.
    '''
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': user_agents[randint(0,len(user_agents)-1)],
        }
    def __init__(self, name=None, **kwargs):
        """
        This is a constructor method that initializes an object with a name and an argument link.
        
        :param name: The name parameter is an optional argument that can be passed to the constructor of
        the class. If a value is provided for name, it will be stored as an instance variable called
        "arg_link". If no value is provided for name, arg_link will be set to None
        """
        super().__init__(name, **kwargs)
        self.arg_link = name
    def start_requests(self):
        """
        This is a function that yields a scrapy request object with a callback function and headers
        based on a given link or start URL.
        """

        if self.arg_link is not None:
            yield scrapy.Request(self.arg_link,callback=self.pagination,headers=self.headers,meta={'main_url':self.arg_link})
        else:
            yield scrapy.Request(self.start_url,callback=self.get_links,headers=self.headers)
        
    def get_links(self,response):
        """
        This function extracts links from a website related to food, beverage, and hospitality
        businesses and other buiness categories and sends requests to those links for further pagination.
        
        :param response: The response object contains the HTML content of the webpage that was requested
        by the spider
        """
        food_and_bev = response.xpath('//li//a[text()="Food, Beverage & Hospitality"]/../../../ul//a/@href').extract()
        food_and_bev = [self.baseUrl+url for url in food_and_bev]
        main_urls = response.xpath('//div[text()="Business Categories"]/../ul/li/div/label/span/a/@href').extract()
        main_urls = [self.baseUrl+url for url in main_urls if url!='/business-for-sale/australia/food-beverage-hospitality/']
        for main_url in main_urls:
            yield scrapy.Request(main_url,callback=self.pagination,headers=self.headers,meta={"main_url":main_url})
        
        for food_url in food_and_bev:
            yield scrapy.Request(food_url,callback=self.pagination,headers=self.headers,meta={"main_url":food_url})
            
    def pagination(self,response):
        """
        This function performs pagination by extracting links from a webpage, following them, and
        recursively calling itself to continue pagination until there are no more pages.
        
        :param response: The response object that is returned after making a request to a URL
        """
        current_page = response.meta.get('page')
        main_url = response.meta.get('main_url')
        links = response.xpath('//h2/a/@href').extract()
        print(f'{response.url}: total links:{len(links)}')
        for link in links:
            new_link = self.baseUrl+link
            yield scrapy.Request(new_link,callback=self.information,headers=self.headers)
        next_page = response.xpath("//a[.//span[contains(@class, 'sr-only') and contains(text(), 'Next page')]]/@href").get()
        if next_page:
            if current_page is None:
                current_page = 1
            next_page = main_url+"?pn="
            cur_page = current_page+1
            next_page = next_page+str(cur_page)
            yield scrapy.Request(next_page, callback=self.pagination, headers=self.headers,meta={'page':cur_page,'main_url':main_url})
       
    def information(self,response):
        """
        This function extracts information from a webpage and returns it as a dictionary.
        
        :param response: The response object contains the HTML content of the webpage that is being
        scraped
        """

        listing_id = response.xpath('//td[contains(@data-testid,"Business ID")]/text()').get(default='NA')
        listing_type = response.xpath('//span[@data-testid="mainCategory"]/text()').get(default='NA')
        listing_title = response.xpath('//h1/text()').get(default='NA').replace('\n',' ').replace('\r','')
        listing_price = response.xpath('//span[@class="icon-text" and contains(text(), "$")]/text()').get(default='NA')
        listing_location = response.xpath('//li//span[@class="icon-text" and not(contains(text(), "$"))]/text()').get(default='NA')
        category_list = response.xpath('//th[text()="Category"]/../td//a/text()').extract()
        unique_category_list = ", ".join(list(dict.fromkeys(category_list)))
        broker = response.xpath('//span[@title="View broker profile"]/text()').extract()
        broker_name = 'NA'
        broker_organization = 'NA'
        if len(broker)>=2:
            broker_name = broker[0]
            broker_organization = broker[1]
        elif len(broker)==1:
            broker_name = broker[0]
        item = {}

        item['Listing URL'] = response.url
        item['Listing Id'] = listing_id
        item['Listing Type'] = listing_type
        item['Listing Title'] = listing_title
        item['Listing Price'] = listing_price
        item['Listing Categories'] = unique_category_list
        item['Listing Location'] = listing_location
        item['Seller Organization'] = broker_organization
        item['Seller Personal Name'] = broker_name

        yield item

