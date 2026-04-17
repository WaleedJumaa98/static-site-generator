import unittest
from md_parser.converter import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):

    # ── Paragraph ────────────────────────────────────────────────────────────

    def test_paragraph_with_inline_markdown(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div>"
            "<p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p>"
            "</div>",
        )

    def test_paragraph_plain_text(self):
        md = "Just a plain sentence."
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><p>Just a plain sentence.</p></div>")

    def test_paragraph_multiline_joins_with_space(self):
        md = "line one\nline two\nline three"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>line one line two line three</p></div>",
        )

    def test_paragraph_starting_with_digit_is_not_ordered_list(self):
        # "5 things" starts with a digit but is not "1. " so it's a paragraph
        md = "5 things to know about Python"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>5 things to know about Python</p></div>",
        )

    # ── Headings ──────────────────────────────────────────────────────────────

    def test_heading_h1(self):
        node = markdown_to_html_node("# Hello")
        self.assertEqual(node.to_html(), "<div><h1>Hello</h1></div>")

    def test_heading_h2(self):
        node = markdown_to_html_node("## Hello")
        self.assertEqual(node.to_html(), "<div><h2>Hello</h2></div>")

    def test_heading_h6(self):
        node = markdown_to_html_node("###### Deep heading")
        self.assertEqual(node.to_html(), "<div><h6>Deep heading</h6></div>")

    def test_heading_with_inline_bold(self):
        node = markdown_to_html_node("## Hello **world**")
        self.assertEqual(node.to_html(), "<div><h2>Hello <b>world</b></h2></div>")

    def test_heading_with_inline_italic(self):
        node = markdown_to_html_node("### Title with _emphasis_")
        self.assertEqual(
            node.to_html(), "<div><h3>Title with <i>emphasis</i></h3></div>"
        )

    # ── Code block ───────────────────────────────────────────────────────────

    def test_codeblock_inline_markdown_not_processed(self):
        # Inline markdown inside a code block must NOT be converted
        md = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_codeblock_simple(self):
        md = "```\nprint('hello')\n```"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>print('hello')</code></pre></div>",
        )

    # ── Blockquote ────────────────────────────────────────────────────────────

    def test_quote_single_line(self):
        node = markdown_to_html_node("> This is a quote")
        self.assertEqual(
            node.to_html(), "<div><blockquote>This is a quote</blockquote></div>"
        )

    def test_quote_multiline(self):
        md = "> line one\n> line two"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>line one\nline two</blockquote></div>",
        )

    def test_quote_with_inline_bold(self):
        node = markdown_to_html_node("> **important** note")
        self.assertEqual(
            node.to_html(),
            "<div><blockquote><b>important</b> note</blockquote></div>",
        )

    # ── Unordered list ───────────────────────────────────────────────────────

    def test_unordered_list_basic(self):
        md = "- item one\n- item two\n- item three"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>item one</li><li>item two</li><li>item three</li></ul></div>",
        )

    def test_unordered_list_with_inline_markdown(self):
        md = "- **bold** item\n- _italic_ item"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li><b>bold</b> item</li><li><i>italic</i> item</li></ul></div>",
        )

    # ── Ordered list ─────────────────────────────────────────────────────────

    def test_ordered_list_basic(self):
        md = "1. first\n2. second\n3. third"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>",
        )

    def test_ordered_list_with_inline_markdown(self):
        md = "1. **step one**\n2. _step two_"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li><b>step one</b></li><li><i>step two</i></li></ol></div>",
        )

    def test_ordered_list_out_of_order_is_paragraph(self):
        # Numbers not starting at 1 or not sequential → treated as paragraph
        md = "2. second\n3. third"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>2. second 3. third</p></div>",
        )

    # ── Mixed blocks ─────────────────────────────────────────────────────────

    def test_multiple_block_types(self):
        md = "# Title\n\nA paragraph.\n\n- item one\n- item two"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h1>Title</h1><p>A paragraph.</p><ul><li>item one</li><li>item two</li></ul></div>",
        )

    # ── Edge cases ───────────────────────────────────────────────────────────

    def test_empty_markdown_returns_empty_div(self):
        node = markdown_to_html_node("")
        self.assertEqual(node.to_html(), "<div></div>")

    def test_whitespace_only_returns_empty_div(self):
        node = markdown_to_html_node("   \n\n   \n")
        self.assertEqual(node.to_html(), "<div></div>")

    def test_extra_blank_lines_between_blocks_ignored(self):
        md = "# Heading\n\n\n\nParagraph here"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h1>Heading</h1><p>Paragraph here</p></div>",
        )

    def test_paragraph_with_link(self):
        md = "Visit [example](https://example.com) for more."
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            '<div><p>Visit <a href="https://example.com">example</a> for more.</p></div>',
        )

    def test_paragraph_with_inline_code(self):
        md = "Use the `print()` function."
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>Use the <code>print()</code> function.</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
