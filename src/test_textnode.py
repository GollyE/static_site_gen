import unittest

from textnode import TextNode, TextType


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
        
        


if __name__ == "__main__":
    unittest.main()