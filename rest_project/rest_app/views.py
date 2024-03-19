from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.

from rest_app.forms import VerificationRequestForm


def get_form_view(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = VerificationRequestForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            print(form.cleaned_data)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = VerificationRequestForm()

    return render(request, "verify_request.html", {"form": form})