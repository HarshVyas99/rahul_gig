from django import forms
from rest_app.models import advance_search_options

class VerificationRequestForm(forms.Form):
    email_address = forms.EmailField(label="Your email address", max_length=100, required=True)
    phone = forms.CharField(max_length=20, required=False)
    advanced_search = forms.ChoiceField(required=True, choices=advance_search_options, initial="no")