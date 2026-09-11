---
project: SEP490
type: domain
status: open
authority: team
last_verified: 2026-09-11
---

# JD Extraction Evaluation Dataset

> **Tracking:** [[KAN-45]]  
> **Committed Deadline:** 2026-09-12 23:59  
> **Status:** `QUEUED`

---

## 1. Objective
Establish a reusable, automated evaluation benchmark to measure the accuracy, recall, and consistency of the JD extraction LLM pipeline across various software engineering domains and formats.

---

## 2. Dataset Design & Coverage
The dataset should contain 15–20 curated real-world JD samples spanning diverse roles and seniority:
- **Roles:** Backend (Go, Java, Python), Frontend (React, Next.js), Mobile (Flutter, iOS), DevOps/Cloud, Fullstack.
- **Seniority:** Internship, Junior, Mid-Level, Senior, Staff/Lead.
- **Formats:** Plain text listings, multi-column PDF layouts, brief job descriptions, detailed enterprise specs.

---

## 3. Schema of Benchmark Test Fixtures
Each benchmark entry consists of:
```json
{
  "id": "jd-eval-001",
  "sourceType": "pdf",
  "sourcePath": "testdata/jds/golang-senior-backend.pdf",
  "groundTruth": {
    "expectedJobTitle": "Senior Backend Go Engineer",
    "expectedSeniority": "senior",
    "mustHaveSkills": ["Go", "PostgreSQL", "Docker", "Kubernetes", "gRPC"],
    "niceToHaveSkills": ["Kafka", "Redis"],
    "minimumYears": 4
  }
}
```

---

## 4. Evaluation Metrics
- **Skill Precision:** $rac{	ext{Correctly extracted skills}}{	ext{Total extracted skills}}$ (punishes hallucinations).
- **Skill Recall:** $rac{	ext{Correctly extracted skills}}{	ext{Ground-truth required skills}}$ (punishes missed technologies).
- **Format Compliance:** 100% valid JSON adhering to schema.
