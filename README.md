# Human-verified operational memory for AI workflows

**Product direction:** automated testing and colleague verification → evidence-backed operational memory → source-grounded knowledge assistant.

**What this repository is today:** a small, openly inspectable **synthetic AI safety evaluation**, not the full product. It explores a critical risk in that workflow: an agent or a test system treating **unreviewed, stale, revoked or cross-context results as trusted knowledge**.

[Research question, experimental design and provisional grant budget](docs/AI_SAFETY_RESEARCH_PILOT.md)

## The three-part product direction

1. **Automated testing + human verification** — produce repeatable test evidence and let responsible colleagues make the final judgment. Automation does not sign off its own results.
2. **Operational memory + conversational AI** — after authorized human review, preserve test outcomes, defect resolutions, corrections, and provenance so an assistant can retrieve grounded answers.
3. **Knowledge base / system digital SME** — maintain scoped and versioned SOPs, business rules, known exceptions, and approved operational history for explain, guide and document-drafting workflows.

These are **intended capabilities**, not evidence that integrations with ChatGPT, colleagues, test systems, or an enterprise knowledge base have been built here.

## The specific AI safety failure mode

A superficially successful agent may produce an incorrect conclusion. If its output becomes a trusted system memory without appropriate review, the mistake can persist and later be repeated by a knowledge assistant. The risk is **unsafe promotion of agent output to operational knowledge**.

The current prototype simulates defensive boundaries; the grant would fund more realistic, independently labeled model-driven experiments in fully isolated mock environments.

## Runnable evidence — no external dependencies

Requires Python 3.10+:

```bash
python -m unittest discover -v
python agent_boundary_eval.py > synthetic_evidence.json
python human_verified_memory.py
```

The current GitHub Actions run should verify **20 unit tests**, including 15 tests for human-reviewed memory promotion.

| Implemented | Evidence | Important limit |
| --- | --- | --- |
| Tool-action boundary toy harness | 15 synthetic action scenarios × 3 stylized regimes = 45 policy decisions | Not real LLM actions or real human approvals |
| Human-verified memory gate toy | Explicit scoped review, version checks, tenant checks, revocation, expiry, citation and evidence digest | Reviewer identities are only synthetic strings; no real authentication |
| Negative-path tests | 15 new unit tests for unsafe memory promotion and retrieval | Tests exercise programmed rules, not independent field measurements |
| CI | GitHub Actions runs the Python unit tests | Passing tests does not prove actual production safety |

For the earlier action-boundary fixtures, unguarded mode executes 7 labeled unauthorized actions while two idealized gated modes execute 0; those zeros arise from fixture assumptions and **must not be presented as empirically measured protection**. The new memory gate demonstrates a narrow, deterministic fail-closed decision, not a validated human-approval service.

## Research to be funded — not yet performed

A proposed [AI safety pilot](docs/AI_SAFETY_RESEARCH_PILOT.md) will test when LLM-generated tool outputs and test results should or should not become trusted memory. It will use held-out synthetic cases, independently labeled truth, controlled mock-tool calls and failure analysis. Relevant measures include unauthorized memory promotions, legitimate promotions blocked, retrieval of stale facts, citation quality, cost and review burden.

**Provisional project-cost request:** US$1,000 for usage-metered model evaluations, isolated test compute and evidence handling, subject to provider quotations and BlueDot approval. It is **restricted-purpose research funding**, not salary, investment or unrestricted personal cash; grant approval and payment are not implied.

## Source, privacy and licensing

- All demonstration data in this repository are synthetic; no employer systems, customer records, internal code or live endpoints are included.
- This prototype was prepared with AI assistance. No statement of human-only authorship or independent safety validation is made.
- This repository has **no open-source license at present**. Public access is not permission to reuse the code beyond applicable platform and legal rights.
- Legal/IP, grant and any external publishing permissions must be addressed separately; the code does not substitute for those determinations.

[BlueDot Impact Rapid Grants](https://bluedot.org/programs/rapid-grants) | [Research pilot](docs/AI_SAFETY_RESEARCH_PILOT.md)
