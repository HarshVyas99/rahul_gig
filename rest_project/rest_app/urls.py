from django.urls import path, include
from rest_app.views import get_form_view

urlpatterns = [
    path('form/', get_form_view, name='form-view'),
    path('api/',include('rest_app.api.urls'))
]