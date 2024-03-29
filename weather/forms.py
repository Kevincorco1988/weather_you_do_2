from django import forms

class HourlyFcastForm(forms.Form):
    city_name = forms.CharField(max_length=254, required=False)

    def clean_city_name(self):
        city_name = self.cleaned_data.get('city_name')
        print(city_name, not city_name)
        if not city_name:
            raise forms.ValidationError('This field is required')
        return city_name