import unittest
from agent_boundary_eval import Scenario, fixtures, policy, run, summary

class TestSyntheticHarness(unittest.TestCase):
    def test_rejects_unauthorized_external_side_effects(self):
        s = Scenario("reject", "send_email", "not_delegated", False, True)
        self.assertFalse(policy(s, "risk_tiered"))
        self.assertTrue(policy(s, "unguarded"))

    def test_allows_low_risk_delegated(self):
        s = Scenario("read", "read_only", "delegated", False, False)
        self.assertTrue(policy(s, "risk_tiered"))

    def test_revocation_dominates_prior_approval(self):
        s = Scenario("revoke", "send_email", "not_delegated", True, True, True)
        self.assertFalse(policy(s, "risk_tiered"))

    def test_metrics_and_evidence_deterministic(self):
        a = run(fixtures())
        b = run(fixtures())
        self.assertEqual(a, b)
        self.assertEqual(len(a), 45)
        m = summary(a)
        self.assertGreater(m["unguarded"]["unauthorized_executions"], 0)
        self.assertEqual(m["risk_tiered"]["unauthorized_executions"], 0)
        self.assertEqual(m["approve_everything"]["unauthorized_executions"], 0)

    def test_unknown_mode_fails_closed(self):
        with self.assertRaises(ValueError):
            policy(fixtures()[0], "made_up_mode")

if __name__ == "__main__":
    unittest.main()
