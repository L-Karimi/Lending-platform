import os
from dotenv import load_dotenv

load_dotenv()

INSTALLED_APPS = [
    # ...
    'rest_framework',
    'loans',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
    ],
}

# CBS SOAP Settings
CBS_WSDL_KYC = os.getenv('CBS_WSDL_KYC', 'https://kycapitest.credable.io/service/customerWsdl.wsdl')
CBS_WSDL_TRANSACTIONS = os.getenv('CBS_WSDL_TRANSACTIONS', 'https://trxapitest.credable.io/service/transactionWsdl.wsdl')
CBS_USERNAME = os.getenv('CBS_USERNAME', 'admin')
CBS_PASSWORD = os.getenv('CBS_PASSWORD', 'pwd123')

# Scoring Engine Settings
SCORING_BASE_URL = os.getenv('SCORING_BASE_URL', 'https://scoringtest.credable.io/api/v1')
SCORING_REGISTER_URL = f"{SCORING_BASE_URL}/client/createClient"
SCORING_INITIATE_URL = f"{SCORING_BASE_URL}/scoring/initiateQueryScore"
SCORING_QUERY_URL = f"{SCORING_BASE_URL}/scoring/queryScore"

# Our service settings
SERVICE_NAME = os.getenv('SERVICE_NAME', 'DigitalLendingPlatform')
SERVICE_USERNAME = os.getenv('SERVICE_USERNAME', 'lending_user')
SERVICE_PASSWORD = os.getenv('SERVICE_PASSWORD', 'lending_pass123')
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')