from django import forms  # Importing necessary modules

class HourlyFcastForm(forms.Form):  # Defines a form class for handling hourly forecast data
    city_name = forms.CharField(max_length=254, required=False)  # Defines a form field for city name input

    def clean_city_name(self):  # Defines a method to clean and validate city name input
        city_name = self.cleaned_data.get('city_name')  # Gets the cleaned city name input
        print(city_name, not city_name)  # Prints city name and whether it's empty
        if not city_name:  # Checks if city name is empty
            raise forms.ValidationError('This field is required')  # Raises a validation error if city name is empty
        return city_name  # Returns the cleaned city name input
