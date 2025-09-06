from rest_framework import serializers
from .models import  Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "payment_method", "amount", "status", "transaction_id", "paid_at"]
        read_only_fields = ["amount", "status", "transaction_id", "paid_at"]