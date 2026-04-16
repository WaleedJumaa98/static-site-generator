import unittest
from parent_node import ParentNode
from leaf_node import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        child1 = ParentNode(
            "span", [ParentNode("b", [LeafNode(None, "Hello")], None)], None
        )
        child2 = ParentNode(
            "span", [ParentNode("i", [LeafNode(None, "World")], None)], None
        )
        parent = ParentNode("div", [child1, child2], {"class": "container"})
        expected_html = '<div class="container"><span><b>Hello</b></span><span><i>World</i></span></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_to_html_no_tag(self):
        parent = ParentNode(
            None, [ParentNode("span", [ParentNode(None, ["Hello"], None)], None)], None
        )
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_no_children(self):
        parent = ParentNode("div", None, {"class": "container"})
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
