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
    #print(result)

    # matches = extract_markdown_links(
    #         "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    #     )
    # print(matches)

    node = TextNode(
        "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
        TextType.TEXT,
    )

    node2 = TextNode(
                "This is 2text with an ![2image](https://i.22imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            )

    new_nodes = split_nodes_link([node])
    print(f"the new nodes are: {new_nodes}")



main()

