# Incident response

NIST SP 800-61 Rev. 3 was Final when checked on 2026-07-15 and integrates incident
response with CSF 2.0 risk management. Apply the project response plan and legal,
privacy, contractual, and organizational requirements; do not invent authority.

1. Stabilize people and critical service. Establish incident lead, severity, affected
   assets, known facts, uncertainty, timeline, and safe communication channel.
2. Contain only with explicit authority. Prefer reversible isolation; consider
   attacker observation, evidence loss, business impact, and credential rotation.
3. Preserve evidence with timestamps, provenance, access records, hashes where useful,
   and redaction. Do not paste secrets or sensitive personal data into project memory.
4. Communicate facts, impact, uncertainty, actions, owner, and next update time. Do
   not speculate, conceal material risk, or claim eradication prematurely.
5. Eradicate the mechanism and address root cause and contributing conditions. Verify
   fixes in a safe environment and track broader exposure.
6. Recover from a known-good state, validate data and security boundaries, restore
   progressively, and monitor for recurrence through a defined window.
7. Record lessons and owned follow-up work without blame. Separate confirmed facts,
   evidence-supported inference, and unknowns.

If evidence suggests an active compromise, stop ordinary feature work and follow the
authorized incident path. A coding agent assists analysis and repair; it does not
grant itself production, forensic, legal, or disclosure authority.
