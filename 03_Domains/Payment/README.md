---
project: SEP490
type: domain
status: open
authority: lecturer
last_verified: 2026-09-11
---

# Billing & Payment Domain

## 1. Purpose & Requirements
- Support candidate purchase of mock interview credits or subscription plans.
- Provide payment processing compliant with university capstone requirements (supporting Vietnamese gateways e.g. VNPay, MoMo, PayOS, or Stripe).
- Maintain immutable transaction logs and automated webhook reconciliation.

## 2. Invariants
- No interview session can consume more credits than the account balance.
- All balance adjustments must be executed inside ACID database transactions.
