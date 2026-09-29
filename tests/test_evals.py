"""Tests hors ligne de evals/evals.json : structure, fixtures et vérificateur.

Ils ne lancent pas Claude. Ils garantissent que les cas sont bien formés,
que les sorties de référence passent le vérificateur et que les sorties
fautives déclenchent les règles attendues.
"""
import io
import json
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EVALS_DIR = os.path.join(ROOT, "evals")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import verifier  # noqa: E402

ORDER = {"P0": 0, "P1": 1, "P2": 2}


def load():
    with io.open(os.path.join(EVALS_DIR, "evals.json"), encoding="utf-8") as fh:
        return json.load(fh)


def read(rel):
    with io.open(os.path.join(EVALS_DIR, rel), encoding="utf-8") as fh:
        return fh.read()


def references(case):
    refs = []
    if "reference_output" in case:
        refs.append(case["reference_output"])
    refs.extend(case.get("extra_reference_outputs", []))
    return refs


class Structure(unittest.TestCase):
    def test_at_least_three_realistic_cases(self):
        self.assertGreaterEqual(len(load()["evals"]), 3)

    def test_each_case_is_complete_and_ids_are_unique(self):
        ids = set()
        for case in load()["evals"]:
            self.assertNotIn(case["id"], ids)
            ids.add(case["id"])
            for key in ("prompt", "expected_output", "assertions", "should_trigger"):
                self.assertIn(key, case, case["id"])
            self.assertGreaterEqual(len(case["assertions"]), 2, case["id"])
            for a in case["assertions"]:
                self.assertIn(a["kind"], ("humain", "verifier"), case["id"])

    def test_referenced_files_exist(self):
        for case in load()["evals"]:
            if "input_file" in case:
                self.assertTrue(os.path.isfile(os.path.join(EVALS_DIR, case["input_file"])))
            for ref in references(case):
                self.assertTrue(os.path.isfile(os.path.join(EVALS_DIR, ref["file"])), ref["file"])
                self.assertIn(ref["network"], verifier.NETWORKS)
            if "flawed_output" in case:
                self.assertTrue(os.path.isfile(os.path.join(EVALS_DIR, case["flawed_output"]["file"])))

    def test_no_real_email_address_in_evals(self):
        pattern = re.compile(r"[\w.+-]+@(?!example\.)[\w-]+\.[a-z]{2,}", re.I)
        for folder in (EVALS_DIR, os.path.join(EVALS_DIR, "fixtures")):
            for name in os.listdir(folder):
                path = os.path.join(folder, name)
                if os.path.isfile(path):
                    with io.open(path, encoding="utf-8") as fh:
                        self.assertIsNone(pattern.search(fh.read()), name)


class ReferenceOutputs(unittest.TestCase):
    def test_reference_outputs_respect_their_verifier_assertions(self):
        for case in load()["evals"]:
            checks = [a for a in case["assertions"] if a["kind"] == "verifier"]
            for ref in references(case):
                self.assertTrue(checks, case["id"])
                _, findings = verifier.verify(read(ref["file"]), ref["network"])
                for check in checks:
                    limit = ORDER[check["max_priority_allowed"]]
                    allowed = set(check["allowed_rules"])
                    for f in findings:
                        if f.rule in allowed:
                            continue
                        self.assertGreater(
                            ORDER[f.priority], limit,
                            "%s (%s) : %s %s" % (case["id"], ref["file"], f.priority, f.rule),
                        )

    def test_reference_outputs_have_no_p0(self):
        for case in load()["evals"]:
            for ref in references(case):
                _, findings = verifier.verify(read(ref["file"]), ref["network"])
                self.assertFalse([f for f in findings if f.priority == "P0"], ref["file"])


class FlawedOutputs(unittest.TestCase):
    def test_flawed_outputs_trigger_expected_rules(self):
        for case in load()["evals"]:
            flawed = case.get("flawed_output")
            if not flawed:
                continue
            _, findings = verifier.verify(read(flawed["file"]), flawed["network"])
            found = {f.rule for f in findings}
            for rule in flawed["expected_rules"]:
                self.assertIn(rule, found, "%s : %s" % (case["id"], rule))


if __name__ == "__main__":
    unittest.main()
