from forms import CAPESearchForm
from models import CAPE
from db import get_db

from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse

import re

class SearchView(FormView):
    template_name = 'search.html'
    form_class = CAPESearchForm
    url = None

    def form_valid(self, form):
        data = form.cleaned_data
        self.url = "%s?"
        first = False
        for key in data:
            if data[key] != "":
                if first:
                    self.url += "&"
                self.url += key + "=" + data[key]
                first = True
        return super(SearchView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return self.url % reverse('results')


class ResultsView(ListView):

    template_name = 'results.html'

    def get_queryset(self):

        kwargs = dict(self.request.GET)

        match_query = {}
        for key, value in kwargs.items():
            match_query[key] = {"$regex": "{}".format(value[0])}
        mq = {"$match": match_query}

        group_query = {"_id": {}}
        for key in kwargs:
            group_query["_id"][key] = "${}".format(key)
        gq = {"$group": group_query}

        cape_collection = get_db()
        mongo_cursor = cape_collection.aggregate([mq, gq])
        objs = []

        for cape in mongo_cursor:
            objs.append(cape["_id"])

        return objs
