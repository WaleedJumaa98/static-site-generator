import unittest
from text_node import TextType, TextNode
from split_nodes import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

# Test cases for split_nodes_delimiter function


class TestSplitNodesDelimiter(unittest.TestCase):
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


# Test cases for split_nodes_image function


class TestSplitNodesImage(unittest.TestCase):
    def test_split_image(self):
        nodes = [
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"
            ),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_image(self):
        nodes = [TextNode("This is text without an image", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        expected = [TextNode("This is text without an image", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_unmatched_image(self):
        nodes = [
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png",
                TextType.TEXT,
            )
        ]
        self.assertEqual(new_nodes, expected)

    def test_image_at_start(self):
        nodes = [
            TextNode(
                "![image](https://i.imgur.com/zjjcJKZ.png) text after image",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" text after image", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_image_at_end(self):
        nodes = [
            TextNode(
                "text before image ![image](https://i.imgur.com/zjjcJKZ.png)",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("text before image ", TextType.TEXT),
            TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_only_image(self):
        nodes = [
            TextNode(
                "![image](https://i.imgur.com/zjjcJKZ.png)",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_non_text_node_image(self):
        nodes = [TextNode("some text", TextType.BOLD)]
        new_nodes = split_nodes_image(nodes)
        expected = [TextNode("some text", TextType.BOLD)]
        self.assertEqual(new_nodes, expected)

    def test_multiple_nodes_with_image(self):
        nodes = [
            TextNode("text without image", TextType.TEXT),
            TextNode(
                "text with ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT
            ),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("text without image", TextType.TEXT),
            TextNode("text with ", TextType.TEXT),
            TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(new_nodes, expected)


# Test cases for split_nodes_link function


class TestSplitNodesLink(unittest.TestCase):
    def test_split_link(self):
        nodes = [
            TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_link(self):
        nodes = [TextNode("This is text without a link", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        expected = [TextNode("This is text without a link", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_unmatched_link(self):
        nodes = [
            TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev",
                TextType.TEXT,
            )
        ]
        self.assertEqual(new_nodes, expected)

    def test_link_at_start(self):
        nodes = [
            TextNode(
                "[boot dev](https://www.boot.dev) is a great resource",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" is a great resource", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_link_at_end(self):
        nodes = [
            TextNode(
                "Check out [boot dev](https://www.boot.dev)",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("Check out ", TextType.TEXT),
            TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_only_link(self):
        nodes = [
            TextNode(
                "[boot dev](https://www.boot.dev)",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_non_text_node_link(self):
        nodes = [TextNode("some text", TextType.ITALIC)]
        new_nodes = split_nodes_link(nodes)
        expected = [TextNode("some text", TextType.ITALIC)]
        self.assertEqual(new_nodes, expected)

    def test_multiple_nodes_with_link(self):
        nodes = [
            TextNode("text without link", TextType.TEXT),
            TextNode("text with [a link](https://www.boot.dev)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("text without link", TextType.TEXT),
            TextNode("text with ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "https://www.boot.dev"),
        ]
        self.assertEqual(new_nodes, expected)


# Test cases for text_to_textnodes function
class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **bold** text with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image",
                TextType.IMAGES,
                "https://i.imgur.com/fJRm4Vk.jpeg",
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_nodes, expected)

    def test_text_to_textnodes_no_markdown(self):
        text = "This is plain text without any markdown."
        text_nodes = text_to_textnodes(text)
        expected = [TextNode("This is plain text without any markdown.", TextType.TEXT)]
        self.assertEqual(text_nodes, expected)

    def test_text_to_textnodes_only_bold(self):
        text = "**bold text**"
        text_nodes = text_to_textnodes(text)
        expected = [TextNode("bold text", TextType.BOLD)]
        self.assertEqual(text_nodes, expected)

    def test_text_to_textnodes_only_italic(self):
        text = "_italic text_"
        text_nodes = text_to_textnodes(text)
        expected = [TextNode("italic text", TextType.ITALIC)]
        self.assertEqual(text_nodes, expected)

    def test_text_to_textnodes_only_code(self):
        text = "`code block`"
        text_nodes = text_to_textnodes(text)
        expected = [TextNode("code block", TextType.CODE)]
        self.assertEqual(text_nodes, expected)

    def test_text_to_textnodes_multiple_bold(self):
        text = "**first bold** and **second bold**"
        text_nodes = text_to_textnodes(text)
        expected = [
            TextNode("first bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("second bold", TextType.BOLD),
        ]
        self.assertEqual(text_nodes, expected)

    def test_text_to_textnodes_multiple_italic(self):
        text = "_first italic_ and _second italic_"
        text_nodes = text_to_textnodes(text)
        expected = [
            TextNode("first italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("second italic", TextType.ITALIC),
        ]
        self.assertEqual(text_nodes, expected)

    def test_text_to_textnodes_multiple_code(self):
        text = "`code1` and `code2`"
        text_nodes = text_to_textnodes(text)
        expected = [
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
        ]
        self.assertEqual(text_nodes, expected)

    def test_text_to_textnodes_only_image(self):
        text = "![alt text](https://example.com/image.png)"
        text_nodes = text_to_textnodes(text)
        expected = [
            TextNode("alt text", TextType.IMAGES, "https://example.com/image.png")
        ]
        self.assertEqual(text_nodes, expected)

    def test_text_to_textnodes_only_link(self):
        text = "[click here](https://example.com)"
        text_nodes = text_to_textnodes(text)
        expected = [TextNode("click here", TextType.LINK, "https://example.com")]
        self.assertEqual(text_nodes, expected)

    def test_text_to_textnodes_multiple_images(self):
        text = "![image1](https://example.com/1.png) and ![image2](https://example.com/2.png)"
        text_nodes = text_to_textnodes(text)
        expected = [
            TextNode("image1", TextType.IMAGES, "https://example.com/1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image2", TextType.IMAGES, "https://example.com/2.png"),
        ]
        self.assertEqual(text_nodes, expected)

    def test_text_to_textnodes_multiple_links(self):
        text = "[link1](https://example1.com) and [link2](https://example2.com)"
        text_nodes = text_to_textnodes(text)
        expected = [
            TextNode("link1", TextType.LINK, "https://example1.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://example2.com"),
        ]
        self.assertEqual(text_nodes, expected)

    def test_text_to_textnodes_bold_and_italic(self):
        text = "**bold** and _italic_"
        text_nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(text_nodes, expected)

    def test_text_to_textnodes_code_and_link(self):
        text = "`code` and [link](https://example.com)"
        text_nodes = text_to_textnodes(text)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(text_nodes, expected)

    def test_text_to_textnodes_consecutive_markdown(self):
        text = "**bold**_italic_`code`"
        text_nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(text_nodes, expected)


if __name__ == "__main__":
    unittest.main()
