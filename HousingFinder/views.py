import urllib

from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from rest_framework.renderers import JSONRenderer

from forms import RentalPropertySearchForm
from models import RentalProperty
from serializers import RentalPropertySerializer


class RentalPropertyMapView(FormView):
    
    form_class = RentalPropertySearchForm
    template_name = 'rental_property_map.html'
    data = None

    def get_context_data(self, **kwargs):

        raw_filters = dict(self.request.GET)
        filters = {}

        for filter, target in raw_filters.iteritems():
            if "min_price" in raw_filters:
                filters[""]

        objects = RentalProperty.objects.filter(**filters)
        ser_objects = RentalPropertySerializer(objects, many=True)
        kwargs['object_list'] = JSONRenderer().render(ser_objects.data)

        return super(RentalPropertyMapView, self).get_context_data(**kwargs)

    def form_valid(self, form):

        print(form.cleaned_data)

        self.data = form.cleaned_data
        return super(RentalPropertyMapView, self).form_valid(form)

    def get_success_url(self):
        return "%s?%s" % (reverse_lazy('rental-property-map'),
                  urllib.urlencode(self.data))