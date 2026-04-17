import unittest
from ssg.builder import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# This is a title"
        self.assertEqual(extract_title(markdown), "This is a title")

    def test_extract_title_with_whitespace(self):
        markdown = "   # This is a title with whitespace   "
        self.assertEqual(extract_title(markdown), "This is a title with whitespace")

    def test_extract_title_no_title(self):
        markdown = "This is some text without a title"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertIn("No h1 header found", str(context.exception))

    def test_extract_title_with_multiple_lines(self):
        markdown = """Some intro text

# The Real Title

Some more content"""
        self.assertEqual(extract_title(markdown), "The Real Title")

    def test_extract_title_ignores_h2(self):
        with self.assertRaises(Exception):
            extract_title("## This is h2, not h1")

    def test_extract_title_ignores_h3(self):
        with self.assertRaises(Exception):
            extract_title("### This is h3, not h1")

    def test_extract_title_single_word(self):
        self.assertEqual(extract_title("# Title"), "Title")

    def test_extract_title_with_special_chars(self):
        markdown = "# Title with **bold** and _italic_"
        self.assertEqual(extract_title(markdown), "Title with **bold** and _italic_")


if __name__ == "__main__":
    unittest.main()
