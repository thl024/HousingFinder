import datetime

def parse_craigslist_date(datestr):
    current_date = datetime.datetime.now().date()
    if datestr == "now":
        return current_date
    else:
        # No year specified on availability date; assume year of the next time the month/day will be reached
        avail_date = datetime.datetime.strptime(datestr, '%b %d').date()
        avail_date = avail_date.replace(year=2018)
        if current_date > avail_date:
            avail_date = avail_date.replace(year=current_date.year + 1)
        return avail_date

def parseRFC3339(datetimestr):
    for idx, character in enumerate(datetimestr):
        if not (character.isdigit() or character == '-'):
            post_date = datetime.datetime.strptime(str(datetimestr[:idx]), '%Y-%m-%d').date()
            return post_date

    # Expected date format incorrect
    return None
    