import requests
from zeep import Client,Settings
from django.conf import settings
from requests.auth import HTTPBasicAuth
import uuid
import time
from .models import ClientRegistration

class CBSService:
    @staticmethod
    def get_customer_kyc(customer_number):
        settings_zeep = Settings(strict=False, xml_huge_tree=True)
        client = Client(settings.CBS_WSDL_KYC, settings=settings_zeep)
        
        try:
            response = client.service.getCustomerKYC(
                customerNumber=customer_number,
                username=settings.CBS_USERNAME,
                password=settings.CBS_PASSWORD
            )
            return response
        except Exception as e:
            print(f"Error fetching KYC: {str(e)}")
            return None

    @staticmethod
    def get_customer_transactions(customer_number):
        settings_zeep = Settings(strict=False, xml_huge_tree=True)
        client = Client(settings.CBS_WSDL_TRANSACTIONS, settings=settings_zeep)
        
        try:
            response = client.service.getCustomerTransactions(
                customerNumber=customer_number,
                username=settings.CBS_USERNAME,
                password=settings.CBS_PASSWORD
            )
            return response
        except Exception as e:
            print(f"Error fetching transactions: {str(e)}")
            return None

class ScoringService:
    @staticmethod
    def register_client():
        payload = {
            "url": f"{settings.BASE_URL}/api/v1/transactions/",
            "name": settings.SERVICE_NAME,
            "username": settings.SERVICE_USERNAME,
            "password": settings.SERVICE_PASSWORD
        }
        
        try:
            response = requests.post(settings.SCORING_REGISTER_URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                client = ClientRegistration.objects.create(
                    client_id=data['id'],
                    url=data['url'],
                    name=data['name'],
                    username=data['username'],
                    password=data['password'],
                    token=data['token']
                )
                return client
            return None
        except Exception as e:
            print(f"Error registering client: {str(e)}")
            return None

    @staticmethod
    def initiate_scoring(customer_number, client_token):
        url = f"{settings.SCORING_INITIATE_URL}/{customer_number}"
        headers = {'client-token': client_token}
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json().get('token')
            return None
        except Exception as e:
            print(f"Error initiating scoring: {str(e)}")
            return None

    @staticmethod
    def query_score(token, client_token, max_retries=5, retry_interval=10):
        url = f"{settings.SCORING_QUERY_URL}/{token}"
        headers = {'client-token': client_token}
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
            
            if attempt < max_retries - 1:
                time.sleep(retry_interval)
        
        return None