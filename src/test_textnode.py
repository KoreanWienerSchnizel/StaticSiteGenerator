import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_text_to_html(self):
        text_node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(repr(html_node), "HTMLNode(b, bold text, None, {})")

    def test_text_to_html_img(self):
        text_node = TextNode("image text", TextType.IMAGE, "img.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            repr(html_node),
            "HTMLNode(img, None, None, {'src': 'img.png', 'alt': 'image text'})",
        )


if __name__ == "__main__":
    unittest.main()
