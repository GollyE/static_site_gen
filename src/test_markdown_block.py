import unittest

from textnode import TextNode, TextType
from inline import *
import textwrap
from markdown_blocks import *

class TestTextNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = textwrap.dedent("""
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """)
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["This is **bolded** paragraph","This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line","- This is a list\n- with items",],
        )

    def test_blocktype_id_code(self):
        block = "```this is a code block```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)
    
    def test_blocktype_id_heading(self):
        block = "###### this is a heading block ######"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_blocktype_id_heading2(self):
        block = "##### this is a heading block #####"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_blocktype_id_heading3(self):
        block = "# this is a heading block #"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_blocktype_id_quote(self):
        block = "> this is a quote block"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_blocktype_id_unordered(self):
            block = "- this is an unordered list block\n- item2\n- item3"
            result = block_to_block_type(block)
            self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_blocktype_id_ordered(self):
        block = "1. this is an ordered block\n2. item2"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_blocktype_id_code(self):
        block = "This is a paragraph block"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


def test_single_h1(self):
    md = "# Welcome to my site"
    self.assertEqual(extract_title(md), ["Welcome to my site"])

def test_multiple_h1(self):
    md = "# First Heading\nSome paragraph\n# Second Heading"
    self.assertEqual(extract_title(md), ["First Heading", "Second Heading"])

def test_no_h1(self):
    md = "## Subheading\nSome text\n### Smaller heading"
    self.assertEqual(extract_title(md), [])

def test_mixed_headings(self):
    md = "# Main Heading\n## Subheading\n# Another Main Heading\nText"
    self.assertEqual(extract_title(md), ["Main Heading", "Another Main Heading"])

def test_h1_with_extra_spaces(self):
    md = "#    Heading with spaces   "
    self.assertEqual(extract_title(md), ["Heading with spaces"])




if __name__ == "__main__":
    unittest.main()