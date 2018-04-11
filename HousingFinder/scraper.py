import scrapy
import date

class CraigslistURLScraper(scrapy.Spider):
    name = 'Cragislist URL Scraper'
    allowed_domains = ['craigslist.org']

    # Currently on east SD Apartments
    start_urls = [
        'https://sandiego.craigslist.org/search/esd/apa'
    ]

    def parse(self, response):
        # Get URLs to housings
        for house_url in response.selector.css('.result-title').xpath("@href").extract():
            yield scrapy.Request(house_url, callback=self.parse_house_details)

        # Deal with pagination
        
    def parse_house_details(self, response):
        name = response.selector.xpath('//span[@id=$val]/text()', val='titletextonly').extract_first()
        address = response.selector.css('.mapaddress').xpath('./text()').extract_first()
        rent_price = response.selector.css('.price').xpath('./text()').extract_first()[1:]
        description = response.selector.xpath('//section[@id=$val]/text()', val='postingbody').extract_first()
        
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
        tags = [x.encode('UTF8') for x in tags]

        listing_url = response.request.url

        # Use address and post_datetime_str as keys

