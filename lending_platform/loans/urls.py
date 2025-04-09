from django.urls import path
from .views import (
    SubscriptionAPI, LoanRequestAPI, 
    LoanStatusAPI, TransactionDataAPI
)

urlpatterns = [
    path('subscribe/', SubscriptionAPI.as_view(), name='subscription'),
    path('request/', LoanRequestAPI.as_view(), name='loan-request'),
    path('status/<str:application_id>/', LoanStatusAPI.as_view(), name='loan-status'),
    path('transactions/<str:customer_number>/', TransactionDataAPI.as_view(), name='transaction-data'),
]