from scrapy import Spider,Request
from random import randint
import json


class Businessforsale_Spider(Spider):
    name = "businessforsale"
    base_url = "https://www.businessforsale.com.au/"
    location_url = "https://www.businessforsale.com.au/search?location="
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/100.0.100.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/604.1 Edg/100.0.100.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edge/18.19042',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edge/18.19042',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/65.0.3467.48',
            'Mozilla/5.0 (X11; CrOS x86_64 10066.0.0) AppwleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        ]

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': user_agents[randint(0,len(user_agents)-1)],
        }

    def start_requests(self):
        url = "https://www.businessforsale.com.au/search"
        yield Request(url,callback=self.parse_location,headers=self.headers)
    def parse_location(self,response):
        locations = json.loads(response.xpath('//listing-sidebar').get().split('location_options')[-1].split('selected_regions')[0][2:-3].replace('&quot;','"').strip())
        for location in locations:
            print(location["name"].replace(" ","-").lower())
            location_name = location["name"].replace(" ","-").lower()
            new_url = self.location_url+location_name
            yield Request(new_url,callback=self.parse_listing,headers=self.headers)
            # break

    
    def parse_listing(self,response):
        no_data = response.xpath('//h1[contains(text(),"No exact matches found")]/text()').get()
        if no_data:
            return
        
        listing_urls = response.xpath('//a[@id="main-link"]/@href').extract()

        for listing_url in listing_urls:
            yield Request(listing_url, callback=self.parse_information, headers=self.headers)

        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            yield Request(next_page,callback=self.parse_listing,headers=self.headers)

    def parse_information(self,response):

        title = response.xpath('//h1[@class="title"]/text()').get()
        price = response.xpath('//strong[@class="price"]/text()').get()
        categories = " > ".join([cat.strip() for cat in response.xpath('//ul[@class="breadcrumb"]//li//text()').extract() if cat.strip() != ""])
        location = response.xpath('//span[@class="location"]/text()').get()
        listing_id = response.xpath('//span[@class="ref-num"]/text()').get()
        if listing_id:
            listing_id = listing_id.split(":")[-1].strip()
        
        
        location_type = response.xpath('//li[@class="breadcrumb-item active"]/text()').get()

        associations = response.xpath('//a[@class="user-logo"]/@href').get()
        '''
        Listing URL
        Listing id 
        Listing type 
        Listing title 
        Listing price where available 
        Listing categories 
        Listing location (suburb, state, postcode) 
        Seller’s organisation’s name
        '''
        items = {}
        items['ListingURL'] = response.url
        items['ListingID'] = listing_id
        items['ListingType'] = location_type
        items['ListingTitle'] = title
        items['ListingPrice'] = price
        items['ListingCategory'] = categories
        items['ListingLocations'] = location
        items['SellersOrganizationName'] = associations

        yield items