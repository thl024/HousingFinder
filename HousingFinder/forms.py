from django import forms

class CAPESearchForm(forms.Form):
    instructor = forms.CharField(label="Instructor", required=True)
    course = forms.CharField(label="Course", required=False)
    # TODO; add more filters

    # Validate such that at least one field needs to be populated
    # def clean(self):
    #     cleaned_data = super(CAPESearchForm, self).clean()
    #     if not (cleaned_data.get('course') or cleaned_data.get('instructor')):
    #         raise forms.ValidationError('Fill out at least one field')
    #     return cleaned_data