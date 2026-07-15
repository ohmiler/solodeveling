# Security policy

Solodeveling is alpha software. No version has been published as a supported stable
release. Security fixes currently target the latest reviewed commit; older commits and
unmerged branches do not receive guaranteed backports.

## Report a vulnerability

Do not open a public issue for a suspected vulnerability or include credentials,
private source code, exploit details, or personal data in repository discussions.
Use GitHub's private vulnerability reporting for
`ohmiler/solodeveling` when available. If that channel is unavailable, open a minimal
public issue asking the maintainer to enable a private contact path without disclosing
the vulnerability.

Include the affected commit or artifact hash, runtime and operating system, impact,
minimal reproduction, and any safe recovery action. Do not test against systems or
data you do not own or have explicit authority to assess.

## Scope and expectations

Relevant reports include unsafe adapter overwrite or deletion, path or symlink escape,
secret retention, permission escalation, release artifact tampering, prompt/data trust
boundary failures, and dependency vulnerabilities with a demonstrated impact.

A hash match proves integrity against known bytes, not publisher identity or safety.
The project does not promise a response or remediation SLA while it remains an
individual alpha project, but reports should receive an acknowledgement and a bounded
triage decision before public disclosure whenever practical.
