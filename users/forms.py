from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# Retrieve the custom User model
User = get_user_model()

# Form for user registration
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    # Initialize form with crispy form helper
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Sign Up'))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Form for profile editing
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'username', 'email', 'image']

    # Initialize form with crispy form helper
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        # Sets form control class for styling
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control w-100'})
