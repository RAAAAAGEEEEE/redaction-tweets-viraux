"""Tests hors ligne de scripts/verifier.py."""
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import verifier  # noqa: E402

SCRIPT = os.path.join(ROOT, "scripts", "verifier.py")


def rules(text, network="x", **kw):
    _, findings = verifier.verify(text, network, **kw)
    return {(f.priority, f.rule) for f in findings}


class Length(unittest.TestCase):
    def test_plain_text_counts_one_per_character(self):
        self.assertEqual(verifier.length_x("abc é"), 5)

    def test_url_counts_23_on_x_whatever_its_length(self):
        self.assertEqual(verifier.length_x("a " + "https://example.com/" + "x" * 200), 2 + 23)

    def test_emoji_counts_two_on_x_even_when_composed(self):
        self.assertEqual(verifier.length_x("\U0001F600"), 2)
        self.assertEqual(verifier.length_x("\U0001F468‍\U0001F469‍\U0001F467"), 2)

    def test_ellipsis_euro_and_narrow_nbsp_count_two_on_x(self):
        self.assertEqual(verifier.length_x("…"), 2)
        self.assertEqual(verifier.length_x("€"), 2)
        self.assertEqual(verifier.length_x(" "), 2)

    def test_no_break_space_counts_one_on_x(self):
        self.assertEqual(verifier.length_x(" "), 1)

    def test_bluesky_counts_graphemes(self):
        self.assertEqual(verifier.length_bluesky("é"), 1)
        self.assertEqual(verifier.length_bluesky("\U0001F468‍\U0001F469‍\U0001F467"), 1)
        self.assertEqual(verifier.length_bluesky("\U0001F1EB\U0001F1F7"), 1)
        self.assertEqual(verifier.length_bluesky("ab"), 2)

    def test_limits_are_enforced_per_network(self):
        self.assertIn(("P0", "longueur"), rules("a" * 281 + " ?", "x"))
        self.assertNotIn(("P0", "longueur"), rules("a" * 250 + " ?", "x"))
        self.assertIn(("P0", "longueur"), rules("a" * 301 + " ?", "bluesky"))
        self.assertNotIn(("P0", "longueur"), rules("a" * 297 + " ?", "bluesky"))
        self.assertIn(("P0", "longueur"), rules("a" * 501 + " ?", "threads"))
        self.assertNotIn(("P0", "longueur"), rules("a" * 400 + " ?", "threads"))

    def test_custom_limit_for_longer_accounts(self):
        self.assertNotIn(("P0", "longueur"), rules("a" * 400 + " ?", "x", limit=25000))


class HardRules(unittest.TestCase):
    def test_em_dash_is_p0(self):
        self.assertIn(("P0", "cadratin"), rules("Un outil — pas dix. Tu utilises quoi ?"))

    def test_leftover_placeholder_is_p0(self):
        self.assertIn(("P0", "placeholder"), rules("Bienvenue à [Ville] ?"))

    def test_open_item_is_p1(self):
        self.assertIn(("P1", "a-confirmer"), rules("Tu paies [[à confirmer : prix]] ?"))

    def test_hashtag_maximum_per_network(self):
        four = "Test #a #b #c #d ?"
        self.assertIn(("P1", "hashtags"), rules(four, "x"))
        self.assertNotIn(("P1", "hashtags"), rules("Test #a #b #c ?", "x"))
        self.assertIn(("P1", "hashtags"), rules("Test #a #b ?", "threads"))
        self.assertNotIn(("P1", "hashtags"), rules("Test #a ?", "threads"))

    def test_more_than_five_links_fails_on_threads(self):
        text = " ".join("https://example.com/%d" % i for i in range(6)) + " ?"
        self.assertIn(("P0", "liens"), rules(text, "threads"))

    def test_emoji_flagged_by_default_and_allowed_on_request(self):
        self.assertIn(("P1", "emoji"), rules("Test \U0001F680 ?"))
        self.assertNotIn(("P1", "emoji"), rules("Test \U0001F680 ?", allow_emoji=True))

    def test_ai_tic_is_p1(self):
        self.assertIn(("P1", "formule-ia"), rules("Dans un monde où tout va vite, tu fais quoi ?"))


class Softer(unittest.TestCase):
    def test_numbers_are_listed_for_sourcing(self):
        self.assertIn(("P2", "chiffre-a-sourcer"), rules("Tu paies 200 € par mois ?"))

    def test_thread_numbering_and_steps_are_not_numbers(self):
        self.assertNotIn(("P2", "chiffre-a-sourcer"), rules("1/3 Étape 2 : relance. Tu le fais ?"))

    def test_last_post_needs_a_question(self):
        self.assertIn(("P2", "pas-de-question-finale"), rules("Arrête de perdre du temps."))
        self.assertNotIn(("P2", "pas-de-question-finale"), rules("Arrête. Tu fais quoi ?"))

    def test_missing_space_before_high_punctuation(self):
        self.assertIn(("P1", "espace-ponctuation"), rules("Tu fais quoi?"))
        self.assertNotIn(("P1", "espace-ponctuation"), rules("Tu fais quoi ?"))
        self.assertNotIn(("P1", "espace-ponctuation"), rules("Tu fais quoi ?"))


class Thread(unittest.TestCase):
    def test_thread_is_split_on_dashes_line(self):
        lengths, _ = verifier.verify("Un.\n---\nDeux.\n---\nTrois ?", "x")
        self.assertEqual(len(lengths), 3)

    def test_empty_input_is_p0(self):
        self.assertIn(("P0", "vide"), rules("  \n"))


class CommandLine(unittest.TestCase):
    def run_cli(self, text, *args):
        return subprocess.run(
            [sys.executable, SCRIPT, "-", *args],
            input=text.encode("utf-8"), capture_output=True,
        )

    def test_exit_0_without_p0(self):
        self.assertEqual(self.run_cli("Tu fais quoi ?").returncode, 0)

    def test_exit_1_with_p0(self):
        self.assertEqual(self.run_cli("a" * 400 + " ?").returncode, 1)

    def test_exit_2_when_file_is_unreadable(self):
        r = subprocess.run([sys.executable, SCRIPT, os.path.join(HERE, "absent.txt")], capture_output=True)
        self.assertEqual(r.returncode, 2)

    def test_json_output(self):
        import json
        r = self.run_cli("Tu fais quoi ?", "--json", "--network", "bluesky")
        data = json.loads(r.stdout.decode("utf-8"))
        self.assertEqual(data["network"], "bluesky")
        self.assertEqual(data["limit"], 300)


if __name__ == "__main__":
    unittest.main()
