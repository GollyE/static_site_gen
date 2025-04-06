from textnode import *
from htmlnode import *


def main():
    test_node = TextNode("This is some anchor text",TextType.LINK,"https://www.google.com")
    print(test_node)

    test_node2=LeafNode("a", "Click me!",props = {"href":"https://www.google.com"})
    print(test_node2)
main()

