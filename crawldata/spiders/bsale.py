import scrapy
from random import randint
import re
class Bsale_Spider(scrapy.Spider):
    name = "bsale"
    baseUrl = "https://bsale.com.au"
    start_url = "https://bsale.com.au/businesses-for-sale"

    # `custom_settings` is a dictionary that contains custom settings for the Scrapy spider.
    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 32,
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
        yield scrapy.Request(self.start_url,callback=self.pagination,headers=self.headers)

    def pagination(self,response):
        """
        This function extracts links from a webpage, sends requests to each link, and recursively calls
        itself to navigate to the next page if available.
        
        :param response: The response parameter is the HTTP response received after sending a request to
        a website using Scrapy. It contains the HTML content of the webpage and other metadata such as
        headers, status code, etc
        """
        links = response.xpath('//div[@class="listing-details"]/h3[1]/a/@href').extract()
        for link in links:
            # new_link = self.baseUrl+link
            yield scrapy.Request(link, callback=self.information,headers=self.headers,dont_filter=True)
        print(f'Search URL: {response.url} :Links:{len(links)} ')
        next_url = response.xpath('//li[@class="page-item"]/a/@href').extract()[-1]
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

        categories = response.xpath("//p/strong[text()='Business Category']/following-sibling::a/span/text()").extract()
        seller_org = response.xpath('//div[@class="p-3"]/a/@href').get(default="NA")
        if seller_org !="NA":
            seller_org = self.baseUrl+seller_org
        list_type = "NA"
        if len(categories)>0:
            list_type = categories[0]
        
        category = ", ".join(categories)
        item = {}
        sellerName = response.xpath('//div[@itemprop="seller"]//a[contains(@href,"/business-broker/")]/text()').get(default='NA').strip()
        if sellerName == "NA":
            sellerName = response.xpath("//div[h4/text() = 'Vendor details']/div/div[contains(div, 'Name:')]/div[2]/text()").get(default='NA').strip()
        item['Listing URL'] = response.url
        item['Listing Id'] = response.xpath('//p/strong[text()="Bsale ID:"]/following-sibling::text()').get(default='NA').strip()
        item['Listing Type'] = list_type
        item['Listing Title'] = response.xpath('//h1/text()').get(default='NA').replace('\n','').strip()
        item['Listing Price'] = response.xpath('//h2[contains(text(),"$")]/text()').get(default='NA').strip().replace('\n','')
        item['Listing Categories'] = category
        item['Listing Location'] = response.xpath('//strong[@class="mr-3"]/following-sibling::text()').get(default='NA').strip()
        item['Seller Organization'] = response.xpath('//div[@class="p-3"]/a/img/@alt').get(default='NA').strip()
        item['Seller Personal Name'] = response.xpath('//h5[text()="Contact Seller"]/following-sibling::div//h4/text()').get(default='NA').strip()

        yield item

