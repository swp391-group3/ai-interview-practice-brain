---
title: Conceptual Domain Model
tags:
  - system
  - domain-model
  - entities
  - relationships
aliases:
  - Domain Model
  - Conceptual Model
---

# Conceptual Domain Model

This document maps the primary business entities of the RoleCue platform and illustrates their conceptual relationships and boundaries.

---

## 1. Conceptual Entity-Relationship Model

```mermaid
classDiagram
    class UserAccount {
        +UUID id
        +String email
        +String password_hash
        +Role role
        +Status status
    }

    class CandidateProfile {
        +UUID id
        +String full_name
        +String headline
        +String resume_url
    }

    class RecruiterProfile {
        +UUID id
        +String company_name
    }

    class TargetJD {
        +UUID id
        +String title
        +SeniorityLevel seniority_level
        +String raw_text
        +JSONB parsed_data
        +String refinement_notes
        +JDStatus status
    }

    class InterviewBlueprint {
        <<Internal Hidden>>
        +UUID id
        +Difficulty difficulty
        +Integer duration_minutes
        +Integer question_count
        +JSONB blueprint_data
        +String contract_version
    }

    class InterviewSession {
        +UUID id
        +InterviewStatus status
        +Integer current_turn_index
        +JSONB blueprint_snapshot
        +String recording_url
        +Timestamp started_at
        +Timestamp ended_at
    }

    class SessionTurn {
        +UUID id
        +Integer turn_index
        +String question_text
        +String candidate_transcript
        +Float candidate_latency_sec
        +JSONB turn_evaluation
    }

    class PerformanceReport {
        +UUID id
        +Float overall_score
        +JSONB competency_scores
        +JSONB turn_critiques
        +JSONB learning_roadmap
    }

    class JobPosting {
        +UUID id
        +String title
        +SeniorityLevel seniority_level
        +String description
        +Array~String~ required_technologies
        +PostingStatus status
    }

    class Application {
        +UUID id
        +String resume_url
        +String cover_note
        +ApplicationStatus status
        +Timestamp submitted_at
    }

    class VoiceProfile {
        +UUID id
        +String provider_voice_id
        +String display_name
        +String language_code
        +String accent
        +String gender
        +Boolean is_active
    }

    class PersonalAvatar {
        +UUID id
        +String model_glb_url
        +String thumbnail_url
        +AvatarStatus status
    }

    class MembershipSubscription {
        +UUID id
        +MembershipStatus status
        +Timestamp started_at
        +Timestamp expires_at
    }

    class PaymentTransaction {
        +UUID id
        +String order_ref
        +Decimal amount
        +String currency
        +PaymentStatus status
        +Timestamp created_at
    }

    %% Relationships
    UserAccount "1" -- "0..1" CandidateProfile : profile
    UserAccount "1" -- "0..1" RecruiterProfile : profile
    UserAccount "1" -- "0..1" MembershipSubscription : owns
    UserAccount "1" -- "0..*" PaymentTransaction : initiates

    CandidateProfile "1" -- "0..*" TargetJD : owns
    CandidateProfile "1" -- "0..*" PersonalAvatar : owns
    CandidateProfile "1" -- "0..*" Application : submits

    TargetJD "1" -- "0..*" InterviewBlueprint : generates
    InterviewBlueprint "1" -- "0..*" InterviewSession : instantiates
    InterviewSession "1" -- "0..*" SessionTurn : records
    InterviewSession "1" -- "0..1" PerformanceReport : produces

    RecruiterProfile "1" -- "0..*" JobPosting : authors
    JobPosting "1" -- "0..*" Application : receives

    VoiceProfile "1" -- "0..*" InterviewSession : voices
```

---

## 2. Entity Descriptions & Invariants

### 2.1. Identity & Profiles
* **`UserAccount`:** Root authentication record. Holds system role (`Candidate`, `Recruiter`, `Admin`) and status (`ACTIVE`, `LOCKED`).
* **`CandidateProfile`:** Profile metadata specific to candidates, containing personal background and default resume links.
* **`RecruiterProfile`:** Employer identity metadata attached to a Recruiter account. Stores basic company identification. *Note:* Recruiter manages Job Postings directly. There is no multi-tenant company hierarchy, tenant workspace, or tenant isolation middleware.

### 2.2. Practice & Simulation Pipeline
* **`TargetJD`:** The candidate's personal practice JD. Stores the original raw text, the AI-extracted requirements, and the candidate's natural-language `refinement_notes`.
* **`InterviewBlueprint`:** The internal assessment plan. Contains topic coverage, question slots, depth milestones, and grading rubrics.
  * **Invariant:** Generated from `TargetJD` + `refinement_notes` + candidate configuration. Hidden from the candidate.
* **`InterviewSession`:** Concrete practice execution. Stores an immutable `blueprint_snapshot` on creation to freeze evaluation criteria permanently.
* **`SessionTurn`:** Granular dialogue unit within a session. Captures interviewer questions, candidate transcripts, audio timing, and real-time probing notes.
* **`PerformanceReport`:** Final evaluation artifact produced from completed sessions. Contains 0–100 overall score, 5-competency breakdown, and learning roadmap.

### 2.3. Recruitment Board
* **`JobPosting`:** The company's Job Description authored by a Recruiter. Serves as the public advertisement for an open position.
  * **Invariant:** Canonical concept representing the company's JD. No separate "Corporate JD" entity exists.
* **`Application`:** The candidate's application to a `JobPosting`.
  * **Invariant:** Status transitions strictly from `PENDING` $\rightarrow$ `APPROVED` or `REJECTED`. Bounded strictly at binary decision.

### 2.4. Audio-Visual Presentation
* **`VoiceProfile`:** Voice configuration sourced from external TTS providers. Curated and managed by Administrators.
* **`PersonalAvatar`:** 3D humanoid avatar generated from candidate portrait photo (feasibility demonstrated via Avaturn spike). Stored in the Candidate's profile library.

### 2.5. Membership & Payments
* **`MembershipSubscription`:** Tracks candidate membership status and entitlement period.
* **`PaymentTransaction`:** Immutable ledger of payment orders, amounts, and gateway outcomes.
