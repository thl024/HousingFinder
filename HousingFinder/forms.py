from django import forms


class RentalPropertySearchForm(forms.Form):
    max_price = forms.IntegerField(label="Maximum Price")
    min_price = forms.IntegerField(label="Minimum Price")
