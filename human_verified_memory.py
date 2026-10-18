"""Synthetic human-verified operational memory boundary.

Standalone proof of a proposed safety control. No LLM, ChatGPT connection,
database, organization identity system, real tester, or production integration.
Do not use this module as an authorization service.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json


def digest(payload: dict) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return sha256(canonical.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class TestObservation:
    tenant: str
    system: str
    case_id: str
    version: str
    run_id: str
    outcome: str
    source_ref: str


@dataclass(frozen=True)
class HumanReview:
    decision_id: str
    tenant: str
    system: str
    case_id: str
    version: str
    run_id: str
    reviewer_id: str
    approved: bool
    expires_at: int


@dataclass(frozen=True)
class MemoryEntry:
    observation: TestObservation
    decision_id: str
    reviewer_id: str
    approved_at: int
    evidence_sha256: str

    def evidence_payload(self) -> dict:
        return {
            "observation": asdict(self.observation),
            "decision_id": self.decision_id,
            "reviewer_id": self.reviewer_id,
            "approved_at": self.approved_at,
        }


class UntrustedEvidence(ValueError):
    """Fail closed rather than accepting an unverified memory update."""


class MemoryGate:
    """Mock memory promotion and source-grounded exact-match retrieval."""

    def __init__(self) -> None:
        self.current_versions: dict[tuple[str, str], str] = {}
        self.reviews: dict[str, HumanReview] = {}
        self.revoked: set[str] = set()
        self.entries: dict[tuple[str, str, str], MemoryEntry] = {}

    def set_version(self, tenant: str, system: str, version: str) -> None:
        self.current_versions[(tenant, system)] = version

    def add_review(self, review: HumanReview) -> None:
        if not review.decision_id or review.decision_id in self.reviews:
            raise UntrustedEvidence("missing or duplicate review ID")
        self.reviews[review.decision_id] = review

    def revoke(self, decision_id: str) -> None:
        # Revocation takes effect on subsequent reads; records remain in the ledger.
        if decision_id not in self.reviews:
            raise UntrustedEvidence("review not found")
        self.revoked.add(decision_id)

    def promote(self, observation: TestObservation, decision_id: str, now: int) -> MemoryEntry:
        review = self.reviews.get(decision_id)
        if review is None:
            raise UntrustedEvidence("no human review exists")
        if not review.approved or decision_id in self.revoked:
            raise UntrustedEvidence("review rejected or revoked")
        if now >= review.expires_at:
            raise UntrustedEvidence("review expired")
        if not review.reviewer_id or review.reviewer_id.strip().lower() in {"agent", "ai", "llm"}:
            raise UntrustedEvidence("no independent human reviewer")
        if not all([observation.tenant, observation.system, observation.case_id,
                    observation.version, observation.run_id, observation.source_ref]):
            raise UntrustedEvidence("missing provenance")
        if observation.outcome not in {"PASS", "FAIL"}:
            raise UntrustedEvidence("unknown test outcome")
        actual = (observation.tenant, observation.system, observation.case_id,
                  observation.version, observation.run_id)
        expected = (review.tenant, review.system, review.case_id, review.version,
                    review.run_id)
        if actual != expected:
            raise UntrustedEvidence("review scope does not match evidence")
        if self.current_versions.get((observation.tenant, observation.system)) != observation.version:
            raise UntrustedEvidence("out-of-date or unknown system version")
        payload = {"observation": asdict(observation), "decision_id": decision_id,
                   "reviewer_id": review.reviewer_id, "approved_at": now}
        entry = MemoryEntry(observation, decision_id, review.reviewer_id, now, digest(payload))
        key = (observation.tenant, observation.system, observation.case_id)
        # Deliberately reject competing values until a new human-approved workflow
        # replaces them; this prototype does not implement conflict resolution.
        if key in self.entries and self.entries[key] != entry:
            raise UntrustedEvidence("conflicting memory entry requires separate review")
        self.entries[key] = entry
        return entry

    def lookup(self, tenant: str, system: str, case_id: str, now: int) -> dict | None:
        key = (tenant, system, case_id)
        entry = self.entries.get(key)
        if entry is None:
            return None
        review = self.reviews.get(entry.decision_id)
        if (review is None or not review.approved or entry.decision_id in self.revoked
                or now >= review.expires_at
                or self.current_versions.get((tenant, system)) != entry.observation.version
                or digest(entry.evidence_payload()) != entry.evidence_sha256):
            return None
        # This returns a referenced fact for future retrieval; it is NOT a
        # language-model answer, RAG implementation, or source correctness proof.
        return {"case_id": case_id, "outcome": entry.observation.outcome,
                "system_version": entry.observation.version,
                "citation": entry.observation.source_ref,
                "review_id": entry.decision_id,
                "sha256": entry.evidence_sha256}


def synthetic_demo() -> dict:
    gate = MemoryGate()
    gate.set_version("synthetic-tenant", "demo-app", "v1")
    case = TestObservation("synthetic-tenant", "demo-app", "CASE-001", "v1",
                           "RUN-001", "FAIL", "synthetic://run/RUN-001")
    gate.add_review(HumanReview("REVIEW-001", case.tenant, case.system, case.case_id,
                                case.version, case.run_id, "human-reviewer-01", True, 1000))
    entry = gate.promote(case, "REVIEW-001", now=100)
    before = gate.lookup(case.tenant, case.system, case.case_id, now=101)
    gate.revoke("REVIEW-001")
    after = gate.lookup(case.tenant, case.system, case.case_id, now=102)
    return {"environment": "fully_synthetic_no_llm_no_network",
            "evidence_sha256": entry.evidence_sha256,
            "approved_before_revocation": before is not None,
            "available_after_revocation": after is not None,
            "data": before}


if __name__ == "__main__":
    print(json.dumps(synthetic_demo(), sort_keys=True, indent=2))
