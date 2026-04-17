import unittest
from src.extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# This is a title"
        expected = "This is a title"
        result = extract_title(markdown)
        self.assertEqual(result, expected)

    def test_extract_title_with_whitespace(self):
        markdown = "   # This is a title with whitespace   "
        expected = "This is a title with whitespace"
        result = extract_title(markdown)
        self.assertEqual(result, expected)

    def test_extract_title_no_title(self):
        markdown = "This is some text without a title"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertTrue("No h1 header found" in str(context.exception))

    def test_extract_title_with_multiple_lines(self):
        markdown = """Some intro text

# The Real Title

Some more content"""
        expected = "The Real Title"
        result = extract_title(markdown)
        self.assertEqual(result, expected)

    def test_extract_title_ignores_h2(self):
        markdown = "## This is h2, not h1"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_ignores_multiple_hashes(self):
        markdown = "### This is h3, not h1"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_single_word(self):
        markdown = "# Title"
        expected = "Title"
        result = extract_title(markdown)
        self.assertEqual(result, expected)

    def test_extract_title_with_special_chars(self):
        markdown = "# Title with **bold** and _italic_"
        expected = "Title with **bold** and _italic_"
        result = extract_title(markdown)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
