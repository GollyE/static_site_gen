import unittest
from textnode import *
from htmlnode import *


class TestHTMLNode(unittest.TestCase):

    def test_missing_arg(self):
        node = HTMLNode(tag="https://www.google.com")
        pass

    def test_LeafNode_construct(self):
        node = LeafNode("tag test value","value test value")
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
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!",props = {"href":"https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")    
    
    def test_text_italic(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node") 

    def test_text_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node") 

    def test_text_link(self):
        node = TextNode("This is a link text node", TextType.LINK,"https/www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href":"https/www.google.com"}) 

    def test_text_image(self):
        node = TextNode("google doodle",TextType.IMAGE,"https/www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"https/www.google.com","alt":"google doodle"}) 

    def test_text_err(self):
        with self.assertRaises(Exception):
            node = TextNode("google doodle",TextType.BEER,"https/www.google.com")
     
if __name__ == "__main__":
    unittest.main()