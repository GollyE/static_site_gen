import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):

    def test_missing_arg(self):
        node = HTMLNode(tag="https://www.google.com")
        pass


    def test_repr(self):
        node = HTMLNode(tag="a",value="google",props={"href":"https/www.google.com"})
        self.assertEqual(
             "HTMLNode(a,google,None,{'href': 'https/www.google.com'})", repr(node)
         )
    def test_props(self):
        node = HTMLNode(tag="a",value="google",props={"href":"https/www.google.com"})
        self.assertEqual(
             ' href="https/www.google.com"', node.props_to_html()
         )
    def test_props2(self):
         node = HTMLNode(tag="a",value="google",props={"href":"https/www.google.com", "target":"_blank"})
         
         self.assertEqual(
             ' href="https/www.google.com" target="_blank"', node.props_to_html()
         )              

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )

        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )


if __name__ == "__main__":
    unittest.main()