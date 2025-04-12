from textnode import *
from htmlnode import *
from inline import *


def main():
    test_node = TextNode("This is some anchor text",TextType.LINK,"https://www.google.com")
    #print(test_node)

    test_node2=LeafNode("a", "Click me!",props = {"href":"https://www.google.com"})
    #print(test_node2)

    test_node3 = TextNode("##bold## is the best ##bold2## is really ##bold3##",TextType.TEXT)

    old_nodes = [test_node,test_node3]
    delimiter = "##"
    text_type = TextType.BOLD
    result = split_nodes_delimiter(old_nodes, delimiter, text_type)
    print(result)
main()

