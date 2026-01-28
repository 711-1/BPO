from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['user', 'reference', 'status']
    
    def validate(self, data):
        if data['transaction_type'] in ['deposit', 'withdrawal']:
            if data['amount'] <= 0:
                raise serializers.ValidationError("Сумма должна быть положительной")
        
        return data

class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=10)
    payment_method = serializers.CharField(max_length=50)

class WithdrawalSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=50)
    bank_account = serializers.CharField(max_length=100)