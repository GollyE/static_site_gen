from enum import Enum
from textnode import *
from htmlnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    split_nodes_list = []
    for old_node in old_nodes:
        match (old_node.text_type):
            case (TextType.TEXT):
                try:
                    split_old_node = old_node.text.split(delimiter)
                except:
                    raise Exception("That's invalid markdown syntax")
                if old_node.text.count(delimiter)%2 != 0:
                    raise Exception("That's invalid markdown syntax")
                else:
                    #unter = 0
                    for item_num in range(0, len(split_old_node)):
                        if split_old_node[item_num] == "":
                            #pass
                            continue
                        elif item_num%2 == 0:
                            split_nodes_list.append(TextNode(split_old_node[item_num],TextType.TEXT))
                        else:
                            split_nodes_list.append(TextNode(split_old_node[item_num],text_type))
                        #counter +=1
                new_list.extend(split_nodes_list)
            case _:
                new_list.append(old_node)
    return new_list
