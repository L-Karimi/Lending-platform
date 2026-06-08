# Digital Lending Platform API

A Django REST Framework-based Digital Lending Platform designed to automate loan origination, customer onboarding, credit scoring, loan processing, and repayment tracking.

The platform integrates with external services such as Credit Scoring Engines, Core Banking Systems (CBS), and KYC verification providers to enable secure and efficient loan processing.

## Overview

This project provides APIs for:

* Customer registration and subscription
* Customer KYC verification
* Credit scoring and eligibility assessment
* Loan application processing
* Loan status tracking
* Transaction history retrieval
* Core Banking System (CBS) integration
* Repayment management

The solution is designed to support digital lending institutions, SACCOs, microfinance organizations, and fintech companies seeking to automate their lending operations.

---

## Features

### Customer Management

* Customer registration and onboarding
* Customer subscription management
* Customer profile management
* KYC verification

### Loan Processing

* Loan application submission
* Loan eligibility checks
* Credit scoring integration
* Loan approval and rejection workflows
* Loan status tracking

### Transaction Management

* Customer transaction history
* Loan disbursement tracking
* Repayment tracking
* Account activity monitoring

### Integrations

* Core Banking System (CBS)
* Credit Scoring Engine
* KYC Verification Services
* REST APIs

---

## Technology Stack

### Backend

* Python
* Django
* Django REST Framework

### Database

* PostgreSQL / MySQL

### API Tools

* Postman
* REST APIs

### Authentication

* Token Authentication
* API Key Integration

---

## System Architecture

```text
Customer
   │
   ▼
Digital Lending Platform
   │
   ├── KYC Verification Service
   │
   ├── Credit Scoring Engine
   │
   ├── Core Banking System (CBS)
   │
   └── Loan Management Module
```

---

# Loan Application Workflow

1. Customer registers on the platform.
2. Customer completes KYC verification.
3. Platform retrieves customer profile information.
4. Credit Scoring Engine evaluates customer risk.
5. Loan eligibility is determined.
6. Customer submits loan application.
7. Loan application is reviewed.
8. Approved loans are disbursed through CBS.
9. Repayment schedules are generated.
10. Customer can track loan status and repayments.

---

# User Stories

### Customer Registration

As a customer,

I want to register on the platform

So that I can access lending services.

### Loan Application

As a customer,

I want to apply for a loan

So that I can receive financial assistance.

### Credit Assessment

As a lending institution,

I want to evaluate customer creditworthiness

So that I can reduce lending risk.

### Loan Tracking

As a customer,

I want to monitor my loan status

So that I know the progress of my application.

---

# API Endpoints

## Customer APIs

### Register Customer

```http
POST /api/customers/register/
```

Creates a new customer account.

Request:

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "254700000000",
  "national_id": "12345678"
}
```

---

### Customer Profile

```http
GET /api/customers/{customer_id}/
```

Returns customer profile information.

---

### Customer Subscription

```http
POST /api/customers/subscribe/
```

Subscribes a customer to lending services.

---

## KYC APIs

### Verify Customer KYC

```http
POST /api/kyc/verify/
```

Validates customer identity information.

---

## Scoring APIs

### Retrieve Customer Score

```http
GET /api/scoring/{customer_id}/
```

Returns customer credit score and eligibility information.

---

## Loan APIs

### Apply for Loan

```http
POST /api/loans/apply/
```

Creates a new loan application.

Request:

```json
{
  "customer_id": 1,
  "loan_amount": 50000,
  "loan_term": 12
}
```

---

### Get Loan Details

```http
GET /api/loans/{loan_id}/
```

Returns loan information.

---

### Get Loan Status

```http
GET /api/loans/{loan_id}/status/
```

Returns current loan processing status.

---

### List Customer Loans

```http
GET /api/customers/{customer_id}/loans/
```

Returns all loans associated with a customer.

---

## Transaction APIs

### Customer Transactions

```http
GET /api/customers/{customer_id}/transactions/
```

Returns customer transaction history.

---

### Repayment History

```http
GET /api/loans/{loan_id}/repayments/
```

Returns repayment records.

---

## Integration APIs

### CBS Customer Validation

```http
POST /api/integrations/cbs/customer-validation/
```

Validates customer details with the Core Banking System.

---

### CBS Account Information

```http
GET /api/integrations/cbs/account/{account_number}/
```

Returns account information from CBS.

---

### Credit Scoring Integration

```http
POST /api/integrations/scoring/
```

Retrieves customer scoring information from the scoring engine.

---

# Future Enhancements

* Mobile lending application
* AI-powered credit risk assessment
* Automated loan recommendations
* SMS and Email notifications
* Digital wallet integration
* Fraud detection module
* Analytics dashboard
* Customer self-service portal

---

# Author

Lucy Karimi

* GitHub: https://github.com/L-Karimi
* Email: [karimiluccy@gmail.com](mailto:karimiluccy@gmail.com)

---

# License

This project is intended for educational, portfolio, and demonstration purposes.
