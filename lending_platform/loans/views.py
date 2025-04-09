import uuid
from django.utils import timezone
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from .models import CustomerSubscription, LoanApplication
from .serializers import (
    SubscriptionSerializer,
    LoanApplicationSerializer,
    LoanRequestSerializer,
    LoanStatusSerializer,
    ClientRegistrationSerializer,
)
from .services import CBSService, ScoringService

class SubscriptionAPI(APIView):
    def post(self, request):
        customer_number = request.data.get('customer_number')
        if not customer_number:
            return Response(
                {"error": "Customer number is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if customer exists in CBS
        kyc_data = CBSService.get_customer_kyc(customer_number)
        if not kyc_data:
            return Response(
                {"error": "Customer not found in CBS"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check for existing subscription
        subscription, created = CustomerSubscription.objects.get_or_create(
            customer_number=customer_number,
            defaults={'is_active': True}
        )
        
        # Check for active loans
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

class LoanRequestAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = LoanRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        customer_number = serializer.validated_data['customer_number']
        amount = serializer.validated_data['amount']
        
        # Check for active loans
        active_loans = LoanApplication.objects.filter(
            customer_number=customer_number,
            status__in=['PENDING', 'PROCESSING', 'APPROVED', 'DISBURSED']
        ).exists()
        
        if active_loans:
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
        
        # Start scoring process (async in real implementation)
        client_reg = ClientRegistration.objects.first()
        if client_reg:
            scoring_token = ScoringService.initiate_scoring(customer_number, client_reg.token)
            if scoring_token:
                loan.scoring_token = scoring_token
                loan.save()
                
                # In production, this would be a Celery task
                score_data = ScoringService.query_score(scoring_token, client_reg.token)
                if score_data:
                    loan.score = score_data.get('score')
                    loan.credit_limit = score_data.get('limitAmount')
                    
                    # Simple loan decision logic
                    if loan.score >= 500 and amount <= loan.credit_limit:
                        loan.status = 'APPROVED'
                        loan.approved_amount = amount
                        loan.interest_rate = 12.5  # Example rate
                        loan.term_days = 30
                        loan.disbursement_date = timezone.now().date()
                        loan.due_date = timezone.now().date() + timedelta(days=30)
                    else:
                        loan.status = 'REJECTED'
                    
                    loan.save()
        
        response_data = {
            "status": loan.status,
            "message": "Loan application received and being processed",
            "applicationId": application_id,
            "timestamp": timezone.now().isoformat()
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

class LoanStatusAPI(APIView):
    def get(self, request, application_id):
        try:
            loan = LoanApplication.objects.get(application_id=application_id)
            serializer = LoanStatusSerializer(loan)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except LoanApplication.DoesNotExist:
            return Response(
                {"error": "Loan application not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class TransactionDataAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, customer_number):
        transactions = CBSService.get_customer_transactions(customer_number)
        if not transactions:
            return Response(
                {"error": "No transactions found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Convert SOAP response to JSON format expected by scoring engine
        transaction_list = []
        
        if hasattr(transactions, 'transaction'):
            for tx in transactions.transaction:
                tx_data = {field: getattr(tx, field, None) for field in tx.__dict__['__values__']}
                transaction_list.append(tx_data)
        
        response_data = {
            "customerNumber": customer_number,
            "transactions": transaction_list
        }
        
        return Response(response_data, status=status.HTTP_200_OK)