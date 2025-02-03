import unittest

from markdown_utils import split_nodes_delimiter, text_node_to_html_node
from textnode import TextNode, TextType


class TestMarkdownUtils(unittest.TestCase):
    # text_node_to_html_node tests
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

    # split_nodes_delimiter tests
    def test_split_delimiter(self):
        node = TextNode("Text with **bold** text", TextType.TEXT)
        node_list = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            node_list,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_delimiter_more_nodes(self):
        node = TextNode("Text with **bold** text", TextType.TEXT)
        node2 = TextNode("more **bold** text", TextType.TEXT)
        node_list = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        self.assertEqual(
            node_list,
            [
                TextNode("Text with "),
                TextNode("bold", TextType.BOLD),
                TextNode(" text"),
                TextNode("more "),
                TextNode("bold", TextType.BOLD),
                TextNode(" text"),
            ],
        )

    def test_split_delimiter_no_normal(self):
        node = TextNode("**bold text**", TextType.TEXT)
        node_list = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(node_list, [TextNode("bold text", TextType.BOLD)])

    def test_split_delimiter_trailing(self):
        node = TextNode("**bold text**text**", TextType.TEXT)
        node_list = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            node_list, [TextNode("bold text", TextType.BOLD), TextNode("text**")]
        )

    def test_split_delimiter_doubled(self):
        node = TextNode("****bold text****", TextType.TEXT)
        node_list = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(node_list, [TextNode("bold text")])

    def test_split_delimiter_no_closing(self):
        node = TextNode("bold text**text", TextType.TEXT)
        node_list = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(node_list, [TextNode("bold text**text")])


if __name__ == "__main__":
    unittest.main()
