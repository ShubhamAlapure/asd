# Mobile Banking Application (MBAJ2) — Agile Jury Assessment 2

Enterprise Agile Software Development setup, Jira task breakdown, and technical governance for **Mobile Banking Application (MBAJ2)**.

---

## 📌 Project Overview
* **Project Name:** Mobile Banking Application – Agile Jury 2
* **Project Key:** `MBAJ2`
* **Methodology:** Agile Scrum Framework
* **Sprint Cadence:** 2-Week Sprints
* **Total Story Points:** 85 SP across 21 User Stories

---

## 🏛️ The 5 Architecture Epics

1. **`MBAJ2-4` — Security and Authentication**
   * Multi-factor authentication (MFA/OTP), device biometrics (Fingerprint/Face ID), session inactivity timeout, and secure account recovery.
2. **`MBAJ2-5` — Account Management**
   * Multi-account balance aggregation (Savings, Checking, Credit), paginated transaction ledger, and PDF statement generation.
3. **`MBAJ2-6` — Payments and Fund Transfers**
   * Beneficiary management, instant intra/inter-bank transfers (IMPS/NEFT), idempotency duplicate prevention, and digital receipts.
4. **`MBAJ2-7` — Loan Services**
   * Digital loan catalog, interactive EMI calculator, pre-approved loan eligibility engine, and digital application with KYC document upload.
5. **`MBAJ2-8` — Notifications and Alerts**
   * Real-time push/SMS debit/credit alerts, configurable low-balance threshold warnings, and customer notification preferences center.

---

## 🚀 Sprints Structure

| Sprint | Status | Story Points | Focus / Goal |
| :--- | :---: | :---: | :--- |
| **Sprint 1: Secure Foundation** | **Active** | **32 SP** | *Authentication and basic account functionality.* |
| **Sprint 2: Core Transactions** | Future | **26 SP** | *Core Banking Transactions: beneficiaries, transfers, validation, and transaction status.* |
| **Sprint 3: Loans & Integration** | Future | **27 SP** | *Loans, Notifications and Integration: loan workflows, alerts, and regression testing.* |

---

## 📋 Scrum Board Workflow

The active sprint workflow is tracked across 4 columns:
$$\text{To Do} \longrightarrow \text{In Progress} \longrightarrow \text{In Review} \longrightarrow \text{Done}$$

* **Done:** Password/Biometric Login (`MBAJ2-9`), Account Balance Overview (`MBAJ2-13`)
* **In Review:** Two-Factor OTP (`MBAJ2-10`), Secure Password Reset (`MBAJ2-12`)
* **In Progress:** Session Inactivity Timeout (`MBAJ2-11`), Paginated Transaction History (`MBAJ2-14`)
* **To Do:** Statement PDF Generation (`MBAJ2-15`), Profile & KYC Management (`MBAJ2-16`)

---

## 🛠️ Agile Governance & Supporting Tasks

* **`MBAJ2-30`:** Cross-Module Integration Architecture & Core Banking API Contracts
* **`MBAJ2-31`:** Automated Unit and Integration Testing Suite Setup (Jest, PyTest, 80% coverage)
* **`MBAJ2-32`:** End-to-End Regression Testing Suite & UAT Plan (Appium/Maestro)
* **`MBAJ2-33`:** Agile Governance Framework: Definition of Ready (DoR) and Definition of Done (DoD)
* **`MBAJ2-34`:** Defect Tracking Workflow, Risk Management Matrix & Severity Protocol (P1-P4)
* **`MBAJ2-35`:** GitHub GitFlow Branching Strategy, PR Templates & CI/CD Pipeline
* **`MBAJ2-36`:** Jury Assessment Demonstration Board Preparation & Demo Script Walkthrough

---

## 📄 Documentation

* Master Assessment Guide: [`Agile_Jury_Assessment_2_Master_Guide.pdf`](./Agile_Jury_Assessment_2_Master_Guide.pdf)
