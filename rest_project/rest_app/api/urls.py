from django.urls import path
from rest_app.api.views import VerificationRequestCreateView

urlpatterns = [
    path('verify-request/', VerificationRequestCreateView.as_view(), name='user-data'),
]

