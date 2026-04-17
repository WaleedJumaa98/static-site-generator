import unittest
from blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_newlines(self):
        md = "\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_no_newlines(self):
        md = "This is a single block of text without any newlines."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [md.strip()])

    def test_markdown_to_blocks_multiple_consecutive_newlines(self):
        md = "First block\n\n\n\nSecond block\n\n\nThird block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block", "Third block"])

    def test_markdown_to_blocks_leading_and_trailing_newlines(self):
        md = "\n\nLeading and trailing newlines\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Leading and trailing newlines"])

    def test_markdown_to_blocks_blocks_with_only_whitespace(self):
        md = "First block\n\n   \n\nSecond block\n\n\t\nThird block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block", "Third block"])


if __name__ == "__main__":
    unittest.main()
