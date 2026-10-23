#!/usr/bin/env python3
"""
Production setup script for Mobile Banking Application - Agile Jury 2 (MBAJ2).
Creates Epics, User Stories, Supporting Tasks, Sample Bugs, and organizes Sprints.
"""

import sys
import time
import json
import jira_helper
from adf_helper import text_to_adf

PROJECT_KEY = "MBAJ2"
BOARD_ID = 35

# Sprints mapping
SPRINTS = {
    1: {"id": 35, "name": "Sprint 1: Secure Foundation"},
    2: {"id": 36, "name": "Sprint 2: Core Transactions"},
    3: {"id": 37, "name": "Sprint 3: Loans & Integration"}
}

# Issue Types
ISSUE_TYPES = {
    "Epic": "10045",
    "Story": "10048",
    "Task": "10047",
    "Bug": "10050"
}

STORY_POINT_FIELD = "customfield_10016"

EPICS_DATA = [
    {
        "name": "Security and Authentication",
        "description": """## Epic: Security and Authentication
Robust, multi-factor security framework ensuring end-to-end encryption, biometric authentication, session lifecycle management, and account recovery compliant with banking regulatory standards.
- Module: Security / Identity & Access Management (IAM)
- Target Sprint: Sprint 1 (Foundation)"""
    },
    {
        "name": "Account Management",
        "description": """## Epic: Account Management
Centralized dashboard for customer accounts, real-time balance inquiries across savings/checking/credit, comprehensive paginated transaction ledger, and PDF statement downloads.
- Module: Core Banking / Accounts
- Target Sprint: Sprint 1 (Foundation)"""
    },
    {
        "name": "Payments and Fund Transfers",
        "description": """## Epic: Payments and Fund Transfers
High-integrity payment engine supporting intra-bank transfers, external inter-bank settlement (IMPS/NEFT), beneficiary management, duplicate prevention via idempotency keys, and instant digital receipts.
- Module: Transaction Engine / Payments
- Target Sprint: Sprint 2 (Core Transactions)"""
    },
    {
        "name": "Loan Services",
        "description": """## Epic: Loan Services
End-to-end digital credit products module featuring interactive EMI calculation, real-time credit eligibility evaluation, digital loan applications with KYC document upload, and status tracking.
- Module: Retail Lending / Credit Services
- Target Sprint: Sprint 3 (Loans & Integration)"""
    },
    {
        "name": "Notifications and Alerts",
        "description": """## Epic: Notifications and Alerts
Multi-channel event-driven alerting system notifying customers of financial debits/credits, low balance warnings, security anomalies, and customizable customer alert preferences.
- Module: Event Messaging / Customer Alerts
- Target Sprint: Sprint 3 (Loans & Integration)"""
    }
]

STORIES_DATA = [
    # --- EPIC: Security and Authentication ---
    {
        "epic": "Security and Authentication",
        "summary": "Customer Authentication with Password & Biometrics",
        "priority": "Highest",
        "points": 5,
        "sprint": 1,
        "labels": ["Security", "Authentication", "Sprint-1"],
        "description": """## User Story
As a registered banking customer,
I want to log in securely using my alphanumeric password or device biometrics (Fingerprint / Face ID),
So that I can quickly and securely access my banking dashboard while keeping my funds protected.

### Acceptance Criteria
- Given a registered customer enters valid credentials or scans enrolled biometrics, When authentication is submitted, Then access token is issued and user is redirected to Dashboard within 1.5 seconds.
- Given an invalid password is entered 3 consecutive times, When the 4th attempt fails, Then the account is temporarily locked for 15 minutes and security notification is dispatched.
- Given an enrolled biometric prompt fails or is dismissed, When fallback is requested, Then the standard password login screen is presented.

### Technical & Architecture Notes
- JWT bearer tokens with 15-minute expiry.
- Secure Enclave / KeyStore biometric validation on iOS & Android.

### Dependencies
- Core User Directory & IAM API service."""
    },
    {
        "epic": "Security and Authentication",
        "summary": "Two-Factor Authentication (OTP / SMS / Email)",
        "priority": "Highest",
        "points": 5,
        "sprint": 1,
        "labels": ["Security", "MFA", "Sprint-1"],
        "description": """## User Story
As a customer logging in from an unrecognized device or performing high-value actions,
I want to verify my identity via a 6-digit Time-Based One-Time Password (OTP) sent to my registered mobile/email,
So that unauthorized individuals cannot access my account even if my password is breached.

### Acceptance Criteria
- Given primary authentication is successful from a new device, When 2FA is triggered, Then a 6-digit cryptographic OTP is generated and delivered via SMS/Email within 5 seconds.
- Given an active OTP, When entered correctly within 120 seconds, Then the session is elevated to authenticated state.
- Given an expired or incorrect OTP entered 3 times, When verification fails, Then OTP is invalidated and resend is throttled for 60 seconds.

### Dependencies
- Dependency on Story: Customer Authentication with Password & Biometrics
- External SMS Gateway / SMTP Dispatcher Service."""
    },
    {
        "epic": "Security and Authentication",
        "summary": "Session Inactivity Timeout and Automatic Logout",
        "priority": "High",
        "points": 3,
        "sprint": 1,
        "labels": ["Security", "SessionManagement", "Sprint-1"],
        "description": """## User Story
As a security-conscious mobile banking customer,
I want the application to automatically terminate my session after 5 minutes of inactivity,
So that my account is shielded from unauthorized access if I leave my mobile device unattended.

### Acceptance Criteria
- Given an active logged-in session, When no user touch or navigation event occurs for 4 minutes, Then an inactivity modal warning appears with a 60-second countdown.
- Given no user response during the countdown, When the timer reaches 0, Then the session token is revoked on client and server, and app returns to Login screen.
- Given the user taps "Keep Me Logged In", When confirmed, Then the session timer is reset to 5 minutes.

### Dependencies
- Dependency on Story: Customer Authentication with Password & Biometrics."""
    },
    {
        "epic": "Security and Authentication",
        "summary": "Secure Password Reset & Account Recovery Workflow",
        "priority": "High",
        "points": 3,
        "sprint": 1,
        "labels": ["Security", "AccountRecovery", "Sprint-1"],
        "description": """## User Story
As a customer who has forgotten my password,
I want a self-service password reset mechanism requiring multi-point identity verification,
So that I can regain access to my account securely without having to physically visit a branch.

### Acceptance Criteria
- Given the user taps "Forgot Password", When registered email or customer ID is submitted, Then identity verification via OTP and debit card PIN/security questions is initiated.
- Given identity is verified, When the user specifies a new password adhering to complexity requirements (min 10 chars, uppercase, lowercase, number, symbol), Then the password is updated.
- Given a successful password reset, When completed, Then all existing active sessions across all devices are immediately terminated.

### Dependencies
- Dependency on Story: Two-Factor Authentication (OTP / SMS / Email)."""
    },

    # --- EPIC: Account Management ---
    {
        "epic": "Account Management",
        "summary": "Real-Time Account Balance Overview for Multiple Accounts",
        "priority": "Highest",
        "points": 5,
        "sprint": 1,
        "labels": ["AccountManagement", "Dashboard", "Sprint-1"],
        "description": """## User Story
As a banking customer with savings and checking accounts,
I want to view my real-time available and ledger balances immediately on the dashboard,
So that I have an accurate snapshot of my financial position before making financial commitments.

### Acceptance Criteria
- Given an authenticated customer, When the Home dashboard loads, Then all linked accounts (Savings, Current, Credit) are displayed with masked account numbers and current balances.
- Given the user pulls to refresh, When the action triggers, Then balances are re-synchronized with Core Banking in under 1 second.
- Given an account has an active hold or overdraft, When tapped, Then available balance and ledger balance are explicitly distinguished.

### Dependencies
- Dependency on Story: Customer Authentication with Password & Biometrics
- Core Banking Balance Inquiry API."""
    },
    {
        "epic": "Account Management",
        "summary": "Paginated & Categorized Transaction History",
        "priority": "High",
        "points": 5,
        "sprint": 1,
        "labels": ["AccountManagement", "Transactions", "Sprint-1"],
        "description": """## User Story
As an active banking customer,
I want to scroll through my transaction history with date filters and spending categories,
So that I can track past debits, credits, merchants, and understand my spending habits.

### Acceptance Criteria
- Given an account is selected, When transaction history is viewed, Then transactions are displayed in chronological order with date, merchant name, category icon, and amount (red for debit, green for credit).
- Given a search query or date range filter (Last 30 days, Custom), When applied, Then matching records are returned instantaneously without full page reload.
- Given more than 20 records exist, When user reaches the bottom of the list, Then the next page is loaded asynchronously via infinite scroll.

### Dependencies
- Dependency on Story: Real-Time Account Balance Overview."""
    },
    {
        "epic": "Account Management",
        "summary": "Account Statement Generation and PDF/CSV Export",
        "priority": "Medium",
        "points": 3,
        "sprint": 1,
        "labels": ["AccountManagement", "Statements", "Sprint-1"],
        "description": """## User Story
As a banking customer needing formal financial documentation,
I want to download official monthly or custom-period account statements in password-protected PDF or CSV format,
So that I can maintain tax records, share proof of income, or analyze finances offline.

### Acceptance Criteria
- Given an account and date range (1 month, 3 months, 6 months, Custom up to 1 year), When "Generate Statement" is triggered, Then a digitally signed PDF statement is rendered.
- Given the generated statement, When downloaded or shared, Then it includes the bank's official letterhead, branch IFSC/MICR, customer details, and opening/closing balances.
- Given the customer enables security, When exported, Then PDF is encrypted using the customer's DOB and last 4 digits of phone number.

### Dependencies
- Dependency on Story: Paginated & Categorized Transaction History."""
    },
    {
        "epic": "Account Management",
        "summary": "Customer Profile & KYC Information Management",
        "priority": "Medium",
        "points": 3,
        "sprint": 1,
        "labels": ["AccountManagement", "Profile", "Sprint-1"],
        "description": """## User Story
As a customer with changing contact details,
I want to view my profile details, communication address, and KYC verification status,
So that my banking records remain up-to-date and compliant with regulatory guidelines.

### Acceptance Criteria
- Given a customer navigates to Settings > Profile, When viewed, Then registered phone, email, mailing address, and KYC status (Verified / Pending) are shown.
- Given an update to communication email or address is submitted, When verified via OTP, Then the change request is saved with audit timestamp.
- Given sensitive fields (PAN, Government ID, Primary Phone), When viewed, Then they are masked for privacy.

### Dependencies
- Dependency on Story: Customer Authentication with Password & Biometrics."""
    },

    # --- EPIC: Payments and Fund Transfers ---
    {
        "epic": "Payments and Fund Transfers",
        "summary": "Beneficiary Management (Add, Edit, Verify & Delete Payee)",
        "priority": "High",
        "points": 5,
        "sprint": 2,
        "labels": ["Payments", "Beneficiaries", "Sprint-2"],
        "description": """## User Story
As a customer who frequently sends money to family and vendors,
I want to add, verify, and maintain a list of trusted beneficiaries with bank details,
So that I can transfer funds quickly without re-entering account numbers and IFSC codes each time.

### Acceptance Criteria
- Given a customer enters payee account number, confirm account number, IFSC code, and nickname, When "Add Beneficiary" is clicked, Then bank branch is auto-resolved and verified.
- Given a new beneficiary is submitted, When confirmed via MFA OTP, Then the beneficiary is activated with a 30-minute cooling period (maximum transfer limit of $500 during cooling).
- Given an existing beneficiary, When the user chooses "Delete Payee", Then user confirmation is required and payee is removed immediately.

### Dependencies
- Dependency on Story: Two-Factor Authentication (OTP / SMS / Email)
- Bank IFSC / Routing Directory API."""
    },
    {
        "epic": "Payments and Fund Transfers",
        "summary": "Instant Intra-Bank and Inter-Bank Fund Transfers (IMPS/NEFT)",
        "priority": "Highest",
        "points": 8,
        "sprint": 2,
        "labels": ["Payments", "Transfers", "Sprint-2"],
        "description": """## User Story
As a customer needing to pay bills or send money,
I want to execute instant intra-bank and inter-bank fund transfers with real-time debit and credit confirmations,
So that funds are transferred accurately and instantly to the recipient.

### Acceptance Criteria
- Given an active sender account with sufficient funds and an active beneficiary, When amount and transfer mode (Instant IMPS or NEFT) are selected, Then fee breakdown and total debit are displayed.
- Given the user enters their transaction MPIN or biometric confirmation, When submitted, Then the transaction is processed through payment gateway within 3 seconds.
- Given successful completion, When transaction settles, Then sender balance updates instantly and a unique Reference Number (URN) is issued.

### Dependencies
- Dependency on Story: Beneficiary Management
- Dependency on Story: Real-Time Account Balance Overview
- National Payment Switch / Inter-Bank Clearing Gateway."""
    },
    {
        "epic": "Payments and Fund Transfers",
        "summary": "Idempotency Key Validation & Duplicate Transfer Prevention",
        "priority": "Highest",
        "points": 3,
        "sprint": 2,
        "labels": ["Payments", "Integrity", "Sprint-2"],
        "description": """## User Story
As a banking customer experiencing fluctuating network connectivity,
I want the payment system to prevent duplicate transactions if I accidentally tap 'Pay' multiple times or retry on connection drop,
So that I am never charged twice for the same transfer.

### Acceptance Criteria
- Given a user taps the 'Submit Payment' button, When request is initiated, Then a client-generated UUID idempotency key is attached in the request header and the UI button is disabled.
- Given a repeated request with the same idempotency key arrives at backend within 120 seconds, When evaluated, Then the existing transaction status is returned without executing a second debit.
- Given a network retry succeeds, When response arrives, Then the user is shown the original receipt with duplicate detection notification.

### Dependencies
- Dependency on Story: Instant Intra-Bank and Inter-Bank Fund Transfers."""
    },
    {
        "epic": "Payments and Fund Transfers",
        "summary": "Failed Transaction Handling, Auto-Reversals & Error State UI",
        "priority": "High",
        "points": 5,
        "sprint": 2,
        "labels": ["Payments", "ErrorHandling", "Sprint-2"],
        "description": """## User Story
As a customer whose transfer fails due to inter-bank timeout or technical rejection,
I want immediate transparent error explanations and automatic balance reversal,
So that I am not left in confusion about where my money is.

### Acceptance Criteria
- Given a payment request fails at recipient bank gateway, When failure is reported, Then the app displays a clear human-readable error (e.g. "Beneficiary bank unavailable, funds reversed").
- Given funds were momentarily deducted before downstream failure, When reversal event triggers, Then ledger balance is credited back within 5 seconds with an audit log.
- Given an unresolved pending status from clearing house, When 30 seconds elapse, Then ticket is assigned a "Pending Verification" state with tracking instructions.

### Dependencies
- Dependency on Story: Instant Intra-Bank and Inter-Bank Fund Transfers."""
    },
    {
        "epic": "Payments and Fund Transfers",
        "summary": "Digital Transaction Receipts & Shareable Payment Confirmations",
        "priority": "Medium",
        "points": 2,
        "sprint": 2,
        "labels": ["Payments", "Receipts", "Sprint-2"],
        "description": """## User Story
As a customer who completed a payment,
I want an interactive digital receipt containing reference number, beneficiary details, and timestamp with share options,
So that I can send proof of payment to the payee via WhatsApp, Email, or save as image.

### Acceptance Criteria
- Given a successful transfer completion, When the success screen is rendered, Then transaction ID, beneficiary name, account number (masked), timestamp, and amount are presented.
- Given the user taps "Share Receipt", When native sharing dialog opens, Then a branded digital receipt card is exported as image or PDF.
- Given past transactions in history, When any item is tapped, Then the full digital receipt can be re-viewed and re-shared at any time.

### Dependencies
- Dependency on Story: Instant Intra-Bank and Inter-Bank Fund Transfers."""
    },
    {
        "epic": "Payments and Fund Transfers",
        "summary": "Daily and Per-Transaction Transfer Limit Controls & Warnings",
        "priority": "High",
        "points": 3,
        "sprint": 2,
        "labels": ["Payments", "Limits", "Sprint-2"],
        "description": """## User Story
As a customer managing security risk,
I want to view and configure my daily transfer limits and receive warnings when approaching the limit,
So that I can control my maximum exposure and prevent unauthorized large withdrawals.

### Acceptance Criteria
- Given customer initiates a transfer that exceeds their remaining daily limit (e.g., $5,000/day), When calculated before authorization, Then transfer is blocked with error stating remaining allowable quota.
- Given customer attempts to raise daily transfer limit, When submitted, Then cooling period and high-level biometric/OTP authentication are enforced.
- Given remaining daily limit is within 10% of maximum, When user views transfer screen, Then an informational warning banner is displayed.

### Dependencies
- Dependency on Story: Instant Intra-Bank and Inter-Bank Fund Transfers
- Core Banking Limits Configuration Engine."""
    },

    # --- EPIC: Loan Services ---
    {
        "epic": "Loan Services",
        "summary": "Loan Products Catalog & Interactive Loan EMI Calculator",
        "priority": "Medium",
        "points": 3,
        "sprint": 3,
        "labels": ["Loans", "Calculator", "Sprint-3"],
        "description": """## User Story
As a customer exploring borrowing options,
I want to browse available loan products (Personal, Home, Auto, Education) and simulate monthly EMIs using sliders for principal, tenure, and interest,
So that I can determine an affordable monthly repayment schedule before applying.

### Acceptance Criteria
- Given the Loans section is opened, When loan products catalog renders, Then interest rates, maximum tenure, and processing fees are compared clearly.
- Given user adjusts the loan amount slider ($1,000 - $50,000) and tenure (6 - 60 months), When sliders change, Then monthly EMI, total interest payable, and amortization breakdown update instantaneously.
- Given simulated EMI is acceptable, When user taps "Apply with these Terms", Then values are carried forward into the digital loan application.

### Dependencies
- Financial Amortization Formula Service."""
    },
    {
        "epic": "Loan Services",
        "summary": "Instant Pre-Approved Loan Eligibility Assessment Engine",
        "priority": "High",
        "points": 5,
        "sprint": 3,
        "labels": ["Loans", "Eligibility", "Sprint-3"],
        "description": """## User Story
As an existing customer with regular banking history,
I want the app to assess my credit profile and inform me of pre-approved loan amounts and interest rates,
So that I can access credit instantly without waiting days for manual underwriting.

### Acceptance Criteria
- Given an active customer with >= 6 months of account transactions, When "Check Eligibility" is requested, Then eligibility engine evaluates monthly inflow, average balance, and credit score.
- Given credit criteria are met, When calculation completes within 3 seconds, Then pre-approved limit and special APR offer are presented.
- Given criteria are not met, When decision is returned, Then helpful suggestions for improving eligibility are displayed without hard credit inquiry impact.

### Dependencies
- Dependency on Story: Real-Time Account Balance Overview
- Credit Bureau / Underwriting Decisioning Service API."""
    },
    {
        "epic": "Loan Services",
        "summary": "Digital Personal Loan Application with Document Upload & e-KYC",
        "priority": "High",
        "points": 8,
        "sprint": 3,
        "labels": ["Loans", "Application", "Sprint-3"],
        "description": """## User Story
As an eligible customer needing funds,
I want to complete an end-to-end digital loan application including income verification and document upload,
So that I can get approval and loan disbursal entirely online without paperwork.

### Acceptance Criteria
- Given an applicant selects a loan amount and tenure, When personal details are confirmed, Then income proof (salary slip or bank statement) and identity document upload prompts are presented.
- Given document files (PDF, JPG, PNG under 5MB) are selected, When uploaded, Then OCR scans and validates documents for readability and integrity.
- Given all steps and terms are accepted via digital signature, When submitted, Then application reference number is generated and queued for final automated decision.

### Dependencies
- Dependency on Story: Instant Pre-Approved Loan Eligibility Assessment Engine
- Document Storage & Secure File Scanning Service."""
    },
    {
        "epic": "Loan Services",
        "summary": "Loan Application Lifecycle Status Tracking & Disbursal History",
        "priority": "Medium",
        "points": 3,
        "sprint": 3,
        "labels": ["Loans", "Tracking", "Sprint-3"],
        "description": """## User Story
As a customer who submitted a loan application,
I want to track the real-time review, approval, and disbursal progress on a visual milestone timeline,
So that I am informed of when my funds will be credited to my account.

### Acceptance Criteria
- Given an active loan application, When user opens "My Loans", Then current stage is highlighted on a step tracker: Submitted -> Under Review -> Approved -> Disbursed.
- Given application is approved and loan contract signed, When disbursal executes, Then loan amount is credited to primary savings account and active loan account appears with repayment schedule.
- Given additional documentation is required, When flagged by underwriter, Then app highlights missing item with direct re-upload link.

### Dependencies
- Dependency on Story: Digital Personal Loan Application with Document Upload & e-KYC."""
    },

    # --- EPIC: Notifications and Alerts ---
    {
        "epic": "Notifications and Alerts",
        "summary": "Real-Time Push & SMS Notifications for Debit and Credit Events",
        "priority": "High",
        "points": 3,
        "sprint": 3,
        "labels": ["Notifications", "Push", "Sprint-3"],
        "description": """## User Story
As a mobile banking customer,
I want to receive immediate push and SMS alerts whenever a transaction occurs on my account,
So that I have instant visibility into all debits/credits and can flag potential fraud immediately.

### Acceptance Criteria
- Given any debit or credit event settles in Core Banking, When ledger changes, Then a push notification and SMS are dispatched within 2 seconds.
- Given the notification arrives, When viewed, Then it displays amount, merchant/beneficiary name, remaining account balance, and timestamp.
- Given a customer taps the push notification, When app opens, Then user is taken directly to the specific transaction detail screen.

### Dependencies
- Dependency on Story: Instant Intra-Bank and Inter-Bank Fund Transfers
- Push Notification Service (APNs / FCM) & Telephony Provider."""
    },
    {
        "epic": "Notifications and Alerts",
        "summary": "Configurable Low Balance & Overdraft Threshold Alerts",
        "priority": "High",
        "points": 3,
        "sprint": 3,
        "labels": ["Notifications", "Alerts", "Sprint-3"],
        "description": """## User Story
As a customer who wants to avoid accidental overdraft fees or bounced payments,
I want to set a custom minimum balance threshold and receive an urgent alert when balance falls below it,
So that I can transfer funds in time to maintain sufficient funds.

### Acceptance Criteria
- Given a customer navigates to Alerts Settings, When low-balance threshold is set (e.g. $200), Then setting is saved to customer notification profile.
- Given a debit transaction causes available balance to drop below $200, When transaction completes, Then high-priority alert is dispatched immediately: "Alert: Account balance below $200".
- Given balance is restored above threshold, When fresh debits occur later, Then alert re-arms correctly.

### Dependencies
- Dependency on Story: Real-Time Account Balance Overview."""
    },
    {
        "epic": "Notifications and Alerts",
        "summary": "Customer Notification Preferences Management",
        "priority": "Low",
        "points": 2,
        "sprint": 3,
        "labels": ["Notifications", "Preferences", "Sprint-3"],
        "description": """## User Story
As a customer who wants control over my communication channels,
I want to customize my notification preferences across push, SMS, and email for marketing vs transactional categories,
So that I only receive relevant communications on my preferred channels without notification fatigue.

### Acceptance Criteria
- Given Notification Settings screen is opened, When viewed, Then toggle switches for Push, SMS, and Email are available across categories (Security, Transactions, Low Balance, Offers).
- Given mandatory regulatory security alerts (OTP, login notifications), When viewed, Then toggles are permanently locked ON with explanation tooltip.
- Given toggles for optional promotional notifications are turned OFF, When saved, Then customer is unsubscribed from marketing queue immediately.

### Dependencies
- Dependency on Story: Real-Time Push & SMS Notifications."""
    }
]

SUPPORTING_TASKS_DATA = [
    {
        "summary": "Cross-Module Integration Architecture & Core Banking API Contracts",
        "priority": "Highest",
        "labels": ["Architecture", "Integration", "Sprint-1"],
        "description": """## Task Objective
Establish the cross-module integration architecture, OpenAPI 3.0 contract specifications, and shared DTOs between Mobile Frontend, BFF (Backend-For-Frontend) layer, and legacy Core Banking Systems.

### Scope & Deliverables
- Define RESTful API schema specifications for Auth, Accounts, Payments, Loans, and Notifications.
- Establish centralized error code dictionary (e.g., ERR_AUTH_001, ERR_PAY_409) and HTTP status code standards.
- Implement mutual TLS (mTLS) and API Gateway rate limiting policies for all microservice endpoints.
- Document cross-service sequence diagrams for payment processing and loan lifecycle."""
    },
    {
        "summary": "Automated Unit and Integration Testing Suite Setup",
        "priority": "High",
        "labels": ["Testing", "Automation", "Sprint-1"],
        "description": """## Task Objective
Configure the automated unit testing and integration testing frameworks across mobile and backend repositories to ensure minimum 80% code coverage before feature deployment.

### Scope & Deliverables
- Set up Jest / React Native Testing Library for mobile UI unit tests.
- Set up PyTest / JUnit test suites with mock Core Banking payment gateways.
- Implement automated test runners in GitHub Actions workflow executing on pull request creation.
- Configure code coverage reporting (Codecov/SonarQube) with PR blocking gates for coverage regressions."""
    },
    {
        "summary": "End-to-End Regression Testing Suite & User Acceptance Testing (UAT) Plan",
        "priority": "High",
        "labels": ["Testing", "Regression", "UAT", "Sprint-3"],
        "description": """## Task Objective
Design and execute comprehensive automated end-to-end regression suites and author the formal UAT test plan covering all critical customer banking journeys.

### Scope & Deliverables
- Implement automated Appium / Maestro E2E test flows for Login -> Transfer -> Statement -> Logout.
- Build test datasets covering edge cases: negative balances, expired OTPs, network timeouts, and concurrency.
- Author UAT sign-off matrix for Agile Jury demonstration.
- Document regression test results and pass/fail audit report."""
    },
    {
        "summary": "Agile Governance Framework: Definition of Ready (DoR) and Definition of Done (DoD)",
        "priority": "High",
        "labels": ["Governance", "Agile", "Process"],
        "description": """## Task Objective
Formalize and publish the Agile project governance criteria, establishing clear standards for when a story is ready for sprint ingestion and when it meets the bar for production release.

### Definition of Ready (DoR)
- User Story follows standard format (As a / I want / So that).
- Acceptance criteria written in unambiguous Given/When/Then format.
- Epic link and module label assigned.
- Story points estimated using Fibonacci scale (consensus reached).
- UX wireframes/mockups attached and approved.
- Upstream service dependencies identified.

### Definition of Done (DoD)
- Code implemented and passes linting/static analysis.
- Unit tests written and passing (minimum 80% branch coverage).
- Integration testing passed against staging environment.
- Peer code review completed with at least 1 approval.
- Security scan (SAST/DAST) passed with zero Critical/High vulnerabilities.
- Acceptance criteria verified and signed off by Product Owner."""
    },
    {
        "summary": "Defect Tracking Workflow, Risk Management Matrix & Severity Protocol",
        "priority": "Medium",
        "labels": ["QA", "RiskManagement", "Governance"],
        "description": """## Task Objective
Define the defect triage lifecycle, risk mitigation matrix, and escalation SLAs for production defects and jury assessment scenarios.

### Scope & Deliverables
- Establish Bug lifecycle statuses and resolution guidelines.
- Author Severity Classification matrix (P1 Blocker: <2 hr SLA, P2 Major: <8 hr SLA, P3 Normal, P4 Minor).
- Create Risk Register identifying technical risks (e.g. 3rd-party SMS gateway failure, inter-bank clearing delays) and mitigation fallbacks.
- Provide sample bug templates with pre-configured reproduction steps and environment headers."""
    },
    {
        "summary": "GitHub GitFlow Branching Strategy, PR Templates & CI/CD Automated Pipeline",
        "priority": "High",
        "labels": ["DevOps", "CI-CD", "GitHub"],
        "description": """## Task Objective
Document the team branching model, branch protection rules, pull request templates, and continuous delivery pipeline for mobile and backend artifacts.

### Scope & Deliverables
- Define GitFlow strategy (`main`, `develop`, `feature/*`, `release/*`, `hotfix/*`).
- Enforce GitHub branch protection: require linear history, passing CI checks, and mandatory peer approvals.
- Author `.github/pull_request_template.md` containing Jira issue link, testing checklist, and screenshot section.
- Configure CI/CD automated build pipeline generating testable Android APK and iOS IPA build artifacts."""
    },
    {
        "summary": "Jury Assessment Demonstration Board Preparation & Demo Script Walkthrough",
        "priority": "Highest",
        "labels": ["Assessment", "Demonstration", "Jury"],
        "description": """## Task Objective
Prepare the Jira board, sprint backlogs, and step-by-step presentation script for the Agile Jury Assessment 2 demonstration.

### Scope & Deliverables
- Verify all Epics, User Stories, Story Points, Priorities, and Sprints are organized cleanly on Jira.
- Verify backlog priority ordering reflects realistic banking priorities (Security -> Transactions -> Loans).
- Draft a 10-minute Jury demonstration script highlighting Agile methodology, user story quality, sprint planning, and risk management.
- Prepare live walkthrough showing board filters, sprint backlogs, and traceability."""
    }
]

SAMPLE_BUGS_DATA = [
    {
        "summary": "[SAMPLE BUG] Intermittent Timeout During Inter-Bank IMPS Transfer Confirmation Step",
        "priority": "High",
        "labels": ["SampleBug", "Payments", "IMPS"],
        "description": """## [SAMPLE SCENARIO - FOR DEMONSTRATION PURPOSES ONLY]
This is a sample bug scenario created to demonstrate defect triage, risk tracking, and QA reporting. This does not represent an active production defect.

### Bug Description
During peak load simulation, external IMPS clearing gateway occasionally returns HTTP 504 Gateway Timeout while deducting sender account, leaving transaction status ambiguous in the UI.

### Steps to Reproduce
1. Initiate an inter-bank IMPS transfer of $1,200.
2. Simulate a 10-second latency spike on national clearing gateway.
3. Submit transaction MPIN.

### Expected Behavior
App should trigger auto-reversal or display pending state with tracking reference within 5 seconds.

### Actual Behavior
App hangs on spinner until client timeout, and balance displays old value until manual refresh.

### Proposed Fix
Implement exponential backoff polling and automated idempotency resolution on timeout."""
    },
    {
        "summary": "[SAMPLE BUG] Biometric Fingerprint Prompt Fails to Re-trigger After App Minimization",
        "priority": "Medium",
        "labels": ["SampleBug", "Security", "Biometrics"],
        "description": """## [SAMPLE SCENARIO - FOR DEMONSTRATION PURPOSES ONLY]
This is a sample bug scenario created to demonstrate defect triage, risk tracking, and QA reporting. This does not represent an active production defect.

### Bug Description
When user minimizes the mobile app during the biometric authentication prompt and returns after 30 seconds, the biometric dialog disappears and screen becomes unresponsive to touch.

### Steps to Reproduce
1. Launch app to login screen.
2. Tap "Login with Fingerprint".
3. Minimize app to background while system biometric dialog is active.
4. Re-open app from recent apps tray after 30 seconds.

### Expected Behavior
Biometric dialog should re-prompt or gracefully fall back to alphanumeric password entry.

### Actual Behavior
Screen remains frozen with dimmed background overlay; user is forced to kill and restart app."""
    },
    {
        "summary": "[SAMPLE BUG] Account Statement PDF Export Shows Blank Rows for Zero-Fee Transactions",
        "priority": "Low",
        "labels": ["SampleBug", "AccountManagement", "Statements"],
        "description": """## [SAMPLE SCENARIO - FOR DEMONSTRATION PURPOSES ONLY]
This is a sample bug scenario created to demonstrate defect triage, risk tracking, and QA reporting. This does not represent an active production defect.

### Bug Description
Generated monthly statement PDF renders blank rows in the "Transaction Fee" column when fee amount is $0.00 instead of explicitly printing "$0.00" or "FREE".

### Steps to Reproduce
1. Open Account Statements.
2. Select past calendar month containing internal zero-fee transfers.
3. Export PDF.

### Expected Behavior
Fee column should explicitly state "$0.00" or "-" to maintain tabular integrity.

### Actual Behavior
Fee cell is completely empty, causing optical misalignment on some PDF readers."""
    }
]

def main():
    print(f"=== INITIALIZING JIRA SETUP FOR PROJECT {PROJECT_KEY} ===")
    myself = jira_helper.get_myself()
    account_id = myself.get("accountId")
    print(f"Authenticated as: {myself.get('displayName')} ({account_id})")

    # Step 1: Create the 5 Epics
    print("\n--- STEP 1: CREATING 5 EPICS ---")
    epic_keys = {}
    for epic in EPICS_DATA:
        summary = epic["name"]
        print(f"Creating Epic: {summary}...")
        body = {
            "fields": {
                "project": {"key": PROJECT_KEY},
                "summary": summary,
                "issuetype": {"id": ISSUE_TYPES["Epic"]},
                "priority": {"name": "High"},
                "labels": ["Epic", summary.replace(" ", "")],
                "description": text_to_adf(epic["description"]),
                "assignee": {"accountId": account_id}
            }
        }
        res = jira_helper.request("/rest/api/3/issue", method="POST", body=body)
        epic_keys[summary] = res["key"]
        print(f"-> Created Epic [{res['key']}] {summary}")
        time.sleep(0.5)

    print("\nCreated Epics:", epic_keys)

    # Step 2: Create 21 User Stories and link to Epics
    print("\n--- STEP 2: CREATING USER STORIES ---")
    created_stories = []
    sprint_assignments = {1: [], 2: [], 3: []}

    for story in STORIES_DATA:
        epic_name = story["epic"]
        parent_key = epic_keys.get(epic_name)
        summary = story["summary"]
        points = story["points"]
        priority = story["priority"]
        sprint_num = story["sprint"]
        labels = story["labels"]

        print(f"Creating Story: {summary} (Epic: {epic_name}, Points: {points}, Priority: {priority})...")
        body = {
            "fields": {
                "project": {"key": PROJECT_KEY},
                "summary": story["summary"],
                "issuetype": {"id": ISSUE_TYPES["Story"]},
                "parent": {"key": parent_key},
                "priority": {"name": priority},
                "labels": labels,
                STORY_POINT_FIELD: points,
                "description": text_to_adf(story["description"]),
                "assignee": {"accountId": account_id}
            }
        }
        res = jira_helper.request("/rest/api/3/issue", method="POST", body=body)
        story_key = res["key"]
        created_stories.append({"key": story_key, "summary": summary, "points": points, "sprint": sprint_num, "epic": epic_name})
        sprint_assignments[sprint_num].append(story_key)
        print(f"-> Created Story [{story_key}] (Points: {points})")
        time.sleep(0.5)

    # Step 3: Assign Stories to Sprints
    print("\n--- STEP 3: ASSIGNING STORIES TO SPRINTS ---")
    for s_num, issues in sprint_assignments.items():
        sprint_id = SPRINTS[s_num]["id"]
        sprint_name = SPRINTS[s_num]["name"]
        print(f"Assigning {len(issues)} issues to Sprint {s_num} ({sprint_name}, ID: {sprint_id})...")
        jira_helper.request(f"/rest/agile/1.0/sprint/{sprint_id}/issue", method="POST", body={"issues": issues})
        print(f"-> Successfully assigned {len(issues)} issues to {sprint_name}!")
        time.sleep(0.5)

    # Step 4: Create Supporting Tasks
    print("\n--- STEP 4: CREATING SUPPORTING TASKS ---")
    created_tasks = []
    for task in SUPPORTING_TASKS_DATA:
        summary = task["summary"]
        priority = task["priority"]
        labels = task["labels"]
        print(f"Creating Task: {summary}...")
        body = {
            "fields": {
                "project": {"key": PROJECT_KEY},
                "summary": summary,
                "issuetype": {"id": ISSUE_TYPES["Task"]},
                "priority": {"name": priority},
                "labels": labels,
                "description": text_to_adf(task["description"]),
                "assignee": {"accountId": account_id}
            }
        }
        res = jira_helper.request("/rest/api/3/issue", method="POST", body=body)
        created_tasks.append({"key": res["key"], "summary": summary, "priority": priority})
        print(f"-> Created Task [{res['key']}]")
        time.sleep(0.5)

    # Step 5: Create Sample Bug Issues
    print("\n--- STEP 5: CREATING SAMPLE BUG ISSUES ---")
    created_bugs = []
    for bug in SAMPLE_BUGS_DATA:
        summary = bug["summary"]
        priority = bug["priority"]
        labels = bug["labels"]
        print(f"Creating Bug: {summary}...")
        body = {
            "fields": {
                "project": {"key": PROJECT_KEY},
                "summary": summary,
                "issuetype": {"id": ISSUE_TYPES["Bug"]},
                "priority": {"name": priority},
                "labels": labels,
                "description": text_to_adf(bug["description"]),
                "assignee": {"accountId": account_id}
            }
        }
        res = jira_helper.request("/rest/api/3/issue", method="POST", body=body)
        created_bugs.append({"key": res["key"], "summary": summary, "priority": priority})
        print(f"-> Created Bug [{res['key']}]")
        time.sleep(0.5)

    # Summary
    print("\n=== EXECUTION COMPLETE ===")
    print(f"Epics created: {len(epic_keys)}")
    print(f"Stories created: {len(created_stories)}")
    print(f"Supporting Tasks created: {len(created_tasks)}")
    print(f"Sample Bugs created: {len(created_bugs)}")
    total_sp = sum(s["points"] for s in created_stories)
    print(f"Total Story Points: {total_sp}")

if __name__ == "__main__":
    main()
