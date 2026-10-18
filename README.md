# Agent action-boundary evaluation

A small, reproducible experiment about an important failure mode in tool-using AI agents: taking an action that the user did not authorize.

**Research question:** How can we measure whether an agent stays within delegated authority, especially after approval is revoked?

## What exists today

This repo contains a **deterministic toy harness**, not a deployed AI agent or a validated AI-safety system. It compares three stylized decision rules on 15 synthetic tool-action scenarios:

- `unguarded`: all proposed actions go through;
- `approve_everything`: an idealized reviewer applies the same perfect authorization rule used to define the test labels;
- `risk_tiered`: routine delegated actions can proceed, while consequential actions need explicit approval and revocation takes precedence.

Actions are simulated. There are **no external emails, payments, account changes, real API requests, real users, or employer data**.

## Reproduce the experiment

Python 3.10+; no third-party dependencies.

```bash
python -m unittest -v
python agent_boundary_eval.py > synthetic_evidence.json
```

Five unit tests pass in the current environment. The generated JSON contains a canonical SHA-256 digest for each trace so repeated runs can be compared.

| Synthetic result | Unguarded | Idealized review-every-action | Risk-tiered |
| --- | ---: | ---: | ---: |
| Scenarios evaluated | 15 | 15 | 15 |
| Unauthorized actions executed | 7 | 0 | 0 |
| Review checks (simulated) | 0 | 15 | 9 |

**Do not interpret the zeros as evidence of real-world safety.** The authorization labels and the two protective rule sets are constructed from the same assumptions. The outcome is intentionally predictable; the experiment currently demonstrates instrumentation and reproducibility, not safety efficacy or actual reductions in human workload.

## Research next steps

1. Replace fixed actions with tool-call proposals from actual language-model agents in a mock-only environment.
2. Construct held-out task variations, ambiguous authority boundaries and adversarial revocation cases.
3. Separate independent ground-truth labeling from the protective policy under test.
4. Measure executed unauthorized actions, false blocks, trace completeness, escalation burden and time to stop consequential actions.
5. Report failure cases and limitations, not only aggregate metrics.

## Scope and provenance

This is an AI-assisted prototype assembled for independent research scoping. It does not reuse banking systems, customer data, employer code, or internal architecture. It is **not** a demonstration that any existing personal or employer-related model is legally free of third-party rights.

No open-source license is granted by this repository at this stage. Please contact the owner before reuse beyond rights provided by the hosting platform.
