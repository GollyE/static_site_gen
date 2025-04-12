import unittest

from textnode import TextNode, TextType
from inline import*


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is another node", TextType.ITALIC,url="https://www.apple.com")
        node2 = TextNode("This is another node", TextType.ITALIC,url="https://www.apple.com")
        self.assertEqual(node,node2)
    
    def test_not_eq(self):
        node = TextNode("Test that text has to be equal", TextType.BOLD, url="https://www.google.com")
        node2 = TextNode("Test text not equal", TextType.BOLD, url="https://www.google.com")
        self.assertNotEqual(node,node2)

    def test_not_eq2(self):
        node = TextNode("Test for TextType not equal", TextType.BOLD, url="https://www.google.com")
        node2 = TextNode("Test for TextType not equal", TextType.TEXT, url="https://www.google.com")
        self.assertNotEqual(node,node2)

    def test_not_eq3(self):
        node = TextNode("Test for url not equal", TextType.TEXT, url="https://www.google.com")
        node2 = TextNode("Test for url not equal", TextType.TEXT, url="https://www.apple.com")
        self.assertNotEqual(node,node2)

    def test_missing_arg(self):
        with self.assertRaises(Exception):
            node = TextNode("Test for url not equal", url="https://www.google.com")

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )
        
    def test_split_del1(self):
        test_node = TextNode("This is some anchor text",TextType.LINK,"https://www.google.com")
        test_node3 = TextNode("##bold## is the best ##bold2## is really ##bold3##",TextType.TEXT)
        old_nodes = [test_node,test_node3]
        delimiter = "##"
        text_type = TextType.BOLD
        result = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(
            result, [TextNode("This is some anchor text",TextType.LINK,"https://www.google.com"),
                     TextNode("bold", TextType.BOLD, None), TextNode(" is the best ",TextType.TEXT, None),
                     TextNode("bold2", TextType.BOLD, None), TextNode(" is really ",TextType.TEXT, None),
                     TextNode("bold3", TextType.BOLD, None)]
        )
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()