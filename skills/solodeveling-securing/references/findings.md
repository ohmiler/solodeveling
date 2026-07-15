# Security findings

Store durable findings under `.solodeveling/security/findings/FINDING-NNN.md` with
`solodeveling_schema: 1` and these fields:

```yaml
id: FINDING-001
title: Short observed issue
severity: high
confidence: high
source: manual-review
affected_asset: Trusted component or data flow
evidence:
  - Reproducible, non-secret observation
impact: Bounded consequence
recommendation: Smallest effective response
status: open
verification: []
```

Allowed status values are `open`, `in-progress`, `mitigated`, `accepted-risk`, and
`false-positive`. A mitigated or false-positive finding needs verification. An
automated-scanner finding marked `confirmed` needs a separate confirmation method.
Do not paste raw secret values, exploit payloads that create unnecessary risk, or
large scanner logs into durable artifacts.

Accepted risk additionally records:

```yaml
risk_acceptance:
  rationale: Why mitigation is not selected now
  owner: Authorized decision owner
  review_condition: Date, event, release, or exposure change that reopens review
```

Severity estimates impact; confidence estimates evidence strength. Keep them
separate. Re-test the affected behavior after mitigation and preserve remaining
scope and limitations. Never treat the absence of findings as proof of security.