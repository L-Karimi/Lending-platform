import uuid
import time
import logging
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import CustomerSubscription, LoanApplication, ClientRegistration
from .serializers import (
    LoanRequestSerializer,
    LoanStatusSerializer,
    SubscriptionSerializer
)
from .services import CBSService, ScoringService
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Welcome to the Lending Platform API!")
logger = logging.getLogger(__name__)

class SubscriptionAPI(APIView):
    """
    Handles customer subscription and initial checks
    """
    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        customer_number = serializer.validated_data['customer_number']
        
        try:
            # Check cache first
            cache_key = f"kyc_{customer_number}"
            kyc_data = cache.get(cache_key)
            
            if not kyc_data:
                kyc_data = CBSService.get_customer_kyc(customer_number)
                if not kyc_data:
                    return Response(
                        {"error": "Customer not found in CBS"},
                        status=status.HTTP_404_NOT_FOUND
                    )
                # Cache for 1 hour
                cache.set(cache_key, kyc_data, 3600)

            # Atomic transaction for subscription creation
            with transaction.atomic():
                subscription, created = CustomerSubscription.objects.get_or_create(
                    customer_number=customer_number,
                    defaults={'is_active': True}
                )

                active_loans = LoanApplication.objects.filter(
                    customer_number=customer_number,
                    status__in=['PENDING', 'PROCESSING', 'APPROVED', 'DISBURSED']
                ).exists()

            response_data = {
                "status": "SUCCESS",
                "message": "Customer subscribed successfully",
                "customerDetails": {
                    "name": getattr(kyc_data, 'customerName', ''),
                    "accountStatus": getattr(kyc_data, 'accountStatus', 'UNKNOWN'),
                    "existingLoan": active_loans
                }
            }
            
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Subscription error for {customer_number}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoanRequestAPI(APIView):
    """
    Handles loan applications with scoring integration
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = LoanRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        customer_number = serializer.validated_data['customer_number']
        amount = serializer.validated_data['amount']
        
        try:
            with transaction.atomic():
                # Check for active loans
                if LoanApplication.objects.filter(
                    customer_number=customer_number,
                    status__in=['PENDING', 'PROCESSING', 'APPROVED', 'DISBURSED']
                ).exists():
                    return Response(
                        {"error": "Customer has an active loan application"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Create loan application
                application_id = str(uuid.uuid4())
                loan = LoanApplication.objects.create(
                    application_id=application_id,
                    customer_number=customer_number,
                    requested_amount=amount,
                    status='PROCESSING'
                )

                # Get client registration
                client_reg = ClientRegistration.objects.first()
                if not client_reg:
                    loan.status = 'FAILED'
                    loan.save()
                    return Response(
                        {"error": "Scoring service not configured"},
                        status=status.HTTP_503_SERVICE_UNAVAILABLE
                    )

                # Initiate scoring
                scoring_token = ScoringService.initiate_scoring(
                    customer_number, 
                    client_reg.token
                )
                
                if not scoring_token:
                    loan.status = 'FAILED'
                    loan.save()
                    return Response(
                        {"error": "Could not initiate scoring"},
                        status=status.HTTP_502_BAD_GATEWAY
                    )

                loan.scoring_token = scoring_token
                loan.save()

                # Query score with retry mechanism
                max_retries = 3
                retry_delay = 2  # seconds
                score_data = None
                
                for attempt in range(max_retries):
                    try:
                        score_data = ScoringService.query_score(
                            scoring_token, 
                            client_reg.token
                        )
                        if score_data:
                            break
                    except Exception as e:
                        logger.warning(f"Scoring attempt {attempt + 1} failed: {str(e)}")
                        if attempt == max_retries - 1:
                            loan.status = 'FAILED'
                            loan.save()
                            return Response(
                                {
                                    "status": "FAILED",
                                    "message": "Scoring service unavailable",
                                    "applicationId": application_id
                                },
                                status=status.HTTP_200_OK
                            )
                        time.sleep(retry_delay)

                # Process scoring results
                if score_data:
                    loan.score = score_data.get('score', 0)
                    loan.credit_limit = score_data.get('limitAmount', 0)
                    loan.exclusion = score_data.get('exclusion', '')
                    
                    # Loan decision logic
                    if (loan.score >= 500 and 
                        amount <= loan.credit_limit and
                        loan.exclusion == 'No Exclusion'):
                        loan.status = 'APPROVED'
                        loan.approved_amount = amount
                        loan.interest_rate = 12.5  # Example rate
                        loan.term_days = 30
                        loan.disbursement_date = timezone.now().date()
                        loan.due_date = timezone.now().date() + timedelta(days=30)
                    else:
                        loan.status = 'REJECTED'
                        loan.rejection_reason = (
                            f"Score: {loan.score}, " 
                            f"Limit: {loan.credit_limit}, "
                            f"Exclusion: {loan.exclusion}"
                        )
                    
                    loan.save()

                response_data = {
                    "status": loan.status,
                    "message": "Loan application processed",
                    "applicationId": application_id,
                    "timestamp": timezone.now().isoformat()
                }
                
                if loan.status == 'REJECTED':
                    response_data['reason'] = loan.rejection_reason

                return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Loan request error: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoanStatusAPI(APIView):
    """
    Provides loan application status
    """
    def get(self, request, application_id):
        try:
            # Check cache first
            cache_key = f"loan_status_{application_id}"
            loan_data = cache.get(cache_key)
            
            if not loan_data:
                loan = LoanApplication.objects.get(application_id=application_id)
                serializer = LoanStatusSerializer(loan)
                loan_data = serializer.data
                # Cache for 5 minutes
                cache.set(cache_key, loan_data, 300)
            
            return Response(loan_data, status=status.HTTP_200_OK)
            
        except LoanApplication.DoesNotExist:
            return Response(
                {"error": "Loan application not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Status check error: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TransactionDataAPI(APIView):
    """
    Provides transaction data to Scoring Engine
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, customer_number):
        try:
            # Check cache first
            cache_key = f"transactions_{customer_number}"
            transactions = cache.get(cache_key)
            
            if not transactions:
                transactions = CBSService.get_customer_transactions(customer_number)
                if not transactions:
                    return Response(
                        {"error": "No transactions found"},
                        status=status.HTTP_404_NOT_FOUND
                    )
                # Cache for 1 hour
                cache.set(cache_key, transactions, 3600)
            
            # Convert SOAP response to JSON
            transaction_list = []
            if hasattr(transactions, 'transaction'):
                for tx in transactions.transaction:
                    tx_data = {
                        field: getattr(tx, field, None) 
                        for field in tx.__dict__['__values__']
                    }
                    transaction_list.append(tx_data)
            
            return Response({
                "customerNumber": customer_number,
                "transactions": transaction_list
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Transaction data error: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )