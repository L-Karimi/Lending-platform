from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionAPI, LoanRequestAPI, LoanStatusAPI, TransactionDataAPI
router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('subscribe/', SubscriptionAPI.as_view(), name='subscription'),
    path('request/', LoanRequestAPI.as_view(), name='loan-request'),
    path('status/<str:application_id>/', LoanStatusAPI.as_view(), name='loan-status'),
    path('transactions/<str:customer_number>/', TransactionDataAPI.as_view(), name='transaction-data'),
]