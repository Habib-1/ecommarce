from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from .models import Customer,User

class CustomRegisterSerializer(RegisterSerializer):
    username = None 
    email = serializers.EmailField(required=True)

class CustomLoginSerializer(LoginSerializer):
    username = None  
    email = serializers.EmailField(required=True)


class CustomerSerializer(serializers.ModelSerializer):
    
    name = serializers.CharField(source='user.name')
    phone = serializers.CharField(source='user.phone')

    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'address','city','postal_code','country']
       

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        user.name = user_data.get('name', user.name)
        user.phone = user_data.get('phone', user.phone)
        user.save()

        return super().update(instance, validated_data)
