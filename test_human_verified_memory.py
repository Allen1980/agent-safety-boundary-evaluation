"""Unit tests use synthetic fixtures only; no live AI or human respondents."""
from dataclasses import replace
import unittest

from human_verified_memory import (
    HumanReview, MemoryGate, TestObservation, UntrustedEvidence, synthetic_demo,
)


class TestHumanVerifiedMemory(unittest.TestCase):
    def setUp(self):
        self.gate = MemoryGate()
        self.case = TestObservation("tenant-A", "system-1", "case-01", "v1",
                                    "run-01", "FAIL", "synthetic://run-01")
        self.review = HumanReview("approval-01", "tenant-A", "system-1",
                                  "case-01", "v1", "run-01", "reviewer-01",
                                  True, 500)
        self.gate.set_version("tenant-A", "system-1", "v1")
        self.gate.add_review(self.review)

    def test_approved_observation_is_citable(self):
        entry = self.gate.promote(self.case, self.review.decision_id, 10)
        result = self.gate.lookup("tenant-A", "system-1", "case-01", 11)
        self.assertEqual(result["citation"], "synthetic://run-01")
        self.assertEqual(result["outcome"], "FAIL")
        self.assertEqual(len(entry.evidence_sha256), 64)

    def test_without_review_cannot_promote(self):
        with self.assertRaisesRegex(UntrustedEvidence, "no human review"):
            self.gate.promote(self.case, "unknown", 10)

    def test_rejected_review_cannot_promote(self):
        self.gate = MemoryGate()
        self.gate.set_version("tenant-A", "system-1", "v1")
        self.gate.add_review(replace(self.review, approved=False))
        with self.assertRaises(UntrustedEvidence):
            self.gate.promote(self.case, "approval-01", 10)

    def test_wrong_tenant_fails_closed(self):
        with self.assertRaisesRegex(UntrustedEvidence, "review scope"):
            self.gate.promote(replace(self.case, tenant="tenant-B"), "approval-01", 10)

    def test_review_does_not_cover_new_test_run(self):
        with self.assertRaisesRegex(UntrustedEvidence, "review scope"):
            self.gate.promote(replace(self.case, run_id="run-02"), "approval-01", 10)

    def test_version_is_checked_during_promotion(self):
        self.gate.set_version("tenant-A", "system-1", "v2")
        with self.assertRaisesRegex(UntrustedEvidence, "out-of-date"):
            self.gate.promote(self.case, "approval-01", 10)

    def test_expired_approval_fails_closed(self):
        with self.assertRaisesRegex(UntrustedEvidence, "expired"):
            self.gate.promote(self.case, "approval-01", 500)

    def test_revoked_review_invalidates_existing_memory(self):
        self.gate.promote(self.case, "approval-01", 10)
        self.gate.revoke("approval-01")
        self.assertIsNone(self.gate.lookup("tenant-A", "system-1", "case-01", 11))

    def test_stale_system_version_invalidates_retrieval(self):
        self.gate.promote(self.case, "approval-01", 10)
        self.gate.set_version("tenant-A", "system-1", "v2")
        self.assertIsNone(self.gate.lookup("tenant-A", "system-1", "case-01", 11))

    def test_unauthorized_tenant_cannot_retrieve(self):
        self.gate.promote(self.case, "approval-01", 10)
        self.assertIsNone(self.gate.lookup("tenant-B", "system-1", "case-01", 11))

    def test_agent_cannot_impersonate_reviewer_label(self):
        gate = MemoryGate()
        gate.set_version("tenant-A", "system-1", "v1")
        gate.add_review(replace(self.review, reviewer_id="agent"))
        with self.assertRaisesRegex(UntrustedEvidence, "independent human"):
            gate.promote(self.case, "approval-01", 10)

    def test_missing_evidence_is_rejected(self):
        with self.assertRaisesRegex(UntrustedEvidence, "missing provenance"):
            self.gate.promote(replace(self.case, source_ref=""), "approval-01", 10)

    def test_conflicting_second_write_requires_review(self):
        self.gate.promote(self.case, "approval-01", 10)
        with self.assertRaisesRegex(UntrustedEvidence, "conflicting"):
            self.gate.promote(self.case, "approval-01", 11)

    def test_tampered_entry_refuses_retrieval(self):
        original = self.gate.promote(self.case, "approval-01", 10)
        changed = replace(original, observation=replace(self.case, outcome="PASS"))
        self.gate.entries[("tenant-A", "system-1", "case-01")] = changed
        self.assertIsNone(self.gate.lookup("tenant-A", "system-1", "case-01", 11))

    def test_synthetic_demo_is_reproducible(self):
        a, b = synthetic_demo(), synthetic_demo()
        self.assertEqual(a, b)
        self.assertTrue(a["approved_before_revocation"])
        self.assertFalse(a["available_after_revocation"])


if __name__ == "__main__":
    unittest.main()
