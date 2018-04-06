from django.core.management.base import BaseCommand, CommandError
from HousingFinder.scraper import Scraper
from optparse import make_option

# class Command(BaseCommand):
#     help = 'Scrapes CAPE url for storage into database.'

#     option_list = BaseCommand.option_list + (
#         make_option('--startdept',
#             dest='startdept',
#             help='Select a department to start scraping from (Department Prefix)',
#             type='string'),

#         make_option('--enddept',
#             dest='enddept',
#             help='Select a department to end scraping from (Department Prefix)',
#             type='string'),

#         make_option('--count',
#             dest='count',
#             help='Number of elements to scrape',
#             type=int),
#     )

#     def handle(self, *args, **options):
#         startdept = None if 'startdept' not in options else options['startdept']
#         enddept = None if 'enddept' not in options else options['enddept']
#         count= None if 'count' not in options else options['count']
#         s = Scraper(startdept, enddept, count)
#         s.begin()
