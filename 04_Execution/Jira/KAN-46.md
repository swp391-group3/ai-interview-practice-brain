---
project: SEP490
type: execution
status: done
authority: jira
last_verified: 2026-09-18
---

# KAN-46: JD Interview Blueprint Contract

**Jira:** `DONE`. The contract preserves separation among JD, reviewed JD, configuration, blueprint, session, and snapshot; it treats blueprints as reusable assessment plans rather than static question lists.

**Implementation distinction:** merged PR #15 creates the standalone `interview_blueprints` table and JD foreign key restriction. It does not demonstrate session re-parenting or all target ERD/business rules. See [[JD-Blueprint]].
