from scrapy import Spider,Request
import json
class Franchisedirect_Spider(Spider):
    name = 'franchisedirect'
    headers = {
        'authority': 'www.franchisedirect.com.au',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
    def start_requests(self):
        yield Request(
            url = 'https://www.franchisedirect.com.au/search/options/location?moduleId=0000016c-096d-dd02-ab6e-297fd8c50000',
            headers = self.headers,
            callback=self.main_page
        )

    def main_page(self,response):
            headers = {
                'authority': 'www.franchisedirect.com.au',
                'accept': 'text/html, */*; q=0.01',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'no-cache, no-store, must-revalidate',
                'expires': '0',
                'pragma': 'no-cache',
                'referer': 'https://www.franchisedirect.com.au/search/?sort=name',
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Linux"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }
            headers['referer'] = response.url
            for pgno in range(1,10):
                # url = 'https://www.franchisedirect.com.au/search/?sort=name&page={}&multiPage=false&_viewType=ajaxTag&format=json'
                yield Request(
                    url = f'https://www.franchisedirect.com.au/search/?page={pgno}&multiPage=false&_viewType=ajaxTag&format=json',#&location_id={value}',
                    callback=self.listing,
                    headers=headers,
                )
                headers['referer'] = response.url
    def listing(self,response):
        meta = response.meta
        locations = meta.get('locations')
        franching = response.xpath('//li[@data-franchiseinfo]')
        for franchise in franching:
            franch_info = franchise.xpath('.//@data-franchiseinfo').get()
            link = franchise.xpath('.//a/@href').get()
            yield Request(
                url= link,
                headers=self.headers,
                callback=self.information,
                meta = {'franchise':franch_info,'locations':locations},
                dont_filter=True,
            )
    def information(self,response):
        """
        The function extracts information from a web page response and returns a dict object
        with the extracted data.
        
        :param response: The `response` parameter is the response object that is returned after making a
        request to a URL. It contains the HTML content of the webpage that was requested
        """
        """
        1. Listing URL -> done
        2. Listing id -> done
        3. Listing type 
        4. Listing title -> done
        5. Listing price where available 
        6. Listing categories -> done
        7. Listing locations
        8. Seller's organisation's name
        """
        meta = response.meta
        # locations = meta.get('locations')

        franchise_info = meta.get('franchise')
        franchise_info = json.loads(franchise_info)
        franchise_id = franchise_info.get('franchiseId').replace('\r','').replace('\n','')
        franchise_name = franchise_info.get('franchiseName').replace('\r','').replace('\n','')
        # franchise_category = franchise_info.get('franchiseTrackingCategory')
        category = response.xpath('//li[@itemprop="itemListElement"]/a/@title')[-1].get().replace('\r','').replace('\n','')
        source_id = franchise_info.get('requestListSourceId')
        try:
            investment = response.xpath('//dt[contains(text(),"Investment:")]/following-sibling::dd')[0].xpath('.//text()').get()
        except:
            investment = None
        try:
            locations = response.xpath('//dt[contains(text(),"Available Locations:")]/following-sibling::dd/text()')[0].get()
        except:
            locations = None
        try:
            location_type = response.xpath('//dt[contains(text(),"Type:")]/following-sibling::dd/text()')[0].get()
        except:
            location_type = None

        try:
            associations =response.xpath('//dt[contains(text(),"Franchise Associations")]/following-sibling::dd//text()')[0].get()
        except:
            associations = None
        
        if investment:
            investment = investment.strip().strip('$').replace(',','').replace('\r','').replace('\n','')
        if locations:
            locations = locations.strip().replace('\r','').replace('\n','')
        if location_type:
            location_type = location_type.strip().replace('\r','').replace('\n','')
        if associations:
            associations = associations.strip().replace('\r','').replace('\n','')
        items = {}
        items['ListingURL'] = response.url
        items['ListingID'] = franchise_id
        items['ListingType'] = location_type
        items['ListingTitle'] = franchise_name
        items['ListingPrice'] = investment
        items['ListingCategory'] = category
        items['ListingLocations'] = locations
        items['SellersOrganizationName'] = associations
        yield items
