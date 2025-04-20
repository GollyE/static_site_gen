from enum import Enum
from textnode import *
from htmlnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits inline text nodes.

    Args:
        old_nodes (list): The original list of text nodes to split.
        delimiter (str): The text pattern to split on.
        text_type (str): The type to assign to matched segments.

    Returns:
        list: A list of new nodes.
    """
    new_list = []
    
    for old_node in old_nodes:
        split_nodes_list = []
        match (old_node.text_type):
            case (TextType.TEXT):
                try:
                    split_old_node = old_node.text.split(delimiter)
                except:
                    raise Exception("That's invalid markdown syntax")
                if old_node.text.count(delimiter)%2 != 0:
                    print(f"the number of instances of the delimiter: {delimiter} in{old_node.text} is {old_node.text.count(delimiter)}")
                    raise Exception("That's invalid markdown syntax")
                else:
                    
                    for item_num in range(0, len(split_old_node)):
                        if split_old_node[item_num] == "":
                            continue
                        elif item_num%2 == 0:
                            split_nodes_list.append(TextNode(split_old_node[item_num],TextType.TEXT))
                        else:
                            split_nodes_list.append(TextNode(split_old_node[item_num],text_type))
                        
                new_list.extend(split_nodes_list)
            case _:
                new_list.append(old_node)

    return new_list

def extract_markdown_images(text):
    #return a list of tuples containing
    # the alt_text and url in the raw markdown
    # text submitted to the function
    
   
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    #return a list of tuples containing
    # the anchor text and url in the raw markdown
    # text submitted to the function
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_list = []
    split_nodes_list = []
    for old_node in old_nodes:
        sections = ""
        extracted_images_list = []
        splits_required = 0
        split_nodes_list = []
        match (old_node.text_type):
            case (TextType.TEXT):
                if len(old_node.text) == 0:
                    continue
                elif extract_markdown_images(old_node.text) == []:
                    new_list.append(old_node)
                else:
                    extracted_images_list = extract_markdown_images(old_node.text)
                    splits_required = len(extracted_images_list)
                    #print(f"the splits required are: {splits_required}")
                    sections = old_node.text
                    for item_num in range(0, splits_required):
                        image = extracted_images_list[item_num][0]
                        image_link = extracted_images_list[item_num][1]
                        sections = sections.split(
                            f"![{image}]({image_link})", 1)
                        #print(f"the split sections are: {sections}")
                        if len(sections) != 2:
                            raise ValueError("invalid markdown, image section not closed")
                        elif sections[0]=="":
                            split_nodes_list.append(TextNode(image,TextType.IMAGE,image_link))
                        else:    
                            split_nodes_list.append(TextNode(sections[0],TextType.TEXT))
                            split_nodes_list.append(TextNode(image,TextType.IMAGE,image_link))
                            original_text = sections[1]
                            if item_num == (splits_required-1) and original_text != "":
                                split_nodes_list.append(TextNode(original_text, TextType.TEXT))
                        sections = sections[1]
                new_list.extend(split_nodes_list)
            case _:
                new_list.append(old_node)
    return new_list
def split_nodes_link(old_nodes):
    new_list = []
    split_nodes_list = []
    for old_node in old_nodes:
        sections = ""
        extracted_links_list = []
        splits_required = 0
        split_nodes_list = []
        match (old_node.text_type):
            case (TextType.TEXT):
                if len(old_node.text) == 0:
                    continue
                elif extract_markdown_links(old_node.text) == []:
                    new_list.append(old_node)
                else:
                    extracted_links_list = extract_markdown_links(old_node.text)
                    splits_required = len(extracted_links_list)
                    #print(f"splits required are: {splits_required}")
                    sections = old_node.text
                    for item_num in range(0, splits_required):
                        link = extracted_links_list[item_num][0]
                        link_link = extracted_links_list[item_num][1]
                        sections = sections.split(
                            f"[{link}]({link_link})", 1)
                        #print(f"before the if's, section 0 equal to {sections[0]}")
                        if len(sections) != 2:
                            raise ValueError("invalid markdown, link section not closed")
                        elif sections[0]=="":
                            split_nodes_list.append(TextNode(link,TextType.LINK,link_link))
                        else:
                            split_nodes_list.append(TextNode(sections[0],TextType.TEXT))
                            split_nodes_list.append(TextNode(link,TextType.LINK,link_link))
                            original_text = sections[1]
                            if item_num == (splits_required-1) and original_text != "":
                                split_nodes_list.append(TextNode(original_text, TextType.TEXT))
                        #print(f"the sections in {item_num} times through loop are {sections}")
                        sections = sections[1]
                        
                new_list.extend(split_nodes_list)
            case _:
                new_list.append(old_node)
    return new_list

def text_to_textnodes(text):
    """
        This function takes a text string and splits it into a list of correctly typed text nodes.
        Args:
            text (str): The full text to convert.
        Returns:
            list: A list containing nodes split by type.
        """ 
    orig_text_node_list  = [TextNode(text,TextType.TEXT)]
    #print (f"the original text is: {text}")
    #print(f"the original list is: {orig_text_node_list}")
    bold_split = split_nodes_delimiter(orig_text_node_list,"**",text_type=TextType.BOLD)
    input_to_italic = bold_split.copy()
    
    italic_split = split_nodes_delimiter(input_to_italic,"_",text_type=TextType.ITALIC)
    input_to_code = italic_split.copy()
    code_split = split_nodes_delimiter(input_to_code,"`",TextType.CODE)
    input_to_image = code_split.copy()
    image_split= split_nodes_image(input_to_image)
    input_to_link = image_split.copy()
    link_split = split_nodes_link(input_to_link)
    split_node_list = link_split.copy()
    #print(f"the length of the final list is {len(link_split)}")
    return split_node_list


    