---
solodeveling_schema: 1
id: WORK-027
title: README Positioning and Honest Comparison
status: done
level: standard
type: change
goal: Make the public README explain Solodeveling's value, speed model, intended users, and documented differences from adjacent agent-development frameworks without unsupported superiority claims.
scope: Root README publication status, one-command quick start, product positioning, comparison table, best-fit guidance, measured project evidence, source links, alpha limitations, linked installation publication status, and documentation verification.
out_of_scope: Skill behavior changes, new benchmark executions, competitor implementation review beyond public documentation, version changes, package publication, release assets, and claims of cross-framework speed or quality superiority without controlled evidence.
acceptance:
- README no longer says npm or PyPI are unpublished and links to the live installation channels.
- The opening explains single-agent-first, risk-scaled workflow behavior in plain language before implementation details.
- A readable table compares Solodeveling with Superpowers, GSD, GitHub Spec Kit, and BMAD Method using documented defaults and neutral wording.
- README states who should and should not choose Solodeveling.
- Speed claims distinguish reduced workflow overhead and measured repository evidence from unrun cross-framework benchmarks.
- Existing security, installation, runtime, alpha, and Tier 1 limitations remain accurate.
- Documentation regressions, protocol validation, skill validation, full tests, and diff checks pass.
risks:
- Marketing language could overstate behavioral evidence or misrepresent actively changing third-party projects.
- A wide comparison table could be difficult to read on narrow screens.
- Root README changes intentionally select the full CI gate.
decisions:
- Position Solodeveling as disciplined when risk is high and quiet when work is small.
- Compare fit and defaults, not declare a universal winner.
- Use only official project documentation links for adjacent frameworks.
- Publish measured local evidence with dates and limitations; defer controlled comparative benchmarking.
verification:
- Run focused README/documentation tests and stale-publication searches.
- Run protocol and canonical skill-suite validation.
- Run the complete Python regression suite because root README uses the full gate.
- Inspect rendered Markdown structure and links textually, then verify protected-main CI.
next_action: Preserve the evidence-backed positioning and require a controlled benchmark before adding comparative speed or quality claims.
evidence:
- EVIDENCE-027
---

# Planned structure

1. Lead with the one-agent, right-sized-process promise and live one-command install.
2. Explain how Quick, Standard, and Critical work avoid both under-control and ceremony.
3. Compare documented defaults in a compact table plus best-fit guidance.
4. Show measured repository evidence separately from future comparative benchmarks.
5. Retain operational, security, runtime, and alpha limitations.
