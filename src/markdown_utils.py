from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("TextNode Error: unknown TextType")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            node_list.append(node)
            continue

        split_text = node.text.split(delimiter)
        if len(split_text) < 3:
            node_list.append(TextNode(node.text, TextType.TEXT))
            continue

        type_toggle = False
        for i in range(len(split_text)):
            text = split_text[i]
            if not type_toggle and i + 1 < len(split_text) and i + 2 >= len(split_text):
                text += delimiter + split_text[i + 1]
            if text:
                node_list.append(
                    TextNode(text, text_type if type_toggle else TextType.TEXT)
                )
            type_toggle = not type_toggle
    return node_list
