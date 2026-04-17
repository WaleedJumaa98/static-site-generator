import unittest
from nodes.text_node import TextNode, TextType
from md_parser.inline import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_no_match(self):
        matches = extract_markdown_images("This is text without an image")
        self.assertListEqual([], matches)

    def test_extract_markdown_image_no_alt_text(self):
        matches = extract_markdown_images(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_image_no_url(self):
        matches = extract_markdown_images("This is text with an ![image]()")
        self.assertListEqual([("image", "")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_markdown_links_no_match(self):
        matches = extract_markdown_links("This is text without a link")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_no_link_text(self):
        matches = extract_markdown_links(
            "This is text with a link [](https://www.boot.dev)"
        )
        self.assertListEqual([("", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_no_url(self):
        matches = extract_markdown_links("This is text with a link [to boot dev]()")
        self.assertListEqual([("to boot dev", "")], matches)


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
        self.assertIn("Invalid markdown: missing closing delimiter", str(context.exception))


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
            TextNode("second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_image(self):
        nodes = [TextNode("This is text without an image", TextType.TEXT)]
        self.assertEqual(split_nodes_image(nodes), nodes)

    def test_image_at_start(self):
        nodes = [TextNode("![image](https://i.imgur.com/zjjcJKZ.png) text after", TextType.TEXT)]
        expected = [
            TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" text after", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image(nodes), expected)

    def test_image_at_end(self):
        nodes = [TextNode("text before ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)]
        expected = [
            TextNode("text before ", TextType.TEXT),
            TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(split_nodes_image(nodes), expected)

    def test_only_image(self):
        nodes = [TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)]
        expected = [TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png")]
        self.assertEqual(split_nodes_image(nodes), expected)

    def test_non_text_node_skipped(self):
        nodes = [TextNode("some text", TextType.BOLD)]
        self.assertEqual(split_nodes_image(nodes), nodes)

    def test_multiple_nodes(self):
        nodes = [
            TextNode("text without image", TextType.TEXT),
            TextNode("text with ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
        ]
        expected = [
            TextNode("text without image", TextType.TEXT),
            TextNode("text with ", TextType.TEXT),
            TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(split_nodes_image(nodes), expected)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_link(self):
        nodes = [
            TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.TEXT,
            )
        ]
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(split_nodes_link(nodes), expected)

    def test_no_link(self):
        nodes = [TextNode("This is text without a link", TextType.TEXT)]
        self.assertEqual(split_nodes_link(nodes), nodes)

    def test_link_at_start(self):
        nodes = [TextNode("[boot dev](https://www.boot.dev) is a great resource", TextType.TEXT)]
        expected = [
            TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" is a great resource", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_link(nodes), expected)

    def test_link_at_end(self):
        nodes = [TextNode("Check out [boot dev](https://www.boot.dev)", TextType.TEXT)]
        expected = [
            TextNode("Check out ", TextType.TEXT),
            TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
        ]
        self.assertEqual(split_nodes_link(nodes), expected)

    def test_only_link(self):
        nodes = [TextNode("[boot dev](https://www.boot.dev)", TextType.TEXT)]
        expected = [TextNode("boot dev", TextType.LINK, "https://www.boot.dev")]
        self.assertEqual(split_nodes_link(nodes), expected)

    def test_non_text_node_skipped(self):
        nodes = [TextNode("some text", TextType.ITALIC)]
        self.assertEqual(split_nodes_link(nodes), nodes)


class TestTextToTextNodes(unittest.TestCase):
    def test_all_types(self):
        text = "This is **bold** text with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_plain_text(self):
        text = "This is plain text without any markdown."
        expected = [TextNode("This is plain text without any markdown.", TextType.TEXT)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_only_bold(self):
        self.assertEqual(text_to_textnodes("**bold text**"), [TextNode("bold text", TextType.BOLD)])

    def test_only_italic(self):
        self.assertEqual(text_to_textnodes("_italic text_"), [TextNode("italic text", TextType.ITALIC)])

    def test_only_code(self):
        self.assertEqual(text_to_textnodes("`code block`"), [TextNode("code block", TextType.CODE)])

    def test_multiple_bold(self):
        text = "**first bold** and **second bold**"
        expected = [
            TextNode("first bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("second bold", TextType.BOLD),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_bold_and_italic(self):
        text = "**bold** and _italic_"
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_consecutive_markdown(self):
        text = "**bold**_italic_`code`"
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(text_to_textnodes(text), expected)


if __name__ == "__main__":
    unittest.main()
