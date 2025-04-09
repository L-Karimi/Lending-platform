from django.db import models
from django.utils import timezone

class CustomerSubscription(models.Model):
    customer_number = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer_number} - {'Active' if self.is_active else 'Inactive'}"

class LoanApplication(models.Model):
    APPLICATION_STATUS = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('DISBURSED', 'Disbursed'),
        ('REPAID', 'Repaid'),
        ('FAILED', 'Failed'),
    ]
    
    application_id = models.CharField(max_length=36, unique=True)
    customer_number = models.CharField(max_length=50)
    requested_amount = models.DecimalField(max_digits=12, decimal_places=2)
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='PENDING')
    scoring_token = models.CharField(max_length=100, null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    term_days = models.IntegerField(null=True, blank=True)
    application_date = models.DateTimeField(auto_now_add=True)
    disbursement_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    repayment_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.application_id} - {self.customer_number} - {self.status}"

class ClientRegistration(models.Model):
    client_id = models.IntegerField()
    url = models.URLField()
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.token}"