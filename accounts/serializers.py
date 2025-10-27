from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from .models import Customer,User

class CustomRegisterSerializer(RegisterSerializer):
    username = None  # we use email as username
    name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    
    # Customer fields
    address = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    state = serializers.CharField(required=False, allow_blank=True)
    postal_code = serializers.CharField(required=False, allow_blank=True)
    country = serializers.CharField(required=False, default="Bangladesh")

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            "name": self.validated_data.get("name", ""),
            "phone": self.validated_data.get("phone", ""),
            "address": self.validated_data.get("address", ""),
            "city": self.validated_data.get("city", ""),
            "state": self.validated_data.get("state", ""),
            "postal_code": self.validated_data.get("postal_code", ""),
            "country": self.validated_data.get("country", "Bangladesh"),
        })
        return data

    def save(self, request):
        # 1. Save the User
        user = super().save(request)
        user.name = self.cleaned_data.get("name")
        user.phone = self.cleaned_data.get("phone")
        user.save()

        # 2. Create Customer with extra fields
        Customer.objects.create(
            user=user,
            address=self.cleaned_data.get("address"),
            city=self.cleaned_data.get("city"),
            state=self.cleaned_data.get("state"),
            postal_code=self.cleaned_data.get("postal_code"),
            country=self.cleaned_data.get("country"),
        )
        return user

class CustomLoginSerializer(LoginSerializer):
    username = None  
    email = serializers.EmailField(required=True)


class CustomerSerializer(serializers.ModelSerializer):
    
    name = serializers.CharField(source='user.name')
    phone = serializers.CharField(source='user.phone')

    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'address','city','state','postal_code','country']
       

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        user.name = user_data.get('name', user.name)
        user.phone = user_data.get('phone', user.phone)
        user.save()

        return super().update(instance, validated_data)
