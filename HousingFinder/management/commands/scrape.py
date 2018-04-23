from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess

from HousingFinder.scraper import CraigslistURLScraper


class Command(BaseCommand):
    help = 'Scrapes url for storage into database.'

    # option_list = BaseCommand.option_list + (
    #     make_option('--startdept',
    #         dest='startdept',
    #         help='Select a department to start scraping from (Department Prefix)',
    #         type='string'),

    #     make_option('--enddept',
    #         dest='enddept',
    #         help='Select a department to end scraping from (Department Prefix)',
    #         type='string'),

    #     make_option('--count',
    #         dest='count',
    #         help='Number of elements to scrape',
    #         type=int),
    # )

    def handle(self, *args, **options):
        # startdept = None if 'startdept' not in options else options['startdept']
        # enddept = None if 'enddept' not in options else options['enddept']
        # count = None if 'count' not in options else options['count']
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })

        process.crawl(CraigslistURLScraper)
        process.start()
