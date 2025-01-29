import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        child1 = HTMLNode()
        node = HTMLNode("<h1>", "Title", [child1], {"key": "value"})
        self.assertEqual(
            repr(node),
            "HTMLNode(<h1>, Title, [HTMLNode(None, None, None, {})], {'key': 'value'})",
        )


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "raw text")
        self.assertEqual(node.to_html(), "raw text")

    def test_to_html_with_props(self):
        node = LeafNode("a", "Link", {"href": "google.com"})
        self.assertEqual(node.to_html(), '<a href="google.com">Link</a>')


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p", [LeafNode("b", "Bold text"), LeafNode("i", "Italic Text")]
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b><i>Italic Text</i></p>")

    def text_to_html_nested(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "p", [LeafNode(None, "Raw Text"), LeafNode("i", "Italic Text")]
                ),
            ],
        )
        self.assertEqual(
            node.to_html(), "<p><b>Bold text</b><p>Raw Text<i>Italic Text</i></p></p>"
        )

    def test_to_html_one_child(self):
        node = ParentNode("p", [LeafNode("i", "Italic Text")])
        self.assertEqual(node.to_html(), "<p><i>Italic Text</i></p>")

    def test_to_html_no_child(self):
        node = ParentNode("p", [])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_with_props(self):
        node = ParentNode(
            "a",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "p", [LeafNode(None, "Raw Text"), LeafNode("i", "Italic Text")]
                ),
            ],
            {"href": "google.com"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="google.com"><b>Bold text</b><p>Raw Text<i>Italic Text</i></p></a>',
        )


if __name__ == "__main__":
    unittest.main()
