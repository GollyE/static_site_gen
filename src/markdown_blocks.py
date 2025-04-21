import re
from enum import Enum
from htmlnode import *
from inline import *
from textnode import *
import textwrap

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    split_to_blocks = markdown.split("\n\n")
    block_list = []
    
    for item in split_to_blocks:
        new_item = item.strip()
        #print(f"The new item: ({item}), it's length is {len(item)} in the markdown to blocks is: {new_item}, length of newitem is {len(new_item)}")
        if new_item != '':
            #print(f"a nonbalnk item: {item} is being checked for first newline char")
            if new_item[0]=="\n":
                new_item=new_item[1:]
            if new_item[-1]=="\n":
                new_item=new_item[:-1]
            new_item = new_item.strip()
            block_list.append(new_item)
    return block_list

def block_to_block_type(block_of_markdown):
    if re.match(r"\s*```(?:[^\n]*)\n(.*?)\n\s*```", block_of_markdown,re.DOTALL):
        return BlockType.CODE
    elif re.match(r"^#{1,6} .+", block_of_markdown):
        return BlockType.HEADING
    elif re.match(r"(?:^>.*\n?)+", block_of_markdown,re.MULTILINE):
        return BlockType.QUOTE
    elif re.match(r"(?:^- .+\n?)+", block_of_markdown,re.MULTILINE):
        return BlockType.UNORDERED_LIST
    elif re.match(r"(?:^\d+[.)] .+\n?)+",block_of_markdown,re.MULTILINE):
        return BlockType.ORDERED_LIST
    elif re.match(r".+", block_of_markdown):
        return BlockType.PARAGRAPH
    else:
        raise Exception("not able to find any markdown blocks")
    
def markdown_to_html_node(markdown):
    """This function takes an entire markdown document
    and converts it to a single parent HTML Node 
    Args:
        markdown (str): A markdown document
    Returns:
        HTMLNode: An HTML representaiton of the markdown input
    """
    # Create the top-level div container
    parent_node = ParentNode(tag="div", children=None)
    block_child_list = []    
    
    # Split markdown into blocks using existing function
    list_of_blocks = markdown_to_blocks(markdown)

    # Loop over each block
    for block in list_of_blocks:
    #Determine block type using exisitng function

        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            block_child_list.append(handle_paragraph_block(block))
        elif block_type == BlockType.CODE:
            block_child_list.append(handle_code_block(block))
        elif block_type == BlockType.HEADING:
            block_child_list.append(handle_heading_block(block))
        elif block_type == BlockType.QUOTE:
            block_child_list.append(handle_quote_block(block))
        elif block_type == BlockType.UNORDERED_LIST:
            block_child_list.append(handle_unordered_list_block(block))
        elif block_type == BlockType.ORDERED_LIST:
            block_child_list.append(handle_ordered_list_block(block))

    parent_node.children = block_child_list
    #print(f"The parent node html is: {parent_node.to_html()}")
    return parent_node

def text_to_children(text):
    """
    Takes text of a markdown block, creates blocks for each piece of markdown in block

    Args:
        text (str): text of the markdown block
    Returns:
        list: list of parent and children blocks 
    """
    list_of_text_nodes_in_block = text_to_textnodes(text)
    leaf_list = create_leaf_from_list(list_of_text_nodes_in_block)
    return leaf_list


def create_leaf_from_list(tn_list):
    child_list = []
    for item in tn_list:
        html_node = text_node_to_html_node(item)
        child_list.append(html_node)
    return child_list


def handle_paragraph_block(paragraph_block):

    paragraph_block = paragraph_block.replace("\n"," ")
    clean_paragraph_block = re.sub(r'\s+', ' ', paragraph_block)
    paragraph_node = ParentNode(tag="p",children = None)

    child_nodes = text_to_children(clean_paragraph_block)
    paragraph_node.children = child_nodes
    return paragraph_node

def handle_code_block(code_block):
    # Create pre node (outermost parent)
    pre_node = ParentNode(tag="pre", children=None)
    
    # Create code node (inner parent)
    code_node = ParentNode(tag="code", children=None)
    
    code_block = code_block.strip("`")
    code_block = code_block.strip("\n")
    clean_code_block = textwrap.dedent(code_block).strip()
    if not clean_code_block.endswith('\n'):
        clean_code_block += '\n'


    text_node = TextNode(clean_code_block, text_type=TextType.TEXT)
    
    # Convert text node to HTML node
    html_text_node = text_node_to_html_node(text_node)
    
    # Set up the hierarchy
    code_node.children = [html_text_node]
    pre_node.children = [code_node]
    return pre_node
def handle_heading_block(heading_block):
    level = 0
    for char in heading_block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(heading_block):
        raise ValueError(f"invalid heading level: {level}")
    text = heading_block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def handle_quote_block(quote_block):
    lines = quote_block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def handle_unordered_list_block(unordered_block):
    items = unordered_block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def handle_ordered_list_block(ordered_block):
    items = ordered_block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    #print(f"the blocks of markdown are: {blocks}")
    for item in blocks:
        #print(f"the item is: {item}")
        item_block_type = block_to_block_type(item)
        if item_block_type == BlockType.HEADING:
            heading_node = handle_heading_block(item)
            #print(f"The heading node is: {heading_node}")
            if heading_node.tag == "h1":
                #print('found the title')
                return heading_node.children[0].value
    raise Exception("No H1 Heading Found")
    