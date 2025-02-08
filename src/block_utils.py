from enum import Enum
import re

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_utils import text_to_children


class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODEBLOCK = 3
    QUOTE = 4
    U_LIST = 5
    O_LIST = 6


def markdown_to_blocks(markdown):
    lines = markdown.splitlines()
    block = ""
    blocks = []
    for line in lines:
        if line:
            block += line + "\n"
            continue
        elif block:
            block = block.strip()
            blocks.append(block)
            block = ""
    if block:
        block = block.strip()
        blocks.append(block)
    return blocks


def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODEBLOCK

    lines = block.splitlines()
    if block[0] == ">":
        for line in lines:
            if line[0] != ">":
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block[:2] == "* " or block[:2] == "- ":
        for line in lines:
            if line[:2] == "* " or line[:2] == "- ":
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.U_LIST

    if block[:3] == "1. ":
        for i in range(len(lines)):
            if lines[i][:3] != f"{i + 1}. ":
                return BlockType.PARAGRAPH
        return BlockType.O_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        match type:
            case BlockType.PARAGRAPH:
                text = block.strip()
                children = text_to_children(text)
                block_nodes.append(ParentNode("p", children))

            case BlockType.HEADING:
                heading_value = block.find(" ")
                text = block[heading_value:]
                text = text.strip()
                children = text_to_children(text)
                block_nodes.append(ParentNode(f"h{heading_value}", children))

            case BlockType.CODEBLOCK:
                text = block[4:-3]
                code_node = LeafNode("code", text)
                block_nodes.append(ParentNode("pre", [code_node]))

            case BlockType.QUOTE:
                text = block[1:].replace("\n>", "\n")
                text = text.strip()
                children = text_to_children(text)
                block_nodes.append(ParentNode("blockquote", children))

            case BlockType.U_LIST:
                lines = block.splitlines()
                list_items = []
                for line in lines:
                    text = line[2:].strip()
                    children = text_to_children(text)
                    list_items.append(ParentNode("li", children))
                block_nodes.append(ParentNode("ul", list_items))

            case BlockType.O_LIST:
                lines = block.splitlines()
                list_items = []
                for line in lines:
                    text = line[3:].strip()
                    children = text_to_children(text)
                    list_items.append(ParentNode("li", children))
                block_nodes.append(ParentNode("ul", list_items))

            case _:
                raise Exception("No BlockType")

    return ParentNode("div", block_nodes)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("no title extracted")
