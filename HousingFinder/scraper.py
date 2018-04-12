from models import Apartment

import scrapy
import date

from db import get_db

class CraigslistURLScraper(scrapy.Spider):
    name = 'Cragislist URL Scraper'
    allowed_domains = ['craigslist.org']

    # Currently on east SD Apartments
    start_urls = [
        'https://sandiego.craigslist.org/search/esd/apa'
    ]

    def __init__(self, *a, **kw):
        super(CraigslistURLScraper, self).__init__(*a, **kw)
        self.db = get_db()
        self.db.drop()

    def parse(self, response):
        # Get URLs to housings
        for house_url in response.selector.css('.result-title').xpath("@href").extract():
            yield scrapy.Request(house_url, callback=self.parse_house_details)

        # Deal with pagination
        
    def parse_house_details(self, response):
        name = response.selector.xpath('//span[@id=$val]/text()', val='titletextonly').extract_first()

        address = response.selector.css('.mapaddress').xpath('./text()').extract_first()
        if not address is None:
            address = address.encode('UTF8').strip("\n").strip("\t") if not address.isspace() else None

        latitude = response.selector.xpath('//div[@id=$val]/@data-latitude', val='map').extract_first()
        longitude = response.selector.xpath('//div[@id=$val]/@data-longitude', val='map').extract_first()

        rent_price = response.selector.css('.price').xpath('./text()').extract_first()
        if rent_price is not None: # Rent not always populated
            rent_price = rent_price[1:]

        description_a = response.selector.xpath('//section[@id=$val]/text()', val='postingbody').extract()
        description = []
        for sentence in description_a:
            stped = sentence.encode('UTF8').strip("\n")
            if not stped.isspace() and stped:
                description.append(stped)
        
        size = None
        bedrooms = None
        bathrooms = None
        available = None

        attrs = response.selector.css('.shared-line-bubble')

        if len(attrs) > 0:

            ind = 0
            e = attrs[ind].xpath('./b/text()').extract()

            if e:
                bedrooms = ''.join(character for character in e[0] if character.isdigit())
                if len(e) > 1:
                    bathrooms = ''.join(character for character in e[1] if character.isdigit())
                ind += 1

            e = attrs[ind].xpath('./b/text()').extract_first()
            if e != None and e.isdigit():
                size = e
                ind += 1

            available = attrs[ind].xpath('./text()').extract_first().replace('available ', '')

        date_available = date.parse_craigslist_date(available)
        post_datetime_str = response.selector.xpath('//p[@id=$val]/time/@datetime', val='display-date').extract_first()
        post_date = date.parseRFC3339(post_datetime_str)

        # tags
        tags = response.selector.css('.attrgroup')[1].xpath('./span/text()').extract()
        tags = [x.encode('UTF8').strip("\n").strip("\t") for x in tags if not x.isspace()]

        listing_url = response.request.url

        if address is not None:
            # Use address and post_datetime_str as keys
            data = {
                "name": name,
                "address": address,
                "latitude": latitude,
                "longitude": longitude,
                "offered_by": None,
                "description": description,

                "date_available": date_available,
                "post_date": post_date,

                "rent_price": rent_price,
                "application_fee": None,
                "security_deposit": None,

                "size": size,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "amenities": None,
                "tags": tags,

                "listing_url": listing_url, 
            }

            identifier = {
                "address": address,
            }

            
            try:
                self.db.replace_one(identifier, data, upsert=True)
                print("Saved new element: {}".format(address))
            except Exception as e:
                print("Failed to save apartment: {}".format(address))
                print(e)
        else:
            print("No address, not saving: {}".format(address))
