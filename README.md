# Digital Lending Platform API

A Django REST Framework-based Digital Lending Platform API designed to support customer subscription, loan application processing, credit scoring, loan status tracking, and transaction data retrieval.

The platform integrates with a Core Banking System (CBS) and a Scoring Engine to automate digital lending workflows, including KYC checks, loan eligibility assessment, and loan decisioning.

## Overview

This project provides backend APIs for a digital lending workflow where customers can be subscribed, verified against CBS data, assessed through a scoring engine, and processed for loan approval or rejection.

The system is suitable for financial institutions, SACCOs, microfinance institutions, and fintech platforms that want to automate loan origination and customer credit assessment.

## Features

* Customer subscription and onboarding
* CBS-based customer KYC lookup
* Active loan validation
* Loan application submission
* Credit scoring integration
* Automated loan approval or rejection
* Loan status tracking
* Customer transaction data retrieval
* API authentication for protected endpoints
* Caching for KYC, loan status, and transaction data
* Error handling and logging
* Atomic database transactions for data consistency

## Technology Stack

* Python
* Django
* Django REST Framework
* Django ORM
* Django Cache Framework
* REST APIs
* Core Banking System integration
* Scoring Engine integration

## API Base URL

```http
/api/v1/loans/
```

The main project URL configuration routes all loan-related APIs through:

```python
path('api/v1/loans/', include('loans.urls'))
```

## Available API Modules

The project includes the following API views:

* `SubscriptionAPI`
* `LoanRequestAPI`
* `LoanStatusAPI`
* `TransactionDataAPI`

## API Endpoints

> Note: The final endpoint paths depend on the mappings defined in `loans/urls.py`. The examples below use recommended endpoint names based on the available API views.

### 1. Customer Subscription API

```http
POST /api/v1/loans/subscribe/
```

Subscribes a customer to the lending platform after checking customer KYC details from the Core Banking System.

#### Functionality

* Validates submitted customer data
* Checks customer KYC details from CBS
* Caches KYC data for one hour
* Creates or retrieves a customer subscription
* Checks whether the customer has an active loan
* Returns customer subscription status and customer details

#### Sample Request

```json
{
  "customer_number": "CUS001"
}
```

#### Sample Success Response

```json
{
  "status": "SUCCESS",
  "message": "Customer subscribed successfully",
  "customerDetails": {
    "name": "John Doe",
    "accountStatus": "ACTIVE",
    "existingLoan": false
  }
}
```

#### Possible Error Responses

```json
{
  "error": "Customer not found in CBS"
}
```

```json
{
  "error": "Internal server error"
}
```

## 2. Loan Request API

```http
POST /api/v1/loans/apply/
```

Handles loan applications and integrates with the scoring engine to determine whether a loan should be approved or rejected.

This endpoint requires authentication.

#### Functionality

* Validates loan request data
* Checks whether the customer already has an active loan
* Creates a loan application with a unique application ID
* Initiates customer scoring
* Queries the scoring engine with retry logic
* Applies loan decision rules
* Approves or rejects loan applications based on:

  * Customer score
  * Credit limit
  * Exclusion status
  * Requested loan amount

#### Sample Request

```json
{
  "customer_number": "CUS001",
  "amount": 5000
}
```

#### Loan Approval Logic

A loan is approved if:

```text
score >= 500
requested amount <= credit limit
exclusion == "No Exclusion"
```

If approved, the system sets:

* Approved amount
* Interest rate
* Loan term
* Disbursement date
* Due date

#### Sample Success Response

```json
{
  "status": "APPROVED",
  "message": "Loan application processed",
  "applicationId": "generated-uuid",
  "timestamp": "2026-06-08T10:00:00"
}
```

#### Sample Rejection Response

```json
{
  "status": "REJECTED",
  "message": "Loan application processed",
  "applicationId": "generated-uuid",
  "timestamp": "2026-06-08T10:00:00",
  "reason": "Score: 450, Limit: 3000, Exclusion: No Exclusion"
}
```

#### Possible Error Responses

```json
{
  "error": "Customer has an active loan application"
}
```

```json
{
  "error": "Scoring service not configured"
}
```

```json
{
  "error": "Could not initiate scoring"
}
```

## 3. Loan Status API

```http
GET /api/v1/loans/status/{application_id}/
```

Returns the current status of a loan application.

#### Functionality

* Retrieves loan application by application ID
* Uses cached loan status data where available
* Caches loan status for five minutes
* Returns serialized loan application status

#### Sample Response

```json
{
  "application_id": "generated-uuid",
  "customer_number": "CUS001",
  "requested_amount": 5000,
  "status": "APPROVED",
  "approved_amount": 5000,
  "score": 700,
  "credit_limit": 10000,
  "interest_rate": 12.5,
  "term_days": 30,
  "disbursement_date": "2026-06-08",
  "due_date": "2026-07-08"
}
```

#### Possible Error Response

```json
{
  "error": "Loan application not found"
}
```

## 4. Transaction Data API

```http
GET /api/v1/loans/transactions/{customer_number}/
```

Provides customer transaction data to the scoring engine.

This endpoint requires authentication.

#### Functionality

* Retrieves customer transaction data from CBS
* Caches transaction data for one hour
* Converts SOAP transaction responses into JSON
* Returns customer transaction history

#### Sample Response

```json
{
  "customerNumber": "CUS001",
  "transactions": [
    {
      "transactionDate": "2026-06-01",
      "amount": 2500,
      "transactionType": "CREDIT",
      "description": "Deposit"
    }
  ]
}
```

#### Possible Error Response

```json
{
  "error": "No transactions found"
}
```

## Authentication

Some endpoints require authentication using Django REST Framework permissions.

Protected endpoints include:

* Loan Request API
* Transaction Data API

```python
permission_classes = [IsAuthenticated]
```

## Loan Statuses

The system supports the following loan statuses:

* `PENDING`
* `PROCESSING`
* `APPROVED`
* `DISBURSED`
* `REJECTED`
* `FAILED`

## Core Business Logic

### Customer Subscription Flow

1. Customer submits customer number.
2. System checks cached KYC data.
3. If no cache exists, the system retrieves KYC data from CBS.
4. System creates or retrieves customer subscription.
5. System checks whether the customer has an active loan.
6. Customer subscription details are returned.

### Loan Application Flow

1. Customer submits loan request.
2. System checks for existing active loans.
3. Loan application is created.
4. Scoring service is initiated.
5. Credit score is retrieved.
6. Loan decision rules are applied.
7. Loan is approved, rejected, or marked as failed.
8. Application status is returned.

### Scoring Decision Flow

```text
Loan Request
   ↓
Check Active Loan
   ↓
Create Loan Application
   ↓
Initiate Scoring
   ↓
Query Score
   ↓
Evaluate Score, Limit, and Exclusion
   ↓
Approve or Reject Loan
```

## Project Structure

```text
lending_platform/
│
├── lending_platform/
│   ├── urls.py
│   └── settings.py
│
├── loans/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── services.py
│   └── urls.py
│
└── manage.py
```

## Key Integrations

### CBS Service

Used for:

* Customer KYC lookup
* Customer transaction retrieval

### Scoring Service

Used for:

* Initiating credit scoring
* Querying customer score
* Returning credit limit and exclusion status

## Error Handling

The API handles common errors such as:

* Invalid request data
* Customer not found in CBS
* Existing active loan application
* Missing scoring service configuration
* Scoring engine failure
* Loan application not found
* Missing transaction data
* Internal server errors

## Caching

The project uses Django caching to improve performance:

| Data                  | Cache Duration |
| --------------------- | -------------: |
| Customer KYC data     |         1 hour |
| Loan status           |      5 minutes |
| Customer transactions |         1 hour |



## Author

Lucy Karimi

* GitHub: https://github.com/L-Karimi
* Email: [karimiluccy@gmail.com](mailto:karimiluccy@gmail.com)

## License

This project is intended for learning, portfolio demonstration, and fintech API development practice.
