from enum import Enum
from textnode import *
from htmlnode import *
import re

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
                    sections = old_node.text
                    for item_num in range(0, splits_required):
                        image = extracted_images_list[item_num][0]
                        image_link = extracted_images_list[item_num][1]
                        sections = sections.split(
                            f"![{image}]({image_link})", 1)
                        split_nodes_list.append(TextNode(sections[0],TextType.TEXT))
                        split_nodes_list.append(TextNode(image,TextType.IMAGE,image_link))
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
                    sections = old_node.text
                    for item_num in range(0, splits_required):
                        link = extracted_links_list[item_num][0]
                        link_link = extracted_links_list[item_num][1]
                        sections = sections.split(
                            f"[{link}]({link_link})", 1)
                        split_nodes_list.append(TextNode(sections[0],TextType.TEXT))
                        split_nodes_list.append(TextNode(link,TextType.LINK,link_link))
                        sections = sections[1]
                new_list.extend(split_nodes_list)
            case _:
                new_list.append(old_node)
    return new_list