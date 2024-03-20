from rest_framework import serializers
from rest_app.models import VerificationRequest, advance_search_options
import json

class VerificationRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email_address = serializers.EmailField(required=True, max_length=100)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=20)
    advanced_search= serializers.ChoiceField(choices=advance_search_options, default="no")
    request_status= serializers.CharField(required=False, allow_blank=True, max_length=10, allow_null=True, read_only=True)
    request_response= serializers.JSONField(required=False, allow_null=True, read_only=True)
    
    def create(self, validated_data):
        """
        Create and return a new `VerificationRequest` instance, given the validated data.
        """
        return VerificationRequest.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `VerificationRequest` instance, given the validated data.
        """
        instance.email_address = validated_data.get('email_address', instance.email_address)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.advanced_search = validated_data.get('advanced_search', instance.advanced_search)
        instance.save(update_fields=['email_address', 'phone', 'advanced_search'])
        return instance
    
    def to_representation(self, instance):
        # Get the default representation of the data
        data = super().to_representation(instance)
        # Converting text back to JSON
        if data['request_response'] is not None:
            data['request_response'] = json.loads(data['request_response'])  # Converting text back to JSON
        
        return data