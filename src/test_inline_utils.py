import unittest

from htmlnode import LeafNode
from inline_utils import (
    extract_markdown_links,
    extract_markdown_images,
    markddown_delimiter_to_regex_pattern,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_children,
    text_to_textnodes,
)
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
        self.assertEqual(
            node_list,
            [TextNode("**"), TextNode("bold text", TextType.BOLD), TextNode("**")],
        )

    def test_split_delimiter_no_closing(self):
        node = TextNode("bold text**text", TextType.TEXT)
        node_list = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(node_list, [TextNode("bold text**text")])

    def test_split_delimiter_multiple_types(self):
        node = TextNode("this is **bold** and *italic*", TextType.TEXT)
        node_list = split_nodes_delimiter([node], "**", TextType.BOLD)
        node_list = split_nodes_delimiter(node_list, "*", TextType.ITALIC)
        self.assertEqual(
            node_list,
            [
                TextNode("this is "),
                TextNode("bold", TextType.BOLD),
                TextNode(" and "),
                TextNode("italic", TextType.ITALIC),
            ],
        )

    # extract_markdown_images and links tests
    def test_extract_image(self):
        text = "this is a ![image](image_url.png)"
        match = extract_markdown_images(text)
        self.assertEqual(match, [("image", "image_url.png")])

    def test_extract_image_no_alt(self):
        text = "this is a ![](image_url.png)"
        match = extract_markdown_images(text)
        self.assertEqual(match, [("", "image_url.png")])

    def test_extract_link(self):
        text = "this is a [link](url.com)"
        match = extract_markdown_links(text)
        self.assertEqual(match, [("link", "url.com")])

    def test_extract_link_no_match(self):
        text = "this is a ![image](image_url.png)"
        match = extract_markdown_links(text)
        self.assertEqual(match, [])

    # markdown_delimter_to_regex tests
    def test_delim_to_regex(self):
        text = "**"
        regex = markddown_delimiter_to_regex_pattern(text)
        self.assertEqual(regex, r"\*\*(.*?)\*\*")

    # split_nodes_link and images tests
    def test_split_nodes_image(self):
        node = TextNode("this is an ![image](img.png) image")
        node_list = split_nodes_image([node])
        self.assertEqual(
            node_list,
            [
                TextNode("this is an "),
                TextNode("image", TextType.IMAGE, "img.png"),
                TextNode(" image"),
            ],
        )

    def test_split_nodes_image_no_text(self):
        node = TextNode("![image](img.png)")
        node_list = split_nodes_image([node])
        self.assertEqual(
            node_list,
            [
                TextNode("image", TextType.IMAGE, "img.png"),
            ],
        )

    def test_split_nodes_link(self):
        node = TextNode("this is a [link](link.com)")
        node_list = split_nodes_link([node])
        self.assertEqual(
            node_list,
            [TextNode("this is a "), TextNode("link", TextType.LINK, "link.com")],
        )

    def test_split_nodes_link_multiple(self):
        node = TextNode("this is a [link](link.com) and then [another](link.org)")
        node_list = split_nodes_link([node])
        self.assertEqual(
            node_list,
            [
                TextNode("this is a "),
                TextNode("link", TextType.LINK, "link.com"),
                TextNode(" and then "),
                TextNode("another", TextType.LINK, "link.org"),
            ],
        )

    def test_split_nodes_image_with_a_link(self):
        node = TextNode("this is an ![image](img.png) and then [link](link.com)")
        node_list = split_nodes_image([node])
        self.assertEqual(
            node_list,
            [
                TextNode("this is an "),
                TextNode("image", TextType.IMAGE, "img.png"),
                TextNode(" and then [link](link.com)"),
            ],
        )

    def test_split_nodes_image_multiple_nodes(self):
        node = TextNode("this is an ![image](img.png)")
        node2 = TextNode("another ![image](img.png) image")
        node_list = split_nodes_image([node, node2])
        self.assertEqual(
            node_list,
            [
                TextNode("this is an "),
                TextNode("image", TextType.IMAGE, "img.png"),
                TextNode("another "),
                TextNode("image", TextType.IMAGE, "img.png"),
                TextNode(" image"),
            ],
        )

    def test_text_to_node(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_text_to_children(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_children(text)
        self.assertEqual(
            nodes,
            [
                LeafNode(None, "This is "),
                LeafNode("b", "text"),
                LeafNode(None, " with an "),
                LeafNode("i", "italic"),
                LeafNode(None, " word and a "),
                LeafNode("code", "code block"),
                LeafNode(None, " and an "),
                LeafNode(
                    "img",
                    None,
                    {"src": "https://i.imgur.com/fJRm4Vk.jpeg", "alt": "obi wan image"},
                ),
                LeafNode(None, " and a "),
                LeafNode("a", "link", {"href": "https://boot.dev"}),
            ],
        )


if __name__ == "__main__":
    unittest.main()
