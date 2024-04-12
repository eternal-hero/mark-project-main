import scrapy
import json
from scrapy.exceptions import CloseSpider


class Edenexchange_Spider(scrapy.Spider):
    name = "edenexchange"
    allowed_domains = ["x"]
    start_urls = ["http://x/"]
    # handle_httpstatus_list  = [500]

    def start_requests(self):
        """
        This function sends a POST request to a website's API to retrieve data on listings, with
        pagination.
        """
        url = "https://listingapi.edenexchange.com/api/v1/public/listings/search"
        for i in range(1, 99):
            payload = json.dumps(
                {
                    "page": {"no": i, "size": 100},
                    "query": {"filter": [], "search": {}},
                    "sort": [],
                }
            )
            headers = {
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.9",
                "Access-Control-Allow-Origin": "*",
                "Cache-Control": "no-cache",
                "Content-Type": "application/json",
                "Cookie": "_ga=GA1.1.1223670527.1687799258; _gcl_au=1.1.624965257.1687799258; _hjFirstSeen=1; _hjIncludedInSessionSample_666562=1; _hjSession_666562=eyJpZCI6IjcwOWJmNGUxLTY3ZGQtNGZiMC04ZDgwLTgzMWY4OWY5M2Y2MCIsImNyZWF0ZWQiOjE2ODc3OTkyNTg3OTcsImluU2FtcGxlIjp0cnVlfQ==; _hjAbsoluteSessionInProgress=0; _fbp=fb.1.1687799258846.1400916201; prism_89464044=85d38d97-3925-4cd2-b4ca-710acb640735; _hjMinimizedPolls=229591; _hjSessionUser_666562=eyJpZCI6ImEzNzBjYjUxLTM2NDktNTBlZS05NDQ1LTRlYzAwYWNjZDI5YiIsImNyZWF0ZWQiOjE2ODc3OTkyNTg3ODYsImV4aXN0aW5nIjp0cnVlfQ==; _hjDonePolls=229591; bid=18d13cf2-f6ca-4e8a-b73b-8dfce8414ce7; _ga_7L35YVY0G4=GS1.1.1687799258.1.1.1687799659.59.0.0",
                "Origin": "https://www.edenexchange.com",
                "Pragma": "no-cache",
                "Referer": "https://www.edenexchange.com/",
                "Sec-Ch-Ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            }
            yield scrapy.Request(
                url,
                callback=self.getProductsIds,
                method="POST",
                headers=headers,
                body=payload,
                dont_filter=True,
            )

    def getProductsIds(self, response):
        """
        This function extracts product IDs and their corresponding categories from a JSON response and
        sends a scrapy request for each ID.

        :param response: The response parameter is the HTTP response received after making a request to
        a website using Scrapy. It contains the HTML content of the webpage or any other data that was
        requested
        """
        jo = json.loads(response.body)
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "no-cache",
            "Content-Type": "application/json",
            "Cookie": "_gcl_au=1.1.624965257.1687799258; _fbp=fb.1.1687799258846.1400916201; prism_89464044=85d38d97-3925-4cd2-b4ca-710acb640735; _hjMinimizedPolls=229591; _hjSessionUser_666562=eyJpZCI6ImEzNzBjYjUxLTM2NDktNTBlZS05NDQ1LTRlYzAwYWNjZDI5YiIsImNyZWF0ZWQiOjE2ODc3OTkyNTg3ODYsImV4aXN0aW5nIjp0cnVlfQ==; _hjDonePolls=229591; bid=18d13cf2-f6ca-4e8a-b73b-8dfce8414ce7; _hjAbsoluteSessionInProgress=0; _gid=GA1.2.1204281100.1687807847; _ga_7L35YVY0G4=GS1.1.1687807835.3.1.1687808663.59.0.0; _ga=GA1.1.1223670527.1687799258; _hjIncludedInSessionSample_666562=1; _hjSession_666562=eyJpZCI6ImI5ZTUyMWY2LTk2NWYtNGJlNS1hM2NkLWRiNGNmOTViOWI0NSIsImNyZWF0ZWQiOjE2ODc4MDg2NjM3NjYsImluU2FtcGxlIjp0cnVlfQ==",
            "Origin": "https://www.edenexchange.com",
            "Pragma": "no-cache",
            "Referer": "https://www.edenexchange.com/",
            "Sec-Ch-Ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        }
        for dic in jo["data"]["content"]:
            id = dic["id"]
            mydic = {}
            print(dic["industries"])
            if dic["industries"] != None:
                for ind in dic.get("industries", []):
                    mydic[ind["industry_id"]] = ind["industry_name"]
                mylist = []
            if dic["sectors"] != None:
                for sec in dic.get("sectors", []):
                    mylist.append(
                        f"{mydic.get(int(sec['industry_id']))}-{sec['sector_name']}"
                    )
            try:
                category = ", ".join(mylist)
            except UnboundLocalError:
                category = ""
            url = f"https://listingapi.edenexchange.com/api/v1/public/listings/{id}"
            yield scrapy.Request(
                url,
                callback=self.parse,
                dont_filter=True,
                headers=headers,
                meta={"category": category},
            )
    def parse(self, response):
        """
        This function parses a response from a website and extracts various information about a business
        listing, which is then returned as a dictionary.

        :param response: The response object contains the data returned by the website after making a
        request to it
        """
        if response.status == 500:
            raise CloseSpider("Received 500 status code")
        mylist = []
        meta = response.meta

        jo = json.loads(response.body)
        code = jo.get("data").get("status_information").get("listing_id")
        ListingPrice = jo.get("data").get("detailed_information").get("asking_price")
        ListingTitle = (
            jo.get("data").get("detailed_information").get("title_of_listing")
        )
        flag = True
        try:
            for dic in jo.get("data").get("industry_sectors"):
                try:
                    mylist.append(
                        f"{dic['industry_sector']['industry_name']}-{dic['industry_sector']['sector_name']}"
                    )
                except KeyError:
                    flag = False
                    ListingType = meta.get("category")
                    ListingCategory = f"{ListingType},{ListingType}"
        except TypeError:
            flag = False
            ListingType = meta.get("category")
            ListingCategory = f"{ListingType},{ListingType}"
        if flag:
            ListingType = ", ".join(mylist)
            if ListingType != "":
                ListingCategory = f"{ListingType},{ListingType}"
            else:
                ListingCategory = ""
        try:
            Suburb = (
                jo.get("data")
                .get("detailed_information")
                .get("listing_address")
                .get("suburb")
            )
        except AttributeError:
            Suburb = None
        try:
            State = (
                jo.get("data")
                .get("detailed_information")
                .get("listing_address")
                .get("state")
            )
        except AttributeError:
            State = None
        try:
            PostCode = (
                jo.get("data")
                .get("detailed_information")
                .get("listing_address")
                .get("pin_code")
            )
        except AttributeError:
            PostCode = None

        SellerOrganizationName = (
            jo.get("data").get("business_information").get("business_trading_name")
        )
        irrelevant_symbs = ['?','/','#','(',')','{','}','[',']']
        urltitle = ListingTitle.replace("  ", " ").replace(" ", "-")
        for symb in irrelevant_symbs:
            urltitle = urltitle.replace(symb,'')
        ListingID = jo.get("data").get("status_information").get("id")
        ListingURL = f"https://www.edenexchange.com/business-for-sale/{code}/{urltitle}?listingId={ListingID}&flowType=home"

        items = {}
        items["ListingURL"] = ListingURL
        items["ListingID"] = ListingID
        items["ListingTitle"] = ListingTitle
        items["ListingPrice"] = ListingPrice
        items["State"] = State
        items["Suburb"] = Suburb
        items["PostCode"] = PostCode
        items["SellerOrganizationName"] = SellerOrganizationName
        items["ListingType"] = ListingType
        items["ListingCategory"] = ListingCategory

        yield items