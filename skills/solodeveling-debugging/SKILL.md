---
name: solodeveling-debugging
description: Diagnose a bug, failing test, regression, or unexpected software behavior from reproducible evidence before implementing a repair. Use whenever observed behavior differs from requirements or expectations, including intermittent failures, integration errors, build failures, and failed verification. Do not use for clearly understood planned implementation.
---

# Debugging

Do not guess at fixes. Preserve current evidence and find the root cause before
implementation changes.

## Diagnose

1. Capture the expected behavior, observed behavior, exact error, environment, scope,
   and impact. Label second-hand reports and inference.
2. Reproduce consistently with the smallest safe procedure. If reproduction is not
   possible, gather logs or state and record the verification limitation.
3. Review recent relevant changes and trace data across component boundaries. Find
   where the first incorrect value, state, assumption, or control flow originates.
4. Compare a working path with the failing path. List material differences and the
   dependencies or conditions each path assumes.
5. State one falsifiable root cause hypothesis and the evidence supporting it. Test
   the smallest variable that can disprove it. Do not stack speculative changes.
6. If repeated attempts reveal different coupling failures, stop and reconsider the
   architecture rather than applying another patch blindly.

## Repair

Create a focused failing regression before implementation when execution is
available, and ensure it demonstrates the defect. If it is unavailable, document the
manual reproduction and limitation. Implement one change that addresses the
confirmed root cause, not only the visible symptom.

Re-run the regression, relevant neighboring tests, and the original reproduction.
Record what was ruled out, scope, remaining limitations, and recent evidence. Return
the work item to execution for remaining planned work or to `verifying` when the
repair is complete. A passing regression alone does not prove unrelated acceptance
criteria.