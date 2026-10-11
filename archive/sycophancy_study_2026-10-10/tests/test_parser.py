"""Parser tests on hand-written synthetic outputs. No model output is used."""

import unittest

from sycoling.parser import ParseStatus, option_letters, parse_answer


class ValidAnswers(unittest.TestCase):
    def test_each_option(self):
        for letter in "ABCD":
            r = parse_answer(f"Reasoning here.\n[[{letter}]]")
            self.assertEqual((r.status, r.letter), (ParseStatus.PARSED, letter))

    def test_harmless_variations(self):
        cases = {
            "[[b]]": "B",  # lower case
            "  [[ C ]]  ": "C",  # whitespace inside and around
            "[[\tD\n]]": "D",
            "**[[A]]**": "A",  # markdown around the marker
            "[[**B**]]": "B",  # markdown inside the marker
            "`[[C]]`": "C",
            "[[(D)]]": "D",  # parentheses inside the marker
            "[[A.]]": "A",  # trailing period inside
            "Final: [[B]].": "B",
            "［［Ｃ］］": "C",  # full-width brackets and letter (NFKC)
            "উত্তর: [[A]]": "A",  # non-Latin surrounding text
            "答案是 [[D]]": "D",
        }
        for text, want in cases.items():
            with self.subTest(text=text):
                r = parse_answer(text)
                self.assertEqual((r.status, r.letter), (ParseStatus.PARSED, want))

    def test_same_letter_repeated_is_not_ambiguous(self):
        r = parse_answer("[[C]] ... so the answer is [[c]]")
        self.assertEqual((r.status, r.letter), (ParseStatus.PARSED, "C"))

    def test_result_records_parser_version(self):
        self.assertTrue(parse_answer("[[A]]").parser_version)


class MustAbstain(unittest.TestCase):
    def assertAbstains(self, text, status):
        r = parse_answer(text)
        self.assertEqual(r.status, status, msg=r.detail)
        self.assertIsNone(r.letter)
        self.assertFalse(r.parsed)

    def test_missing(self):
        for text in (None, "", "   \n\t", "I am not sure.", "I cannot answer that."):
            with self.subTest(text=text):
                self.assertAbstains(text, ParseStatus.NO_ANSWER)

    def test_bare_letters_are_not_answers(self):
        # Without the marker the parser must not guess, even if a letter is obvious.
        for text in ("B", "The answer is B.", "Answer: (B)", "(C)"):
            with self.subTest(text=text):
                self.assertAbstains(text, ParseStatus.NO_ANSWER)

    def test_echoed_correction_target_is_not_an_answer(self):
        r = parse_answer("You said the answer is (B). Let me reconsider the passage.")
        self.assertEqual(r.status, ParseStatus.NO_ANSWER)
        self.assertEqual(r.other_mentions, ("B",))

    def test_incomplete_marker(self):
        for text in ("[[B]", "[B]]", "[B]", "[ [B] ]"):
            with self.subTest(text=text):
                self.assertAbstains(text, ParseStatus.NO_ANSWER)

    def test_conflicting_markers(self):
        self.assertAbstains("[[A]] wait, actually [[C]]", ParseStatus.MULTIPLE)

    def test_invalid_option_letter(self):
        for text in ("[[E]]", "[[Z]]"):
            with self.subTest(text=text):
                self.assertAbstains(text, ParseStatus.MALFORMED)

    def test_malformed_marker_content(self):
        for text in ("[[]]", "[[  ]]", "[[A, C]]", "[[AB]]", "[[A or B]]", "[[2]]", "[[option B]]", "[[ক]]"):
            with self.subTest(text=text):
                self.assertAbstains(text, ParseStatus.MALFORMED)

    def test_any_malformed_marker_poisons_the_reply(self):
        self.assertAbstains("[[B]] and also [[E]]", ParseStatus.MALFORMED)


class ContradictoryExplanation(unittest.TestCase):
    def test_marker_is_answer_of_record_and_contradiction_is_flagged(self):
        r = parse_answer("The passage clearly supports (C). [[B]]")
        self.assertEqual((r.status, r.letter), (ParseStatus.PARSED, "B"))
        self.assertEqual(r.other_mentions, ("C",))
        self.assertIn("other letters", r.detail)

    def test_mention_of_same_letter_is_not_flagged(self):
        r = parse_answer("Option (B) fits. [[B]]")
        self.assertEqual(r.other_mentions, ())


class Inputs(unittest.TestCase):
    def test_non_text_input_raises(self):
        for bad in (b"[[A]]", 1, ["[[A]]"]):
            with self.subTest(bad=bad), self.assertRaises(TypeError):
                parse_answer(bad)

    def test_option_count(self):
        self.assertEqual(option_letters(4), ("A", "B", "C", "D"))
        self.assertEqual(parse_answer("[[D]]", n_options=3).status, ParseStatus.MALFORMED)
        for n in (1, 27):
            with self.subTest(n=n), self.assertRaises(ValueError):
                option_letters(n)


if __name__ == "__main__":
    unittest.main()
