from rest_framework import serializers
from .models import CustomerSubscription, LoanApplication, ClientRegistration

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSubscription
        fields = ['customer_number', 'is_active', 'subscribed_at']

class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = '__all__'

class LoanRequestSerializer(serializers.Serializer):
    customer_number = serializers.CharField(max_length=50)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

class LoanStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = [
            'application_id', 'customer_number', 'requested_amount', 
            'approved_amount', 'status', 'score', 'credit_limit',
            'interest_rate', 'term_days', 'application_date',
            'disbursement_date', 'due_date', 'repayment_date'
        ]

class ClientRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientRegistration
        fields = '__all__'