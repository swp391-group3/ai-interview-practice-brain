---
title: Job Posting and Application Domain
tags:
  - domain
  - job-posting
  - job-application
  - recruiter
  - lightweight-ats
aliases:
  - Job Posting Domain
  - Application Domain
---

# Job Posting & Application Domain

The **Job Posting & Application Domain** provides a lightweight recruitment board enabling Recruiters to advertise employer openings and Candidates to discover and apply to those opportunities.

---

## 1. Purpose

Bridge the gap between technical interview preparation and actual career discovery. Gives Recruiters a direct channel to publish job vacancies and screen incoming candidate applications, while giving Candidates a targeted channel to apply for technical roles.

---

## 2. Core Concepts

* **Job Posting (`job_postings`):** A formal job vacancy created by a Recruiter from JD-like content and representing an employer opening.
  * **Canonical Equivalence:** `Job Posting` **is** the company's Job Description. There is no separate "Corporate JD" entity in RoleCue.
  * The Recruiter may review and confirm AI-extracted structured information before submission.
  * **Interview Configuration:** Company 3D interviewer model and Voice Profile selected by the Recruiter before Admin approval. A Candidate cannot override either setting for an interview originating from the Job Posting.
  * Attributes: Title, Seniority, Description, Required Technologies, Location, Employment Type, company 3D interviewer model, Voice Profile, Status (`PENDING_APPROVAL`, `APPROVED`, `REJECTED`, `ARCHIVED`).
* **Application (`applications`):** A completed candidate submission to an approved Job Posting.
  * Attributes: Candidate ID, Posting ID, Candidate Application Information, uploaded CV/resume, Interview Result reference, Submission Timestamp, Status.
  * An Interview Result is stored from the required Job Posting interview and attached before the completed Application is made available to the Recruiter.
  * **Status Lifecycle:** Strictly binary:
    $$\text{PENDING} \longrightarrow \text{APPROVED} \quad \text{or} \quad \text{REJECTED}$$

---

## 3. Actors Involved

* **Recruiter:**
  * Creates Job Postings from JD-like content; may review and confirm AI-extracted structured information.
  * Selects a company 3D interviewer model and Voice Profile before submitting a Job Posting for Admin approval.
  * Edits and archives own Job Postings.
  * Views own Job Postings.
  * Searches and filters own Job Postings.
  * Searches and filters received Applications for own postings.
  * Views Application details and attached candidate profiles.
  * Renders a definitive decision: **Approve** or **Reject**.
* **Candidate:**
  * Browses and searches approved public Job Postings.
  * Views Job Posting details.
  * Selects Apply, uploads a CV/resume, and completes the required technical interview using the locked company 3D interviewer model and Voice Profile.
  * Submits a completed Application containing the associated Interview Result.
  * Views own submitted Applications and tracks status updates.
* **Administrator:**
  * Views and filters Job Postings across the platform.
  * Approves or rejects Job Postings for platform governance.

---

## 4. Main Domain Flow

```mermaid
sequenceDiagram
    autonumber
    actor Recruiter
    actor Candidate
    actor Admin
    participant System as Job Posting & App Service
    participant DB as Relational Storage
    participant Mail as Email Provider

    Note over Recruiter,System: 1. Job Posting Lifecycle
    Recruiter->>System: Create Job Posting from JD-like content
    System->>System: Optionally extract structured information for Recruiter review
    Recruiter->>System: Confirm content; select company 3D model and Voice Profile
    Recruiter->>System: Submit Job Posting for approval
    System->>DB: Store Job Posting (Status: PENDING_APPROVAL)
    Admin->>System: Approve or Reject Job Posting
    alt Admin approves
        System->>DB: Set Job Posting Status to APPROVED
    else Admin rejects
        System->>DB: Set Job Posting Status to REJECTED
    end

    opt Job Posting is APPROVED
        Note over Candidate,System: 2. Discovery & Application
        Candidate->>System: Search Approved Job Postings (keyword, tech stack)
        System-->>Candidate: List Matching Job Postings
        Candidate->>System: View Job Posting Details
        Candidate->>System: Select Apply and upload CV/resume
        Candidate->>System: Complete required technical interview
        Note over Candidate,System: Company 3D model and Voice Profile cannot be overridden
        System->>DB: Store Interview Result for Job Posting
        System->>DB: Create completed Application with CV/resume and Interview Result (Status: PENDING)
        System-->>Recruiter: Make completed Application available
        System->>Mail: Notify Recruiter of completed Application
        System-->>Candidate: Confirm Application Submitted

        Note over Recruiter,System: 3. Screening & Binary Adjudication
        Recruiter->>System: Search & Filter Applications (Posting ID, Status)
        Recruiter->>System: View Candidate Application Detail
        alt Recruiter Approves
            Recruiter->>System: Approve Application
            System->>DB: Update Application Status to APPROVED
            System->>Mail: Send Approval Notification to Candidate
        else Recruiter Rejects
            Recruiter->>System: Reject Application
            System->>DB: Update Application Status to REJECTED
            System->>Mail: Send Status Update to Candidate
        end
    end
```

---

## 5. Business Rules & Invariants

1. **Non-ATS Boundary (Scope Termination):**
   * Recruitment scope strictly terminates at **Application Approve / Reject**.
   * RoleCue does **NOT** model or support:
     * Multi-stage recruitment pipelines (e.g., Phone Screen $\rightarrow$ Tech Interview $\rightarrow$ Culture Fit).
     * Interview panel scheduling or calendar synchronization.
     * Candidate ranking algorithms or automated resume scoring.
     * Offer letter generation, compensation negotiation, or digital signature.
     * Employee onboarding or background checks.
2. **Canonical Job Posting Rule:**
   * A `Job Posting` is the company's job description.
   * Do not create or introduce a separate "Corporate JD" entity or database table.
3. **Approval and Interview Configuration:**
   * A Recruiter must select the company 3D interviewer model and Voice Profile before submitting a Job Posting for Admin approval.
   * Admin approves or rejects submitted Job Postings. Only `APPROVED` Job Postings are publicly available and eligible for application.
   * A Job Posting interview always uses its company-defined 3D interviewer model and Voice Profile. The Candidate cannot override them.
4. **Completed Application Prerequisite:**
   * After selecting Apply, the Candidate uploads a CV/resume and completes the required technical interview.
   * The system stores the Interview Result and attaches it to the Application with Candidate application information and the CV/resume before making the completed Application available to the Recruiter.
5. **No Multi-Tenant Company Architecture:**
   * RoleCue does **NOT** implement multi-tenant SaaS architecture.
   * There are no Company tenants, no company workspaces, no company membership hierarchies, no tenant isolation middleware, no Row-Level Security (RLS) tenant policies, and no schema-per-tenant isolation.
   * Job Postings are owned and managed directly by the authoring `recruiter_id`.
6. **No Recruiter Subscriptions or Corporate Billing:**
   * Recruiter features do not include subscription plans, corporate invoicing, VAT invoices, or payment tiers.
   * Basic recruiter identity metadata exists as ordinary profile data.
7. **Access Control & Privacy:**
   * Candidates can **only** browse approved public Job Postings and view their own submitted applications.
   * Recruiters can **only** view and modify Job Postings they personally created.
   * Recruiters can **only** view applications submitted specifically to their own Job Postings.
8. **Application Status Immutability:**
   * Once an application moves to `APPROVED` or `REJECTED`, the decision is final and cannot be reverted back to `PENDING`.
9. **Archived Posting Behavior:**
   * When a Recruiter archives a Job Posting, it is removed from candidate search and discovery. Candidates with existing applications can still view their application status.

---

## 6. Relationships to Other Domains

* **[[01_Domains/Auth/README|Auth Domain]]:**
  Authenticates Candidates and Recruiters. Enforces role boundaries on job board operations.
* **[[01_Domains/Job-Description/README|Job-Description Domain]]:**
  A Candidate browsing a Job Posting may copy its requirements to create a private **Target JD for Practice** in their personal library. However, the Job Posting and Target JD remain completely decoupled entities.
* **[[01_Domains/Administration/README|Administration Domain]]:**
  Administrators view, filter, and approve or reject Job Postings to ensure platform content quality.
* **[[01_Domains/Interview/README|Interview Domain]]:**
  Runs the required technical interview using the Job Posting's locked company 3D interviewer model and Voice Profile, then stores the Interview Result attached to the completed Application.

---

## 7. External Integrations

* **Email Provider:** Dispatches email notifications to Recruiters when new applications arrive, and notifies Candidates when an application status updates to Approved or Rejected.
