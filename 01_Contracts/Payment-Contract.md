---
project: SEP490
type: contract
status: draft
authority: lecturer
last_verified: 2026-09-11
---

# Payment & Subscription Contract

## 1. Status & Metadata
- **Status:** `DRAFT` (Required by Capstone Register; provider and monetization rules under team review)
- **Domain:** Subscription Tiers, Interview Credits, Third-Party Payment Gateways

## 2. Requirements & Scope
- Support candidate purchase of mock interview credits or subscription plans.
- Integration with third-party payment gateway (e.g., PayOS, VNPay, MoMo, or Stripe).
- Maintain immutable transaction history in PostgreSQL.

## 3. Invariants
- Transaction state transitions must be idempotent (`PENDING` -> `SUCCESS` | `FAILED`).
- Credit balance updates must execute within database transactions to avoid race conditions.
- Payment webhooks must verify cryptographic signatures before granting credits.

## 4. Open Questions
- Gateway provider selection (PayOS vs. VNPay vs. Stripe).
- Free tier credit allocation on initial candidate registration.

## 5. Traceability
- **Reference:** [[08_Reports/Lecturer/9_GFA26SE84_AI_Virtual_Technical_Interview_Capstone_Register.pdf]]
- **Open Questions:** [[Open-Questions]] OQ-08
