import unittest
from textnode import TextType, TextNode
from split_nodes import split_nodes_delimiter


class TestSplitNodes(unittest.TestCase):
    def test_split_bold(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_italic(self):
        nodes = [TextNode("This is *italic* text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_unmatched_delimiter(self):
        nodes = [TextNode("This is **bold text", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertTrue(
            "Invalid markdown: missing closing delimiter" in str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
