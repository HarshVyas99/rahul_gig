from django.db import models

advance_search_options=[("yes","Yes"),("no","No")]

# Create your models here.
class VerificationRequest(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    email_address = models.EmailField(max_length=100, blank=False, null=False)
    phone = models.CharField(max_length=20,blank=True,null=True)
    advanced_search = models.CharField(max_length=3, choices=advance_search_options, default="no", blank=False,null=False)
    request_status=models.CharField(max_length=10,blank=True,null=True)
    request_response=models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['created']