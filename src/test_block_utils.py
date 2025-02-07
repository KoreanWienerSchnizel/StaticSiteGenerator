import unittest

from block_utils import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)
from htmlnode import LeafNode, ParentNode


class TestBlockUtils(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = "#heading\n\nparagraph of text\n\n*list of items\n*list of items 2\n*list of items 3\n"
        blocks = markdown_to_blocks(text)
        self.assertEqual(
            blocks,
            [
                "#heading",
                "paragraph of text",
                "*list of items\n*list of items 2\n*list of items 3",
            ],
        )

    def test_markdown_to_blocks_extra_whitespace(self):
        text = "\n\n#heading\n\n  paragraph of text\n\n\n\n*list of items\n*list of items 2\n*list of items 3    \n\n\n\n"
        blocks = markdown_to_blocks(text)
        self.assertEqual(
            blocks,
            [
                "#heading",
                "paragraph of text",
                "*list of items\n*list of items 2\n*list of items 3",
            ],
        )

        # block_to_block_type tests

    def test_block_to_type_head(self):
        text = "###### heading"
        type = block_to_block_type(text)
        self.assertEqual(type, BlockType.HEADING)

    def test_block_to_type_head_too_many(self):
        text = "####### heading"
        type = block_to_block_type(text)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_block_to_type_codeblock(self):
        text = "```\ncode\nmore code\n```"
        type = block_to_block_type(text)
        self.assertEqual(type, BlockType.CODEBLOCK)

    def test_block_to_type_quote(self):
        text = ">quotes\n>more quotes\n>even more quotes"
        type = block_to_block_type(text)
        self.assertEqual(type, BlockType.QUOTE)

    def test_block_to_type_ulist(self):
        text = "* item1 \n* item2\n* item3\n"
        type = block_to_block_type(text)
        self.assertEqual(type, BlockType.U_LIST)

    def test_block_to_type_olist(self):
        text = "1. item1\n2. item2\n3. item3"
        type = block_to_block_type(text)
        self.assertEqual(type, BlockType.O_LIST)

        # block_to_htmlnode tests

    def test_block_to_html(self):
        text = """
# heading

paragraph

* list
* [link](url.com)

**bold** paragraph

"""
        node = markdown_to_html_node(text)
        self.assertEqual(
            node.to_html(),
            '<div><h1>heading</h1><p>paragraph</p><ul><li>list</li><li><a href="url.com">link</a></li></ul><p><b>bold</b> paragraph</p></div>',
        )


if __name__ == "__main__":
    unittest.main()
