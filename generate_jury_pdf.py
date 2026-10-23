#!/usr/bin/env python3
"""
Generates a comprehensive, professional PDF guide for the Agile Jury Assessment 2.
Target: /Users/shubhamalapure/Desktop/jira/Agile_Jury_Assessment_2_Master_Guide.pdf
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "Mobile Banking Application (MBAJ2) — Agile Jury Assessment 2 Master Guide")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 747, 558, 747)
            
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "CONFIDENTIAL & PROPRIETARY — PREPARED FOR AGILE JURY ASSESSMENT")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 46, 558, 46)
        self.restoreState()

def build_pdf():
    pdf_path = "/Users/shubhamalapure/Desktop/jira/Agile_Jury_Assessment_2_Master_Guide.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    PRIMARY = colors.HexColor("#1E3A8A")   # Deep Navy
    SECONDARY = colors.HexColor("#0D9488") # Teal Accent
    DARK_TEXT = colors.HexColor("#0F172A") # Slate 900
    MUTED_TEXT = colors.HexColor("#475569")# Slate 600
    BG_LIGHT = colors.HexColor("#F8FAFC")  # Light Slate
    BORDER_COL = colors.HexColor("#E2E8F0")

    # Typography styles
    styles.add(ParagraphStyle(
        name="DocTitle",
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name="DocSubtitle",
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceAfter=15
    ))
    styles.add(ParagraphStyle(
        name="SecHeader",
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name="SubSecHeader",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name="BodyCustom",
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name="BulletCustom",
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT,
        leftIndent=15,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        name="TableHead",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    ))
    styles.add(ParagraphStyle(
        name="TableCell",
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=DARK_TEXT
    ))
    styles.add(ParagraphStyle(
        name="TableCellBold",
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        textColor=DARK_TEXT
    ))
    styles.add(ParagraphStyle(
        name="CalloutText",
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=13,
        textColor=PRIMARY
    ))
    styles.add(ParagraphStyle(
        name="QAQuestion",
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=PRIMARY,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name="QAAnswer",
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT,
        leftIndent=10,
        spaceAfter=6
    ))

    story = []

    # Title Banner
    story.append(Paragraph("Agile Software Development Assessment 2", styles["DocSubtitle"]))
    story.append(Paragraph("Mobile Banking Application (MBAJ2)", styles["DocTitle"]))
    story.append(Paragraph("Comprehensive Jira Setup, Architecture & Jury Defense Master Guide", styles["DocSubtitle"]))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceAfter=15))

    # Meta Info Table
    meta_data = [
        [
            Paragraph("<b>Candidate / Lead:</b> Shubham Alapure", styles["TableCell"]),
            Paragraph("<b>Project Key:</b> MBAJ2 (ID: 10034)", styles["TableCell"])
        ],
        [
            Paragraph("<b>Jira Site:</b> shubhamalapure.atlassian.net", styles["TableCell"]),
            Paragraph("<b>Board ID:</b> 35 (Scrum Board)", styles["TableCell"])
        ],
        [
            Paragraph("<b>Methodology:</b> Agile Scrum Framework", styles["TableCell"]),
            Paragraph("<b>Total Issues:</b> 36 Issues | 85 Story Points", styles["TableCell"])
        ]
    ]
    meta_table = Table(meta_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COL),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COL),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary & Assessment Overview", styles["SecHeader"]))
    story.append(Paragraph(
        "This project represents the complete enterprise Agile setup for a mission-critical <b>Mobile Banking Application</b>. "
        "The objective was to translate complex financial business requirements into a structured, traceable, and production-grade Jira Scrum project. "
        "The workspace contains <b>5 foundational Epics</b>, <b>21 prioritized User Stories</b> with behavior-driven acceptance criteria, "
        "<b>7 supporting engineering/governance tasks</b>, and <b>3 representative QA defect scenarios</b> organized across <b>three two-week Sprints</b>.",
        styles["BodyCustom"]
    ))

    # 2. Key Agile Concepts (Plain English)
    story.append(Paragraph("2. Core Agile & Scrum Concepts Explained Simply", styles["SecHeader"]))
    story.append(Paragraph(
        "If the jury asks foundational questions about why Jira and Scrum were used, here are the core principles:",
        styles["BodyCustom"]
    ))

    concepts = [
        ("Agile vs Waterfall", "Waterfall follows a rigid linear phase (months of planning before coding). In Mobile Banking, security guidelines, regulatory APIs, and user preferences evolve rapidly. Agile delivers functional, tested increments in 2-week iterations, reducing risk and allowing immediate course correction."),
        ("Scrum Framework", "A lightweight agile framework where a cross-functional team works in fixed timeboxes called <b>Sprints</b>. Each sprint has a clear goal, a committed set of backlog items, and ends with a potentially shippable product increment."),
        ("Epic", "A large body of work that cannot be completed in a single sprint. It groups related features under a unified business objective (e.g., <i>Payments and Fund Transfers</i>)."),
        ("User Story", "The smallest unit of product value told from the end-user's perspective: <i>'As a [role], I want [capability], so that [benefit]'</i>."),
        ("Acceptance Criteria (Given/When/Then)", "Unambiguous conditions of satisfaction. We used Behavior-Driven Development (BDD) / Gherkin format: <b>Given</b> a precondition, <b>When</b> an action is executed, <b>Then</b> a verifiable outcome must happen."),
        ("Story Points & Fibonacci Scale", "We estimate using the modified Fibonacci sequence (<b>1, 2, 3, 5, 8, 13</b>). Story points measure <b>relative complexity, uncertainty, and effort</b>—not raw hours. Why? Hourly estimates are notoriously inaccurate; humans are significantly better at estimating relative size (e.g., Story B is twice as complex as Story A)."),
        ("Scrum Board vs Backlog", "In Jira Scrum, the <b>Backlog</b> contains the master prioritized list of all future sprints and unassigned tasks. The <b>Active Board</b> only displays cards for the currently running sprint across workflow columns.")
    ]

    for title, desc in concepts:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", styles["BulletCustom"]))

    story.append(Spacer(1, 10))

    # 3. The 5 Epics
    story.append(Paragraph("3. The Five Architecture Epics", styles["SecHeader"]))
    epic_table_data = [
        [Paragraph("Epic Key", styles["TableHead"]), Paragraph("Epic Title", styles["TableHead"]), Paragraph("Domain / Scope", styles["TableHead"]), Paragraph("Target Sprint", styles["TableHead"])],
        [Paragraph("<b>MBAJ2-4</b>", styles["TableCellBold"]), Paragraph("Security & Authentication", styles["TableCell"]), Paragraph("IAM, biometric login (Face/Fingerprint), 2FA/MFA, auto-timeout, account recovery", styles["TableCell"]), Paragraph("Sprint 1", styles["TableCell"])],
        [Paragraph("<b>MBAJ2-5</b>", styles["TableCellBold"]), Paragraph("Account Management", styles["TableCell"]), Paragraph("Real-time balances across accounts, paginated transaction history, PDF statements, KYC", styles["TableCell"]), Paragraph("Sprint 1", styles["TableCell"])],
        [Paragraph("<b>MBAJ2-6</b>", styles["TableCellBold"]), Paragraph("Payments & Fund Transfers", styles["TableCell"]), Paragraph("Intra/inter-bank (IMPS/NEFT), beneficiaries, idempotency duplicate prevention, receipts", styles["TableCell"]), Paragraph("Sprint 2", styles["TableCell"])],
        [Paragraph("<b>MBAJ2-7</b>", styles["TableCellBold"]), Paragraph("Loan Services", styles["TableCell"]), Paragraph("Loan catalog, interactive EMI calculator, real-time eligibility engine, digital application", styles["TableCell"]), Paragraph("Sprint 3", styles["TableCell"])],
        [Paragraph("<b>MBAJ2-8</b>", styles["TableCellBold"]), Paragraph("Notifications & Alerts", styles["TableCell"]), Paragraph("Real-time push/SMS debit/credit alerts, low balance warnings, customer preferences center", styles["TableCell"]), Paragraph("Sprint 3", styles["TableCell"])],
    ]
    t_epics = Table(epic_table_data, colWidths=[65, 140, 230, 69])
    t_epics.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COL),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COL),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_epics)
    story.append(Spacer(1, 14))

    # Page Break for Sprints and Stories
    story.append(PageBreak())

    # 4. Sprint Breakdown & Active Board Status
    story.append(Paragraph("4. Sprint Planning, Velocity & Active Board Workflow", styles["SecHeader"]))
    story.append(Paragraph(
        "The project is structured into <b>three two-week Sprints</b> representing an iterative release cadence. "
        "Total backlog estimation is <b>85 Story Points</b>, averaging <b>28 SP per sprint</b>, which aligns with standard high-performing 5-7 person agile engineering squads.",
        styles["BodyCustom"]
    ))

    sprint_table_data = [
        [Paragraph("Sprint Name", styles["TableHead"]), Paragraph("Status", styles["TableHead"]), Paragraph("Story Points", styles["TableHead"]), Paragraph("Sprint Goal & Architectural Focus", styles["TableHead"])],
        [
            Paragraph("<b>Sprint 1: Secure Foundation</b><br/>(ID: 35)", styles["TableCell"]),
            Paragraph("<b>ACTIVE</b><br/>(2 Weeks)", styles["TableCellBold"]),
            Paragraph("<b>32 SP</b><br/>(8 Stories)", styles["TableCell"]),
            Paragraph("<b>Goal:</b> Authentication and basic account functionality.<br/>Focus: IAM, biometrics, 2FA, session security, balance overview, transaction history.", styles["TableCell"])
        ],
        [
            Paragraph("<b>Sprint 2: Core Transactions</b><br/>(ID: 36)", styles["TableCell"]),
            Paragraph("Future", styles["TableCell"]),
            Paragraph("<b>26 SP</b><br/>(6 Stories)", styles["TableCell"]),
            Paragraph("<b>Goal:</b> Core Banking Transactions: beneficiaries, transfers, validation, and transaction status.<br/>Focus: Payee management, IMPS/NEFT, idempotency, failure auto-reversal, limits.", styles["TableCell"])
        ],
        [
            Paragraph("<b>Sprint 3: Loans & Integration</b><br/>(ID: 37)", styles["TableCell"]),
            Paragraph("Future", styles["TableCell"]),
            Paragraph("<b>27 SP</b><br/>(7 Stories)", styles["TableCell"]),
            Paragraph("<b>Goal:</b> Loans, Notifications and Integration: loan workflows, alerts, and regression testing.<br/>Focus: EMI calculator, eligibility, KYC upload, real-time alerts, preferences.", styles["TableCell"])
        ],
    ]
    t_sprints = Table(sprint_table_data, colWidths=[130, 60, 65, 249])
    t_sprints.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COL),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COL),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_sprints)
    story.append(Spacer(1, 10))

    # Active Board Distribution Explanation
    story.append(Paragraph("Why the Board is Organized This Way Right Now", styles["SubSecHeader"]))
    story.append(Paragraph(
        "To demonstrate an active in-flight sprint during the jury review, <b>Sprint 1</b> is actively running with tickets distributed across all 4 stages of the Definition of Done pipeline:",
        styles["BodyCustom"]
    ))

    board_status_data = [
        [Paragraph("Column", styles["TableHead"]), Paragraph("Issues", styles["TableHead"]), Paragraph("Story Points", styles["TableHead"]), Paragraph("Explanation for the Jury", styles["TableHead"])],
        [Paragraph("<b>Done</b>", styles["TableCellBold"]), Paragraph("MBAJ2-9, MBAJ2-13", styles["TableCell"]), Paragraph("10 SP", styles["TableCell"]), Paragraph("Foundational features: Core Password/Biometric Login and Account Balance Dashboard have been built, reviewed, unit-tested, and verified against acceptance criteria.", styles["TableCell"])],
        [Paragraph("<b>In Review</b>", styles["TableCellBold"]), Paragraph("MBAJ2-10, MBAJ2-12", styles["TableCell"]), Paragraph("8 SP", styles["TableCell"]), Paragraph("Two-Factor Authentication (OTP) and Password Reset are completed by engineering and are currently undergoing peer code review & QA security validation.", styles["TableCell"])],
        [Paragraph("<b>In Progress</b>", styles["TableCellBold"]), Paragraph("MBAJ2-11, MBAJ2-14", styles["TableCell"]), Paragraph("8 SP", styles["TableCell"]), Paragraph("Developers are actively implementing Inactivity Session Timeout and Paginated Transaction History with category filters.", styles["TableCell"])],
        [Paragraph("<b>To Do</b>", styles["TableCellBold"]), Paragraph("MBAJ2-15, MBAJ2-16", styles["TableCell"]), Paragraph("6 SP", styles["TableCell"]), Paragraph("Statement PDF generation and Profile Management are scheduled next in the sprint queue and ready for dev pickup.", styles["TableCell"])],
    ]
    t_board = Table(board_status_data, colWidths=[80, 110, 65, 249])
    t_board.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COL),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COL),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_board)
    story.append(Spacer(1, 14))

    # Page Break for Detailed Stories Catalog
    story.append(PageBreak())

    # 5. Complete Catalog of 21 User Stories
    story.append(Paragraph("5. Detailed Catalog of 21 User Stories", styles["SecHeader"]))
    story.append(Paragraph(
        "Each story was created with a full description containing user story narrative, testable Given/When/Then acceptance criteria, and explicit technical dependencies:",
        styles["BodyCustom"]
    ))

    stories_summary = [
        ("MBAJ2-9", "Customer Auth with Password & Biometrics", "Security", "Highest", 5, 1, "Given valid credentials, When logged in, Then JWT issued and dashboard loaded <1.5s."),
        ("MBAJ2-10", "Two-Factor Authentication (OTP/SMS/Email)", "Security", "Highest", 5, 1, "Given new device login, When 2FA triggers, Then 6-digit OTP delivered <5s with 120s expiry."),
        ("MBAJ2-11", "Session Inactivity Timeout & Auto-Logout", "Security", "High", 3, 1, "Given 4 min inactivity, When modal countdown expires at 5 min, Then session revoked."),
        ("MBAJ2-12", "Secure Password Reset & Recovery Workflow", "Security", "High", 3, 1, "Given forgot password, When OTP & card PIN verified, Then user sets compliant password."),
        ("MBAJ2-13", "Real-Time Account Balance Overview", "Accounts", "Highest", 5, 1, "Given home screen, When loaded, Then savings, checking, and credit balances displayed masked."),
        ("MBAJ2-14", "Paginated & Categorized Transaction History", "Accounts", "High", 5, 1, "Given account selected, When scrolled, Then chronological entries load asynchronously."),
        ("MBAJ2-15", "Account Statement Generation (PDF/CSV)", "Accounts", "Medium", 3, 1, "Given custom date range, When requested, Then password-protected official PDF generated."),
        ("MBAJ2-16", "Customer Profile & KYC Management", "Accounts", "Medium", 3, 1, "Given settings, When contact details updated, Then OTP verification required before save."),
        ("MBAJ2-17", "Beneficiary Management (Add/Edit/Delete)", "Payments", "High", 5, 2, "Given new payee, When added with IFSC, Then 30-min cooling limit ($500) enforced."),
        ("MBAJ2-18", "Intra/Inter-Bank Fund Transfers (IMPS/NEFT)", "Payments", "Highest", 8, 2, "Given payee selected, When MPIN confirmed, Then funds settle via gateway <3s with URN."),
        ("MBAJ2-19", "Idempotency & Duplicate Prevention", "Payments", "Highest", 3, 2, "Given rapid multiple taps, When UUID key matches, Then duplicate debit is strictly blocked."),
        ("MBAJ2-20", "Failed Transaction Handling & Auto-Reversal", "Payments", "High", 5, 2, "Given downstream gateway timeout, When reported, Then ledger balance auto-credited <5s."),
        ("MBAJ2-21", "Digital Transaction Receipts & Sharing", "Payments", "Medium", 2, 2, "Given transfer complete, When tapped, Then shareable receipt exported as PDF/image."),
        ("MBAJ2-22", "Daily & Per-Transaction Transfer Limits", "Payments", "High", 3, 2, "Given transfer exceeds daily quota, When submitted, Then blocked with quota warning."),
        ("MBAJ2-23", "Loan Products Catalog & EMI Calculator", "Loans", "Medium", 3, 3, "Given amount & tenure sliders, When adjusted, Then monthly EMI and interest recalculate."),
        ("MBAJ2-24", "Pre-Approved Loan Eligibility Engine", "Loans", "High", 5, 3, "Given 6 months banking history, When checked, Then real-time credit APR offer returned."),
        ("MBAJ2-25", "Digital Loan Application & KYC Upload", "Loans", "High", 8, 3, "Given eligible customer, When salary slip/ID uploaded, Then OCR verifies and queues app."),
        ("MBAJ2-26", "Loan Lifecycle Tracking & Disbursal History", "Loans", "Medium", 3, 3, "Given submitted loan, When viewed, Then step tracker shows review, approval, and disbursal."),
        ("MBAJ2-27", "Push & SMS Debit/Credit Notifications", "Notifications", "High", 3, 3, "Given any ledger change, When settled, Then SMS and push alert dispatched <2s."),
        ("MBAJ2-28", "Configurable Low Balance & Overdraft Alerts", "Notifications", "High", 3, 3, "Given balance dips below custom limit ($200), When debit completes, Then urgent alert sent."),
        ("MBAJ2-29", "Notification Preferences Management", "Notifications", "Low", 2, 3, "Given alert settings, When toggled, Then marketing muted while security alerts stay locked.")
    ]

    stories_table_data = [
        [Paragraph("Key", styles["TableHead"]), Paragraph("Summary", styles["TableHead"]), Paragraph("Module", styles["TableHead"]), Paragraph("Pri", styles["TableHead"]), Paragraph("SP", styles["TableHead"]), Paragraph("Sprint", styles["TableHead"]), Paragraph("Core Acceptance Criteria", styles["TableHead"])]
    ]
    for k, s, m, p, sp, spr, ac in stories_summary:
        stories_table_data.append([
            Paragraph(f"<b>{k}</b>", styles["TableCellBold"]),
            Paragraph(s, styles["TableCell"]),
            Paragraph(m, styles["TableCell"]),
            Paragraph(p, styles["TableCell"]),
            Paragraph(str(sp), styles["TableCellBold"]),
            Paragraph(f"S{spr}", styles["TableCell"]),
            Paragraph(ac, styles["TableCell"])
        ])

    t_stories = Table(stories_table_data, colWidths=[45, 120, 50, 40, 20, 30, 199])
    t_stories.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COL),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COL),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_stories)
    story.append(Spacer(1, 14))

    # Page Break for Governance and Tasks
    story.append(PageBreak())

    # 6. Agile Governance & Supporting Tasks
    story.append(Paragraph("6. Agile Governance & Supporting Engineering Tasks", styles["SecHeader"]))
    story.append(Paragraph(
        "Seven formal Jira Tasks were authored to provide structural governance, DevOps standards, quality gates, and demonstration readiness:",
        styles["BodyCustom"]
    ))

    tasks_data = [
        ("MBAJ2-30", "Cross-Module Integration Architecture & Core Banking API Contracts", "Highest", "Defines RESTful OpenAPI 3.0 contracts, mutual TLS (mTLS), standardized error codes (e.g. ERR_PAY_409), and DTO schemas across mobile, BFF, and Core Banking."),
        ("MBAJ2-31", "Automated Unit and Integration Testing Suite Setup", "High", "Establishes Jest/React Native testing framework for mobile UI and PyTest/JUnit with mock payment gateways. Enforces 80% code coverage threshold in CI."),
        ("MBAJ2-32", "End-to-End Regression Testing Suite & UAT Plan", "High", "Appium/Maestro automated test scripts covering the full customer journey (Login -> Transfer -> Statement -> Logout) and formal UAT sign-off matrix for jury review."),
        ("MBAJ2-33", "Agile Governance: Definition of Ready (DoR) & Definition of Done (DoD)", "High", "Publishes formal entry and exit criteria. DoR ensures stories have BDD criteria, points, wireframes; DoD ensures code review, 80% unit test coverage, and PO sign-off."),
        ("MBAJ2-34", "Defect Tracking Workflow, Risk Management Matrix & SLAs", "Medium", "Defines bug lifecycle statuses, severity classifications (P1 Blocker <2hr SLA to P4 Minor), and risk mitigation register (e.g. 3rd-party SMS gateway fallback)."),
        ("MBAJ2-35", "GitHub GitFlow Branching Strategy, PR Templates & CI/CD Pipeline", "High", "Enforces GitFlow (`main`, `develop`, `feature/*`, `release/*`, `hotfix/*`), mandatory pull request checklists, linear commit history, and automated Android APK/iOS IPA build triggers."),
        ("MBAJ2-36", "Jury Assessment Demonstration Board Preparation & Script", "Highest", "Verifies board traceability, sprint backlog cleanliness, story point consistency, and a step-by-step 10-minute presentation walkthrough for the examiners.")
    ]

    for k, s, p, d in tasks_data:
        story.append(Paragraph(f"• <b>[{k}] {s}</b> (Priority: <i>{p}</i>): {d}", styles["BulletCustom"]))

    story.append(Spacer(1, 10))

    # 7. Sample Bugs
    story.append(Paragraph("7. Sample Defect Scenarios (Labelled QA Scenarios)", styles["SecHeader"]))
    story.append(Paragraph(
        "Three representative defects were created with reproduction steps to demonstrate QA tracking and defect triage. "
        "Per assessment requirements, they are explicitly tagged as sample scenarios:",
        styles["BodyCustom"]
    ))

    bugs_data = [
        ("MBAJ2-37", "[SAMPLE BUG] Intermittent Timeout During Inter-Bank IMPS Transfer Confirmation", "High", "Payments", "Peak-load network latency causes gateway HTTP 504. Verifies auto-reversal and idempotency polling logic."),
        ("MBAJ2-38", "[SAMPLE BUG] Biometric Prompt Fails to Re-trigger After App Minimization", "Medium", "Security", "App minimization during biometric prompt freezes UI overlay. Demonstrates lifecycle event handling defect."),
        ("MBAJ2-39", "[SAMPLE BUG] Account Statement PDF Export Shows Blank Rows for Zero-Fee Transactions", "Low", "Statements", "Zero-fee transactions render as blank cells instead of '$0.00'. Demonstrates UI/formatting defect triage.")
    ]

    for k, s, p, m, d in bugs_data:
        story.append(Paragraph(f"• <b>[{k}] {s}</b> (Priority: <i>{p}</i> | Module: <i>{m}</i>): {d}", styles["BulletCustom"]))

    story.append(Spacer(1, 14))

    # Page Break for Jury Q&A
    story.append(PageBreak())

    # 8. Jury Q&A Cheat Sheet (Top 12 Questions & Answers)
    story.append(Paragraph("8. Jury Q&A Cheat Sheet (Top 12 Defense Questions)", styles["SecHeader"]))
    story.append(Paragraph(
        "These are the exact questions examiners and jury members frequently ask during Agile assessments, along with clear model answers:",
        styles["BodyCustom"]
    ))

    qa_list = [
        (
            "Q1: Why did you choose Scrum over Kanban for this project?",
            "Mobile banking requires strict regulatory compliance, milestone deadlines, and coordinated releases with external banking networks. Scrum's time-boxed Sprints provide predictability, clear Sprint Goals, and regular retrospectives. Kanban is better suited for continuous support/maintenance rather than initial multi-module feature delivery."
        ),
        (
            "Q2: Why are your Story Points in Fibonacci numbers (1, 2, 3, 5, 8, 13) instead of hours?",
            "Humans are notoriously poor at estimating absolute hours due to unforeseen technical blockers, but we excel at relative sizing. Fibonacci creates exponential scale differences, preventing bikeshedding between arbitrary numbers (e.g. arguing 6 vs 7 hours). If a story is 13 or larger, it signals excessive risk and must be sliced into smaller stories."
        ),
        (
            "Q3: What is the difference between an Epic, a Story, and a Task?",
            "An <b>Epic</b> represents a major functional theme (e.g., Payments and Fund Transfers) that takes multiple sprints to deliver. A <b>User Story</b> delivers end-to-end user value within a single sprint (e.g., Transfer to Beneficiary). A <b>Task</b> covers technical, architectural, or procedural work that does not have direct user narrative (e.g., CI/CD Pipeline Setup)."
        ),
        (
            "Q4: What is the difference between Definition of Ready (DoR) and Definition of Done (DoD)?",
            "<b>DoR</b> is the entry gate: A story cannot enter a sprint unless it has clear BDD acceptance criteria, story point consensus, wireframes, and identified dependencies. <b>DoD</b> is the exit gate: A story cannot be marked Done unless it has passed peer review, has 80% automated test coverage, passes security scans, and is verified by the Product Owner."
        ),
        (
            "Q5: How did you decide what went into Sprint 1 vs Sprint 2 vs Sprint 3?",
            "We followed risk-first architectural sequencing. <b>Sprint 1 (Secure Foundation)</b> delivers IAM, biometrics, and account visibility—without which no transactions can occur. <b>Sprint 2 (Core Transactions)</b> builds the core money transfer and duplicate-prevention engine. <b>Sprint 3 (Loans & Integration)</b> builds high-level credit products, alert preference centers, and executes end-to-end regression."
        ),
        (
            "Q6: Why are some tickets in 'Done' and 'In Review' on your board right now?",
            "To demonstrate an active in-flight sprint during the assessment! Sprint 1 is running, showing realistic progress: foundational login and balance overview are completed (Done), MFA and password recovery are undergoing code review (In Review), session timeout and transaction history are actively being coded (In Progress), and statements are queued (To Do)."
        ),
        (
            "Q7: What is an Idempotency Key and why is it essential in banking?",
            "In mobile banking, poor network connectivity can lead users to tap 'Pay' multiple times or retry dropped requests. An idempotency key is a unique client-generated UUID attached to the payment header. The backend checks if the key was already processed within 120 seconds; if so, it returns the existing receipt without deducting funds twice."
        ),
        (
            "Q8: How do you handle non-functional requirements like security and timeout?",
            "Non-functional requirements are treated as first-class citizens. Session timeout (MBAJ2-11) is an explicit User Story with a 3-point estimate and 5-minute threshold. Encryption, mTLS, and error dictionary standards are captured in architecture Task MBAJ2-30 and the Definition of Done."
        ),
        (
            "Q9: How do you manage dependencies between stories?",
            "Dependencies are documented directly in the issue descriptions. For example, <i>Fund Transfers (MBAJ2-18)</i> explicitly depends on <i>Beneficiary Management (MBAJ2-17)</i> and <i>Account Balance Overview (MBAJ2-13)</i>. This dictates sprint sequencing so prerequisite APIs are completed in earlier sprints."
        ),
        (
            "Q10: What is your branching and CI/CD strategy?",
            "We follow GitFlow: feature branches fork from `develop` and merge via Pull Requests that require passing CI checks and 1 peer approval. Automated GitHub Actions run unit tests and SonarQube static analysis. The `release` branch undergoes regression testing, and `main` represents production releases tagged with semantic versioning."
        ),
        (
            "Q11: Why are there Bugs in your backlog if development is just starting?",
            "They are explicitly labelled <i>[SAMPLE BUG]</i> scenarios created to demonstrate our QA defect triage workflow. They prove that our Jira board has a functioning bug lifecycle with reproduction steps, severity tagging (P1-P4), and root-cause analysis protocols."
        ),
        (
            "Q12: How do you calculate team velocity in future sprints?",
            "At the end of Sprint 1, team velocity is calculated as the sum of Story Points for all stories fully meeting the Definition of Done. If 20 out of 32 points are completed, our historical velocity is 20 SP. We use this moving average to forecast Sprint 2 and Sprint 3 commitments accurately."
        )
    ]

    for q, a in qa_list:
        story.append(Paragraph(q, styles["QAQuestion"]))
        story.append(Paragraph(f"<b>Answer:</b> {a}", styles["QAAnswer"]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF at: {pdf_path}")

if __name__ == "__main__":
    build_pdf()
