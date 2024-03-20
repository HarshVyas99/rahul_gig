from rest_app.api.serializers import VerificationRequestSerializer
from rest_app.models import VerificationRequest
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_app.script import main
import json


class VerificationRequestCreateView(CreateAPIView):
    serializer_class = VerificationRequestSerializer
    
    def get_queryset(self):
         return VerificationRequest.objects.all()
     
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            valid=serializer.is_valid(raise_exception=True)
            if valid:
                # Create a validation request for user and verify the details
                self.perform_create(serializer)
                # Call the script for verification
                response=main(serializer.validated_data['email_address'],serializer.validated_data['phone'],serializer.validated_data['advanced_search'])
                if not response['status'] == 'Success':
                    raise Exception
                request_id=serializer.data['id']
                obj=VerificationRequest.objects.filter(id=request_id).first()
                obj.request_status=response['status']
                obj.request_response=json.dumps(response)
                obj.save(update_fields=['request_status','request_response'])
                serializer=self.get_serializer(obj)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)   
        except Exception as e:
            return Response({'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
            
            