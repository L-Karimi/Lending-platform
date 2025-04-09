import os
from dotenv import load_dotenv

load_dotenv()

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'loans',
]
ROOT_URLCONF = 'lending_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
    ],
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'lending_platform_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
STATIC_URL = '/static/'
TIME_ZONE = os.getenv('TIME_ZONE', 'Africa/Nairobi')
SECRET_KEY = os.getenv('SECRET_KEY', 't+zlp_hmj0uro^3kye(w-c#$nz(ojf6umu_h-z-0m2gtun2544')

DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
# Allowed hosts - handle string splitting safely
allowed_hosts = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts.split(',') if host.strip()]
# CBS SOAP Settings
CBS_WSDL_KYC = os.getenv('CBS_WSDL_KYC', 'https://kycapitest.credable.io/service/customerWsdl.wsdl')
CBS_WSDL_TRANSACTIONS = os.getenv('CBS_WSDL_TRANSACTIONS', 'https://trxapitest.credable.io/service/transactionWsdl.wsdl')
CBS_USERNAME = os.getenv('CBS_USERNAME', 'admin')
CBS_PASSWORD = os.getenv('CBS_PASSWORD', 'pwd123')
DEBUG = True
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
