from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers

class CustomRegisterSerializer(RegisterSerializer):
    username = None 
    email = serializers.EmailField(required=True)

    # name = serializers.CharField(required=True, max_length=100)
    # phone = serializers.CharField(required=True, max_length=20)

    # def get_cleaned_data(self):
    #     data = super().get_cleaned_data()
    #     data.update({
    #         'name': self.validated_data.get('name', ''),
    #         'phone': self.validated_data.get('phone', ''),
    #     })
    #     return data

class CustomLoginSerializer(LoginSerializer):
    username = None  
    email = serializers.EmailField(required=True)