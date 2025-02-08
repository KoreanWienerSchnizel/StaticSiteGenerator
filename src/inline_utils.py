import re

from htmlnode import LeafNode
from textnode import TextNode, TextType


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def markddown_delimiter_to_regex_pattern(delimiter):
    delimiter = re.escape(delimiter)
    return rf"{delimiter}(.*?){delimiter}"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for node in old_nodes:
        # NOTE: consider implementing nesting
        if node.text_type != TextType.TEXT:
            node_list.append(node)
            continue

        text = node.text
        pattern = re.compile(markddown_delimiter_to_regex_pattern(delimiter))
        i = 0
        while len(text) > 0:
            match = pattern.search(text, i)
            if not match:
                node_list.append(TextNode(text, TextType.TEXT))
                break
            if match.group(1) == "":
                i = match.end() - len(delimiter)
                continue
            if match.start() > 0:
                node_list.append(TextNode(text[: match.start()], TextType.TEXT))
            node_list.append(TextNode(match.group(1), text_type))
            text = text[match.end() :]
    return node_list


def split_nodes_image(old_nodes):
    node_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            node_list.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)
        if not images:
            node_list.append(node)
            continue
        for alt, path in images:
            split_text = text.split(f"![{alt}]({path})", 1)
            if split_text[0]:
                node_list.append(TextNode(split_text[0], TextType.TEXT))
            node_list.append(TextNode(alt, TextType.IMAGE, path))
            text = split_text[1]
        if text:
            node_list.append(TextNode(text, TextType.TEXT))
    return node_list


def split_nodes_link(old_nodes):
    node_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            node_list.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)
        if not links:
            node_list.append(node)
            continue
        for alt, path in links:
            split_text = text.split(f"[{alt}]({path})", 1)
            if split_text[0]:
                node_list.append(TextNode(split_text[0], TextType.TEXT))
            node_list.append(TextNode(alt, TextType.LINK, path))
            text = split_text[1]
        if text:
            node_list.append(TextNode(text, TextType.TEXT))
    return node_list


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
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("TextNode Error: unknown TextType")


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def text_to_children(text):
    nodes = text_to_textnodes(text)
    return list(map(text_node_to_html_node, nodes))
