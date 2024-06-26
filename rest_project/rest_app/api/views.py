from rest_app.api.serializers import VerificationRequestSerializer
from rest_app.models import VerificationRequest
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_app.script import main
import json
from json import JSONEncoder
import logging

debug_logger = logging.getLogger('debug_logger')


class CustomEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            # If the object is bytes, decode it to string
            return obj.decode('utf-8', errors='replace')
        elif isinstance(obj, str):
            # If the object is already string, return it as is
            return obj
        else:
            # For other types, return their default JSON representation
            return super().default(obj)

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
                obj.request_response = json.dumps(response, cls=CustomEncoder)
                obj.save(update_fields=['request_status','request_response'])
                serializer=self.get_serializer(obj)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)   
        except Exception as e:
            debug_logger.exception(f"Exception occured {e} during processing API request.")
            return Response({'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
            
            