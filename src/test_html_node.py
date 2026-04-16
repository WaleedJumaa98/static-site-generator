import unittest
from html_node import HtmlNode


class TestHtmlNode(unittest.TestCase):
    def test_init(self):
        node = HtmlNode("div", "Hello", None, {"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"class": "container"})

    def test_props_to_html(self):
        node = HtmlNode("div", "Hello", None, {"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')

    def test_props_to_html_empty(self):
        node = HtmlNode("div", "Hello")
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HtmlNode("div", "Hello", None, {"class": "container"})
        expected_repr = "HtmlNode(tag=div, value=Hello, children=None, props={'class': 'container'})"
        self.assertEqual(repr(node), expected_repr)

    if __name__ == "__main__":
        unittest.main()
