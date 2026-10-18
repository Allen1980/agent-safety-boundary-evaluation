# Pilot study: Unsafe promotion into AI operational memory

**Status:** Independent synthetic prototype; not a completed large-language-model evaluation. No grant has been submitted or awarded.

## The safety problem

Tool-using agents can produce apparently useful execution traces, regression-test outcomes, defect summaries, and suggestions. If a system promotes these artifacts into trusted operational memory before competent human review, a later knowledge assistant may repeat an inaccurate result, an unapproved procedure, or guidance that is no longer valid. This creates an amplification pathway: a single incorrect agent action becomes future institutional knowledge.

This pilot tests one narrow intervention: **fail closed when attempting to promote or retrieve operational memory without matching evidence, an explicit scoped human-review record, current version and active authority.**

## Larger product context (roadmap, not implemented by this repository)

1. Automated testing and repeatable evidence generation, with a colleague making the final verification decision.
2. Reviewed test outcomes and human corrections become system-scoped operational memory; a conversational assistant may later use that memory with cited sources.
3. A system-specific knowledge package combines approved SOPs, workflow rules, known exceptions and operational history to support grounded explain/guide/draft actions.

The proposal funded here would investigate the **safety boundary between the first and second steps**, before a later assistant treats promoted memory as authoritative. A commercial end-to-end testing/knowledge product is outside this grant's requested scope.

## What has actually been implemented

- `agent_boundary_eval.py`: 15 toy synthetic action scenarios tested under three idealized policies. These are deterministic demonstrations of logging, not measured agent behavior.
- `human_verified_memory.py`: a tiny in-memory simulator that rejects unsupported promotions and suppresses lookup after approval revocation, expiration, source-version changes, cross-tenant mismatches, or entry tampering.
- `test_*.py`: 20 no-dependency local/CI unit tests of toy policy logic.
- No ChatGPT or live-agent API connection, UI automation, real coworker identity verification, third-party test management integration, persistent database, or model-generated knowledge answer has been implemented.

## Research hypotheses (proposals, not findings)

- **H1:** Models will sometimes recommend memory updates based on plausible but unaudited tool output, even when the user expects human validation.
- **H2:** Scoping approvals to a particular test-run and system version will reduce the acceptance of stale, cross-context and unauthorized updates compared with unguarded promotion.
- **H3:** Strict checks will also reject some legitimate records and increase review costs; these costs must be measured independently.

## Proposed next evaluation if resources are approved

1. Build a disjoint synthetic corpus of test-case histories, mock defects, SOP revisions, and reviewer corrections; ensure assessment labels are authored independently of the promotion policy.
2. Run a small, pre-specified collection of model-driven agent proposals with **mock tools only**, varying the review status, version, source authenticity, tenant and revocation state.
3. Compare **unguarded ingestion**, simple manual approval, and a scoped human-review policy on held-out scenarios.
4. Count unauthorized promotions, false rejections, stale facts appearing in retrieval, citation correctness, cost per evaluated case and reviewer workload (simulated until actual human reviewers participate).
5. Release reproducible synthetic fixtures, failure analyses, baseline results and limitations **only after rights and publication checks**.

### Failure conditions

This research will not claim improved safety if it merely filters hand-coded bad examples; if the evidence label and enforcing policy are defined by the same rule; if a reviewer is only represented by an unverifiable string; or if results cannot be replicated on held-out cases. SHA-256 traces demonstrate determinism and accidental-change checks; they do not confer trustworthy identity, signing, or immutable audit storage.

## Funding use (provisional, not quoted)

The proposed **US$1,000** Rapid Grant request is a *ceiling for project-specific research expenses*, not compensation, investment, guaranteed cash, or a claim that funds are already available:

| Intended cost | Preliminary ceiling | What it unlocks |
| --- | ---: | --- |
| Metered LLM API inference | US$600 | Multiple model baselines and adversarial memory-update proposals |
| Isolated mock-tool compute | US$250 | Repeatable held-out evaluations and trace processing |
| Project-specific traces/storage | US$150 | Reproducibility and evidence review |
| **Total** | **US$1,000** | Only approved research costs |

Vendor unit rates and model token usage have **not** been verified. The application amount and breakdown should be revised if actual quotes or workload estimates are materially lower. No funds will be spent in anticipation of reimbursement without written authorization; the funder may pay upfront or reimburse later.

## Deliverables conditional on approval

- D1: Public/synthetic protocol and independent labeling scheme.
- D2: Isolated model-driven agent proposals against mock tools.
- D3: Comparable evidence and failure report, including adverse cases.
- D4: Reproducibility instructions and a safe publication artifact.

## Applicant and legal boundaries

This independent work is intended to use only synthetic and public examples. It does not claim that existing employer-related code, experience or architecture can be publicly licensed. The applicant must confirm any applicable employment/IP, eligibility, tax, AI-use and publication terms; the public repository currently has no explicit open-source license.

**Funding source:** [BlueDot Impact Rapid Grants](https://bluedot.org/programs/rapid-grants). Eligibility and terms are set by the funder, not this repository.
