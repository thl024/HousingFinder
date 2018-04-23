from django.db import connections

DB_NAME = "HousingFinder_rentalproperties"


def get_db():
    db_wrap = connections['default']
    return db_wrap.get_collection(DB_NAME)
